# Stratham, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: **Revize CMS** (see PATTERNS.md), PHP-based. No bot protection.

## Platform notes

- Site: `https://www.strathamnh.gov`.
- Board hub: `/boards/planning_board/index.php`, with a "Related Pages"
  sidebar: Agendas & Minutes, ⭐ Public Hearing Notices (see below),
  Technical Review Committee / Route 108 Corridor Study Committee / Age
  Friendly Communities Project (sub-bodies, same pattern as Exeter's
  TRC), Meeting Schedule PDF.
- Agendas & Minutes page is a year-accordion (2026: 23 docs, 2025: 26,
  2024: 23, 2023: 22 — ~biweekly cadence). Blank cells when a type isn't
  posted yet. Has a "Search for file name" box.
- Static path: `.../Documents/Boards and Committees/Planning Board/
  Agendas and Minutes/{year}/{Agenda|Minutes}/{YYYY.MM.DD} {PB Agenda|
  approved minutes}.pdf` — paths contain literal spaces, URL-encode as
  `%20` when fetching scripted. Filenames not perfectly uniform, safest
  to read the exact href off the listing.

## ⭐ Key find: "Public Hearing Notices" page — Hampton-style leads page

- `/boards/planning_board/public_hearing_notices.php` — a **standalone,
  continuously-updated leads page** (see PATTERNS.md), each entry giving
  applicant/owner name, exact street address, **Tax Map and Lot number**,
  zoning district, hearing date, plain-English description, and direct
  links to full plan sets, architectural renderings, drainage analyses,
  NRCS soils reports, NHDOT driveway permits, etc.
- Sample cases (live as of Sept 2026): **Packer Brook Holdings LLC /
  "Mighty Roots"**, 170 Portsmouth Avenue (Tax Map 17, Lot 86) — final
  site plan approval for a ±6,110 sq ft light-manufacturing office/shop
  behind an existing single-family home, Route 33 Legacy Highway Heritage
  District; **Red Barn Property LLC**, 210 Portsmouth Avenue (Tax Map 21,
  Lot 81) — major subdivision + CUPs for a shared driveway, well, barn,
  and multi-duplex residential development (4 duplex buildings) in
  wetland setback/buffer areas, continued across at least three meetings.
- Unlike Hampton's page, Stratham's regular agenda PDFs are *not* terse —
  they carry essentially the same case-level narrative and document links
  as this page, so the two sources are largely redundant here; still
  worth checking as the single place to see everything currently
  pending.

## Document content

- **Agenda PDF** ("Legal Notice"-style): 1 page, dense case detail on par
  with Exeter's — applicant/owner name, full street address, Tax
  Map/Lot, zoning district, real project description, inline links to
  plan set/renderings/drainage/permit documents.
- **Minutes PDF**: 5 pages, standard motion-and-discussion narrative.
- **Public Hearing Notices plan-set PDF** (sample: 22 pages, **39 MB**):
  CAD-exported engineering drawing set (large-format pages). Mixed
  extractability — most pages a few hundred chars of title-block text, 4
  of 22 pages have **zero extractable text** (fully rasterized drawings)
  — worth `PdfRenderPages` on targeted sheets rather than bulk text
  extraction.
- No separate bundled "meeting packet" PDF — supporting materials are
  linked individually from the agenda/hearing-notice text itself.

## Sample downloads (in `working/stratham_nh/`)

- `2026.09.16 PB Agenda.pdf` — Red Barn Property LLC subdivision/CUP case
- `2026.08.19 approved minutes.pdf` — 5 pages
- `5613 - Mighty Roots World Headquaters Plan Set - 8.6.26.pdf` — 22-page
  CAD plan set

## Open questions / not yet checked

- Whether other Stratham boards have an equivalent Public Hearing
  Notices page — the URL pattern suggests a site-wide Revize template
  feature.
- Exact minutes filename convention for draft (not yet approved) minutes.
- How far back the accordion goes before 2023.
- Whether the Public Hearing Notices page is manually pruned after each
  hearing resolves.
