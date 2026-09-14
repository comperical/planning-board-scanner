# Milton, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town, Maine border, north of Farmington. Platform:
node-based CivicPlus (see PATTERNS.md). No bot protection.

## Platform notes

- Main site: `https://www.miltonnh-us.com`. Planning Board hub:
  `/planning-board`. Agendas index: `/node/107/agenda`,
  `/node/107/agenda/2026` for current year.
- ⚠️ Search results also surfaced `miltonma.gov` (Milton,
  *Massachusetts*) and `miltonny.gov` — don't confuse domains;
  `miltonnh-us.com` is the correct NH town.
- Entry slugs mostly follow `/planning-board/agenda/planning-board-
  meeting-agenda-{n}` (sequential counter), with an occasional
  differently-named entry (`notice-public-hearings`) interleaved.
- Static PDF path: `sites/g/files/vyhlif916/f/agendas/milton_pb_agenda_
  {MM-DD-YY}.pdf`. Meetings: 1st & 3rd Tuesday monthly, 6pm.

## Document content

- **Agenda PDF** (Sept 15, 2026, 156KB): light — `PdfKeywordScan` found 3
  hits, but all administrative/procedural (a discussion item on the list
  of zoning/subdivision/site-plan regulations requiring public-hearing
  scheduling, plus the town's own address "55 Industrial Way" matching
  the "industrial" keyword) rather than an active development case. No
  named applicant in this sample — worth trying another meeting date.

## Sample files downloaded

- `working/milton_nh/milton_pb_agenda_09-15-26.pdf`
