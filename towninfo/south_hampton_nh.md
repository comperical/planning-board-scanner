# South Hampton, NH — Planning Board Web Access

Investigated: 2026-09-14

Very small Rockingham County town (pop. ~900). A custom/independent site
(iPage hosting), not CivicPlus — files hosted on Google Cloud Storage,
not the town's own domain (see PATTERNS.md). No bot protection
encountered.

## Platform notes

- Main site: `http://southhamptonnh.org` (plain HTTP works). Planning
  Board hub: `/planning-board` — members/schedule plus static form PDFs
  hosted at `southhamptonnhorg.ipage.com/townofsouthhampton_nh/media/...`.
- **Agendas/minutes live on a separate page**: `/planning-agendas-and-
  minutes` (reached via `/meetings-hearings` → "Planning Board Minutes &
  Agendas") — not linked from the Planning Board hub page itself in an
  obvious way (the hub page's own link renders as `/url: undefined`, a
  broken/JS-driven link).
- Files: `storage.googleapis.com/production-ipage-v1-0-0/890/1310890/
  SHiydKZf/{hash}?fileName={date} {Agenda|Minutes}.pdf` — `{hash}` is a
  long opaque per-file token, must be scraped from the listing page.
  `FetchUrl`'s filename fallback lands on just the hash (no `.pdf`
  extension) since it takes the URL's last path segment rather than the
  `fileName=` query param — inspect/rename before assuming file type.
- Minutes explicitly labeled **"Draft Minutes"** (not "Approved").
- Meetings: 1st & 3rd Monday, occasionally shifted; occasional extra
  "Site Walk" sessions.

## Document content

- **Agenda PDF** (Jul 20, 2026, 111KB): real project detail —
  `PdfKeywordScan` found 3 hits: a Tri Town Gravel Pit reclamation item
  (Map 6, Lot 28) and a Kozacka Subdivision hearing (PB File #001-26, Map
  5, Lots 25 & 25-1) under a "Hearings on Subdivisions/Site Plans/Lot
  Line Adjustments" section — good signal for a town this small.
- **Minutes PDF** (Jul 6, 2026, 123KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/south_hampton_nh/fc6c61d884624679b1e5ef78b1f3bba5` (Jul 20,
  2026 agenda — no extension, is a PDF)
- `working/south_hampton_nh/f44905b55f1e4a00905213a4269e50c2` (Jul 6,
  2026 minutes — same, is a PDF)
