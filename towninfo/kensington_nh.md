# Kensington, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Runs CivicPlus CivicEngage with the Agenda
Center module (same shape as Hampton Falls/Greenland/Newfields/East
Kingston) — plain PDFs, no bot protection. Has a **direct per-board Agenda
Center URL** like Hampton Falls/Greenland (no click-to-expand needed).

## Platform

- Main site: `https://www.kensingtonnh.gov` — CivicPlus CivicEngage.
- Planning Board Agenda Center: `/AgendaCenter/Planning-Board-3` — page
  title renders as "MEETING FILES" (a CivicPlus-side label override, not a
  different platform) but the URL/table structure is identical to the
  other AgendaCenter towns.
- Kensington's agenda **titles themselves are unusually descriptive** —
  town staff append a short project summary to the meeting title, e.g.
  "Planning Board Library / Subdivision Plan reviews. Part 1- Library Part
  2 - 2 subdivision applications" (Aug 19, 2026) and "Planning Board Mtg -
  8 Highland Rd Subdivision" (Jun 17, 2026) — meaning useful signal is
  sometimes visible straight from the agenda *listing* page, before even
  opening a PDF.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_08192026-288`,
  `/AgendaCenter/ViewFile/Minutes/_06172026-262`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — agenda got a sane filename via
  Content-Disposition (`PB Agenda 08.19.26.pdf`); minutes fell back to the
  bare `_{date}-{id}` with no extension (same recurring AgendaCenter quirk
  — it is a PDF).
- Meetings are frequent for a small town: near-biweekly "Monthly Mtg" /
  "Workshop" alternation (1st Wed = workshop, 3rd Wed = regular meeting,
  roughly), 6:30-7pm.

## Document content

- **Agenda PDF** (Aug 19, 2026, 98KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Minor Subdivision Application (Final
  Plat, owner Alnoba Lewis Family Foundation, 8 Hudson Drive) and an
  informational item on the Kensington Social Library Site Plan.
- **Minutes PDF** (Jun 17, 2026, 141KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/kensington_nh/PB Agenda 08.19.26.pdf`
- `working/kensington_nh/_06172026-262` (Jun 17, 2026 minutes — no
  extension in the saved filename; it is a PDF)
