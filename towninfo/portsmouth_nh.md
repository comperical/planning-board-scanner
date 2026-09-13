# Portsmouth, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Main city site: `https://www.portsmouthnh.gov` — custom CMS (not CivicPlus), section path prefix `/planportsmouth/...` for this board.
- Actual PDF documents are hosted on a **separate static file host**: `https://files.portsmouthnh.gov` — plain file server, not a document-management portal like Dover's Treeno.
- **No bot protection encountered** — no Cloudflare/challenge page on the main site or the file host, in headed or default Playwright mode. Plain `requests`/`curl` fetches PDFs directly with no browser/session needed at all (unlike Dover).

## Finding the archive

- Board landing/archive page: `https://www.portsmouthnh.gov/planportsmouth/planning-board/planning-board-archived-meetings-and-material`
- This single page lists each meeting (newest first) as a block with a date/title and an "Attachments:" line containing direct links to every document for that meeting — no click-through to a per-meeting detail page needed, and no pagination-per-meeting scraping like Dover's Treeno grid.
- General current schedule: `https://www.portsmouthnh.gov/planportsmouth/meetings-schedule`

## URL structure — static and guessable

Current-era (2020s) pattern, folder per meeting:

```
https://files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}+Meeting/{M}-{D}-{YYYY}_pb_ag.pdf       # Agenda
https://files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}+Meeting/{M}-{D}-{YYYY}_pb_packet.pdf   # Full meeting packet (all submitted materials)
https://files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}+Meeting/{M}-{D}-{YYYY}_pb_min.pdf      # Minutes (published ~1 meeting cycle later)
https://files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}+Meeting/{M}-{D}-{YYYY}_pb_as.pdf       # Action Sheet (vote outcomes only, terse)
https://files.portsmouthnh.gov/agendas/{YYYY}/Planning+Board/{M}-{D}-{YYYY}+Meeting/{M}-{D}-{YYYY}_LOD_FOF_Final-Combined_final.pdf  # Letters of Decision w/ Findings of Fact (per-case legal decision doc)
```

Plus per-meeting one-off supporting docs in the same folder (staff memos, draft ordinance redlines, waiver requests, etc.) — filenames vary, always found via the archive page's Attachments list rather than guessed.

- `+` in URLs is a literal space-encoding (`Planning+Board`, `8-20-2026+Meeting`) — works fine with `requests`/`curl`, no URL-encoding gymnastics needed beyond that.
- Older archive (pre-~2022) uses a flatter, differently-punctuated pattern with no per-meeting folder, e.g. `https://files.portsmouthnh.gov/agendas/2014/planningboard/pb112014m.pdf` and `https://files.portsmouthnh.gov/agendas/2022/planning+board/12-16-2021_pb_min.pdf` — not reverse-engineered in detail since the archive page itself supplies exact links for any date; only worth guessing URLs for **recent/upcoming** meetings where the page already shows the pattern.

## Access method — easy case

- All PDFs are static, unauthenticated, session-independent files — `FetchUrl`/`curl` works directly on any link found on the archive page, or on a guessed current-pattern URL, with no browser round-trip required to "unlock" a temp link (contrast with Dover's Treeno).
- Browser (Playwright) is only needed to **enumerate** the archive page's list of meetings/links — a single page load + `find`/snapshot gets every recent meeting's full attachment set at once (no per-meeting navigation).

## Document content notes (from sample PDFs, in `working/portsmouth_nh/`)

- **Agendas** (`_pb_ag.pdf`) can be very light on real case detail — the 8-20-2026 agenda was almost entirely administrative (CIP presentation, minutes approval, City Council referrals on zoning amendments, one waiver request) with **no** new site-plan/subdivision case items that meeting. Agendas are not reliable alone; check the packet/minutes too.
- **Meeting packet** (`_pb_packet.pdf`) is large (175 pages / 5.6MB for 8-20-2026) — bundles staff memos, draft ordinance redlines, and supporting exhibits; mostly selectable text (2 fully-scanned pages found in the sample), one oversized landscape page (likely a plan sheet). Good source for exhibits/drawings.
- **Minutes** (`_pb_min.pdf`) are the richest source for actual development leads: narrative with applicant name, address, case type, and full description. Sample (6-18-2026 minutes) surfaced a real project — "150 Portsmouth Boulevard... Site Plan Review approval for the construction of three (3), six (6) story multifamily residential buildings" — plus wetland conditional-use permits, a site-plan extension, and a school renovation project. Keyword scan (`PdfKeywordScan`) picked these up cleanly.
- **For a trades-pro lead feed**: minutes are the priority document here (agendas can be nearly empty of case content); packets are useful for scope/detail on a specific case once minutes flag it.

## Sample downloads (in `working/portsmouth_nh/`)

- `8-20-2026_pb_ag.pdf` — regular meeting agenda; administrative-only (no case items)
- `8-20-2026_pb_packet.pdf` — full meeting packet for the same meeting (175 pages)
- `6-18-2026_pb_min.pdf` — minutes; 3-building 6-story multifamily residential site plan (150 Portsmouth Blvd), wetland conditional use permits, site plan extension for a retail project, school renovation

## Open questions / not yet checked

- How far back the archive page's listing goes / whether it paginates for older meetings (only checked the current visible listing, 2026 meetings).
- Whether other Portsmouth boards (ZBA, Historic District Commission, Conservation Commission) use the same `files.portsmouthnh.gov/agendas/{year}/{Board+Name}/...` pattern — plausible given the URL structure but not verified.
- Exact rules for the older (pre-2022) filename pattern if bulk historical scraping is ever needed.
