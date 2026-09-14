# Core Schema

This file defines the shared baseline metadata vocabulary for Engineering Brain vaults. Vaults may extend it in `99_System/Schema.md`, but should avoid contradicting these baseline meanings unless an override is documented explicitly.

## Required properties for canonical Markdown notes

- `type`
- `status`
- `summary`
- `tags`
- `scope`
- `created`
- `updated`

## `type`

Allowed values:

- `map`
- `concept`
- `paper`
- `implementation`
- `project`
- `decision`
- `experiment`
- `simulation`
- `meeting`
- `resource`
- `conversation`

## `status`

Allowed values:

- `seed`
- `developing`
- `canonical`
- `deprecated`
- `archived`

## `scope`

Allowed values:

- `general`
- `domain-specific`
- `method-specific`
- `project-specific`

## Relationship properties

These should usually contain Obsidian wikilinks:

- `domains`
- `methods`
- `parent`
- `related`
- `projects`
- `reference-implementations`

A broad parent may apply to several methods while a specialized child links only to the methods it actually supports.

Illustrative engineering example: `[[Error Estimation]]` may connect both FEM and SIE/MoM, while `[[FEM Residual Error Estimation]]` should link to FEM but not to SIE merely because its parent is broad.

## Applicability properties

Use only when meaningful:

- `formulations`
- `dimensions`
- `frequency-regimes`
- `frequency-min-hz`
- `frequency-max-hz`
- `geometry-regimes`
- `tools`

Keep these flat rather than creating deeply nested YAML objects.

## AI / implementation properties

- `skills` — Claude skills relevant when acting on this knowledge.
- `repo-name` — logical repository name.
- `repo-url` — canonical Git remote URL for an external repository.
- `last-verified-commit` — commit hash against which a mapping was checked.
- `transferability` — expected portability of an implementation.
- `source-inspection` — whether source inspection is normally needed before porting/reproducing exact behavior.

### `transferability`

Allowed values:

- `high`
- `partial`
- `low`
- `implementation-specific`

This field never overrides `methods`, `domains`, or other applicability metadata.

### `source-inspection`

Allowed values:

- `optional`
- `recommended`
- `required`

Implementation notes should still contain a useful portable specification even when source inspection is recommended or required.

## Repository portability

The vault does not own code repositories. Prefer portable metadata:

```yaml
repo-name: example-solver
repo-url: git@host:user/example-solver.git
last-verified-commit: abc1234
```

Do not store machine-specific absolute source paths as canonical knowledge. `$CODE_ROOT/$repo-name` may be used as a local lookup convention. If Claude needs a repository that is not accessible, request `/add-dir /path/to/repo` rather than guessing its contents.

## Source properties

- `source-files`
- `external-root`
- `external-path`

`external-root` is a machine-local alias; `external-path` is relative to it.

## Literature properties

Paper notes may additionally use:

- `citekey`
- `doi`
- `zotero-link`
- `zotero-status`

## Inbox-only property

`ingest-mode: organize-only`

When present, the Inbox processor must preserve authored body text/equations and only classify, link, add/fix metadata, rename/move, and archive provenance.
