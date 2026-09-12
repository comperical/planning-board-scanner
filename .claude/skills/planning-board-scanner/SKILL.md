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

`.claude/settings.local.json` pre-approves exactly the commands this workflow
needs: `playwright-cli -s=planscan ...`, `wwiocode/pyscript/plan_entry.py ...`
(run from the project root), `WebSearch`, and Read/Edit/Write anywhere under
`working/`. Stick to those forms - e.g. don't `cd` into a subdirectory before
invoking `plan_entry.py`, and don't open an unnamed/default Playwright
session - so the task can run without stopping for a new permission prompt.
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
| `PdfExtractText` | Full text extraction (OCR fallback per scanned page). `pdf=working/<path>.pdf` |
| `PdfInfo` | JSON: metadata, page count, file size, per-page text-length/scanned flag. `pdf=working/<path>.pdf` |
| `PdfKeywordScan` | JSON: page/snippet hits for development-project terms (site plan, subdivision, residential, commercial, variance, ...). `pdf=working/<path>.pdf`, override keywords with `keywords=a,b,c` |
| `PdfRenderPages` | Renders pages to PNG via PyMuPDF (no poppler needed) - useful for large scanned "materials packet" PDFs. `pdf=working/<path>.pdf`. Caps at 30 pages by default; pass `pages=1-6,10` to target specific pages or go further |

Example:

```bash
wwiocode/pyscript/plan_entry.py FetchUrl target=https://example.town.gov/agendas/2026.09.22_PlanningBoard.Materials.pdf
wwiocode/pyscript/plan_entry.py PdfKeywordScan pdf=working/TARGET.pdf
cat working/OUTPUT.txt
wwiocode/pyscript/plan_entry.py PdfRenderPages pdf=working/TARGET.pdf pages=1-3
# then Read working/OUTPUT_PAGES/page_001.png etc.

# or analyze an already-downloaded file directly, no copy step:
wwiocode/pyscript/plan_entry.py PdfInfo pdf=working/dover_nh/2026.09.22_PlanningBoard.Materials.pdf
```

For a large "materials"/packet-style PDF (scanned drawings, application
forms), prefer `PdfRenderPages` on a targeted page range and visually
inspecting the images over trying to bulk-extract text - these documents are
often partly or wholly scanned.
