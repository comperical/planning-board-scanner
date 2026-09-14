# Bedford, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town adjacent to Manchester. Platform: standard
CivicPlus Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- ⚠️ **Two domains coexist**: `bedfordnh.gov` and `bedfordnh.org` — both
  resolve to the same live site (confirmed identical `AgendaCenter/
  ViewFile` content on both). Treat as interchangeable, unlike Auburn's
  unresolved `.us`/`.gov` split.
- Planning Board hub: `/218/Planning-Board`. Direct per-board Agenda
  Center: `/AgendaCenter/Planning-Board-13/`.
- Meeting titles carry status flags: "WORKSHOP", "PUBLIC HEARING - LDCR
  Amendments", "CANCELLED DUE TO WEATHER".
- Meetings: near-weekly, Town Meeting Room at BCTV, 10 Meetinghouse Road.

## Document content

- **Agenda PDF** (Aug 17, 2026, 229KB): rich — `PdfKeywordScan` found 4
  hits across multiple named applicants: Potter Properties, LLC
  (applicant & owner) requesting a 15-lot residential subdivision at 410
  Wallace Road (Lot 9-33, Zoned R&A, continued); a Conditional Use Permit
  for electronic changeable-numeral signage (Enterprise, LLC owner /
  Heather Dudko applicant); and — most notably — **Trendezza LLC** (owner
  & applicant) requesting a condominium subdivision for a
  previously-approved **30-unit cottage court development**. Strong,
  well-specified signal.

## Sample files downloaded

- `working/bedford_nh/08 17 2026 PB agenda2 rev 8-13-26.pdf`
