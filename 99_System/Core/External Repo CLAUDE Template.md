# External Repository CLAUDE.md Template

Copy/adapt the block below into important external code repositories.

```markdown
# Project Instructions

The current repository is authoritative for claims about its source code.

A separate engineering knowledge vault may be available through Claude Code's added directories.

## Knowledge retrieval

When `vault-query` is available, use it before broad conceptual research for tasks that may depend on prior project knowledge.

Prefer:
1. this project's implementation notes,
2. linked method-specific concepts,
3. linked general concepts,
4. relevant literature,
5. linked reference implementations when porting/reusing an idea.

Never scan the entire vault.

## Vault vs source code

Vault notes document mathematics, intent, design history, portability, and historically verified implementation mappings. Current source code is authoritative for what a repository actually does. If they disagree, inspect the repository/Git history and report the discrepancy.

Implementation notes are portable specifications plus provenance; they are not substitutes for source inspection when exact behavior, edge cases, or regression compatibility matter.

## Implementing or porting a concept

Use `implement-concept` when the task is to implement/reuse a concept that may already exist in another repository.

Before coding:

1. retrieve the canonical and method-specific concept notes,
2. retrieve relevant implementation notes,
3. separate portable, method/domain-specific, and repository-specific details,
4. inspect a referenced source repository when its `source-inspection` metadata or task requirements make this necessary,
5. map the resulting contract into this repository's current architecture and tests.

A reference repository is read-only unless the user explicitly asks to modify it. If it is not accessible, request `/add-dir /path/to/reference-repo` rather than guessing its contents.

## Literature-driven changes

Use `paper-to-implementation` when a paper/source is the primary specification. Existing implementation notes may be used as supporting evidence, but never override the paper's applicability/assumptions or the target repository's architecture.

When a retrieved note lists `skills`, apply relevant skills before implementation.

## Knowledge write-back

Do not casually rewrite vault knowledge during ordinary coding. Use `capture-session` explicitly when durable conclusions should be recorded.

After a verified implementation/port, update or create the target implementation note with its contract, transferability, code map, validation, reference implementations, and verified commit.
```
