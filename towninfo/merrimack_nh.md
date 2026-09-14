# Merrimack, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town along the Everett Turnpike, south of Manchester.
Runs CivicPlus CivicEngage with the Agenda Center module — same shape as
other towns this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.merrimacknh.gov`.
- ⚠️ Search-indexed URLs are **stale/404**: `/planning-board` (hub page),
  `/planning-board/agenda/...` (detail pages), and even `/node/2261/
  agenda/2026` all 404 — a full site restructure since those were last
  crawled, more thorough than the usual single-stale-link pattern seen
  elsewhere. The live path is the standard `/agendacenter`.
- Agenda Center Planning Board section: expanded by default, but the
  page also has an **"Appointment Committee for the Planning Board"**
  section with visually similar entry titles — filter carefully by exact
  board name, not substring match, when scraping.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`PB_Agenda_2026-09-01.pdf`).
- Meetings: 1st & 3rd Tuesday monthly, 6:30pm, Matthew Thornton Room,
  Town Hall West Wing.

## Document content

- **Agenda PDF** (Sept 1, 2026, 651KB): rich — `PdfKeywordScan` found 6
  hits across multiple cases: a site plan by applicant "...ant" and owner
  John J Flatley to construct **46,648 sq ft of commercial & restaurant
  space plus a 70-room hotel** (parcels at 645 and 673 DW Highway,
  I-1 Industrial / Aquifer Conservation / Elderly Housing Overlay
  Districts); a Conditional Use Permit for a Level II Home Occupation
  spray-tan business (Marianne M. Sullivan, 15 Derry Street, R-4
  Residential, Tax Map 5C Lot 276, Case # PB 2...); and a potential zoning
  amendment on electronic message-center sign display duration. Strong,
  large-scale commercial signal.

## Sample files downloaded

- `working/merrimack_nh/PB_Agenda_2026-09-01.pdf`
