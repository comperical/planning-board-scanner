# Northwood, NH — Planning Board Web Access

Investigated: 2026-09-14

Northwood is the first town in this project on **Legend Software** (see
PATTERNS.md). No bot protection encountered.

## Platform notes

- Main site: `https://www.northwoodnh.org` (footer credit "Website by
  Legend Software"). Planning Board department page:
  `/entity/Planning-Board-10`.
- Agendas & Minutes listing (town-wide, filterable by board):
  `/agendas/Planning-Board-10` — paginated table, each row links to a
  per-meeting detail page `/agenda/{Board-Name}-{id}` (id is a flat
  sequential counter shared across **all** boards, not per-board — ids
  aren't densely enumerable for Planning Board alone). Some ids carry
  descriptive suffixes for special session types (e.g.
  `Planning-Board-Site-Walk-2510`).
- ⚠️ **The listing page's default sort surfaces upcoming/future meetings
  first**, several of which had no agenda posted yet. A lower id (2140)
  pointed to a past meeting (Jan 22, 2026) that did have both Agenda and
  Minutes — check meeting date against "today" and prefer past meetings
  for actual content.
- Agenda PDF: `/file/{fileId}/{MMDDYYYY}.pdf` (a separate numeric id from
  the meeting entry id). Minutes: `/assets/municipal/10/minutes/
  {MMDDYYYY}_Minutes_Official_.pdf` (the `10` matches the entity id).
  Openly `FetchUrl`-able, no referer/cookie gate.
- Meetings (2026): regular meeting ~4th Wednesday + a Work Session ~2nd
  Wednesday, plus per-case Site Walks (with their own minutes). The
  listing also carries Steering Committee / CIP Subcommittee rows - skip.
- Quick enumeration (2026-09-24): in the browser, `fetch('/agenda/{slug}')`
  each meeting's detail page and read `/file/...` + `assets/.../minutes/...`
  hrefs. Minutes are posted fast (draft within ~2 weeks). A meeting can
  list the agenda twice under different file ids (revision) - take the
  higher id. Public notices for big cases are posted as extra files
  (e.g. `Mixed_Use_notice...pdf`, `CUP_Public_Notice.pdf`).
- `FetchUrl` saves agenda files with a **leading space** in the filename
  (` 09232026.pdf`) - quote the `pdf=` arg.

## Document content

- **Agenda PDF** (Jan 22, 2026, 88KB): rich — `PdfKeywordScan` found 3
  hits: a Major Site Plan application by "...ssa Ceppetelli" (likely
  Melissa/Alissa Ceppetelli, partial name from OCR/snippet cutoff), 442
  First NH Turnpike (Map 230, Lot 2), proposing a 1,012 sq ft building
  for a coffee business ("Aro..."); and a much larger **13.5-acre
  Mixed-Use Development** application — two stand-alone commercial
  buildings (a veterinary facility and a medical office) plus three
  3-story residential buildings totaling 36 residential units, on
  property currently owned by "Nort..." (cut off in snippet).

## Sample files downloaded

- `working/northwood_nh/ 01222026.pdf` (note: leading space in filename)

## Open items for later

- A general reminder for any Legend Software town: always check meeting
  date vs. "today" before concluding an agenda/minutes link is missing or
  a town is low-signal.
