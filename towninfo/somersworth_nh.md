# Somersworth, NH — Planning Board Web Access

Investigated: 2026-09-14

Somersworth is a small city (not a town) in Strafford County, on the
Maine border near Dover. Platform: node-based CivicPlus (see
PATTERNS.md), same family as Derry/Nottingham. No bot protection.

## Platform notes

- Main site: `https://www.somersworthnh.gov`. Planning Board hub:
  `/planning-board`. Agendas index: `/node/673/agenda`,
  `/node/673/agenda/2026` for current year.
- ⚠️ Agenda entries titled generically **"Public Notice & Agenda"** with
  URL slugs like `/planning-board/agenda/public-notice-agenda-107` — the
  slug number doesn't map to date, must scrape the year-listing page for
  actual dates.
- Static PDF path: `sites/g/files/vyhlif1226/f/agendas/{MM-DD-YYYY}_pb_
  agenda_.pdf`. Meetings: 3rd Wednesday monthly, 6pm.

## Document content

- **Agenda PDF** (Sept 16, 2026, 173KB): real content — `PdfKeywordScan`
  found 2 hits: a Conditional Use Permit public hearing for Patrick
  Babel, seeking a residential addition within the 150' setback to a
  Riparian and Wetland Buffer.

## Sample files downloaded

- `working/somersworth_nh/09-16-2026_pb_agenda_.pdf`
