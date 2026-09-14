---
name: process-inbox
description: Process unclassified items from the engineering-brain Inbox, preserve raw evidence, and organize/link durable knowledge.
disable-model-invocation: true
context: fork
agent: general-purpose
---

# Process Inbox

Process items under the vault's `00_Inbox/`.

## Locate the vault

Prefer `$BRAIN_ROOT`. If unset, identify the directory containing `99_System/Core/Schema-Core.md`, `00_Inbox/`, and this `.claude/skills/` tree. **Do not assume the current working directory is the vault.**

Before processing Inbox items, attempt a local Zotero metadata refresh exactly once:

```bash
python3 "$BRAIN_ROOT/99_System/Scripts/refresh-zotero.py"
```

If `$BRAIN_ROOT` is unavailable but the vault root was located another way, invoke the same script by its resolved vault path.

If the refresh succeeds, use the regenerated `99_System/Zotero/library.json` and `references.bib`. If it fails because Zotero is closed or local API access is disabled, **do not fail the Inbox run**. Continue with the last successful metadata files if present and report the refresh warning. If no usable `library.json` exists, paper metadata matching may be incomplete; say so rather than inventing metadata.

The refresh script is read-only with respect to Zotero. Do not request local Zotero write authorization as part of Inbox processing.

Before processing anything else, read:

- `99_System/Core/Schema-Core.md`
- `99_System/Core/Tag-Taxonomy-Core.md`
- `99_System/Schema.md` if present (vault-specific extensions)
- `99_System/Tag Taxonomy.md` if present (vault-specific extensions)
- the relevant templates under `91_Templates/`

The Inbox is a queue. Successfully processed material must no longer remain in `00_Inbox/`.

## Core rules

1. Never permanently delete an Inbox source.
2. Search for an existing canonical note before creating a new one.
3. Prefer updating an existing concept over creating a duplicate.
4. Use broad tags only.
5. Use YAML properties for specific applicability.
6. Use wikilinks for conceptual relationships.
7. Preserve source provenance.
8. Do not infer that method-specific knowledge applies to a different method merely because a parent concept is broader.
9. Keep specialized child notes linked only to domains/methods where they genuinely apply.
10. Use portable external references (`external-root` + `external-path`) for authoritative files that live outside the vault.
11. External code repositories remain outside the vault; implementation notes point back to them rather than copying source trees into Obsidian.

## Ingestion mode

If a Markdown file contains:

```yaml
ingest-mode: organize-only
```

preserve its authored body text exactly except for clearly requested metadata/connection sections.

For organize-only notes:

- do not rewrite prose,
- do not summarize it again,
- do not simplify mathematics,
- do not change equations,
- add/fix YAML,
- identify parent/related/project links,
- add relevant `skills`,
- rename/move the file appropriately,
- append a concise `Connections` section only when useful.

Otherwise perform normal synthesis appropriate to the source.

## Classification

Classify durable notes using the schema, normally one of:

- map
- concept
- paper
- implementation
- project
- decision
- experiment
- simulation
- meeting
- resource
- conversation

## Literature

For papers:

1. Search `$BRAIN_ROOT/99_System/Zotero/library.json` if present.
2. Match by DOI first when possible, otherwise title/authors and other available CSL/Zotero identifiers.
3. Add DOI and available Zotero metadata. Add `citekey` only when Zotero/export metadata actually provides one; do not fabricate it.
4. Link the paper to concepts it actually addresses.
5. Never treat a paper note itself as the canonical definition of a reusable concept.
6. Preserve equation numbers, notation, assumptions, page references, and explicit limitations when available.

## Code snippets

1. Preserve the raw snippet under `90_Sources/Processed/Snippets/`.
2. Identify concepts represented by the snippet.
3. Create/update an implementation note only when useful.
4. Never claim correspondence to the current state of an external repository unless that repository has actually been inspected.

## External repository/codebase documentation

When the user asks Claude to process/document a codebase, the repository should stay outside the vault.

For each useful implementation note created from an inspected repository:

1. record `repo-name`,
2. record `repo-url` when a canonical remote exists,
3. record the inspected `last-verified-commit`,
4. set `transferability` deliberately rather than assuming portability,
5. set `source-inspection` based on how complete the note is,
6. include enough mathematical/engineering contract and portable pseudocode for an independent implementation,
7. separate portable, method/domain-specific, and repository-specific details,
8. map important requirements to repository-relative files/symbols/tests,
9. link other useful implementation precedents via `reference-implementations` rather than merging them into one note.

The implementation note should be useful without source access, but exact code remains authoritative for exact implementation behavior.

## Other source archiving

Archive raw evidence into the appropriate `90_Sources/Processed/` subtree. If the file's authoritative copy lives externally (Zotero, external engineering storage, another repository), preserve a stable reference rather than blindly duplicating large binaries.

## Related-note discovery

Search in this order:

1. likely filenames and Maps,
2. YAML summaries and relationship properties,
3. `parent`, `related`, `methods`, `domains`, `projects`, `reference-implementations`,
4. only then full note bodies.

Do not indiscriminately read the whole vault.

## Moving/renaming

Prefer Obsidian-aware move/rename operations (official Obsidian CLI when available) so wikilinks remain valid.

## Completion report

Report:

- Zotero metadata refresh status,
- Inbox files processed,
- canonical notes created,
- existing notes updated,
- important links/properties added,
- source artifacts archived/referenced,
- unresolved classification or interpretation questions.
