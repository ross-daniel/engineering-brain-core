---
name: vault-query
description: Retrieve a small, relevant set of engineering-brain knowledge for a task without loading unrelated projects or workflows.
context: fork
agent: Explore
---

# Vault Query

Answer the knowledge query supplied by the user while keeping retrieval narrow.

## Locate the vault

Prefer `$BRAIN_ROOT`. If unset, identify the directory containing `99_System/Core/Schema-Core.md` and `.claude/skills/`. Do not assume the current working directory is the vault.

## Retrieval order

1. Determine whether the current working repository corresponds to a vault project (`repo-name`, project name, or direct link).
2. Search matching project notes and implementation notes first when working from a code repository.
3. Search Map/index titles.
4. Search note filename, `summary`, `methods`, `domains`, `projects`, `parent`, `related`, and `reference-implementations` metadata.
5. Read only the strongest candidate note bodies.
6. Follow parent links only as needed to understand the broader concept.
7. Follow project/implementation/reference-implementation links only when relevant to the question.

Use the Obsidian CLI search/property/backlink commands when helpful and available.

## Implementation retrieval

When implementation/porting is relevant, return implementation-note provenance rather than silently loading entire repositories. Include when available:

- `repo-name`,
- `repo-url`,
- `last-verified-commit`,
- `transferability`,
- `source-inspection`,
- important code-map entries,
- validation evidence,
- explicit portable vs method-specific vs repository-specific distinctions.

An implementation note can be relevant as a precedent even when the target uses another method, but its method-specific details must not be generalized automatically.

If exact source inspection appears necessary, identify the referenced repository and recommend that the main session obtain access with `/add-dir`; do not claim to have read source code that is not accessible.

## Scope rules

If working from an external repository:

- prioritize that project's hub,
- its implementation notes,
- linked method-specific concepts,
- linked general concepts,
- linked literature.

Do not load unrelated work, school, or personal project histories unless the user's question or an explicit relevant link makes them necessary.

## Applicability

For every technical result preserve the distinction among:

- general,
- domain-specific,
- method-specific,
- project-specific.

Never generalize a specialized child claim merely because its parent has broader applicability.

## Return format

Return a compact context synthesis containing:

1. relevant notes and paths,
2. important facts/equations/design decisions,
3. applicability restrictions and assumptions,
4. source/evidence pointers,
5. implementation provenance/transferability when relevant,
6. applicable `skills` named by those notes.

Prefer roughly 3–8 highly relevant notes over a large dump.
