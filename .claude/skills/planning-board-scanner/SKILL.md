---
name: planning-board-scanner
description: Workflow and conventions for this repo - researching town/city planning board websites (finding agenda/minutes archives, working around bot protection), downloading their PDFs, and analyzing those PDFs to spot residential/commercial development projects. Use whenever the task involves a new or existing town's planning board site, or the PDF tools in wwiocode/pyscript.
---

# Planning Board Scanner

This repo's goal: find public planning-board documents (agendas, minutes, and
supporting materials) for towns/cities, so residential/commercial development
projects can be surfaced for trades pros. Work happens in two phases per town:
(1) recon the town's website and document how to access it, (2) pull and
analyze the actual PDFs.

## Permissions - work within what's pre-approved

`.claude/settings.local.json` pre-approves exactly these Bash command
prefixes, matched against the **whole** command string:

- `playwright-cli -s=planscan ...`
- `wwiocode/pyscript/plan_entry.py ...` (run from the project root)

Plus `WebSearch`, and Read/Edit/Write anywhere under `working/` and
`towninfo/`.

Because the match is against the entire command, **never chain, pipe, or
combine commands** - no `|`, `&&`, `;`, or command substitution tacked onto
a `playwright-cli` or `plan_entry.py` call. Each of these breaks the
allowlist match and forces a new permission prompt:

```bash
# Don't:
playwright-cli -s=planscan goto https://example.town.gov | tail -30
wwiocode/pyscript/plan_entry.py PdfInfo pdf=working/TARGET.pdf 2>&1 | tail -3 && cat working/OUTPUT.txt
mkdir -p working/example_town && wwiocode/pyscript/plan_entry.py FetchUrl ...

# Do: one bare command per call, full output goes to context automatically
playwright-cli -s=planscan goto https://example.town.gov
wwiocode/pyscript/plan_entry.py PdfInfo pdf=working/TARGET.pdf
```

Other consequences:

- Don't `cd` into a subdirectory before invoking `plan_entry.py`, and don't
  open an unnamed/default Playwright session - always `-s=planscan`.
- Never pipe/redirect a call's own output (`| tail`, `| head`, `2>&1 |`,
  `> file`) - if a snapshot or result is large, it's saved to a persisted
  file automatically and the tool result tells you where; read that file
  with the Read tool, not `cat` (there's no bare `cat`/`Bash(cat *)` grant).
- There's no `mkdir` grant either. To create a new `working/<town>/`
  directory, use the Write tool to write a placeholder file inside it
  (e.g. `working/<town>/.keep`) - Write creates missing parent directories
  as a side effect - or just pass `dest=working/<town>` to `FetchUrl` after
  that placeholder write, since `FetchUrl` itself requires the destination
  to already exist.

If a task genuinely needs something outside this set, just ask normally
rather than working around it.

## Repo layout

- `towninfo/<town>.md` - one write-up per town: platform/CMS, bot-protection
  behavior, the exact URL structure for agendas/minutes, and content notes.
  Write one of these for every new town investigated (see existing files for
  the expected level of detail: `rochester_nh.md`, `dover_nh.md`).
- `working/` - gitignored scratch area for downloaded documents.
  - `working/<town>/` - raw PDFs downloaded from that town's site.
  - `working/TARGET.pdf`, `working/OUTPUT.txt`, `working/OUTPUT_PAGES/` -
    the fixed, hardcoded input/output paths for the PDF analysis tools below.
- `wwiocode/pyscript/plan_entry.py` + `plan_util.py` - the tool entry point
  and its implementation.

## Logging a scan pass

Every time you sit down to check a town's site for new documents - whether
it's the first-ever recon of a new town or a routine re-check of one
already set up - bracket that work with `StartScanLog`/`EndScanLog`. This
writes to the `scan_log` table (see `plan_db.py`), which is distinct from
`analysis_log`: `scan_log` records *finding* files by visiting a town's
site, `analysis_log` records *analyzing* an already-downloaded file for
projects.

```bash
wwiocode/pyscript/plan_entry.py StartScanLog town=example_town_nh
# -> prints the new scan_id, e.g. "Started scan_log 12 for example_town_nh. ..."
```

Then, for every file you download and register during this pass, pass that
same `scan_id=` to `IngestPdfTool` (see Phase 2 below) so
`documents.first_scan_id` records which scan pass first found it:

```bash
wwiocode/pyscript/plan_entry.py IngestPdfTool pdf=working/example_town_nh/2026.09.22_Agenda.pdf scan_id=12
```

`first_scan_id` is only ever set once - re-running `IngestPdfTool` later
(without `scan_id=`, or re-ingesting to refresh keyword hits) never
clobbers it, so it's safe to pass `scan_id=` only on the call that
immediately follows discovery.

When you're done checking the site, close the scan out with a short note on
what you found (or didn't):

```bash
wwiocode/pyscript/plan_entry.py EndScanLog scan_id=12 notes="checked Agenda Center back to Jan 2026, found 2 new PDFs"
```

Do this even if the pass turned up nothing new (`notes="no new files since last scan"`) -
same principle as always calling `LogAnalysis` in the analyze-planning-file
skill: a scan pass with no `scan_log` row is invisible to anything that
later wants to know when a town was last checked.

To pick which town to re-scan next, run
`wwiocode/pyscript/plan_entry.py NextToScan` (`limit=0` for all towns) -
never-scanned towns first, then oldest last scan pass. It's the scan-side
counterpart of `NextToAnalyze`; `towns.wisp` shows the same thing as its
"Last Scanned" column / "Next To Scan" sort.

## Phase 1: researching a town's site

Use the `playwright-cli` skill, always with the `planscan` session name
(`-s=planscan` on every call) - never a default/unnamed session:

```bash
playwright-cli -s=planscan open https://example.town.gov   # first call opens the session
playwright-cli -s=planscan goto https://example.town.gov/planning-board
playwright-cli -s=planscan snapshot
playwright-cli -s=planscan find "agenda"
playwright-cli -s=planscan click e15
```

Check `playwright-cli -s=planscan list` first if unsure whether the session
is already open. Navigate the town's site to find its planning board's
agenda/minutes archive. Things to establish and write down in
`towninfo/<town>.md`:

- What CMS/platform the site runs (CivicPlus, a custom site + a document
  management system like Treeno, etc).
- Whether the site has bot protection (Cloudflare or similar), and what
  works to get past it. **Rochester, NH is hard-blocked in headless mode but
  passes cleanly headed** - always try headed first if headless 403s with a
  "Just a moment" / "security verification" page; don't reach for
  fingerprint-spoofing or stealth techniques to force past a block.
- The URL structure for the agenda and minutes archives - ideally a stable,
  guessable pattern (like Rochester's `/node/{id}/agenda/{year}`) rather than
  something that has to be clicked through every time (like Dover's
  session-scoped Treeno temp-file links).
- Whether PDF links are static/guessable (can be `curl`'d directly once
  found) or session-scoped (must be obtained via the browser each time).
- What's actually in the documents - do agendas alone carry enough detail,
  or is there a richer "materials"/packet document worth downloading too.

Download a small number of representative PDFs (a regular meeting, and any
other meeting type the board uses) into `working/<town>/` to ground the
write-up, rather than bulk-downloading an entire archive during recon.

## Phase 2: analyzing a PDF

The tools in `plan_entry.py` are invoked as:

```
wwiocode/pyscript/plan_entry.py <ToolName> [key=value ...]
```

(this exact relative-from-project-root invocation is pre-approved in
`.claude/settings.local.json` - no permission prompt).

The PDF analysis tools' output goes to a single hardcoded location inside
`working/` (no output path to inject):

- Output: `working/OUTPUT.txt` for text/JSON-producing tools (each run
  overwrites it - copy it elsewhere first if you need to keep more than one
  result around).
- Output: `working/OUTPUT_PAGES/` for the page-render tool (one PNG per
  page).

The input PDF, by contrast, is a caller-supplied `pdf=working/<...>.pdf`
argument - not a fixed filename - but it's checked **before any work
happens** against two rules: it must start with `working/`, and it must
already exist as a file. That means you can point a tool straight at
whatever's already sitting in `working/<town>/` - no copy/symlink step
needed - while still keeping every tool confined to the gitignored scratch
area.

Tools:

| Tool | What it does |
|---|---|
| `FetchUrl` | Downloads `target=<url>` via Python `requests` with a normal desktop User-Agent - a `curl` replacement that needs no permission prompt. With no `dest=`, writes straight to `working/TARGET.pdf` (overwriting it) - pass `pdf=working/TARGET.pdf` to the tools below. With `dest=working/<dir>` (must already exist, under `working/`), saves there instead under the file's original name (from the response's `Content-Disposition` header, falling back to the URL's last path segment) - handy for building up a `working/<town>/` archive directly. |
| `ClaimDownload` | For sites that block `FetchUrl` (Cloudflare "Just a moment..." 403 on every non-browser request - kingston, madbury, brentwood): trigger a native download in the headed `planscan` session (`eval` a click on an `<a download>` for the file's href - see towninfo/PATTERNS.md), then `file=working/playwright_output/<f> dest=working/<town> [name=<new name>]` checks it's a real PDF/.docx and moves it into place for `IngestPdfTool`. |
| `PdfExtractText` | Full text extraction (OCR fallback per scanned page). `pdf=working/<path>.pdf` |
| `PdfInfo` | JSON: metadata, page count, file size, per-page text-length/scanned flag. `pdf=working/<path>.pdf` |
| `PdfKeywordScan` | JSON: page/snippet hits for development-project terms (site plan, subdivision, residential, commercial, variance, ...). `pdf=working/<path>.pdf`, override keywords with `keywords=a,b,c` |
| `PdfRenderPages` | Renders pages to PNG via PyMuPDF (no poppler needed) - useful for large scanned "materials packet" PDFs. `pdf=working/<path>.pdf`. Caps at 30 pages by default; pass `pages=1-6,10` to target specific pages or go further |
| `IngestPdfTool` | The single-call equivalent of `PdfInfo` + `PdfKeywordScan` + full text extraction, but writes straight into the SQLite DB (see `plan_db.py`) instead of `working/OUTPUT.txt` - the usual way to register a file found during a scan pass. Also accepts `.docx`. `pdf=working/<path>.pdf\|.docx` `[source_url=...]` `[date=YYYY-MM-DD]` `[scan_id=<id>]` - see "Logging a scan pass" above for `scan_id=` |

Example:

Each of these is its own separate, bare tool call - not chained:

```bash
wwiocode/pyscript/plan_entry.py FetchUrl target=https://example.town.gov/agendas/2026.09.22_PlanningBoard.Materials.pdf
wwiocode/pyscript/plan_entry.py PdfKeywordScan pdf=working/TARGET.pdf
# then Read working/OUTPUT.txt with the Read tool (not cat)
wwiocode/pyscript/plan_entry.py PdfRenderPages pdf=working/TARGET.pdf pages=1-3
# then Read working/OUTPUT_PAGES/page_001.png etc.

# or analyze an already-downloaded file directly, no copy step:
wwiocode/pyscript/plan_entry.py PdfInfo pdf=working/dover_nh/2026.09.22_PlanningBoard.Materials.pdf
```

For a large "materials"/packet-style PDF (scanned drawings, application
forms), prefer `PdfRenderPages` on a targeted page range and visually
inspecting the images over trying to bulk-extract text - these documents are
often partly or wholly scanned.
