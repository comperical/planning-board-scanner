# New Castle, NH — Planning Board Web Access

Investigated: 2026-09-14

New Castle is a very small seacoast town (an island community off
Portsmouth). Platform: node-based CivicPlus (see PATTERNS.md), same
family as Rochester, Exeter, Rye, etc. No bot protection encountered.

## Platform notes

- Main site: `https://www.newcastle.nh.gov` — note the dotted domain, not
  `newcastlenh.gov` (doesn't resolve). Planning Board hub:
  `/planning-board` (internal CivicPlus node id `214`).
- **Agendas index**: `/node/214/agenda` — e.g.
  `/planning-board/agenda/planning-board-agenda-48` (Aug 26, 2026), `-47`
  (Jul 22, 2026) — sequential numeric IDs, though one recent entry breaks
  the pattern with a date-slug instead
  (`planning-board-agenda-may-27-2026`) — don't assume the numbering is
  fully dense.
- **Minutes index**: `/node/214/minutes`, same pattern.
- Static PDF path: `sites/g/files/vyhlif956/f/{agendas|minutes}/
  {filename}.pdf` — filenames hand-typed by staff, no fixed pattern.
- Meetings monthly: 4th Wednesday, 7:00pm, "Macomber Room," 301
  Wentworth Road.
- Only approved minutes are posted; draft minutes are explicitly *not*
  published online — available only as hard copies from the Town Clerk.

## Document content

- **Agenda PDF** (Aug 26, 2026, 126KB): short and sparse — one page, in
  this sample a single item (a lot-line-adjustment hearing, 3 Oliver
  Street, Map 16). `PdfKeywordScan` found 1 hit. Consistent with New
  Castle's tiny size (pop. ~1,000) — expect low meeting volume and few
  items per agenda.
- **Minutes PDF** (Jul 22, 2026, 263KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/new_castle_nh/pb_agenda_8-26-26.pdf`
- `working/new_castle_nh/pb_approved_mins_7-22-26.pdf`
