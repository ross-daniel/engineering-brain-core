---
name: sync-brain
description: One-way comprehensive knowledge sync from another Engineering Brain vault into the current brain without modifying the source brain or mirroring vault-specific infrastructure.
disable-model-invocation: true
context: fork
agent: general-purpose
background: false
---

# One-Way Engineering Brain Knowledge Sync

Synchronize durable knowledge from another Engineering Brain vault into the
**current brain only**.

Invocation:

```text
/sync-brain /absolute/path/to/Other-Brain
```

Optional preview:

```text
/sync-brain /absolute/path/to/Other-Brain --dry-run
```

`$ARGUMENTS` contains the source-brain path and optional flags.

This is a **knowledge merge**, not a filesystem mirror.

The source brain is read-only. Never modify, move, rename, delete, format,
commit, stage, or otherwise mutate anything in the source brain.

The current brain is the target.

---

## 1. Resolve and validate the two brains

Determine:

- `TARGET_BRAIN`: the current Engineering Brain vault.
- `SOURCE_BRAIN`: the brain supplied in `$ARGUMENTS`.

Prefer the current working vault/root for `TARGET_BRAIN`. If the current working
directory is not clearly an Engineering Brain vault, use `$BRAIN_ROOT` only when
it unambiguously identifies the current target brain.

Before doing anything:

1. Resolve both paths to absolute canonical paths.
2. Refuse if source and target resolve to the same directory.
3. Verify both look like Engineering Brain vaults by checking for expected
   knowledge directories and/or core documentation.
4. Verify the source is readable.
5. Verify the target is writable.
6. If Claude does not currently have filesystem access to `SOURCE_BRAIN`, stop
   and instruct the user to add it with:

   ```text
   /add-dir /absolute/path/to/Other-Brain
   ```

   then rerun `/sync-brain`.

7. If the target is a Git repository and has uncommitted changes, warn before
   making changes. Do not mix unrelated local edits into a large sync without
   clearly reporting that state.

If `--dry-run` is present, perform discovery, matching, and planning only. Do not
write or copy anything.

---

## 2. Read the TARGET brain's rules first

The target brain's schema and taxonomy control the imported representation.

Read, when present:

- `99_System/Core/Schema-Core.md`
- `99_System/Schema.md`
- `99_System/Core/Tag-Taxonomy-Core.md`
- `99_System/Tag Taxonomy.md`
- `99_System/Core/Ingestion Workflow.md`

Do not force the source brain's project hierarchy or local taxonomy onto the
target brain.

The target brain owns its organization.

---

## 3. Sync scope

Synchronize durable knowledge from the source brain, including:

- `01_Maps/`
- `02_Concepts/`
- `03_Literature/`
- `04_Implementations/`
- durable project knowledge under `05_Projects/`
- archived source/evidence files under `90_Sources/Processed/`

Also include equivalent durable knowledge directories if a connected brain uses
the same Engineering Brain schema with slightly different subfolder names.

### Never sync these between brains

Do NOT synchronize:

- `00_Inbox/`
- `.git/`
- `.obsidian/`
- `.claude/`
- `.context-packs/`
- `91_Templates/`
- `92_Bases/`
- core/system implementation under `99_System/Core/`
- core scripts under `99_System/Scripts/`
- root `README.md`
- root `Quickstart.md`
- root `CLAUDE.md`
- `.env` or machine-local configuration
- `99_System/Zotero/library.json`
- `99_System/Zotero/references.bib`
- Zotero databases, credentials, API state, or sync settings
- transient source queues such as `90_Sources/Pending-Zotero/`
- duplicate/quarantine queues unless they contain the only surviving copy of a
  source needed by an imported canonical note

Shared operating-system functionality belongs in `engineering-brain-core` and
must propagate through `update-brain-core.sh`, not `/sync-brain`.

---

## 4. Fundamental sync rule

The operation is:

```text
TARGET <- SOURCE
```

Never:

```text
TARGET <-> SOURCE
```

and never:

```text
SOURCE <- TARGET
```

The objective is:

> After the sync, the target should contain every durable piece of knowledge,
> relationship, and source evidence that exists in the source and was missing
> from the target, while preserving all target-only knowledge and local
> organization.

Do not replace a richer target note with a source note merely because the source
file is newer.

Do not delete target information because it is absent from the source.

---

## 5. Build an inventory before writing

Inventory source and target separately.

For each Markdown note, collect when available:

- relative path
- title
- `type`
- `summary`
- `parent`
- `related`
- `domains`
- `methods`
- `projects`
- DOI
- citekey
- repository name / URL
- `last-verified-commit`
- aliases
- linked source files
- body headings

For source/evidence files, collect:

- relative path
- filename
- extension
- file size
- SHA-256 hash when practical

Do not read every large binary source into model context. Hash/copy it using
filesystem tools and inspect content only when required for matching or meaning.

---

## 6. Match equivalent canonical notes semantically

Do not rely on relative path or filename alone.

Match source notes to target notes using the strongest available identity.

### Literature

Prefer, in order:

1. DOI
2. stable citation key when trustworthy
3. normalized title + authors + year
4. normalized title

### Implementations / code documentation

Prefer:

1. repository URL + implementation/concept identity
2. `repo-name` + note purpose
3. project link + normalized title

Do not assume two implementations are equivalent merely because they share a
parent concept.

### Projects

Prefer:

1. repository URL or stable project identifier
2. `repo-name`
3. canonical project title + strong metadata agreement

### Concepts / maps

Use:

- normalized title / aliases
- note `type`
- parent relationships
- domain/method applicability
- summary semantics

Do not merge two similarly named concepts when their applicability differs.

Example:

```text
Error Estimation
```

is not automatically equivalent to:

```text
FEM Residual Error Estimation
```

Likewise, an FEM-specific child note must not acquire SIE applicability merely
because its parent concept is shared.

If equivalence is genuinely ambiguous, keep the notes distinct and report the
ambiguity instead of guessing.

---

## 7. Merge policy for an existing equivalent note

The target note is authoritative for target-local wording and organization.

Perform an **additive semantic merge**.

### YAML / properties

For list-valued semantic fields such as:

- tags
- domains
- methods
- parent
- related
- projects
- skills
- source-files
- reference-implementations
- formulations
- dimensions
- frequency-regimes
- geometry-regimes
- tools

take the semantic union, preserving target values and adding only source values
not already represented.

For scalar fields:

- if the target value is empty/missing and the source has a value, add it;
- if both agree, leave it alone;
- if both contain materially different nonempty values, preserve the target and
  report the discrepancy unless the field is explicitly additive.

Never silently broaden applicability.

For implementation provenance such as `last-verified-commit`, do not replace the
target value just because the source differs. Preserve both meanings in the note
or report that each brain documents a different verified source revision.

### Markdown body

Do not replace the entire target body.

Compare by section meaning, not exact wording.

Add source information only when the target genuinely lacks it, including:

- mathematical definitions
- equations
- assumptions
- limitations
- implementation behavior
- validation evidence
- design rationale
- historical decisions
- unresolved questions
- source/provenance links

When the same fact is already present in different words, do not duplicate it.

When source and target make conflicting claims:

1. preserve the target statement;
2. preserve the source claim with its provenance if it is substantively useful;
3. explicitly mark the conflict/dated implementation distinction;
4. do not invent a reconciliation.

Prefer integrating missing material into the relevant existing section.

If safe integration is not possible, add a clearly titled subsection such as:

```markdown
## Imported evidence / alternate implementation history
```

rather than overwriting existing prose.

---

## 8. Import policy for a note absent from the target

If no equivalent target note exists:

1. import the durable knowledge;
2. normalize its frontmatter to the TARGET brain's current schema;
3. preserve meaningful source metadata and links;
4. place it according to the target brain's organizational rules.

Preferred type destinations:

- `map` -> `01_Maps/`
- `concept` -> `02_Concepts/`
- `paper` -> `03_Literature/`
- `implementation` -> `04_Implementations/`
- project/decision/experiment/meeting/simulation/resource knowledge ->
  appropriate location under `05_Projects/`

Do not reproduce the source brain's top-level project taxonomy if it conflicts
with the target's custom taxonomy.

For project-specific notes:

- first try to match their `projects:` relationship to an existing target
  project;
- place them under that target project when appropriate;
- if the associated project is entirely absent, import the project knowledge
  conservatively under `05_Projects/` without restructuring existing project
  categories;
- report any project-placement choice that was not obvious.

Preserve wikilinks and repair them when imported filenames/locations differ.

---

## 9. Source/evidence synchronization

The source archive is part of the knowledge provenance and must be synchronized.

Primary scope:

```text
90_Sources/Processed/
```

For every source file referenced by imported or merged knowledge:

1. determine whether identical content already exists anywhere appropriate in
   the target source archive;
2. prefer SHA-256 equality over filename equality;
3. if identical content exists, reuse the target copy and update links rather
   than creating a duplicate;
4. if it does not exist, copy it into the target's appropriate
   `90_Sources/Processed/...` category;
5. preserve useful relative organization where compatible with the target.

### Filename collision

If the same destination filename exists but the hashes differ:

- never overwrite either file;
- create a collision-safe filename such as:

  ```text
  original-name__from-SourceBrain_<short-hash>.ext
  ```

- update imported/merged note links to the copied file;
- report the collision.

This applies to:

- PDFs
- conversation/handoff Markdown sources
- code snapshots/snippets
- figures/plots
- screenshots
- documents
- simulation-result artifacts
- other archived evidence

Do not copy external authoritative code repositories into `90_Sources` merely
because an implementation note references them. Repository code remains external
unless a deliberate archived snapshot already exists in the source brain.

---

## 10. Zotero behavior

Brain sync is NOT Zotero sync.

Do not:

- import items into Zotero,
- remove Zotero items,
- copy another brain's `library.json`,
- copy another brain's `references.bib`,
- alter Zotero settings.

A synchronized literature note/PDF may exist in the target brain even if the
target's Zotero metadata has not yet been refreshed or does not contain that
paper.

Preserve a meaningful `zotero-status` if one exists, but never fabricate a
Zotero item/key.

If this creates a target literature note whose Zotero relationship is missing,
report it as a follow-up item.

---

## 11. Current vs historical implementation knowledge

When the same concept or implementation appears in both brains, pay attention to
version/provenance.

A source brain may document:

- an older algorithm,
- a rejected approach,
- a different branch,
- a newer implementation,
- a different codebase implementation of the same general concept.

Do not flatten these into one allegedly timeless truth.

Use:

- repository identity,
- verified Git commit,
- dates,
- source type,
- explicit current/legacy labels

to preserve the distinction.

For scientific/engineering code, current source code remains authoritative for
what a repository presently does; synced vault notes are documentation and
history unless independently reverified.

---

## 12. Idempotency

The skill must be safe to run repeatedly.

A second run with no new source knowledge should produce no substantive target
changes.

Do not re-add:

- equivalent YAML values,
- duplicate wikilinks,
- duplicated paragraphs,
- duplicate source files,
- duplicate literature notes.

If a source note changed since a prior sync, import only the newly missing
knowledge or newly added evidence.

---

## 13. Do not treat source timestamps as truth

Do not use modification time alone to determine which brain is "newer".

The target may contain newer local knowledge even if the source file has a later
mtime due to formatting, Git checkout, or synchronization.

Compare actual content and provenance.

---

## 14. Dry-run output

For `--dry-run`, report a plan containing:

- source brain
- target brain
- new canonical notes to import
- existing notes that would receive additions
- source/evidence files to copy
- duplicate source files that would be reused
- ambiguous note matches
- conflicting claims/provenance
- project-placement uncertainties
- Zotero follow-ups

Do not write anything.

---

## 15. Normal completion report

After a real sync, report:

### Notes imported
Every new canonical note and destination.

### Notes enriched
Every existing target note changed and a concise description of what was added.

### Sources copied
Every new archived source/evidence file.

### Sources reused
Identical target sources reused instead of duplicated.

### Conflicts preserved
Claims/metadata that differed and were not silently reconciled.

### Ambiguities
Potential duplicate concepts/projects left separate.

### Zotero follow-up
Synced literature that is not represented in the target's local Zotero metadata,
when detectable.

### Git status
If the target is a Git repository, show the resulting `git status --short`.

Never automatically commit or push unless the user explicitly asks.
