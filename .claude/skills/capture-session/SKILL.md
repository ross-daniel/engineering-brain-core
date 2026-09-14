---
name: capture-session
description: Distill durable knowledge from the current Claude conversation into the engineering brain.
disable-model-invocation: true
---

# Capture Session

Review the current conversation and write only durable knowledge back into the vault.

## Locate the vault

Prefer `$BRAIN_ROOT`; otherwise identify the vault root from `99_System/Core/Schema-Core.md`.

## Capture

Extract only durable items such as:

- mathematical conclusions,
- engineering decisions,
- architecture choices,
- important successful/failed approaches worth remembering,
- validation results,
- implementation mappings,
- portability/transferability conclusions,
- source-code provenance and verification points,
- unresolved questions that matter later.

Do not create a transcript summary merely for completeness.

## Search before writing

Prefer, in order:

1. updating an existing canonical concept,
2. updating an implementation/project note,
3. creating a decision/experiment/simulation note,
4. creating a new concept only when necessary.

## Implementation-note maintenance

When the session materially changes or verifies an implementation note, update as appropriate:

- mathematical/engineering contract,
- portable pseudocode,
- assumptions/invariants,
- portable vs method/domain-specific vs repository-specific distinctions,
- code map,
- validation evidence,
- `repo-name` and `repo-url`,
- `reference-implementations`,
- `transferability`,
- `source-inspection`,
- `last-verified-commit` when a stable verified commit exists.

Do not claim a commit was verified if it was not inspected/tested in the session.

## Epistemic labels

Preserve the distinction among:

- established fact,
- source claim,
- our derivation,
- implementation/design decision,
- unresolved hypothesis.

Do not convert uncertainty into fact.

## Completion

Report exactly which vault files were created or changed and why.
