# Dover, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Main city site: `https://www.dover.nh.gov` (standard modern CMS, not CivicPlus).
- Actual document archive lives on a **separate document management system**: `https://publicrecords.dover.nh.gov`, product name **Treeno** (page title "Treeno Cabinet" / "Treeno - Docs").
- No Cloudflare (or similar) bot-challenge encountered anywhere in this flow — loaded cleanly in both headed and (untested) headless mode.

## Finding the archive

- Board page: `dover.nh.gov/government/boards-and-commissions/planning-board/`
- That page links to the Treeno portal pre-filtered to this board:
  `https://publicrecords.dover.nh.gov/public/1/deptnum/0/cab/Public_Meetings?index=public_body&autosearch=Planning%20Board`
- There's also a general "Meeting Archives" / "Transparent Dover" entry point at `dover.nh.gov/government/open-government/municipal-documents/` — not yet explored, may cover other boards the same way.

## Treeno portal structure

- The `Public_Meetings` cabinet is **one shared table for every meeting of every body** — filtering by "Planning Board" still includes its subcommittees: Planning Technical Review Committee, Open Lands Committee, Ad-Hoc Community Trail Advisory Subcommittee, TDR Sub-Committee, and Executive Sessions.
- Grid columns: Date, Time, Subcommittee, Public Body, Mtg Location, Meeting Type, Additional Details. Sortable and filterable via column headers.
- **2,590 rows total, 130 pages at 20/page** as of 2026-09-12 — a large, apparently long-running archive (exact earliest date not yet checked).
- Clicking a meeting row navigates to a per-meeting doc page: `/Tabs/Index/{meetingId}/public/1/deptnum/0/cab/Public_Meetings`, with two tabs:
  - **"Agenda and Meeting Notice"** — the agenda PDF itself.
  - **"Agenda Materials"** — a bundled packet of everything submitted for that meeting (applications, site plans, drawings, etc.), one PDF per meeting.

## Access method — IMPORTANT

- PDF links are **not static/guessable**. Each file is served from a **session-scoped temp URL** generated the moment you click it in the browser: `https://publicrecords.dover.nh.gov/TempFiles/{token}_{original_filename}.pdf`.
- Once generated, the temp URL works fine with plain `curl` and no cookies — but you must drive a browser (Playwright) through the row-click → tab-click → file-click sequence to *obtain* each link. No shortcut to enumerate a year's worth of filings without visiting each meeting page.
- **Working pattern**: headed (or plain) Playwright session to click through the grid and collect temp URLs, then `curl` each one to download. This is more browser-interaction-heavy per document than Rochester's approach, since Rochester's agenda PDF paths are stable and guessable from the listing HTML alone.

## Document content

- **Agenda PDF** (small, ~100–150KB): same terse style as Rochester — one paragraph per case with owner/applicant name, Assessor's Map & Lot, zoning district, street address, brief proposal description, and Dover's case-number scheme:
  - `WAIV-YYYY-####` (waiver / site plan amendment)
  - `SUBM-YYYY-####` (minor subdivision)
  - `LOTA-YYYY-####` (lot line adjustment)
  - `COND-YYYY-####` (conditional use permit)
- **Agenda Materials PDF** (large — sample was **34.7 MB / 126 pages** for a single meeting): the actual submitted packet — presumably full site plans, engineering drawings, applications, and abutter materials bundled together. **Not yet read** — this environment has no PDF page-rendering tool (`pdftoppm`/poppler) installed, and per instruction no new packages were installed to add one. This is likely the single richest source of hard project detail (drawings, unit counts, specs) found in this project so far, but needs either (a) a text-extraction pass (may have embedded/searchable text worth grepping even without rendering), or (b) a poppler-equipped environment to inspect visually.

## Sample downloads (in `working/dover_nh/`)

- `2026.09.22_PlanningBoard.Agenda.pdf` — regular meeting agenda; site plan amendment (continued 5x since May), zoning ordinance amendment hearing (TDR, ADUs, home occupations), a minor subdivision, a lot line adjustment, 2 conditional use permits
- `2026.09.22_PlanningBoard.Materials.pdf` — the corresponding materials packet (34.7MB, 126 pages) — downloaded but not yet inspected

## Comparison to Rochester, NH

| | Rochester, NH | Dover, NH |
|---|---|---|
| CMS | CivicPlus (Drupal) | Custom site + Treeno DMS |
| Bot protection | Cloudflare hard-blocks headless | None encountered |
| PDF URLs | Stable, static, guessable from listing HTML | Session-scoped temp URLs, must click through |
| Supporting materials | Not bundled — separate case files "available for inspection" at the Planning Office | Bundled into one "Agenda Materials" PDF per meeting, downloadable |
| Subcommittees mixed in archive | No (separate node ids, not explored) | Yes, same Public_Meetings cabinet |

## Open questions / not yet checked

- Minutes: only agendas + materials explored so far; need to check whether Treeno's per-meeting page also holds minutes (may appear as a third tab, or under a different meeting-type entry, after the meeting occurs and minutes are approved).
- Whether the Agenda Materials PDF has extractable/searchable text (would allow grep-based scanning without visual rendering).
- Exact earliest date covered by the 2,590-row archive.
- Whether other Dover boards (Zoning Board of Adjustment, Conservation Commission) use the same Treeno cabinet/pattern.
- Whether Treeno temp URLs expire, and how long they remain valid after generation (relevant if collecting a batch of links to download later rather than immediately).
