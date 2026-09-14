# Farmington, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town. Runs CivicPlus CivicEngage with the Agenda Center
module — same shape as other towns this session — plain PDFs, no bot
protection. Planning Board section loads already expanded.

## Platform

- Main site: `https://www.farmington.nh.us` — CivicPlus CivicEngage.
- Planning Board hub: `/1363/Planning-Board`.
- Agenda Center: `/agendacenter`.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — clean filename via Content-Disposition
  (`PB Agenda 081926.pdf`).
- Meetings: 1st & 3rd Wednesday monthly, 6:30pm, Selectmen's Chambers,
  Municipal Offices, 356 Main Street.

## Document content

- **Agenda PDF** (Aug 19, 2026, 197KB): very rich — `PdfKeywordScan`
  found 5 hits across multiple active cases: a post-approval-waiver
  request from Subdivision Regulations §6.B(1)(f)(i) to split an existing
  6.38-acre parcel into two lots (project off Grandview..., site plan
  conditionally approved May 6, 2026); a project at 892 Meaderboro Road in
  the Agricultural Residential Zoning District; and — most notably — a
  Subdivision Application for **"Field of Dreams at Post Road, LLC"**
  (Tax Map R16, Lot 6, corner of Chestnut Hill Road and Dodge Cross Road,
  Rural Residential District). Strong signal: named applicant entities,
  tax map/lot, precise regulatory citations.

## Sample files downloaded

- `working/farmington_nh/PB Agenda 081926.pdf`
