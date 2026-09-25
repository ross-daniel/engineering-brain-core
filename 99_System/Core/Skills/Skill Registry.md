# Skill Registry

Claude skills are stored in the hidden filesystem directory `.claude/skills/` and version-controlled with the vault.

## `process-inbox`

Classifies Inbox files, preserves raw evidence, applies schema/tags, links related knowledge, and moves processed material out of the Inbox. For inspected codebases, it creates implementation notes with source provenance and transferability metadata. Manually invoked.

## `vault-query`

Retrieves a small, relevant set of vault context while avoiding unrelated projects/workflows. When implementation work is relevant, it returns repository/commit/transferability/source-inspection information without automatically loading whole codebases.

## `implement-concept`

Implements or ports a reusable concept into the current target repository. It uses canonical knowledge plus existing implementation notes, separates portable/method-specific/repository-specific details, and selectively asks for access to original reference repositories when exact source inspection is needed.

Use this for workflows such as:

- one solver implementation → an analogous implementation in a different solver (for example, FEM → SIE/MoM),
- same algorithm → new programming language,
- existing hardware/software design pattern → new project.

## `paper-to-implementation`

Literature-focused implementation workflow. It translates a paper/source into a target implementation contract and can use existing implementation notes/repositories as supporting references. It follows the source-access/portability rules of `implement-concept`.

## `capture-session`

Writes only durable conclusions from the current Claude coding/research conversation back into the vault. It also maintains implementation-note provenance, transferability, code maps, and verification metadata when relevant.

## `context-pack`

Builds a compact Markdown context bundle for ChatGPT or another agent that cannot directly access the local vault. When implementation work is relevant, it includes repo/commit/transferability pointers rather than copying source repositories.

## `vault-lint`

Checks metadata/schema consistency, unresolved links, orphan notes, duplicates, and implementation provenance/portability problems.

## Domain-specific skills

Add domain-specific skills only after repeated workflows justify them, e.g. `fem-implementation` or `hfss-documentation`. Notes can reference applicable skills in their `skills:` YAML property.

## find-evidence

- `/find-evidence` — Finds papers in the processed research brain that support a supplied sentence or claim, verifies the evidence against the source paper/PDF, returns the exact LaTeX `\cite{...}` argument, and, when Claude is running from or has access to an external writing project, creates or updates that project's `references.bib` using the canonical BibTeX entries from the brain's Zotero export.

## sync-brain

Location:

`.claude/skills/sync-brain/SKILL.md`

Purpose:

Perform a one-way comprehensive knowledge merge from another Engineering Brain
into the current brain.

Usage:

`/sync-brain /absolute/path/to/Other-Brain`

Preview:

`/sync-brain /absolute/path/to/Other-Brain --dry-run`

The source brain is read-only. The skill synchronizes canonical knowledge and
archived source/evidence material while leaving vault-specific infrastructure,
templates, Inbox queues, Zotero metadata exports, and project taxonomy under the
control of the target brain.
