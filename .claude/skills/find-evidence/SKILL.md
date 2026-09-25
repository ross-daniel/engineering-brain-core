---
name: find-evidence
description: Find papers in the engineering brain that support user-supplied claims, verify support against authoritative paper evidence, return exact LaTeX citation commands, and optionally add verified Zotero BibTeX entries to an external writing project's references.bib.
disable-model-invocation: true
context: fork
agent: general-purpose
---

# Find Evidence

Find defensible literature evidence for one or more user-supplied statements.

This skill is designed for a workflow in which:

- Zotero is the canonical bibliography/library,
- papers are processed into the engineering brain,
- the brain contains paper notes and preserved/referenced source evidence,
- the user writes a manuscript in a separate project directory,
- Claude is often launched from that manuscript directory with the brain exposed through `--add-dir "$BRAIN_ROOT"`.

The goal is not merely to find papers that are topically similar. The goal is to determine which papers actually support the user's claim, identify where that support appears, return the exact LaTeX `\cite{...}` argument, and, when safe, copy the corresponding canonical Zotero BibTeX entries into the manuscript project's `references.bib`.

## Invocation

Typical usage:

```text
/find-evidence
<one sentence, several sentences, or a paragraph containing claims that need citations>
```

The user may also specify constraints such as:

```text
Use only papers already in my brain.
Prefer foundational sources.
Prefer recent sources.
Only use papers I have processed.
Do not modify references.bib.
Target bibliography: ./paper/references.bib
```

User-supplied constraints override defaults.

## Locate the brain and working project

### Brain root

Prefer `$BRAIN_ROOT`.

If `$BRAIN_ROOT` is unset, identify the vault root as the directory containing:

- `99_System/Schema.md`,
- `99_System/Zotero/`,
- `.claude/skills/`.

Do not assume the current working directory is the brain.

Set conceptually:

```text
BRAIN_ROOT = engineering-brain vault root
WORK_ROOT  = current working directory at invocation
```

### External writing project

Treat `WORK_ROOT` as an external writing project only when it is outside `BRAIN_ROOT`.

This is the normal intended workflow:

```bash
cd /path/to/conference-paper
claude --add-dir "$BRAIN_ROOT"
```

When `WORK_ROOT` is inside `BRAIN_ROOT`, perform evidence retrieval and citation generation but do not create or modify a manuscript `references.bib` unless the user explicitly provides an external target path.

Never write manuscript-specific bibliography state back into the brain merely because the skill lives there.

## Source-of-truth rules

Use these rules strictly:

1. **Original paper evidence is authoritative for whether a paper supports a claim.**
2. A paper note, concept note, abstract, title, keyword, or Zotero metadata may identify candidates, but is not sufficient by itself to establish exact support when the original processed source is available.
3. `$BRAIN_ROOT/99_System/Zotero/references.bib`, when present, is authoritative for BibTeX entries and citekeys.
4. `$BRAIN_ROOT/99_System/Zotero/library.json`, when present, is authoritative supporting Zotero metadata for matching DOI/title/authors/citekey.
5. Do not invent a citation key.
6. Do not fabricate or silently reconstruct a BibTeX entry from memory when the canonical Zotero export is unavailable.
7. Do not state that a source supports a stronger claim than the source actually establishes.
8. Preserve important assumptions, restrictions, problem classes, function spaces, dimensionality, discretizations, and other applicability conditions.
9. Prefer primary sources for claims about a method's original formulation, derivation, theorem, or reported result.
10. A review or later paper may be useful corroboration, but do not substitute it for a primary source when the user's claim is specifically about who established or introduced something.

## Step 1 — Parse the requested claims

Split the supplied text into individually supportable claims.

Do not mechanically split every sentence if one sentence contains several logically distinct claims.

For each claim, identify:

- the core proposition,
- important qualifiers,
- scope/domain,
- whether the statement is descriptive, theoretical, empirical, historical, comparative, or implementation-specific,
- terms that must remain exact for a source to count as direct evidence.

Example:

```text
"hp-adaptivity can recover exponential convergence for solutions with spatially varying regularity"
```

may contain evidence requirements concerning:

- hp-adaptivity,
- exponential convergence,
- spatially varying/local regularity,
- the assumptions under which the convergence result holds.

## Step 2 — Retrieve candidate papers narrowly

Do not indiscriminately read the entire vault.

Search in this order:

1. relevant project/implementation/concept notes,
2. Maps and related canonical concepts,
3. paper notes linked to those concepts,
4. paper-note metadata including title, authors, DOI, citekey, topics, methods, domains, and summaries,
5. processed source evidence or source references for the strongest candidates,
6. Zotero metadata only as needed for identity/citekey resolution.

Candidate discovery may use summaries and notes.

Candidate **verification** must proceed to authoritative paper evidence whenever available.

Prefer papers already processed by the brain.

If an apparently ideal Zotero item exists but its full text has not been processed or is unavailable, label it as an unverified candidate rather than confirmed evidence.

## Step 3 — Verify evidence against the paper

For each serious candidate, inspect the original processed source or authoritative source reference.

Verify all of the following:

- the paper actually makes or demonstrates the relevant claim,
- the claim is not merely mentioned as background,
- the paper's result applies to the user's scope,
- important assumptions are compatible,
- the wording in the manuscript is not materially stronger than the evidence,
- a quoted or paraphrased result is not being taken out of context.

Record the most useful evidence locator available:

- page number,
- section,
- theorem/proposition,
- equation,
- figure/table,
- or another stable locator.

When possible, include a short paraphrase of what the source establishes.

Do not reproduce long copyrighted passages.

### Evidence classification

Classify each candidate as one of:

- **direct** — the paper directly establishes, derives, demonstrates, or explicitly states the claim under compatible assumptions;
- **supporting** — the paper supports an important part of the claim but does not independently establish the whole statement;
- **background** — relevant context only; not adequate by itself as evidence for the claim;
- **mismatch** — superficially relevant but materially different in scope/assumptions;
- **unverified** — likely relevant, but authoritative full-text evidence was not available to verify.

Only `direct` and, when logically appropriate, `supporting` papers should appear in the recommended `\cite{...}` command.

Never use `background`, `mismatch`, or `unverified` papers merely to make a citation list look stronger.

## Step 4 — Resolve citekeys and canonical BibTeX

For every recommended paper:

1. prefer the citekey recorded in the processed paper note,
2. cross-check it against `$BRAIN_ROOT/99_System/Zotero/references.bib` when present,
3. if necessary, match the paper in `$BRAIN_ROOT/99_System/Zotero/library.json` by DOI first, then exact/near-exact title plus authors,
4. verify that the selected BibTeX entry corresponds to the paper actually inspected.

If citekey identity is ambiguous, do not guess. Report the ambiguity.

If the paper is verified evidence but no canonical BibTeX entry can be found, still report the evidence, but mark bibliography insertion as unresolved and tell the user which Zotero item/export needs to be refreshed.

## Step 5 — Determine the manuscript bibliography target

Only perform this step when `WORK_ROOT` is external to `BRAIN_ROOT`, or the user explicitly supplied an external project path.

### Find an existing bibliography

Prefer, in order:

1. a user-specified `.bib` path,
2. a bibliography explicitly referenced by project `.tex` files through commands such as:
   - `\addbibresource{...}`
   - `\bibliography{...}`
3. `$WORK_ROOT/references.bib`,
4. a single unambiguous `.bib` file in the manuscript project.

Do not search outside the accessible manuscript project just to find a bibliography.

### Multiple bibliography files

If several plausible `.bib` files exist:

- inspect the manuscript's LaTeX bibliography commands to resolve the intended file;
- if still ambiguous, do not write to any of them;
- report the candidate paths and provide the citation command without modifying files.

### No bibliography exists

If no bibliography exists and `WORK_ROOT` is clearly an external writing project, create:

```text
$WORK_ROOT/references.bib
```

unless the user explicitly asked not to modify files.

## Step 6 — Safely update references.bib

When a bibliography target is unambiguous and canonical Zotero BibTeX entries are available:

1. read the existing file first,
2. preserve all existing entries and formatting,
3. determine which required citekeys are already present,
4. append only missing canonical entries copied from the brain's Zotero `references.bib`,
5. do not duplicate an existing citekey,
6. do not rewrite unrelated entries,
7. preserve the canonical entry text rather than reformatting it unnecessarily.

### Citekey conflict

If the target `references.bib` already contains the same citekey but its entry appears to refer to a different work:

- do not overwrite it,
- do not invent a new citekey,
- report the conflict explicitly,
- return the evidence result without modifying that conflicting entry.

### Duplicate work with different citekey

If the same DOI/work is already present under another citekey:

- do not silently add a duplicate,
- report both keys,
- prefer the key already used by the manuscript when it unambiguously identifies the same work,
- do not alter manuscript citations automatically unless the user requested citation cleanup.

## Step 7 — Produce the exact LaTeX citation

For every claim, return a directly copyable command such as:

```latex
\cite{houston2002hp,schwab1998p}
```

Use the exact citekeys that are present in, or were added to, the manuscript bibliography.

If one paper is sufficient, prefer a single well-matched citation over unnecessary citation stacking.

If several papers support different parts of the claim, explain the division of support.

Do not include a key in the final `\cite{...}` command if its BibTeX identity could not be resolved.

## Output format

Keep the final report concise enough to use while writing.

For each claim, report:

```text
Claim:
<claim text>

Recommended evidence:
- <Paper title> — <direct/supporting>
  Supports: <what it actually establishes>
  Evidence: <page/section/equation/theorem/figure/etc.>
  Scope/limitation: <important caveat, or "none material">

Use:
\cite{key1,key2}
```

Then report bibliography changes:

```text
references.bib:
- target: <path>
- added: <citekeys>
- already present: <citekeys>
- unresolved/conflicts: <citekeys or none>
```

If no source adequately supports a claim, say so clearly:

```text
No verified source in the processed brain adequately supports this claim as written.
```

Then explain the narrowest wording change that would be supported by the available literature, when useful.

## Multi-sentence input

When the user provides a paragraph or several sentences:

1. identify which claims actually need literature support,
2. avoid attaching the same citation mechanically to every sentence,
3. group claims only when the same papers genuinely support all of them,
4. return separate `\cite{...}` commands when different claims require different evidence.

## Important failure modes to avoid

Do not:

- select a paper only because its title contains the same keywords,
- cite an abstract without checking the full paper when the full paper is available,
- treat a paper note summary as stronger evidence than the PDF,
- claim a theorem/result applies outside its assumptions,
- conflate scalar, vector, `H^1`, `H(curl)`, DG, CG, 2-D, 3-D, affine, curved, isotropic, anisotropic, or other materially different settings,
- fabricate page numbers,
- fabricate DOI metadata,
- fabricate BibTeX,
- fabricate citation keys,
- overwrite the user's bibliography,
- add duplicate entries,
- modify the manuscript itself unless the user explicitly asks.

## Completion criteria

The skill is complete when it has:

1. decomposed the user's text into citation-worthy claims,
2. found the best candidate papers already in the brain,
3. verified recommended evidence against authoritative paper content,
4. resolved exact Zotero citekeys,
5. safely updated the external project's `references.bib` when appropriate,
6. returned exact copy/paste-ready LaTeX `\cite{...}` commands,
7. clearly identified unsupported, partially supported, or unresolved claims.
