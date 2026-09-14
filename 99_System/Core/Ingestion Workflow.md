# Ingestion Workflow

`00_Inbox/` is a queue. A successfully processed item should no longer remain there.

## Zotero refresh first

At the beginning of every `/process-inbox` run, attempt:

```bash
python3 "$BRAIN_ROOT/99_System/Scripts/refresh-zotero.py"
```

This refreshes `99_System/Zotero/library.json` and `references.bib` from the local Zotero desktop API.

If Zotero is not running or the local API is unavailable, Inbox processing should continue using the last successful metadata files when present. A Zotero refresh failure is a warning, not a reason to abandon unrelated Inbox work.

## Two modes

### Normal synthesis

Raw paper, snippet, screenshot, notes, document, transcript, etc. Claude may extract and synthesize durable knowledge.

### Organize-only

For a Markdown note whose explanation is already finalized, add:

```yaml
ingest-mode: organize-only
```

The processor may add/fix metadata, links, provenance, naming, and placement, but must preserve the body text and equations.

## Raw evidence

Raw sources are never permanently deleted by the ingestion workflow.

Examples:

- PDF → Zotero authoritative copy and/or `90_Sources/Processed/Papers/`
- code snippet → `90_Sources/Processed/Snippets/`
- screenshot/plot → `90_Sources/Processed/Media/`
- transcript → `90_Sources/Processed/Conversations/`
- miscellaneous document → `90_Sources/Processed/Documents/`

Large external project files such as simulation projects, CAD assemblies, raw measurement archives, or fabrication files remain on their authoritative external storage; the vault stores portable references and notes.

## External code repositories

Complete source repositories remain outside the vault. Do not archive source trees under `90_Sources/`.

When a codebase is intentionally inspected/documented, create/update:

1. its project hub,
2. canonical concepts only when genuinely missing,
3. project-specific implementation notes under `04_Implementations/`.

Each substantial implementation note should preserve:

- a mathematical/engineering contract,
- enough portable pseudocode for independent reimplementation,
- assumptions/invariants,
- portable vs method/domain-specific vs repository-specific details,
- a code map to repository-relative files/symbols/tests,
- validation evidence,
- `repo-name`, `repo-url`, and `last-verified-commit`,
- `transferability` and `source-inspection`,
- links to useful `reference-implementations`.

The implementation note is the compact reusable specification. The original repository remains the exact implementation evidence.

For future ports, Claude should normally start from the implementation note. If exact behavior, edge cases, or unresolved conventions matter, it should obtain access to the referenced repository with `/add-dir` rather than guessing or requiring the vault to own a code copy.
