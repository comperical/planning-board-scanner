# South Hampton, NH — Planning Board Web Access

Investigated: 2026-09-14

Very small Rockingham County town (pop. ~900). **First town in this project
that does not run CivicPlus** — it's a custom/independent site (built on
iPage hosting, `southhamptonnh.org`) with files hosted on Google Cloud
Storage. No bot protection encountered.

## Platform

- Main site: `http://southhamptonnh.org` (plain HTTP works; not tested for
  HTTPS redirect behavior). Not CivicPlus — custom nav, hosted via iPage
  (`southhamptonnhorg.ipage.com` shows up as the media host for some static
  form PDFs).
- Planning Board hub: `/planning-board` — a content page listing board
  members and meeting schedule, plus static form PDFs (Site Plan Review,
  Lot Line Adjustment, Lot Line Merge applications) hosted at
  `southhamptonnhorg.ipage.com/townofsouthhampton_nh/media/...`.
- **Agendas/minutes live on a separate page**: `/planning-agendas-and-minutes`
  (reached via `/meetings-hearings` → "Planning Board Minutes & Agendas"),
  not linked from the Planning Board hub page itself in an obvious way —
  the hub page's "Meeting Agendas and Minutes" link text renders with
  `/url: undefined` in the accessibility snapshot (a broken/JS-driven link);
  reach the real archive via `/meetings-hearings` instead.

## URL structure

- Each meeting row on `/planning-agendas-and-minutes` lists an "Agenda" and
  a "Draft Minutes" link (both, one, or neither, depending on what's been
  posted for that date).
- **Files are hosted on Google Cloud Storage**, not the town's own domain:
  `https://storage.googleapis.com/production-ipage-v1-0-0/890/1310890/
  SHiydKZf/{hash}?fileName={date} {Agenda|Minutes}.pdf` — the `{hash}` is a
  long opaque per-file token, not derivable from the date; must be scraped
  from the listing page.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs. Note: `FetchUrl`'s filename fallback
  landed on just the hash (no `.pdf` extension) because it took the URL's
  last path segment rather than the `fileName=` query param — inspect/
  rename before assuming file type downstream (same category of quirk seen
  with CivicPlus AgendaCenter URLs, different mechanism).
- Minutes here are explicitly labeled **"Draft Minutes"** (not "Approved")
  — worth noting if a downstream consumer cares about approval status.
- Meetings: 1st & 3rd Monday of the month, occasionally shifted (e.g. moved
  to Wednesday one week "due to Labor Day"); occasional extra "Site Walk"
  sessions.

## Document content

- **Agenda PDF** (Jul 20, 2026, 111KB): real project detail —
  `PdfKeywordScan` found 3 hits: a Tri Town Gravel Pit reclamation item
  (Map 6, Lot 28) and a Kozacka Subdivision hearing (PB File #001-26, Map
  5, Lots 25 & 25-1) under a "Hearings on Subdivisions/Site Plans/Lot Line
  Adjustments" section — good signal for a town this small.
- **Minutes PDF** (Jul 6, 2026, 123KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/south_hampton_nh/fc6c61d884624679b1e5ef78b1f3bba5` (Jul 20,
  2026 agenda — no extension in the saved filename; it is a PDF)
- `working/south_hampton_nh/f44905b55f1e4a00905213a4269e50c2` (Jul 6, 2026
  minutes — same, it is a PDF)
