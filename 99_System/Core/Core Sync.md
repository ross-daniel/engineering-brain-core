# Core Synchronization

This vault inherits reusable infrastructure from a separate `engineering-brain-core` Git repository while retaining its own project/content structure.

## Ownership boundary

Core-managed content is declared by the core repository's `core-manifest.json`. Typical managed content includes:

- `.claude/skills/`
- `91_Templates/`
- `99_System/Core/`
- selected shared scripts under `99_System/Scripts/`
- the marked shared section of root `CLAUDE.md`

The core does **not** own normal notes, maps, literature, implementations, project folders, `Home.md`, `.obsidian/`, the root `README.md`, or vault-specific extension files unless explicitly added to the manifest.

The root `README.md` is never synchronized by the core. Shared setup/usage documentation lives at `99_System/Core/README-Core.md`.

## Configure the core checkout

Set:

```bash
export BRAIN_CORE_ROOT="$HOME/Documents/engineering-brain-core"
```

or pass a path explicitly:

```bash
./99_System/Scripts/update-brain-core.sh --core /path/to/engineering-brain-core
```

## Preview / apply

```bash
./99_System/Scripts/update-brain-core.sh --dry-run
./99_System/Scripts/update-brain-core.sh
```

If the core Git checkout has a clean working tree and configured upstream, the updater first attempts `git pull --ff-only`.

## Local customizations

Do not edit core-managed files directly when the change should stay private to one vault. Use local extension/profile files instead:

- `99_System/Schema.md`
- `99_System/Tag Taxonomy.md`
- `99_System/Machine Setup.md`
- root `README.md` (entirely vault-owned)
- CLAUDE text outside the core markers

If a core-managed file/section was locally modified, the updater stops before writing anything. `--force` is available for intentional overwrite.
