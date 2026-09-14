#!/usr/bin/env python3
"""Synchronize shared Engineering Brain Core files into a vault.

The core repo owns only paths declared in core-manifest.json and any marked
configuration sections declared there (currently the shared CLAUDE.md rules).
The vault root README.md and all other undeclared content are outside its authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_REL = Path("99_System/Core/.core-sync-state.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def git_commit(repo: Path) -> str | None:
    try:
        return run_git(repo, "rev-parse", "HEAD").stdout.strip() or None
    except Exception:
        return None


def git_is_dirty(repo: Path) -> bool:
    try:
        return bool(run_git(repo, "status", "--porcelain").stdout.strip())
    except Exception:
        return False


def maybe_pull_core(core: Path, no_pull: bool) -> None:
    if no_pull or not (core / ".git").exists():
        return
    if git_is_dirty(core):
        print("[core] Working tree is dirty; skipping automatic pull.")
        return
    upstream = run_git(
        core,
        "rev-parse",
        "--abbrev-ref",
        "--symbolic-full-name",
        "@{u}",
        check=False,
    )
    if upstream.returncode != 0:
        print("[core] No upstream configured; using local core checkout.")
        return
    print(f"[core] Pulling {upstream.stdout.strip()} with --ff-only ...")
    pulled = run_git(core, "pull", "--ff-only", check=False)
    if pulled.returncode != 0:
        print(pulled.stdout, end="")
        print(pulled.stderr, end="", file=sys.stderr)
        raise RuntimeError("Could not fast-forward the core repository.")


def resolve_vault(script_path: Path) -> Path:
    # Script normally lives at <vault>/99_System/Scripts/update-brain-core.py
    candidate = script_path.resolve().parents[2]
    if (candidate / ".claude").exists() or (candidate / "99_System").exists():
        return candidate
    env = os.environ.get("BRAIN_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    raise RuntimeError("Could not determine vault root. Set BRAIN_ROOT.")


def resolve_core(vault: Path, explicit: str | None) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    env = os.environ.get("BRAIN_CORE_ROOT")
    if env:
        candidates.append(Path(env).expanduser())
    candidates.extend(
        [
            vault.parent / "engineering-brain-core",
            Path.home() / "Documents" / "engineering-brain-core",
            Path.home() / "Knowledge" / "engineering-brain-core",
        ]
    )
    for candidate in candidates:
        candidate = candidate.resolve()
        if (candidate / "core-manifest.json").is_file():
            return candidate
    checked = "\n  - ".join(str(p.expanduser()) for p in candidates)
    raise RuntimeError(
        "Could not find engineering-brain-core. Set BRAIN_CORE_ROOT or pass --core.\n"
        f"Checked:\n  - {checked}"
    )


def safe_rel(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe manifest path: {value}")
    return path


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def marker_extract(text: str, start: str, end: str) -> str | None:
    i = text.find(start)
    if i < 0:
        return None
    j = text.find(end, i + len(start))
    if j < 0:
        return None
    return text[i + len(start):j].strip("\n")


def marker_replace(text: str, start: str, end: str, content: str) -> str:
    i = text.find(start)
    j = text.find(end, i + len(start)) if i >= 0 else -1
    if i < 0 or j < 0:
        raise ValueError("Required core markers are missing")
    before = text[: i + len(start)]
    after = text[j:]
    return before + "\n" + content.rstrip() + "\n" + after


def write_file(path: Path, data: bytes, dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".core-sync.tmp")
    tmp.write_bytes(data)
    # Preserve executable bit from existing file only if source does not carry it later;
    # caller handles explicit mode after replacement.
    os.replace(tmp, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--core", help="Path to engineering-brain-core checkout")
    parser.add_argument("--no-pull", action="store_true", help="Do not git pull the core checkout")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--force", action="store_true", help="Overwrite locally modified core-managed content")
    args = parser.parse_args()

    script = Path(__file__)
    vault = resolve_vault(script)
    core = resolve_core(vault, args.core)
    maybe_pull_core(core, args.no_pull)

    manifest_path = core / "core-manifest.json"
    manifest = load_json(manifest_path, None)
    if not manifest or manifest.get("schema_version") != 1:
        raise RuntimeError(f"Unsupported or missing manifest: {manifest_path}")

    state_path = vault / STATE_REL
    old_state = load_json(state_path, {"managed_files": {}, "fragments": {}})
    old_files: dict[str, Any] = old_state.get("managed_files", {})
    old_fragments: dict[str, Any] = old_state.get("fragments", {})

    desired: dict[str, dict[str, Any]] = {}
    for entry in manifest.get("managed_files", []):
        src_rel = safe_rel(entry["source"])
        dst_rel = safe_rel(entry["destination"])
        src = core / src_rel
        if not src.is_file():
            raise RuntimeError(f"Core manifest source does not exist: {src}")
        desired[str(dst_rel)] = {
            "source": src,
            "mode": entry.get("mode"),
            "hash": sha256_file(src),
        }

    conflicts: list[str] = []
    actions: list[tuple[str, str]] = []

    # Files no longer managed by core: delete only if untouched since previous sync.
    stale = sorted(set(old_files) - set(desired))
    for rel in stale:
        dst = vault / safe_rel(rel)
        if not dst.exists():
            continue
        previous_hash = old_files[rel].get("hash") if isinstance(old_files[rel], dict) else old_files[rel]
        current_hash = sha256_file(dst) if dst.is_file() else None
        if dst.is_file() and current_hash == previous_hash:
            actions.append(("DELETE", rel))
        elif args.force:
            actions.append(("DELETE-FORCE", rel))
        else:
            conflicts.append(f"Formerly core-managed file was locally modified: {rel}")

    for rel, meta in desired.items():
        dst = vault / safe_rel(rel)
        new_hash = meta["hash"]
        if dst.exists() and dst.is_file():
            current_hash = sha256_file(dst)
            if current_hash == new_hash:
                continue
            previous = old_files.get(rel)
            previous_hash = previous.get("hash") if isinstance(previous, dict) else previous
            if previous_hash and current_hash != previous_hash and not args.force:
                conflicts.append(f"Core-managed file has local edits: {rel}")
                continue
            if not previous_hash and not args.force:
                # Bootstrap is safe only when the existing file already matches current core.
                conflicts.append(
                    f"Existing file is not yet tracked by core and differs from core: {rel}"
                )
                continue
            actions.append(("UPDATE", rel))
        elif dst.exists():
            conflicts.append(f"Managed destination is not a regular file: {rel}")
        else:
            actions.append(("CREATE", rel))

    fragment_plans: list[dict[str, Any]] = []
    for entry in manifest.get("managed_fragments", []):
        src_rel = safe_rel(entry["source"])
        dst_rel = safe_rel(entry["destination"])
        src = core / src_rel
        content = src.read_text(encoding="utf-8").rstrip()
        content_hash = sha256_bytes(content.encode("utf-8"))
        dst = vault / dst_rel
        start, end = entry["start_marker"], entry["end_marker"]
        if not dst.exists():
            # A new fragment-managed configuration file is okay: create a minimal marked file.
            initial = f"{start}\n{content}\n{end}\n"
            fragment_plans.append(
                {"action": "CREATE-FRAGMENT", "rel": str(dst_rel), "text": initial,
                 "hash": content_hash, "start": start, "end": end}
            )
            continue
        text = dst.read_text(encoding="utf-8")
        current = marker_extract(text, start, end)
        if current is None:
            conflicts.append(
                f"Fragment markers missing in {dst_rel}. Add the documented markers or use the integration patch."
            )
            continue
        current_hash = sha256_bytes(current.rstrip().encode("utf-8"))
        if current_hash == content_hash:
            fragment_plans.append(
                {"action": "UNCHANGED", "rel": str(dst_rel), "text": text,
                 "hash": content_hash, "start": start, "end": end}
            )
            continue
        previous = old_fragments.get(str(dst_rel), {})
        previous_hash = previous.get("hash") if isinstance(previous, dict) else previous
        if previous_hash and current_hash != previous_hash and not args.force:
            conflicts.append(f"Core-managed section has local edits: {dst_rel}")
            continue
        if not previous_hash and not args.force:
            conflicts.append(
                f"Core-managed section in {dst_rel} differs before first recorded sync"
            )
            continue
        new_text = marker_replace(text, start, end, content)
        fragment_plans.append(
            {"action": "UPDATE-FRAGMENT", "rel": str(dst_rel), "text": new_text,
             "hash": content_hash, "start": start, "end": end}
        )

    if conflicts:
        print("\nCore sync stopped because local/core ownership is ambiguous:\n", file=sys.stderr)
        for item in conflicts:
            print(f"  - {item}", file=sys.stderr)
        print(
            "\nNo files were changed. Move local customizations outside core-managed files/sections, "
            "or rerun with --force if you intentionally want core to overwrite them.",
            file=sys.stderr,
        )
        return 2

    print(f"Vault: {vault}")
    print(f"Core:  {core}")
    if actions or any(p["action"] != "UNCHANGED" for p in fragment_plans):
        for action, rel in actions:
            print(f"{action:15} {rel}")
        for plan in fragment_plans:
            if plan["action"] != "UNCHANGED":
                print(f"{plan['action']:15} {plan['rel']}")
    else:
        print("Already synchronized; no managed content changes.")

    if args.dry_run:
        print("Dry run only; nothing written.")
        return 0

    # Apply stale deletes first.
    for action, rel in actions:
        if action.startswith("DELETE"):
            path = vault / safe_rel(rel)
            if path.exists():
                path.unlink()

    # Apply managed files.
    for rel, meta in desired.items():
        dst = vault / safe_rel(rel)
        src: Path = meta["source"]
        if not dst.exists() or sha256_file(dst) != meta["hash"]:
            write_file(dst, src.read_bytes(), dry_run=False)
        mode = meta.get("mode")
        if mode:
            os.chmod(dst, int(str(mode), 8))

    # Apply fragments.
    fragment_state: dict[str, Any] = {}
    for plan in fragment_plans:
        dst = vault / safe_rel(plan["rel"])
        if plan["action"] in {"CREATE-FRAGMENT", "UPDATE-FRAGMENT"}:
            write_file(dst, plan["text"].encode("utf-8"), dry_run=False)
        fragment_state[plan["rel"]] = {
            "hash": plan["hash"],
            "start_marker": plan["start"],
            "end_marker": plan["end"],
        }

    version = (core / "VERSION").read_text(encoding="utf-8").strip() if (core / "VERSION").exists() else None
    commit = git_commit(core)
    new_state = {
        "schema_version": 1,
        "core_version": version,
        "core_commit": commit,
        "core_path_hint": core.name,
        "synced_at_utc": datetime.now(timezone.utc).isoformat(),
        "managed_files": {rel: {"hash": meta["hash"]} for rel, meta in sorted(desired.items())},
        "fragments": fragment_state,
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(new_state, indent=2) + "\n", encoding="utf-8")

    version_md = vault / "99_System/Core/CORE_VERSION.md"
    version_md.write_text(
        "# Engineering Brain Core version\n\n"
        f"- Version: `{version or 'unversioned'}`\n"
        f"- Commit: `{commit or 'not a Git checkout'}`\n"
        f"- Last synchronized (UTC): `{new_state['synced_at_utc']}`\n\n"
        "This file is generated by `update-brain-core.py`.\n",
        encoding="utf-8",
    )

    print("Core synchronization complete.")
    if commit:
        print(f"Core commit: {commit[:12]}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
