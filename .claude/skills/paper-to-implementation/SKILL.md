---
name: paper-to-implementation
description: Translate mathematical or engineering literature into a verified implementation in the current repository, using existing implementations as references when helpful.
---

# Paper to Implementation

Use this workflow when a paper/source is the primary specification for a code change.

This skill is a literature-focused specialization of the broader `implement-concept` workflow.

## 1. Retrieve narrow knowledge

Use `vault-query` to retrieve only relevant:

- paper notes,
- canonical concepts,
- method/domain-specific concepts,
- existing implementation notes,
- target-project decisions.

Read the original paper/source whenever exact equations, assumptions, figures, algorithms, or wording matter and the vault note is insufficient.

## 2. Separate four classes of information

Always distinguish:

A. statements directly made by the source,
B. mathematical/engineering consequences derived from the source,
C. interpretation required for implementation,
D. project-specific engineering decisions.

Do not silently turn category C or D into a claim made by the paper.

## 3. Extract the source implementation contract

Extract as applicable:

- governing equations,
- notation,
- assumptions,
- function spaces / discretization,
- transforms/mappings,
- quadrature/integration requirements,
- constitutive/material rules,
- boundary conditions / excitations,
- algorithmic steps,
- convergence/validation criteria.

Convert each requirement into:

`source requirement → computational operation → data required → evidence/reference → validation/test`.

## 4. Use existing implementations as evidence, not prescriptions

If `vault-query` finds one or more implementation notes for the same/related concept:

1. read their `transferability` and `source-inspection` metadata,
2. separate portable, method-specific, and repository-specific details,
3. use `reference-implementations` links when available,
4. inspect the actual reference repository when exact behavior or unresolved details matter.

Follow the source-access/provenance rules in `implement-concept`, including `/add-dir` for reference repositories that are not already accessible.

A prior FEM implementation, for example, can illuminate software structure or general estimator logic without proving that FEM-specific residual/localization formulas apply to SIE/MoM.

## 5. Inspect the target repository

Map source requirements to actual current:

- files,
- classes/functions,
- data structures,
- tests,
- configuration/input formats.

Classify each requirement as:

- already implemented,
- partially implemented,
- missing,
- incompatible,
- ambiguous.

Read/invoke applicable skills listed in retrieved notes' `skills:` property.

## 6. Coding rule

Do not make code changes until the source-to-math-to-target-code mapping is sufficiently clear.

The current target repository is authoritative for its code state. An external reference repository is read-only unless the user explicitly asks to modify it.

When changing code, add/update validation that demonstrates the relevant source requirement when practical.

## 7. Knowledge write-back

After verification, update/create the target implementation note with:

- source-to-code mapping,
- portable pseudocode,
- assumptions/invariants,
- transferability analysis,
- reference implementation links,
- validation outcome,
- important deviations/decisions,
- target `repo-name`/`repo-url`,
- `last-verified-commit` when a stable commit exists,
- source-inspection guidance for future ports.
