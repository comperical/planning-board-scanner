# Derry, NH — Planning Board Web Access

Investigated: 2026-09-14

Derry is one of the larger municipalities in this project (a "Town of
Derry" with a Town Council, not a Select Board — like Concord in scale).
Runs standard **node-based CivicPlus CivicEngage** (not the Agenda Center
module) — same family as New Castle/Rye/Exeter. No bot protection.

## Platform

- Main site: `https://www.derrynh.gov` — CivicPlus CivicEngage.
- Planning Board hub: `/planning-board` (works directly, unlike some other
  towns' stale node links this session).
- **Agendas index**: `https://www.derrynh.gov/node/206/agenda` — lists
  years (2016-2026) as links (`/node/206/agenda/{year}`); click into a
  year to see individual meeting entries (not shown all on one page).
- Each entry links to a detail page:
  `/planning-board/agenda/planning-board-agenda-{MMDDYYYY}[-N]` (the `-N`
  suffix disambiguates same-date collisions, e.g.
  `planning-board-agenda-09022026-0`).

## URL structure

- Each detail page embeds a **static PDF** under CivicPlus's file store:
  `https://www.derrynh.gov/sites/g/files/vyhlif3026/f/agendas/{filename}.pdf`
  (e.g. `9.2.26_pb_agenda__0.pdf`) — same pattern as New Castle.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** — no referer/cookie gate.
- Meetings: 1st & 3rd Wednesday, 7pm, Derry Municipal Center.
- Sidebar links worth noting for a future pass: "OnCall Professional
  Services FY27-28", "Planning Board Fees per RSA 673", and — most
  relevant — a "Gateway Zoning Committee" sub-page and a "West Running
  Brook Corridor Traffic Study" (signals an active corridor-development
  planning effort in town).

## Document content

- **Agenda PDF** (Sept 2, 2026, 111KB): real project detail — `PdfKeywordScan`
  found a Site Plan Amendment for Bird Enterprises, LLC (PID 10012, 187
  Hampstead Road — addition of a nursery stock area), plus a second item
  beginning for "Cafua Realty Trust CLXXIII, LLC" (a well-known regional
  convenience-store/gas-station developer) that ran past the keyword-scan
  snippet cutoff — worth a full-text read in a future pass, this agenda
  likely has more items than the single hit shown.

## Sample files downloaded

- `working/derry_nh/9.2.26_pb_agenda__0.pdf`
