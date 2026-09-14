---
name: implement-concept
description: Implement or port a vault concept into the current repository using canonical knowledge, existing implementation notes, and selectively inspected reference repositories.
---

# Implement Concept

Use this workflow when the user wants to implement a reusable concept in the current repository, especially when the concept already exists in another codebase.

The current working repository is the **target repository**. External repositories are references unless the user explicitly says otherwise.

## 1. Retrieve narrow vault context

Use `vault-query` to retrieve only the relevant:

- canonical concept/map notes,
- method/domain-specific child concepts,
- target-project notes,
- implementation notes,
- paper/source notes,
- prior engineering decisions.

Do not load unrelated workflows/projects.

## 2. Establish target applicability before reusing anything

Identify the target repository's:

- method,
- domain,
- formulation,
- dimensionality,
- frequency/geometry regime when relevant,
- software/language constraints.

Do not assume an implementation transfers merely because it shares a parent concept.

Example: a FEM error-estimator implementation can be a useful precedent for an SIE/MoM estimator while its element residuals, jump terms, finite-element projections, and function-space machinery may be non-portable.

## 3. Read implementation notes as portable specifications

For each relevant implementation note, inspect:

- `transferability`,
- `source-inspection`,
- `repo-name`,
- `repo-url`,
- `last-verified-commit`,
- `reference-implementations`,
- mathematical/engineering contract,
- portable pseudocode,
- assumptions/invariants,
- transferability section,
- code map,
- validation evidence.

Treat the note as a **portable specification and provenance map**, not as a replacement for source code.

## 4. Split the source implementation into three layers

Before coding, explicitly classify details as:

### A. Portable / concept-level

Mathematical or engineering behavior that should survive a change of language/repository and, where justified, a change of method.

### B. Method/domain-specific

Details that depend on FEM, SIE/MoM, FDTD, a frequency regime, geometry assumptions, hardware constraints, etc. These must be retained only when the target shares the same applicability, otherwise re-derived/replaced.

### C. Repository-specific

Class hierarchy, array shapes, naming, optimization choices, caches, file layout, framework APIs, and other software architecture that should not be mistaken for the underlying concept.

## 5. Decide whether original source inspection is needed

Inspect the original repository when any of the following is true:

- the implementation note has `source-inspection: required`,
- it has `source-inspection: recommended` and exact behavior matters,
- pseudocode/notes leave an ambiguity that affects correctness,
- edge-case handling or numerical conventions matter,
- regression compatibility is desired,
- the recorded implementation appears stale,
- the user explicitly asks to reproduce/port the existing implementation.

Source inspection is usually optional when the note fully specifies the algorithm and the task is an independent implementation rather than behavioral reproduction.

## 6. Obtain source access safely

First check whether the referenced repository is already one of Claude's accessible directories.

If the note gives `repo-name` and `$CODE_ROOT` is defined, `$CODE_ROOT/$repo-name` is a useful local candidate, but do not assume Claude has permission to read it.

If the reference repository exists locally but is not accessible, tell the user exactly which repo is needed and ask them to add it with:

```text
/add-dir /path/to/reference-repo
```

or restart Claude with:

```bash
claude --add-dir "$BRAIN_ROOT" --add-dir /path/to/reference-repo
```

If it is not cloned, report the `repo-url` from the note so the user can clone the correct repository. Do not invent a local path or claim to have inspected inaccessible code.

Treat reference repositories as **read-only** unless the user explicitly asks to modify them.

## 7. Verify provenance before relying on exact source behavior

If the implementation note records `last-verified-commit`:

1. inspect the reference repository's current `HEAD`,
2. note whether it matches the recorded commit,
3. if it differs and exact behavior matters, inspect the relevant history/diff before trusting the old mapping.

The current source code is authoritative for what that repo does now. The implementation note is authoritative only for what was documented at its recorded verification point.

## 8. Build a target implementation contract

Before editing the target repository, write a compact mapping:

`concept requirement → target computational operation → target data/API → validation`

Also state:

- what is being reused unchanged,
- what is being adapted,
- what is being re-derived,
- what source/reference implementation informed each choice.

## 9. Inspect the target repository

Map the target contract to actual current:

- files,
- classes/functions,
- data structures,
- tests,
- configuration/input formats.

Classify target requirements as:

- already implemented,
- partially implemented,
- missing,
- incompatible,
- ambiguous.

Do not code until the conceptual transfer and target mapping are sufficiently clear.

## 10. Implement independently and validate

Implement the target method using the target repository's architecture rather than blindly copying the reference repository.

If copying source text rather than reimplementing the algorithm, verify that ownership/license terms permit it and preserve required notices.

Add or update tests/validation that demonstrate the mathematical/engineering requirement. Prefer independent validation over mere byte-for-byte agreement with the reference implementation.

## 11. Write knowledge back

After validation, create/update an implementation note for the **target** repository containing:

- mathematical/engineering contract,
- portable pseudocode,
- assumptions/invariants,
- transferability analysis,
- code map,
- reference implementation links,
- validation evidence,
- `repo-name`, `repo-url`,
- `last-verified-commit` when a stable target commit exists,
- appropriate `source-inspection` guidance for future ports.

Do not overwrite the source implementation note with target-specific details.
