---
name: context-pack
description: Build a compact Markdown context bundle from the vault for ChatGPT or another agent without direct vault access.
disable-model-invocation: true
context: fork
agent: Explore
---

# Context Pack

Create a focused Markdown context bundle for the requested topic.

## Locate the vault

Prefer `$BRAIN_ROOT`; otherwise identify the vault root from `99_System/Core/Schema-Core.md`.

Create `$BRAIN_ROOT/.context-packs/` if needed. This directory is intentionally Git-ignored.

## Retrieval

Use the same narrow retrieval discipline as `vault-query`:

1. project/implementation notes when relevant,
2. maps,
3. canonical concepts,
4. relevant paper notes/evidence,
5. only source excerpts necessary to preserve provenance.

Avoid unrelated workflows/projects.

## Implementation provenance

When code/porting is relevant, include the implementation-note metadata needed for another agent to understand what was actually verified:

- repository name/remote,
- last verified commit,
- transferability,
- source-inspection guidance,
- portable vs method/domain-specific vs repository-specific distinctions,
- important source-code entry points/tests.

Do not embed whole external repositories into a context pack. If the receiving agent needs source-level verification, identify the repository/files that the user should separately provide or make accessible.

## Pack structure

Create one Markdown file containing:

- task/topic,
- relevant note index with vault paths,
- concise project state,
- relevant canonical concepts,
- key equations/assumptions/restrictions,
- implementation mappings/decisions if relevant,
- implementation provenance/transferability if relevant,
- literature/source references,
- open questions,
- recommended skills/workflow for the receiving agent.

Prefer a compact useful pack over exhaustiveness. Unless the user asks otherwise, target roughly 5–12 source notes and avoid copying whole notes when excerpts/summaries are sufficient.

Name the output descriptively under `.context-packs/` and report the path.
