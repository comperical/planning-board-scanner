# Durham, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- CMS: **CivicPlus "CivicEngage"**, using the standard CivicPlus **Agenda Center** module.
- Root domain: `https://www.durhamnh.gov` — note the town migrated off the old
  `ci.durham.nh.us` domain; that domain (and search results pointing at
  `/boc_planning/planning-board-agendas-minutes`) now 404s and silently
  redirects to the new `durhamnh.gov` host. Always start from
  `https://www.durhamnh.gov/agendacenter`.
- No bot protection encountered — headless Playwright loaded every page fine,
  and plain `curl` works too (see below). Cloudflare is present at the edge
  (response headers show `server: cloudflare`) but it did not challenge either
  page loads or direct PDF fetches.

## Planning Board archive structure

- Agenda Center root: `/agendacenter` — lists every board/commission as a
  collapsible section ("▼ Planning Board", "▼ Zoning Board of Adjustment",
  etc.), each with year tabs (2025, 2026, ...) and a table of meetings newest
  first.
- Each meeting row has an agenda-type link (e.g. "Planning Board Meeting",
  "Planning Board Workshop", "Planning Board Site Walk", "Planning Board
  Meeting Material") and, once posted, a "Minutes" link.
- **PDF URLs are static and directly `curl`-able — no session/browser needed**:
  - Agenda: `https://www.durhamnh.gov/AgendaCenter/ViewFile/Agenda/_{MMDDYYYY}-{id}`
    (the on-page link often appends `?html=true`, which is optional — the
    same URL without it serves the raw PDF directly with
    `content-type: application/pdf`).
  - Minutes: `https://www.durhamnh.gov/AgendaCenter/ViewFile/Minutes/_{MMDDYYYY}-{id}`
  - The `{id}` is an opaque incrementing item id (not derivable from the date
    alone) — get it from the Agenda Center listing page rather than guessing.
- Agendas/minutes **prior to 2025** are not in Agenda Center at all; the page
  says they live in the separate `/DocumentCenter/Index/1556` document
  repository instead.

## Meeting types (all under one "Planning Board" section, mixed by date)

| Type | Notes |
|---|---|
| Planning Board Meeting | Regular meeting — full agenda with real case items (site plans, subdivisions, conditional use, waivers), each with map/lot, district, applicant/engineer, and a "Recommended action". |
| Planning Board Workshop | Same board, still carries real items. |
| Planning Board Site Walk | Short single-purpose notice (site visit), low content value. |
| Planning Board Meeting Material | Seen on several Jan–Mar 2026 dates — **misleading name**: the document behind this link is a 1-page cover sheet just listing the filenames of the actual supporting PDFs (draft minutes, legal notice, agenda) rather than the packet itself. Check whether the individually-named documents it lists are separately reachable in Agenda Center or only inside a packet not captured here — not yet resolved this session. |

## Document content notes (from sample PDFs, in `working/durham_nh/`)

- **Agendas are unusually rich on their own** — no separate "materials
  packet" needed to get real signal. Each item gives: address/location,
  project description (unit counts, square footage, building count),
  applicant/owner name, engineer/surveyor firm, Map/Lot, zoning district, and
  a "Recommended action" (e.g. "Set public hearing", "Final action if
  ready", "Discussion and continuation to..."). This is noticeably more
  detailed than Rochester's terse one-line agenda entries.
- Minutes are Word-generated (`Microsoft® Word for Microsoft 365`), fully
  selectable text, multi-page narrative — same general shape as Rochester's:
  richer than agendas, published after the meeting, good for confirming
  approval status.
- The "Meeting Material" cover-sheet PDF (see table above) has essentially no
  standalone content — do not treat it as a materials packet substitute.

## Sample downloads (in `working/durham_nh/`)

- `2026.09.09_PlanningBoard.Agenda.pdf` — regular meeting; 3 pages, selectable
  text. Items include: Riverwoods Phase II senior-housing modification (55
  units), a 3-lot subdivision at 73 Piscataqua Road, a 3-lot subdivision at 4
  Smith Park Lane, a two-building light-industrial/warehouse site plan (162,000
  sq ft each) at 121 Technology Drive, and a rink/community-center renovation
  discussion.
- `2026.08.26_PlanningBoard.Minutes.pdf` — 11 pages, selectable text.
- `2026.02.21_PlanningBoard.SiteWalk.pdf` — 1 page, low content.
- `2026.03.25_PlanningBoard.Materials.pdf` — 1 page; despite the name, just a
  cover sheet listing 4 other document filenames (see note above).

## Open questions / not yet checked

- Whether the documents listed inside a "Meeting Material" cover sheet (e.g.
  `PLANNING BOARD MEETING SUPPORTING DOCUMENT ... DRAFT MINUTES ....PDF`) are
  independently reachable via their own Agenda Center URLs, or only exist
  packaged some other way.
- Whether other Durham boards (ZBA, Conservation Commission) follow the same
  Agenda Center pattern under their own section — very likely yes, same
  module, just a different section name.
- Pre-2025 archive structure under `/DocumentCenter/Index/1556` — not
  explored.
