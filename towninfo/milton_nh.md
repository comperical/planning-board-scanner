# Milton, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town, Maine border, north of Farmington. Runs node-based
CivicPlus CivicEngage. No bot protection.

## Platform

- Main site: `https://www.miltonnh-us.com` — CivicPlus CivicEngage.
- Planning Board hub: `/planning-board`.
- **Agendas index**: `https://www.miltonnh-us.com/node/107/agenda` —
  lists years; `/node/107/agenda/2026` for current-year entries.
- ⚠️ Note: search results also surfaced `miltonma.gov` (Milton,
  *Massachusetts* — a same-named but unrelated town) and `miltonny.gov` —
  don't confuse domains when searching; `miltonnh-us.com` is the correct
  NH town.
- Entry slugs mostly follow `/planning-board/agenda/planning-board-
  meeting-agenda-{n}` (sequential per-board counter), with an occasional
  differently-named entry (`notice-public-hearings`) interleaved.

## URL structure

- Each detail page embeds a static PDF:
  `https://www.miltonnh-us.com/sites/g/files/vyhlif916/f/agendas/milton_pb_agenda_{MM-DD-YY}.pdf`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the PDF directly** — no referer/cookie gate.
- Meetings: 1st & 3rd Tuesday monthly, 6pm.

## Document content

- **Agenda PDF** (Sept 15, 2026, 156KB): light — `PdfKeywordScan` found 3
  hits, but all administrative/procedural (a discussion item on the list
  of zoning/subdivision/site-plan regulations requiring public-hearing
  scheduling, plus the town's own address "55 Industrial Way" matching
  the "industrial" keyword) rather than an active development case. No
  named applicant in this particular sample — worth trying another
  meeting date before concluding Milton is generally low-signal.

## Sample files downloaded

- `working/milton_nh/milton_pb_agenda_09-15-26.pdf`
