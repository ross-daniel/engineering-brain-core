# Machine Setup

The vault is designed to work from multiple machines while codebases and large engineering files remain external.

## Recommended vault location

Use the same logical location when possible:

```bash
$HOME/Documents/Engineering-Brain
```

Set:

```bash
export BRAIN_ROOT="$HOME/Documents/Engineering-Brain"
```

Add that line to `~/.bashrc`, `~/.zshrc`, or the equivalent shell profile.

## Recommended code-repository root

If most local repositories are kept under one directory, define:

```bash
export CODE_ROOT="$HOME/Desktop/Codebases"
```

Implementation/project notes store portable values such as:

```yaml
repo-name: example-fem-solver
repo-url: git@host:user/example-fem-solver.git
```

rather than an absolute path. When a referenced repo is already cloned, `$CODE_ROOT/$repo-name` is a useful local lookup convention. Claude still needs permission to access that directory; add it with `/add-dir` or `--add-dir` when necessary.

The repository names above are **illustrative engineering examples**, not required project names.

## Optional external-storage root

For large simulation files, CAD, measurement archives, network/project storage, or other files that should remain outside the vault, define a machine-local root such as:

```bash
export EXTERNAL_STORAGE_ROOT="/mnt/engineering-storage"
```

Use a different value on each machine if needed. Canonical notes should store:

```yaml
external-root: EXTERNAL_STORAGE_ROOT
external-path: Project_A/Simulation/final_model.ext
```

rather than a machine-specific absolute path.

## Launch Claude from an external code repository with vault access

Add this helper to your shell configuration:

```bash
cbrain() {
    claude --add-dir "$BRAIN_ROOT" "$@"
}
```

Then, for any repository:

```bash
cd "$CODE_ROOT/my-project"
cbrain
```

Claude's working directory remains the code repository, while the vault is an additional allowed directory and its `.claude/skills/` are available.

**Important:** access to the vault does not mean its contents are automatically loaded. Use the `vault-query` skill to retrieve a narrow subset.

## Add a reference repository during a coding session

The following is an **illustrative CEM/numerical-methods example**.

Suppose the current target is `example-sie-solver` but an implementation note points to `example-fem-solver` as a useful reference.

Start normally:

```bash
cd "$CODE_ROOT/example-sie-solver"
cbrain
```

If Claude determines that exact source inspection is useful, add the reference repo in the Claude session:

```text
/add-dir /home/YOU/Desktop/Codebases/example-fem-solver
```

or start Claude with both directories available:

```bash
claude --add-dir "$BRAIN_ROOT" --add-dir "$CODE_ROOT/example-fem-solver"
```

The current working repo (`example-sie-solver`) remains the implementation target. The reference repo should be treated as read-only unless you explicitly ask Claude to change it.

## Zotero local metadata refresh

This template reads Zotero metadata from the local Zotero desktop API. Zotero must be running and local communication must be enabled.

Test the integration with:

```bash
python3 "$BRAIN_ROOT/99_System/Scripts/refresh-zotero.py"
```

See `99_System/Core/Zotero/Zotero Setup.md` for details.

## Repository-local `CLAUDE.md`

Each important codebase should contain a small `CLAUDE.md` telling Claude to:

- use `vault-query` for prior project knowledge,
- treat current source code as authoritative for implementation claims,
- use `implement-concept` for concept/implementation transfer,
- use `paper-to-implementation` when a paper is the primary specification,
- inspect reference repos when implementation notes indicate this is needed,
- use `capture-session` explicitly when durable conclusions should be written back.
