# Dover, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: **Treeno** document-management system (see PATTERNS.md), not
CivicPlus. No bot protection.

## Platform notes

- Main city site: `https://www.dover.nh.gov` (standard modern CMS).
  Archive lives on a separate DMS: `https://publicrecords.dover.nh.gov`.
- Board page: `dover.nh.gov/government/boards-and-commissions/planning-
  board/` links to the Treeno portal pre-filtered to this board:
  `publicrecords.dover.nh.gov/public/1/deptnum/0/cab/Public_Meetings?
  index=public_body&autosearch=Planning%20Board`.
- The `Public_Meetings` cabinet is **one shared table for every meeting of
  every body** — filtering by "Planning Board" still includes its
  subcommittees (Planning Technical Review Committee, Open Lands
  Committee, Ad-Hoc Community Trail Advisory Subcommittee, TDR
  Sub-Committee, Executive Sessions). 2,590 rows total, 130 pages at
  20/page as of 2026-09-12.
- Clicking a meeting row → `/Tabs/Index/{meetingId}/...`, two tabs:
  **"Agenda and Meeting Notice"** and **"Agenda Materials"** (a bundled
  packet of everything submitted — applications, site plans, drawings —
  one PDF per meeting).

## ⚠️ Access method — session-scoped temp URLs

- PDF links are **not static/guessable**. Each file is served from a
  session-scoped temp URL generated the moment you click it:
  `publicrecords.dover.nh.gov/TempFiles/{token}_{original_filename}.pdf`.
  Once generated it works fine with plain `curl`, no cookies — but you
  must drive a browser through the row-click → tab-click → file-click
  sequence to *obtain* the link first. No shortcut to enumerate a year's
  worth of filings without visiting each meeting page.

## Document content

- **Agenda PDF** (~100–150KB): terse — one paragraph per case with
  owner/applicant name, Assessor's Map & Lot, zoning district, street
  address, brief proposal description, and Dover's own case-number scheme
  (`WAIV-YYYY-####`, `SUBM-YYYY-####`, `LOTA-YYYY-####`,
  `COND-YYYY-####`).
- **Agenda Materials PDF** (sample: **34.7 MB / 126 pages** for one
  meeting): the actual submitted packet — likely the single richest
  source of hard project detail (drawings, unit counts, specs) found in
  this project, but **not yet read** — this environment has no PDF
  page-rendering tool (poppler) installed. Needs either a text-extraction
  pass (may have embedded/searchable text) or a poppler-equipped
  environment.

## Sample downloads (in `working/dover_nh/`)

- `2026.09.22_PlanningBoard.Agenda.pdf` — site plan amendment (continued
  5x since May), zoning ordinance amendment hearing (TDR, ADUs, home
  occupations), a minor subdivision, a lot line adjustment, 2 conditional
  use permits
- `2026.09.22_PlanningBoard.Materials.pdf` — the corresponding 34.7MB/126-
  page materials packet, downloaded but not yet inspected

## Open questions / not yet checked

- Whether Treeno's per-meeting page also holds minutes (may appear as a
  third tab once the meeting occurs and minutes are approved).
- Whether the Agenda Materials PDF has extractable/searchable text.
- Exact earliest date covered by the 2,590-row archive.
- Whether other Dover boards use the same Treeno cabinet/pattern.
- Whether Treeno temp URLs expire, and how long they remain valid.
