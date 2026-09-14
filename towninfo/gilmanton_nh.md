# Gilmanton, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, west of Alton. Runs CivicPlus CivicEngage with the
Agenda Center module — same shape as other towns this session — plain
PDFs, no bot protection.

## Platform

- Main site: `https://www.gilmantonnh.gov` (also `gilmantonnh.gov`
  without `www`).
- Planning Board hub: `/226/Planning-Board`.
- ⚠️ A legacy `gilmantonnh.org` domain also surfaces in search results
  with its own `/sites/g/files/vyhlif4451/f/agendas/...` static PDF path
  for 2024/2025 agendas — not cross-checked for parity with the current
  `.gov` Agenda Center this session.
- Meetings often held at "Old Town Hall, 1800 NH Rte 140, Gilmanton Iron
  Works" (a village within the town).

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`2026-0709 Agenda.pdf`).
- Meetings: roughly biweekly, 6:30pm.

## Document content

- **Agenda PDF** (Jul 9, 2026, 213KB): real content — `PdfKeywordScan`
  found 1 hit: Case #LLA2026-702, property owners Michael & Stephanie
  Fogg requesting a Lot Line Adjustment between their properties on Stone
  Rd (Map & Lot 415-068 and 4...).

## Sample files downloaded

- `working/gilmanton_nh/2026-0709 Agenda.pdf`
