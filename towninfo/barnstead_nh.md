# Barnstead, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, west of Alton/Gilmanton. Platform: standard CivicPlus
Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.barnstead.org`.
- ⚠️ Multiple stale/404 paths: `/planning-board`, `/where`,
  `/boards/planning/index.htm`, and a search-indexed static PDF URL —
  all 404. Live path is `/agendacenter`, section pre-expanded.
- News Flash items use the older `/CivicAlerts.aspx?AID=...` URL style
  still active alongside the modern theme (same mixed-vintage pattern as
  Pelham/East Kingston).

## Document content

- **Agenda PDF** (Jul 2, 2026, 119KB): real content — `PdfKeywordScan`
  found 2 hits: a continued Site Plan Review for Bruce & Jennifer
  Jakubauskas, Trustees of BJJ 2017 Trust; and a Minor Subdivision
  application at 1026 Suncook Valley Rd (Map 30, Lot 1).

## Sample files downloaded

- `working/barnstead_nh/Planning Board Meeting Agenda 07-02-2026.pdf`
