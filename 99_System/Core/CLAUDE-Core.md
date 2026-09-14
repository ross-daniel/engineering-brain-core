## Shared Engineering Brain Operating Rules

This section is managed by `engineering-brain-core`.

### Core rule

**Access to the vault is not permission to indiscriminately load it.** Retrieve only the smallest relevant set of notes for the current task.

### Vault root

Prefer `$BRAIN_ROOT`. If it is unavailable, identify the vault root from the presence of `99_System/Core/Schema-Core.md`, `00_Inbox/`, and `.claude/skills/`. Never assume the current working directory is the vault because Claude may be launched from an external code repository.

### Knowledge roles

Common role folders are:

- `00_Inbox/` — unprocessed queue.
- `01_Maps/` — short maps/indexes.
- `02_Concepts/` — canonical reusable concepts.
- `03_Literature/` — source-specific literature notes.
- `04_Implementations/` — portable specifications plus provenance to external repositories.
- `05_Projects/` — vault-specific project hierarchy; do not assume its subfolder names.
- `90_Sources/` — preserved raw evidence.
- `91_Templates/` — shared note templates.
- `99_System/Core/` — shared baseline rules/documentation.
- `99_System/Schema.md` and `99_System/Tag Taxonomy.md` — optional vault-specific extensions.

### Retrieval rules

1. Do not read the entire vault.
2. Prefer map titles, filenames, YAML `summary`, `parent`, `related`, `methods`, `domains`, `projects`, and `reference-implementations` before full note bodies.
3. Prefer 3–8 strongly relevant notes over dozens of loose matches.
4. If working from an external repository, prioritize the matching project/implementation notes.
5. Preserve distinctions among `general`, `domain-specific`, `method-specific`, and `project-specific` knowledge.
6. Do not infer that a specialized child applies to every method named by a broader parent.

### Schema and taxonomy

Before creating/updating canonical notes, read:

- `99_System/Core/Schema-Core.md`
- `99_System/Schema.md` if present
- `99_System/Core/Tag-Taxonomy-Core.md`
- `99_System/Tag Taxonomy.md` if present

The core files define baseline behavior; vault-specific files may extend or specialize them. Local extensions must not contradict core constraints without explicitly documenting the override.

### Mathematics and engineering

When introducing technical results:

- keep equations in LaTeX,
- define symbols,
- state assumptions/applicability,
- preserve paper equation/page/figure references where relevant,
- distinguish source claims from derivation/interpretation,
- explain implementation consequences when useful.

### Implementation-note contract

Implementation notes are **portable specifications and provenance maps, not substitutes for source code**.

They should distinguish:

1. portable/concept-level behavior,
2. method/domain-specific behavior,
3. repository-specific software choices.

Record, when applicable:

- `repo-name`,
- `repo-url`,
- `last-verified-commit`,
- `transferability`,
- `source-inspection`,
- `reference-implementations`,
- code map to files/symbols/tests,
- validation evidence.

A strong implementation note should contain enough detail/pseudocode for an independent implementation when practical. When exact behavior, edge cases, conventions, regression compatibility, or a stale code map matters, inspect the original repository.

### Reference repository access

The vault does not own codebases. Repositories remain external.

If source inspection is needed:

1. check whether the repository is already accessible,
2. use `$CODE_ROOT/$repo-name` only as a local lookup convention,
3. if needed ask the user to add it with `/add-dir /path/to/repo` or restart Claude with another `--add-dir`,
4. treat reference repos as read-only unless explicitly asked to modify them,
5. compare current `HEAD` with `last-verified-commit` if staleness could matter.

Never hallucinate source behavior from a note when source inspection is required.

### Code claims

The current repository is authoritative for what code actually does. Vault implementation notes record intent, mappings, portability, and history but may become stale.

When retrieved notes list `skills`, use the relevant skill before acting on that knowledge.

Use `/implement-concept` when transferring an existing concept/implementation. Use `/paper-to-implementation` when a paper/source is the primary specification.

### Zotero

`/process-inbox` should attempt `99_System/Scripts/refresh-zotero.py` first. If Zotero is unavailable, continue using the last successful metadata files and report that paper matching may be stale/incomplete. Never invent missing Zotero metadata.

### Knowledge maintenance

- Search before creating canonical concepts.
- Prefer updating an existing concept over duplicating it.
- Use broad tags; properties/wikilinks carry specific relationships.
- Preserve uncertainty and contradictions explicitly.
- Raw source evidence is never permanently deleted by ingestion workflows.
- Do not change vault-specific project folder structure unless explicitly asked.
