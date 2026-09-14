# Goffstown, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town adjacent to Manchester. Runs CivicPlus CivicEngage
with the Agenda Center module — same shape as other towns this session —
plain PDFs, no bot protection. Planning Board section loads collapsed,
needs a click to expand.

## Platform

- Main site: `https://goffstownnh.gov` (also `www.goffstownnh.gov`).
- Agenda Center: `/AgendaCenter`.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Meetings: roughly biweekly, Mildred Stark Meeting Room, 16 Main Street.

## Document content

- **Agenda PDF** (Sept 10, 2026, 24KB): real content despite small size —
  `PdfKeywordScan` found 4 hits: a Site Plan Waiver Request review hearing
  for a proposed dog daycare business (with long-term/overnight boarding
  as a commercial kennel), 553 Mast Road (Goffstown Plaza), Map 18 Lot
  58B; and a Completeness Review/Subdivision Review for a two-lot
  subdivision creating one additional residential lot, 165 St. Anselm
  Drive (Map 14, Lot 5), owned by Falcon Heights....

## Sample files downloaded

- `working/goffstown_nh/09-10-26 Planning Board Agenda (1).pdf`
