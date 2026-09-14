# Bedford, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town adjacent to Manchester. Runs CivicPlus CivicEngage
with the Agenda Center module — same shape as other towns this session —
plain PDFs, no bot protection.

## Platform

- ⚠️ **Two domains coexist**: `bedfordnh.gov` and `bedfordnh.org` — both
  resolve to the same live CivicPlus site (confirmed `AgendaCenter/
  ViewFile` URLs work on `.gov`; `.org` links from search results point at
  the identical content, e.g. minutes at
  `bedfordnh.org/AgendaCenter/ViewFile/Minutes/...`). Treat as
  interchangeable, unlike Auburn's unresolved `.us`/`.gov` split.
- Planning Board hub: `/218/Planning-Board`.
- Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-13/`.
- Meeting titles carry status flags: "WORKSHOP", "PUBLIC HEARING - LDCR
  Amendments", "CANCELLED DUE TO WEATHER" — same pattern as Chester.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`08 17 2026 PB agenda2 rev 8-13-26.pdf`).
- Meetings: near-weekly, Town Meeting Room at BCTV, 10 Meetinghouse Road.

## Document content

- **Agenda PDF** (Aug 17, 2026, 229KB): rich — `PdfKeywordScan` found 4
  hits across multiple named applicants: Potter Properties, LLC
  (applicant & owner) requesting a 15-lot residential subdivision at 410
  Wallace Road (Lot 9-33, Zoned R&A, a continued application); a
  Conditional Use Permit for electronic changeable-numeral signage
  (Enterprise, LLC owner / Heather Dudko applicant); and — most
  notably — **Trendezza LLC** (owner & applicant) requesting a
  condominium subdivision for a previously-approved **30-unit cottage
  court development**. Strong, well-specified signal.

## Sample files downloaded

- `working/bedford_nh/08 17 2026 PB agenda2 rev 8-13-26.pdf`
