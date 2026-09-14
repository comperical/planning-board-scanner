# Northwood, NH — Planning Board Web Access

Investigated: 2026-09-14

Northwood is the **first town in this project on "Legend Software"** — a
different municipal CMS vendor from CivicPlus, Municipal One, or the
custom sites seen elsewhere. No bot protection encountered.

## Platform

- Main site: `https://www.northwoodnh.org` — Legend Software (see footer
  credit "Website by Legend Software").
- Planning Board department page: `/entity/Planning-Board-10`.
- **Agendas & Minutes listing** (town-wide, filterable by board):
  `/agendas/Planning-Board-10` — a paginated table with columns "Agenda
  Detail" / "Meeting Date"; each row links to a per-meeting detail page.
- Per-meeting detail page: `/agenda/{Board-Name}-{id}` (e.g.
  `/agenda/Planning-Board-2140`) — id is a flat sequential counter shared
  across **all** boards (not per-board), so ids aren't densely
  enumerable/guessable for Planning Board alone; must be scraped from the
  listing page. Some ids carry descriptive suffixes for special session
  types, e.g. `Planning-Board-Site-Walk-2510`,
  `Planning-Board-Regulation-Review-Subcommittee-2458`.
- ⚠️ **The listing page's default sort surfaces upcoming/future meetings
  first** (ids like 2413/2415/2442 pointed at meeting dates in
  Nov/Dec 2026, i.e. after this session's "today"), several of which had
  no agenda posted yet ("Attached Meeting Minutes: Please check back
  later" and no Agenda link at all). A **lower id (2140) pointed to a
  past meeting (Jan 22, 2026) that did have both an Agenda and Minutes
  link** — when scraping, don't assume the first few rows are the most
  content-rich; check meeting date against "today" and prefer past
  meetings for actual content.

## URL structure

- Each detail page links an **Agenda** PDF directly:
  `https://www.northwoodnh.org/file/{fileId}/{MMDDYYYY}.pdf` (e.g.
  `/file/6210/01222026.pdf`) — a separate numeric id from the meeting
  entry id.
- Minutes are linked under "Attached Meeting Minutes" at a different path:
  `/assets/municipal/10/minutes/{MMDDYYYY}_Minutes_Official_.pdf` (the
  `10` here matches the Planning Board's own entity id, `Planning-Board-10`).
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the Agenda PDF directly** — no referer/cookie gate. Filename fallback
  included a stray leading space (` 01222026.pdf`) — cosmetic, harmless.
- Meetings: 4th Thursday monthly, 6:30pm, Town Hall (per search results;
  this session's sample showed a Jan 22 Thursday meeting consistent with
  that cadence, allowing for holiday shifts).

## Document content

- **Agenda PDF** (Jan 22, 2026, 88KB): rich — `PdfKeywordScan` found 3
  hits: a Major Site Plan application by "...ssa Ceppetelli" (likely
  Melissa/Alissa Ceppetelli, partial name from OCR/snippet cutoff), 442
  First NH Turnpike (Map 230, Lot 2), proposing a 1,012 sq ft building for
  a coffee business ("Aro..."); and a much larger **13.5-acre Mixed-Use
  Development** application — two stand-alone commercial buildings (a
  veterinary facility and a medical office) plus three 3-story residential
  buildings totaling 36 residential units, on property currently owned by
  "Nort..." (name cut off in snippet). Strong, large-scale signal.

## Sample files downloaded

- `working/northwood_nh/ 01222026.pdf` (note: leading space in filename)

## Open items for later

- The listing page's future-dated entries with no content yet are a
  useful reminder for any future town: always check meeting date vs.
  "today" before concluding an agenda/minutes link is missing or a town
  is low-signal.
