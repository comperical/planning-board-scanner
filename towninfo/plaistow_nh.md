# Plaistow, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, active planning board. Platform: standard
CivicPlus Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.plaistow.com`. Planning Board hub:
  `/1309/Planning-Board`; department page `/1253/Planning-Department`.
- Agenda Center is a busy town-wide page — the `find` tool truncated on a
  plain "Planning Board" text search (same issue as Hampstead); full
  `snapshot` + `grep` was needed.
- Board alternates regular "Planning Board Meeting" and "Planning Board
  Workshop Meeting" sessions roughly biweekly.

## Document content

- **Agenda PDF** (Sept 16, 2026, 135KB): one of the richest single
  agendas found this session — `PdfKeywordScan` found 8 hits spanning
  **five separate named applications**: DSM MB II (amended site plan to
  renovate an existing shopping center); Albert Couillard (lot
  consolidation + lot line adjustment toward a 12-lot residential
  subdivision, Tax Map 66, *and* separately a conditional-use permit to
  fill ~1,400 sq ft of wetlands for a new road); a change-of-use
  application to multifamily residential (expansion of a nonconforming
  use); a conversion of 3 office units to residential at 26 Chandler Ave
  (Tax Map 25, Lot 30, MDR Zone); and a condominium-conversion
  application by Haider Khan (converting an existing duplex). Every case
  gives applicant name, address/tax map, and a plain-English description
  directly in the agenda text.

## Sample files downloaded

- `working/plaistow_nh/PB_Agenda_091626.pdf`
