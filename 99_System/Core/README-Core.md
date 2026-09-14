# Engineering Brain Core — Personalized Vault Setup and Usage

This file is synchronized into connected vaults as `99_System/Core/README-Core.md`. It documents the shared setup and operating model. Do not edit this copy for vault-specific documentation; the vault's root `README.md` is fully local and should describe that personalized vault.

## Operating model

The shared core assumes four distinct layers:

1. **Reusable knowledge** — concepts, mathematics, engineering principles, software patterns.
2. **Literature evidence** — what a specific paper/source actually says.
3. **Implementation/project knowledge** — how a concept is realized in a particular codebase or engineering project.
4. **Raw source material** — PDFs, snippets, plots, transcripts, exported documents, etc.

The ownership model is:

- Obsidian owns durable Markdown knowledge.
- Zotero owns research PDFs and bibliography metadata.
- Codebases remain independent Git repositories.
- Large simulation/CAD/measurement archives remain outside the vault and are referenced by portable metadata.
- `00_Inbox/` is a processing queue, not permanent storage.
- Broad tags identify coarse context/domain; YAML properties encode specific applicability; wikilinks encode conceptual relationships.
- Claude may access the vault without loading the whole vault into context.

A good implementation bridge looks like:

```text
canonical concept
      ↓
implementation note
(portable specification + pseudocode + applicability + provenance)
      ↓
original external repository, only when exact behavior matters
      ↓
new target implementation
```

Implementation notes should be sufficiently complete for an independent implementation when practical, while retaining `repo-name`, `repo-url`, `last-verified-commit`, code-map, validation, `transferability`, and `source-inspection` metadata so exact source behavior can be checked later.

## Required / recommended tools

Install tools from their official sources rather than bundling binaries inside a vault:

- Obsidian: <https://obsidian.md/download>
- Git: <https://git-scm.com/downloads>
- Claude Code: <https://code.claude.com/docs/en/setup>
- Claude Code skills: <https://code.claude.com/docs/en/skills>
- Zotero: <https://www.zotero.org/download/>
- Zotero local API: <https://www.zotero.org/support/dev/web_api/v3/local_api>
- Obsidian CLI: <https://obsidian.md/help/cli>
- Obsidian Git (optional): <https://github.com/Vinzent03/obsidian-git>
- Git LFS (optional): <https://git-lfs.com/>
- Kepano Obsidian skills (optional): <https://github.com/kepano/obsidian-skills>
- Anthropic document skills (optional): <https://github.com/anthropics/skills>

## Zotero 10 local metadata bridge

No Better BibTeX dependency is required. Enable in Zotero:

**Settings → Advanced → Allow other applications on this computer to communicate with Zotero**

The shared script:

```text
99_System/Scripts/refresh-zotero.py
```

reads the local Zotero API and regenerates:

```text
99_System/Zotero/library.json
99_System/Zotero/references.bib
```

`/process-inbox` attempts this refresh before processing the Inbox. If Zotero is closed or the local API is disabled, the Inbox workflow continues with the last successful exports and reports the warning.

For first-time bootstrap you may manually export **CSL JSON** to `library.json` and **BibLaTeX** to `references.bib`, but once the local API works the refresh script can maintain both files.

## Personalize the vault README

The root `README.md` belongs entirely to the personalized vault. Use it for information such as:

- what this particular vault is for,
- its chosen project-folder taxonomy,
- local or organizational conventions,
- machine/storage notes that are appropriate to version,
- links to the most important maps/projects,
- a pointer back to this shared guide.

A simple link from the personalized README can be:

```markdown
For shared Engineering Brain setup and workflows, see [[99_System/Core/README-Core|Engineering Brain Core Guide]].
```

The core updater never rewrites the root `README.md`.

## Knowledge model

Use folders for **note role**, not for every possible domain. A typical vault has role folders such as `01_Maps/`, `02_Concepts/`, `03_Literature/`, `04_Implementations/`, and a vault-specific `05_Projects/` hierarchy.

Keep tags broad. Example engineering tags might include:

```text
#area/software
#area/electronics
#area/numerical-methods
#area/embedded
#area/cem
#area/rf
```

The CEM/RF examples are illustrative engineering-domain examples, not assumptions about the vault owner.

Use YAML for specific applicability. For example:

```yaml
type: concept
status: canonical
scope: method-specific
tags:
  - area/numerical-methods
domains:
  - "[[Computational Electromagnetics]]"
methods:
  - "[[Finite Element Method]]"
parent:
  - "[[Error Estimation]]"
related:
  - "[[Galerkin Orthogonality]]"
```

A broader parent can relate to multiple methods while a specialized child links only to the method(s) it actually supports. For example, `[[Error Estimation]]` may connect FEM and SIE/MoM, while an FEM-only residual estimator should not link itself to SIE simply because the parent concept is broader.

## Adding custom tags and concepts

If you know a note belongs to a new broad context/domain, add a broad tag only when it is useful across many notes. Put precise relationships in properties/wikilinks.

Prompt example:

```text
This note is about RF front-end design. Add the existing broad RF/electronics tags if appropriate. Create or link canonical concepts for impedance matching and noise figure. Do not create a highly specific tag for every concept; use wikilinks and YAML relationships instead.
```

If you know the exact applicability:

```text
This method is FEM-specific. Its parent is [[Error Estimation]], but the method itself does not apply to SIE/MoM. Preserve that distinction in `methods`, `parent`, and related links.
```

## Process a paper

Preferred flow:

1. Save the authoritative PDF in Zotero.
2. Put either the raw PDF or a Markdown summary into `00_Inbox/`.
3. For a hand-written/finalized summary, add:

```yaml
ingest-mode: organize-only
```

4. Start Claude with vault access and run:

```text
/process-inbox
```

The skill refreshes Zotero metadata, matches the paper where possible, creates/updates the literature note and concepts, records applicability, links related material, archives the raw Inbox item, and leaves the Inbox clear.

If you already know the paper classification, say so explicitly:

```text
/process-inbox

For Smith 2026: this paper is about goal-oriented FEM error estimation on curved elements. Link it to [[Error Estimation]], [[Finite Element Method]], and [[Curved Isoparametric Mapping]]. It is not an SIE-specific formulation. Preserve my authored summary unchanged.
```

## Document an external codebase

Keep the repository outside the vault. From the codebase, launch Claude with the vault as an additional directory, for example:

```bash
cd "$CODE_ROOT/example-solver"
claude --add-dir "$BRAIN_ROOT"
```

Ask Claude to document the repository rather than copying it into Obsidian:

```text
Use the vault to document this repository. Create/update the project note and implementation notes. Map mathematical/engineering requirements to repository-relative files, symbols, tests, validation evidence, and the current Git commit. Separate portable behavior from method-specific and repository-specific details.
```

If you know what the code actually implements, tell Claude directly:

```text
This repository implements a frequency-domain FEM eigenproblem with H(curl)-conforming elements. Treat that as authoritative user context, inspect the code to verify the exact implementation, and classify/link the resulting notes accordingly.
```

## Port a concept or implementation between codebases

From the **target** repository:

```bash
cd "$CODE_ROOT/target-solver"
claude --add-dir "$BRAIN_ROOT"
```

Then:

```text
/implement-concept
Port the error-estimation strategy documented in the vault into this target solver. First separate portable concepts from source-method-specific details and repository-specific choices. If exact behavior from the reference implementation is needed, tell me which repository to add with /add-dir before you rely on it.
```

If the original implementation must be inspected, add that repo to the active Claude session:

```text
/add-dir /path/to/reference-repo
```

The target repository remains the main work area; the reference repository should be treated as read-only unless explicitly requested otherwise.

## Implement a specific idea from a paper

When a paper is the primary specification:

```text
/paper-to-implementation
Implement Equation (12) from [[Paper - Example]] in the current repository. Preserve the paper's notation/assumptions, derive the computational contract, inspect existing architecture, map requirements to files/functions/tests, then implement and validate it. Use any relevant implementation notes only as supporting references, not as substitutes for the paper.
```

## Ask ChatGPT for literature synthesis

Generate a narrow context pack first:

```text
/context-pack Explain <concept>, emphasizing the relevant literature and exact source references.
```

Upload that context pack plus any PDFs needed for exact quotations/figures to ChatGPT. Example prompt:

```text
Explain this concept using the attached context pack and source papers. Compare the relevant papers, use short direct quotes where they materially help, and cite exact page numbers, equation numbers, and figure numbers. Clearly separate what each source explicitly states from your synthesis or derivation.
```

For exact quotations/equation/figure references, the source PDF is authoritative; a Markdown summary is not a substitute for checking the paper.

## Shared Claude skills

The core currently provides:

- `/process-inbox` — classify/link/archive Inbox material; refresh Zotero metadata first.
- `/vault-query` — retrieve a small, relevant slice of vault knowledge.
- `/implement-concept` — reimplement/port an existing concept or known implementation.
- `/paper-to-implementation` — translate a paper/source into verified code changes.
- `/capture-session` — persist durable conclusions from a productive Claude session.
- `/context-pack` — produce a compact context bundle for another AI session.
- `/vault-lint` — audit schema/link/provenance quality without silently rewriting the vault.

## Shared-core updates

A connected vault has:

```text
99_System/Scripts/update-brain-core.py
99_System/Scripts/update-brain-core.sh
```

Set, for example:

```bash
export BRAIN_CORE_ROOT="$HOME/Documents/engineering-brain-core"
```

Preview an update:

```bash
./99_System/Scripts/update-brain-core.sh --dry-run
```

Apply it:

```bash
./99_System/Scripts/update-brain-core.sh
```

The updater only touches paths declared by `engineering-brain-core/core-manifest.json` and the marked core section of `CLAUDE.md`. The vault's root `README.md` is entirely vault-owned. The core does not own project folders, notes, `Home.md`, `.obsidian/`, or vault-specific taxonomy/profile files. It records the synchronized core version under `99_System/Core/`.

If you directly edit a core-managed file or marked section, the next update stops instead of silently overwriting your local change. Put vault-specific customizations in the local/profile files outside the managed boundary.
