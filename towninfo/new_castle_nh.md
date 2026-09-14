# New Castle, NH — Planning Board Web Access

Investigated: 2026-09-14

New Castle is a very small seacoast town (an island community off Portsmouth)
and runs the standard **CivicPlus CivicEngage** platform, same family as
Rochester, Exeter, Rye, etc. No bot protection encountered — loads fine
headed (headless not separately tested, but nothing suggested a challenge).

## Platform

- Main site: `https://www.newcastle.nh.gov` — CivicPlus CivicEngage. Note the
  dotted domain (`newcastle.nh.gov`), not `newcastlenh.gov` (that hostname
  doesn't resolve — confirm the exact URL before scripting).
- Planning Board hub page: `/planning-board` (internal CivicPlus node id
  `214`, visible in the calendar/agenda/minutes "view all" links as
  `/node/214/...`).

## URL structure

- **Agendas index**: `https://www.newcastle.nh.gov/node/214/agenda` — one
  row per meeting, e.g. `/planning-board/agenda/planning-board-agenda-48`
  (Aug 26, 2026), `-47` (Jul 22, 2026), `-46` (Jun 24, 2026) — sequential
  numeric IDs, though one entry in the recent list breaks the pattern with a
  date-slug instead (`planning-board-agenda-may-27-2026`), so don't assume
  the numbering is fully guessable/dense.
- **Minutes index**: `https://www.newcastle.nh.gov/node/214/minutes` — same
  pattern, e.g. `/planning-board/minutes/planning-board-minutes-92`.
- Each agenda/minutes detail page embeds (or, for minutes, **redirects
  straight to**) a **static PDF** under CivicPlus's file store:
  `https://www.newcastle.nh.gov/sites/g/files/vyhlif956/f/{agendas|minutes}/{filename}.pdf`
  — filenames are hand-typed by town staff (`pb_agenda_8-26-26.pdf`,
  `pb_approved_mins_7-22-26.pdf`), not a fixed pattern, but the PDFs
  themselves are plain static files: confirmed `FetchUrl` (plain
  `requests`, no browser/session) downloads them directly, no referer or
  cookie needed.
- Meetings are monthly: 4th Wednesday, 7:00pm, in the "Macomber Room," 301
  Wentworth Road.

## Document content

- **Agenda PDF** (Aug 26, 2026, 126KB): short and sparse — one page, in this
  sample a single item (a lot-line-adjustment hearing, 3 Oliver Street, Map
  16). `PdfKeywordScan` found 1 hit ("lot line adjustment"). Consistent with
  New Castle's tiny size (pop. ~1,000) — expect low meeting volume and few
  items per agenda compared to Concord/Rochester/Dover.
- **Minutes PDF** (Jul 22, 2026, 263KB): downloaded but not yet
  content-analyzed in this session.
- Only approved minutes are posted; draft minutes are explicitly *not*
  published online per the Planning Board page text — available only as
  hard copies from the Town Clerk.

## Sample files downloaded

- `working/new_castle_nh/pb_agenda_8-26-26.pdf`
- `working/new_castle_nh/pb_approved_mins_7-22-26.pdf`
