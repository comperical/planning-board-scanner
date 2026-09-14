# Portsmouth, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: custom CMS (not CivicPlus), PDFs on a separate static file host
`files.portsmouthnh.gov` — plain file server, not a DMS portal. No bot
protection encountered.

## Platform notes

- Main city site: `https://www.portsmouthnh.gov` (section path prefix
  `/planportsmouth/...`).
- Board landing/archive page: `/planportsmouth/planning-board/planning-
  board-archived-meetings-and-material` — lists each meeting (newest
  first) as a block with an "Attachments:" line linking every document
  for that meeting directly — no click-through to a per-meeting detail
  page, no per-meeting pagination like Dover's Treeno grid.
- Current-era (2020s) folder-per-meeting pattern:
  `files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}
  +Meeting/{M}-{D}-{YYYY}_pb_{ag|packet|min|as}.pdf` (agenda / full
  packet / minutes ~1 cycle later / action sheet), plus a
  `..._LOD_FOF_Final-Combined_final.pdf` (Letters of Decision w/ Findings
  of Fact, per-case legal decision doc). `+` is a literal space-encoding,
  works fine with `requests`/`curl`.
- Older archive (pre-~2022) uses a flatter, differently-punctuated
  pattern — not reverse-engineered since the archive page supplies exact
  links for any date; only worth guessing URLs for recent/upcoming
  meetings.
- All PDFs static, unauthenticated, `curl`/`FetchUrl`-able directly —
  browser only needed to enumerate the archive page's link list.

## Document content

- **Agendas** (`_pb_ag.pdf`) can be very light — the 8-20-2026 sample was
  almost entirely administrative (CIP presentation, minutes approval,
  City Council referrals, one waiver request) with **no** new
  site-plan/subdivision items that meeting. Agendas are not reliable
  alone; check the packet/minutes too.
- **Meeting packet** (`_pb_packet.pdf`) is large (175 pages / 5.6MB for
  8-20-2026) — bundles staff memos, draft ordinance redlines, supporting
  exhibits; mostly selectable text (2 fully-scanned pages in the sample),
  one oversized landscape page (likely a plan sheet).
- **Minutes** (`_pb_min.pdf`) are the richest source for actual
  development leads: narrative with applicant name, address, case type,
  full description. Sample (6-18-2026) surfaced "150 Portsmouth
  Boulevard... Site Plan Review approval for the construction of three
  (3), six (6) story multifamily residential buildings" — plus wetland
  conditional-use permits, a site-plan extension, and a school renovation
  project.
- **For a trades-pro lead feed**: minutes are the priority document here
  (agendas can be nearly empty of case content); packets useful for
  scope/detail once minutes flag a case.

## Sample downloads (in `working/portsmouth_nh/`)

- `8-20-2026_pb_ag.pdf` — administrative-only, no case items
- `8-20-2026_pb_packet.pdf` — full packet, 175 pages
- `6-18-2026_pb_min.pdf` — 3-building 6-story multifamily site plan (150
  Portsmouth Blvd), wetland conditional use permits, retail-project site
  plan extension, school renovation

## Open questions / not yet checked

- How far back the archive page's listing goes / whether it paginates.
- Whether other Portsmouth boards use the same
  `files.portsmouthnh.gov/agendas/{year}/{Board+Name}/...` pattern.
- Exact rules for the older (pre-2022) filename pattern.
