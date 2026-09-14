# Sandown, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town. Runs CivicPlus CivicEngage with the Agenda Center
module — same shape as the other Rockingham towns this session — plain
PDFs, no bot protection. Has a direct per-board Agenda Center URL.

## Platform

- Main site: `https://www.sandown.us` — CivicPlus CivicEngage.
- Planning Board Agenda Center: `/AgendaCenter/Planning-Board-10/` (trailing
  slash present in the search-indexed URL; works either way).
- Like Raymond, Sandown files individual **"Site Walk Agenda"** documents
  tied to a specific property (e.g. "7.7.26 Planning Board Site Walk
  Agenda for 412 Main Street") separate from regular meeting agendas — a
  useful direct-address signal source.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_08182026-278`,
  `/AgendaCenter/ViewFile/Minutes/_07212026-269`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — agenda got a sane filename via
  Content-Disposition (`PB Agenda 8.18.26.pdf`); minutes fell back to the
  bare `_{date}-{id}` with no extension (recurring AgendaCenter quirk — it
  is a PDF).
- Meetings: 1st & 3rd Tuesday monthly, 6:30pm, Town Hall.

## Document content

- **Agenda PDF** (Aug 18, 2026, 121KB): the richest agenda sampled so far
  this session — `PdfKeywordScan` found 5 hits across three separate
  active cases, each with an applicant name, tax map/lot, and specifics:
  a Site Plan Review by **KRKR Trust** (Tax Map 2, Lot 33, Bobcat Way — a
  proposed non-residential commercial building, 37,856 sq ft); a
  Subdivision of Land by **NTV Builders, LLC** (Tax Map 2, called "Noah
  Estates," continued to 9/15/26); and a Conditional Use Permit
  application also by NTV Builders, LLC. Named developers, named
  subdivisions, and exact building square footage all present directly in
  the agenda text — no packet needed.
- **Minutes PDF** (Jul 21, 2026, 151KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/sandown_nh/PB Agenda 8.18.26.pdf`
- `working/sandown_nh/_07212026-269` (Jul 21, 2026 minutes — no extension
  in the saved filename; it is a PDF)
