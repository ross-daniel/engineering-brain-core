# Core Tag Taxonomy

Tags are intentionally broad. Do not encode the full ontology in tags; use YAML properties and wikilinks for specificity.

## General rules

1. Prefer no tag over a hyper-specific new tag.
2. Specific method/domain applicability belongs in properties such as `methods`, `domains`, `formulations`, and `frequency-regimes`.
3. Relationships belong in `parent`, `related`, and ordinary `[[wikilinks]]`.
4. Add a new broad tag only when it will be reused across many notes and is useful for browsing.
5. Project identity normally belongs in `projects:`, not in a unique project tag.

## Illustrative engineering area tags

These are examples, not mandatory defaults:

- `#area/software`
- `#area/electronics`
- `#area/embedded`
- `#area/numerical-methods`
- `#area/cem`
- `#area/rf`
- `#area/controls`
- `#area/thermal`
- `#area/mechanical`
- `#area/manufacturing`
- `#area/business`

Vault-specific context tags belong in `99_System/Tag Taxonomy.md`.
