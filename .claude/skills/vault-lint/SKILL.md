---
name: vault-lint
description: Audit the engineering-brain vault for structural, metadata, linking, provenance, and portability problems.
disable-model-invocation: true
context: fork
agent: Explore
---

# Vault Lint

Audit the vault without broadly rewriting content.

## Locate the vault

Prefer `$BRAIN_ROOT`; otherwise identify the vault root from `99_System/Core/Schema-Core.md`.

Read `99_System/Core/Schema-Core.md` and `99_System/Core/Tag-Taxonomy-Core.md` first; then read vault-specific `99_System/Schema.md` / `99_System/Tag Taxonomy.md` if present.

## Checks

Check for:

- missing required YAML properties on canonical notes,
- unknown/accidentally invented property names,
- invalid `type`, `status`, or `scope` values,
- invalid `transferability` or `source-inspection` values,
- hyper-specific/unapproved tags,
- unresolved wikilinks,
- orphan/dead-end notes where suspicious,
- likely duplicate canonical concepts,
- literature notes that cannot be matched to available Zotero metadata when a match is expected,
- implementation notes missing `repo-name`,
- implementation notes with a known remote but missing `repo-url`,
- implementation notes missing/stale `last-verified-commit`,
- implementation notes claiming portability but lacking a portable algorithm/contract or transferability discussion,
- implementation notes with `source-inspection: optional` that do not appear sufficient for an independent implementation,
- broken `reference-implementations` links,
- contradictory applicability/transferability metadata,
- source references that no longer resolve,
- Inbox items that appear already processed.

Use official Obsidian CLI commands such as unresolved/orphans/deadends when available.

## Safety

Do not automatically merge/delete likely duplicates or rewrite substantial note bodies. Report proposed fixes unless the user explicitly requests repairs.

## Output

Return a prioritized lint report grouped into:

- errors,
- likely structural problems,
- metadata inconsistencies,
- implementation/provenance/portability problems,
- link/provenance problems,
- optional cleanup suggestions.
