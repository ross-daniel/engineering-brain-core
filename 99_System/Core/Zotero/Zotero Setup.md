# Zotero Setup

Zotero is the source of truth for research PDFs and bibliographic metadata. Obsidian is the source of truth for your understanding, conceptual links, implementation mappings, and project history.

This template uses **Zotero 10's local API** directly; no third-party Zotero export plugin is required.

## 1. Install Zotero

Download Zotero from:

- <https://www.zotero.org/download/>

Install the Zotero Connector for your browser from the same page if you want one-click capture from the web.

## 2. Enable Zotero's local API

In Zotero:

**Settings → Advanced → Allow other applications on this computer to communicate with Zotero**

Enable that setting.

The local API is served by Zotero desktop at:

```text
http://localhost:23119/api/
```

This template only performs **read requests**. No Zotero API key is required for local reads. Zotero must be running when the metadata refresh script is called.

Official documentation:

- <https://www.zotero.org/support/dev/web_api/v3/local_api>
- <https://www.zotero.org/support/dev/web_api/v3/basics>

## 3. Optional first-time manual export

Normally the refresh script can create the metadata files itself as soon as Zotero is running and the local API is enabled.

If you want to seed the files manually first, or if the local API is not available yet, use Zotero's native export:

1. In Zotero, choose **File → Export Library…**.
2. Export **CSL JSON** to:

   ```text
   99_System/Zotero/library.json
   ```

3. Export **BibLaTeX** to:

   ```text
   99_System/Zotero/references.bib
   ```

These exports are ordinary metadata mirrors. Zotero remains authoritative.

## 4. Automatic local refresh

The vault includes:

```text
99_System/Scripts/refresh-zotero.py
```

Run it manually with:

```bash
python3 "$BRAIN_ROOT/99_System/Scripts/refresh-zotero.py"
```

or from the vault root:

```bash
python3 99_System/Scripts/refresh-zotero.py
```

The script reads only top-level bibliography items from the local Zotero API and atomically regenerates:

```text
99_System/Zotero/library.json
99_System/Zotero/references.bib
```

`library.json` is CSL JSON. `references.bib` is BibLaTeX.

The script does **not** edit Zotero's database or PDF files.

## 5. `/process-inbox` behavior

At the beginning of every `/process-inbox` run, Claude should attempt to run the refresh script once.

If refresh succeeds, paper matching uses the newly generated metadata.

If refresh fails because Zotero is closed or the local API is disabled:

- do not fail the entire Inbox run,
- keep the last successful `library.json` and `references.bib` unchanged,
- use the existing `library.json` for paper matching if it exists,
- warn clearly when a paper cannot be matched because no usable metadata file exists.

This makes Inbox processing useful even when Zotero is temporarily unavailable.

## 6. Paper workflow

1. Save/import the paper into Zotero.
2. Correct its bibliographic metadata in Zotero if needed.
3. Read/annotate it in Zotero.
4. Put either the raw PDF or your finished Markdown summary in `00_Inbox/`.
5. If your prose is already finalized, add:

   ```yaml
   ingest-mode: organize-only
   ```

6. Run `/process-inbox`.
7. The Inbox workflow refreshes Zotero metadata, matches the paper by DOI/title/authors where possible, adds links/properties, and moves the durable note into `03_Literature/`.
8. Raw evidence is preserved or referenced according to the Inbox rules.

If a raw PDF is temporarily dropped into the Inbox, the authoritative bibliographic/PDF copy should still live in Zotero. The vault may preserve a source copy only when that is useful for provenance or later agent access.
