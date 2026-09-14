# Strafford, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town (the county's namesake). Platform: custom
WordPress (see PATTERNS.md), not CivicPlus. No bot protection.

## Platform notes

- Main site: `https://strafford.nh.gov`. Planning Board hub:
  `/planning-board/`.
- **Agendas & Meeting Materials page**: `/cell-tower-info/planning-board-
  agendas/` — an odd URL slug (leftover from a page originally about cell
  towers, repurposed) but the actual content is a year-filterable list of
  agenda links, most recent at top.
- Static path: `/wp-content/uploads/{YYYY}/{MM}/PB{YYYYMMDD}Agenda.pdf` —
  reflects upload date/month, not necessarily meeting date (matched in
  this sample). Meetings: 1st Thursday monthly, 6:30pm, Strafford Town
  Hall.

## Document content

- **Agenda PDF** (Sept 10, 2026, 230KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Lot Line Adjustment Application under
  Continuing Business for MJ Properties NH, LLC (157 Old Ridge Road),
  plus a withdrawn Minor Subdivision (3 lots or fewer) application from
  the same applicant/address — both status-flagged (withdrawn vs.
  continuing) right in the text.

## Sample files downloaded

- `working/strafford_nh/PB20260910Agenda.pdf`
