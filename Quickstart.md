# Engineering Brain Core — Quickstart

`engineering-brain-core` is reusable operating infrastructure for Obsidian + Claude Code engineering knowledge vaults.

This repository intentionally contains **no personal notes, no prescribed project-folder taxonomy, and no personalized vault `README.md`**. Each connected vault owns its own content, project hierarchy, Home page, Obsidian workspace, root README, and local conventions.

The core owns only reusable behavior declared in `core-manifest.json`.

## Repository layout

The core repository mirrors the paths it manages inside a connected vault:

```text
engineering-brain-core/
├── .claude/
│   └── skills/
├── 91_Templates/
├── 99_System/
│   ├── Core/
│   └── Scripts/
├── core-manifest.json
├── VERSION
└── Quickstart.md
```

Most managed files therefore have the same source and destination path. For example:

```text
core:  .claude/skills/process-inbox/SKILL.md
vault: .claude/skills/process-inbox/SKILL.md
```

`99_System/Core/` remains nested because those files are themselves shared core metadata *inside a connected vault*: baseline schema/tag rules, synchronization documentation, shared setup/usage documentation, and shared Claude rules.

## Ownership boundary

`core-manifest.json` is the authority boundary. Typical managed content includes:

- `.claude/skills/`
- `91_Templates/`
- `99_System/Core/`
- selected shared scripts in `99_System/Scripts/`
- the marked shared section of a connected vault's root `CLAUDE.md`

The core does **not** own normal vault content such as:

- `00_Inbox/`
- maps, concepts, literature, or implementation notes
- `05_Projects/` or any of its subfolders
- `90_Sources/`
- `Home.md`
- `.obsidian/`
- the vault's root `README.md`
- vault-specific schema/tag/machine-profile extensions

A connected vault can therefore organize projects and document itself however its owner wants without creating synchronization conflicts with the core.

## Initial Git setup

After extracting or cloning this repository:

```bash
cd /path/to/engineering-brain-core
git init -b main
git add -A
git commit -m "Initialize engineering brain core"
```

Add any normal Git remote if desired:

```bash
git remote add origin <YOUR-CORE-REMOTE-URL>
git push -u origin main
```

Because the core contains reusable infrastructure rather than personal knowledge, it can be versioned independently of any connected vault.

## Connect a personalized vault

A connected vault needs the core updater scripts and the shared `CLAUDE.md` integration marker. The root `README.md` is **not** core-managed; write it specifically for that vault.

Set a machine-local pointer to the core checkout:

```bash
export BRAIN_CORE_ROOT="$HOME/Documents/engineering-brain-core"
```

Then, from a connected vault:

```bash
./99_System/Scripts/update-brain-core.sh --dry-run
./99_System/Scripts/update-brain-core.sh
```

The updater will:

1. fast-forward-pull the core when it has a configured upstream and clean working tree,
2. read `core-manifest.json`,
3. detect local edits to previously core-managed content,
4. stop rather than overwrite ambiguous local edits,
5. copy/update only managed paths,
6. refresh only the marked shared section of root `CLAUDE.md`,
7. remove obsolete files only when they were previously core-managed and remain unchanged locally,
8. record the synchronized core revision under `99_System/Core/`.

Use `--force` only when you intentionally want the core version to replace local edits in managed content.

## Changing shared behavior

Shared changes are edited directly where they conceptually live:

```bash
cd "$BRAIN_CORE_ROOT"

$EDITOR .claude/skills/process-inbox/SKILL.md
$EDITOR 91_Templates/Implementation.md
$EDITOR 99_System/Core/Schema-Core.md

git add -A
git commit -m "Improve shared engineering-brain workflow"
git push
```

Then synchronize each connected vault:

```bash
./99_System/Scripts/update-brain-core.sh --dry-run
./99_System/Scripts/update-brain-core.sh
git diff
git add -A
git commit -m "Sync engineering brain core"
git push
```

## Why the root README is not synchronized

A vault's root `README.md` describes the **personalized implementation**: its purpose, project taxonomy, local conventions, and any vault-specific workflows. That content has a different owner and lifecycle from the reusable core.

Shared setup/usage documentation is instead synchronized as a normal core file at:

```text
99_System/Core/README-Core.md
```

This avoids partial README ownership, fragment merge conflicts, and ambiguity about where a documentation change belongs.

The root `CLAUDE.md` remains different: it is active agent configuration, so the core still manages a marked shared rules section while leaving vault-specific Claude rules outside that section.

## Updating the manifest

When adding a reusable file that every connected vault should inherit, add it to `core-manifest.json`. Do **not** add content/project directories or a root `README.md` merely because one particular vault uses them.

The guiding rule is:

> Core owns **how the brain operates**. Each vault owns **what the brain contains, how that vault is organized, and how that vault describes itself**.

## Personalized vault setup and usage

For the full shared setup instructions, knowledge model, Zotero workflow, Claude skills, and example engineering workflows used by a personalized vault, see:

[README-Core — Personalized Vault Setup and Usage](99_System/Core/README-Core.md)
