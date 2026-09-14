# Strafford, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town (the county's namesake town). Runs a **custom
WordPress site**, not CivicPlus. No bot protection.

## Platform

- Main site: `https://strafford.nh.gov` — WordPress (`/wp-content/
  uploads/...` file paths).
- Planning Board hub: `/planning-board/`.
- **Agendas & Meeting Materials page**: `/cell-tower-info/planning-board-
  agendas/` — an odd URL slug (leftover from a page originally about cell
  towers, repurposed) but the actual content is a year-filterable list of
  Planning Board agenda links, most recent at top.

## URL structure

- Files are static WordPress media uploads:
  `https://strafford.nh.gov/wp-content/uploads/{YYYY}/{MM}/PB{YYYYMMDD}Agenda.pdf`
  (e.g. `/wp-content/uploads/2026/09/PB20260910Agenda.pdf`) — path
  reflects the *upload* date/month, not necessarily the meeting date,
  though they matched in this sample.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the PDF directly** — no referer/cookie gate, standard WordPress media
  serving.
- Meetings: 1st Thursday monthly, 6:30pm, Strafford Town Hall.

## Document content

- **Agenda PDF** (Sept 10, 2026, 230KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Lot Line Adjustment Application under
  Continuing Business for MJ Properties NH, LLC (157 Old Ridge Road), plus
  a withdrawn Minor Subdivision (3 lots or fewer) application from the
  same applicant/address — both status-flagged (withdrawn vs. continuing)
  right in the text, useful for filtering active vs. dead cases.

## Sample files downloaded

- `working/strafford_nh/PB20260910Agenda.pdf`
