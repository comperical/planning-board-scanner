# Deerfield, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, western border of the county. Runs CivicPlus
CivicEngage with the Agenda Center module — same shape as other Rockingham
towns — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.deerfieldnh.gov` — CivicPlus CivicEngage.
- ⚠️ Search also surfaced a legacy domain `townofdeerfieldnh.com` with its
  own node-based agenda/minutes URLs — not cross-checked for parity;
  `deerfieldnh.gov` confirmed live and current this session.
- Planning Board hub: `/284/Planning-Board`.
- Agenda Center: `/agendacenter` — Planning Board section loads
  **collapsed**, needs a click to expand (same as Newfields/Fremont).

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Meetings: 2nd & 4th Wednesday, 7pm, George B. White Building, 8 Raymond
  Road.

## Document content

- First sample (Sept 9, 2026, 74KB): 0 keyword hits — likely an
  administrative-only agenda.
- **Second sample (Aug 26, 2026, 77KB)**: real content —
  `PdfKeywordScan` found 2 hits: a continued Site Plan Application public
  hearing and a related Lot Line Adjustment hearing, both for Catherine
  and Anthony Brock, 95 Middle Road, Tax Map 419, Lots 76-1 and 76-2.
  Confirms agenda content varies meeting-to-meeting — sample more than one
  before concluding a town is sparse.

## Sample files downloaded

- `working/deerfield_nh/09092026_a7p.pdf` (0 hits)
- `working/deerfield_nh/08262026_a7p.pdf` (2 hits — the useful sample)
