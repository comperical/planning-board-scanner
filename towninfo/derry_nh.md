# Derry, NH — Planning Board Web Access

Investigated: 2026-09-14

Derry is one of the larger municipalities in this project (a "Town of
Derry" with a Town Council, not a Select Board — like Concord in scale).
Platform: node-based CivicPlus (see PATTERNS.md), same family as New
Castle/Rye/Exeter. No bot protection.

## Platform notes

- Main site: `https://www.derrynh.gov`.
- **Migrated to CivicEngage Agenda Center (found 2026-10-03)**: the old
  `/planning-board` hub and `/node/206/agenda/{year}` listings now 404.
  Use `/AgendaCenter` (section "Planning Board") - standard listing scrape
  from PATTERNS.md works. Files at
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`; plain
  `FetchUrl` works (no Cloudflare as of 2026-10-03). Minutes are posted on
  the same row as their agenda.
- Meetings: 1st & 3rd Wednesday, 7pm, Derry Municipal Center.
- Sidebar links worth a future pass: "Planning Board Fees per RSA 673",
  and — most relevant — a "Gateway Zoning Committee" sub-page and a "West
  Running Brook Corridor Traffic Study" (signals an active
  corridor-development planning effort in town).

## Document content

- **Agenda PDF** (Sept 2, 2026, 111KB): real project detail —
  `PdfKeywordScan` found a Site Plan Amendment for Bird Enterprises, LLC
  (PID 10012, 187 Hampstead Road — addition of a nursery stock area),
  plus a second item beginning for "Cafua Realty Trust CLXXIII, LLC" (a
  well-known regional convenience-store/gas-station developer) that ran
  past the keyword-scan snippet cutoff — worth a full-text read in a
  future pass.

## Sample files downloaded

- `working/derry_nh/9.2.26_pb_agenda__0.pdf`
