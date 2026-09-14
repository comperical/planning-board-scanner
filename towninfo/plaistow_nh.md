# Plaistow, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, active planning board. Runs CivicPlus CivicEngage
with the Agenda Center module — same shape as other Rockingham towns this
session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.plaistow.com` — CivicPlus CivicEngage.
- Planning Board hub: `/1309/Planning-Board`; department page
  `/1253/Planning-Department`.
- Agenda Center: `/agendacenter` — a busy town-wide page (many boards); the
  `find` tool truncated on a plain "Planning Board" text search here too
  (same issue as Hampstead) — full `snapshot` + `grep` for the section
  header was needed to get the actual rows.
- Board alternates **regular "Planning Board Meeting"** and **"Planning
  Board Workshop Meeting"** sessions roughly biweekly.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — got a clean filename via
  Content-Disposition (`PB_Agenda_091626.pdf`).
- Meetings: 1st & 3rd Wednesday monthly.

## Document content

- **Agenda PDF** (Sept 16, 2026, 135KB): one of the richest single agendas
  found this session — `PdfKeywordScan` found 8 hits spanning **five
  separate named applications**: DSM MB II (amended site plan to renovate
  an existing shopping center); Albert Couillard (lot consolidation + lot
  line adjustment toward a 12-lot residential subdivision, Tax Map 66,
  *and* separately a conditional-use permit to fill ~1,400 sq ft of
  wetlands for a new road); a change-of-use application to multifamily
  residential (expansion of a nonconforming use); a conversion of 3 office
  units to residential at 26 Chandler Ave (Tax Map 25, Lot 30, MDR Zone);
  and a condominium-conversion application by Haider Khan (converting an
  existing duplex). Every case gives applicant name, address/tax map, and
  a plain-English project description directly in the agenda text.

## Sample files downloaded

- `working/plaistow_nh/PB_Agenda_091626.pdf`
