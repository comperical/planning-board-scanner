# Gilmanton, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, west of Alton. Platform: standard CivicPlus Agenda
Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.gilmantonnh.gov` (also without `www`). Planning
  Board hub: `/226/Planning-Board`.
- ⚠️ A legacy `gilmantonnh.org` domain also surfaces in search results
  with its own static PDF path for 2024/2025 agendas — not cross-checked
  for parity with the current `.gov` Agenda Center.
- Meetings often held at "Old Town Hall, 1800 NH Rte 140, Gilmanton Iron
  Works" (a village within the town). Roughly biweekly, 6:30pm.

## Access (updated 2026-10-25)

- Listing: `/AgendaCenter` (Planning Board section). Files at
  `/AgendaCenter/ViewFile/Agenda/_{MMDDYYYY}-{id}`. Use headed browser
  `<a download>` + `ClaimDownload` (name= to rename). Minutes are rare
  (only 1/8, 2/12, 3/12, 4/22, 5/19 posted as of 10/25).

## Document content

- **Agenda PDF** (Jul 9, 2026, 213KB): real content — `PdfKeywordScan`
  found 1 hit: Case #LLA2026-702, property owners Michael & Stephanie
  Fogg requesting a Lot Line Adjustment between their properties on Stone
  Rd (Map & Lot 415-068 and 4...).

## Sample files downloaded

- `working/gilmanton_nh/2026-0709 Agenda.pdf`
