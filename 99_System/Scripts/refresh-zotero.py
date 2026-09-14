#!/usr/bin/env python3
"""Refresh vault bibliography metadata from the local Zotero desktop API.

This script is intentionally read-only with respect to Zotero. It reads the
current local library and atomically regenerates:

  99_System/Zotero/library.json   (CSL JSON)
  99_System/Zotero/references.bib (BibLaTeX)

Requirements:
- Zotero desktop must be running.
- Zotero Settings -> Advanced -> "Allow other applications on this computer
  to communicate with Zotero" must be enabled.
- Python 3 standard library only; no third-party packages are required.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

BASE = "http://localhost:23119/api/users/0/items/top"
HEADERS = {
    "User-Agent": "Engineering-Brain-Zotero-Refresh/1.0",
    "Zotero-API-Version": "3",
}


def vault_root() -> Path:
    # .../Engineering-Brain/99_System/Scripts/refresh-zotero.py
    return Path(__file__).resolve().parents[2]


def fetch(export_format: str) -> bytes:
    query = urllib.parse.urlencode({"format": export_format, "sort": "title", "direction": "asc"})
    req = urllib.request.Request(f"{BASE}?{query}", headers=HEADERS, method="GET")
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read()


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    root = vault_root()
    zotero_dir = root / "99_System" / "Zotero"
    library_path = zotero_dir / "library.json"
    bib_path = zotero_dir / "references.bib"

    try:
        csl_raw = fetch("csljson")
        bib_raw = fetch("biblatex")
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print(
                "Zotero metadata refresh skipped: the local Zotero API returned 403.\n"
                "In Zotero, enable Settings -> Advanced -> 'Allow other applications "
                "on this computer to communicate with Zotero'.",
                file=sys.stderr,
            )
        else:
            print(f"Zotero metadata refresh skipped: HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
        print(
            "Zotero metadata refresh skipped: could not reach the local Zotero API at "
            "http://localhost:23119. Make sure Zotero desktop is running.\n"
            f"Details: {exc}",
            file=sys.stderr,
        )
        return 2

    # Validate and normalize CSL JSON before replacing the prior good export.
    try:
        csl_data = json.loads(csl_raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"Zotero metadata refresh failed: invalid CSL JSON response: {exc}", file=sys.stderr)
        return 3

    if not isinstance(csl_data, list):
        print("Zotero metadata refresh failed: expected CSL JSON to be a list.", file=sys.stderr)
        return 3

    csl_bytes = (json.dumps(csl_data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    try:
        bib_text = bib_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"Zotero metadata refresh failed: invalid BibLaTeX response: {exc}", file=sys.stderr)
        return 3

    # Fetch/validate both outputs first, then replace files. This prevents one stale
    # half-update if Zotero returns an error for either export format.
    atomic_write(library_path, csl_bytes)
    atomic_write(bib_path, bib_text.encode("utf-8"))

    print(f"Updated {library_path.relative_to(root)} ({len(csl_data)} top-level items)")
    print(f"Updated {bib_path.relative_to(root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
