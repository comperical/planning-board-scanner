# Pembroke, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, east of Concord. Runs CivicPlus CivicEngage with
the Agenda Center module — same shape as other towns this session — plain
PDFs, no bot protection. Planning Board section loads already expanded.

## Platform

- Main site: `https://www.pembroke-nh.com`.
- Agenda Center: `/AgendaCenter`.
- Also has a "Recorded Meetings" nav item (site-wide video archive) —
  a possible secondary source not explored this session.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`Public Hearing Notice 09-22-26.pdf`).

## Document content

- **Public Hearing Notice PDF** (Sept 22, 2026, 155KB): real content —
  `PdfKeywordScan` found 2 hits: Major Site Plan Application #26-104,
  applicant Peter Madsen (Keach-Nordstrom Associates, Inc. acting as
  agent), owner of Tax Map 266, Lot 76-1, 216 Buck St., in the Medium
  Density Residential (R1) Zone, MS4 Overlay, and Aquifer Conservation
  District.

## Sample files downloaded

- `working/pembroke_nh/Public Hearing Notice 09-22-26.pdf`
