# Merrimack, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town along the Everett Turnpike, south of Manchester.
Platform: standard CivicPlus Agenda Center (see PATTERNS.md) — no bot
protection.

## Platform notes

- Main site: `https://www.merrimacknh.gov`.
- ⚠️ Search-indexed URLs are stale/404: `/planning-board`,
  `/planning-board/agenda/...`, even `/node/2261/agenda/2026` — a full
  site restructure since those were crawled, more thorough than the
  usual single-stale-link pattern elsewhere. Live path is `/agendacenter`.
- Section also has an **"Appointment Committee for the Planning Board"**
  section with visually similar entry titles — filter carefully by exact
  board name, not substring match.
- Meetings: 1st & 3rd Tuesday monthly, 6:30pm, Matthew Thornton Room,
  Town Hall West Wing.

## Document content

- **Agenda PDF** (Sept 1, 2026, 651KB): rich — `PdfKeywordScan` found 6
  hits across multiple cases: a site plan by owner John J Flatley to
  construct **46,648 sq ft of commercial & restaurant space plus a
  70-room hotel** (parcels at 645 and 673 DW Highway, I-1 Industrial /
  Aquifer Conservation / Elderly Housing Overlay Districts); a
  Conditional Use Permit for a Level II Home Occupation spray-tan
  business (Marianne M. Sullivan, 15 Derry Street, R-4 Residential, Tax
  Map 5C Lot 276); and a potential zoning amendment on electronic
  message-center sign display duration. Strong, large-scale commercial
  signal.

## Sample files downloaded

- `working/merrimack_nh/PB_Agenda_2026-09-01.pdf`
