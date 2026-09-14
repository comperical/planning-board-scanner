# Barnstead, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, west of Alton/Gilmanton. Runs CivicPlus CivicEngage
with the Agenda Center module — same shape as other towns this session —
plain PDFs, no bot protection.

## Platform

- Main site: `https://www.barnstead.org` — CivicPlus CivicEngage.
- ⚠️ Multiple stale/404 paths found: `/planning-board`, `/where`,
  `/boards/planning/index.htm` (a very old-style path, likely a leftover
  from a pre-CivicPlus site), and a search-indexed static PDF URL
  (`/sites/g/files/vyhlif6991/f/agendas/10.2.25_planning_board_agenda.pdf`)
  all 404. Live path is the standard `/agendacenter`, Planning Board
  section pre-expanded.
- News Flash items use `/CivicAlerts.aspx?AID=...` — an older CivicPlus
  URL style still active alongside the modern CivicEngage theme (same
  mixed-vintage pattern seen at Pelham/East Kingston).

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`Planning Board Meeting Agenda 07-02-2026.pdf`).

## Document content

- **Agenda PDF** (Jul 2, 2026, 119KB): real content — `PdfKeywordScan`
  found 2 hits: a continued Site Plan Review for Bruce & Jennifer
  Jakubauskas, Trustees of BJJ 2017 Trust; and a Minor Subdivision
  application at 1026 Suncook Valley Rd (Map 30, Lot 1).

## Sample files downloaded

- `working/barnstead_nh/Planning Board Meeting Agenda 07-02-2026.pdf`
