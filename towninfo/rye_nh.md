# Rye, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: standard CivicPlus Agenda Center (see PATTERNS.md). No bot
protection — loaded and navigated cleanly in headless mode.

## Platform notes

- Site: `https://www.ryenh.gov`. The town is mid-migration: old canonical
  hostname `www.town.rye.nh.us` redirects here, but several old-style
  guessed paths 404 — a site banner even says "New Website Updates! Use
  Ryenh.gov to find current pages!" Don't trust guessed slugs; navigate
  from the nav menu.
- Board hub: `/633/Planning-Board` → "View Most Recent Agendas and
  Minutes" → `/AgendaCenter`. Row density roughly monthly (2nd Tuesday) —
  much lower cadence than Exeter/Stratham's near-weekly. Some rows carry
  irregular link text instead of a fixed convention — read the actual
  href.
- `DocumentCenter/View/{id}/{filename}` links (standalone attachments
  like legal notices, application forms) are likewise static and
  `FetchUrl`-able.

## Leads-page check: no Hampton/Stratham-style live leads page

- **"PLANNING BOARD LEGAL NOTICES 2026"** (`/641/...`) — closest analog.
  A static content page with a short, manually-appended list of
  per-meeting Legal Notice PDFs. Only **6 documents** listed as of this
  check, newest dated July 14, 2026 — over two months stale relative to
  the Sept 8, 2026 agenda already posted. Not kept current every
  meeting, no status/hearing-date table — better described as a
  legal-notice archive than a leads page.
- **"2025 Cases heard by the Planning Board"** (`/634/...`) — a single
  attached escrow-account/case-fee status document, not a prose
  case-description page.
- Pending-case detail for Rye lives in the Legal Notice PDFs
  (individually posted when the board chooses to) and the agenda PDF
  itself, not a dedicated always-current listing.

## Document content

- **Agenda PDF** (e.g. `SEPTEMBER 8 2026.pdf`, 2 pages, Word-generated):
  dense, Exeter/Stratham-level case detail — applicant name, property
  owner, full street address, **Tax Map and Lot number**, zoning
  district(s) including overlay districts, plain-English description, and
  the town's own case number (`Case #09-2026`). Sample (Sept 8, 2026):
  - Eversource utility brush-trimming application across ~25 named
    scenic roads (Case #08-2026) — not a development lead, but shows the
    agenda's specificity even for non-development items.
  - Minor site plan by James Holland / Ortholand, LLC, 2203 Ocean Blvd
    Unit C (Tax Map 5.3, Lot 28) — converting a business condo unit to
    residential use (Case #09-2026).
  - Preliminary conceptual consultation for a 7-lot subdivision at 701
    South Rd. (Tax Map 3, Lot 2) — 6 new dwellings plus the existing
    house, new cul-de-sac road, Single Residence / Wetlands Conservation
    / Aquifer & Wellhead Protection districts.
- **Legal Notice PDF** (sample: 120 Brackett + 15 Sagamore, 1 page): same
  case-paragraph format posted standalone ahead of the meeting. Sample
  cases: a minor two-lot subdivision by TFMoran for Dolores F. Lintz, 120
  Brackett Road (Tax Map 22, Lot 95A, Case #05-2026); a **Major Site
  Development and Mixed-Use Development Plan** by Jones & Beach Engineers
  for Pruna Holdings, LLC, 15 Sagamore Rd. (Tax Map 24, Lot 22) — three
  new single-family dwellings plus two mixed-use buildings (Case
  #10-2022, an older case number reappearing on a current-year notice —
  suggests a long-running/continued application).
- No bundled "materials"/"packet" PDF found — the Legal Notice text
  directs inquirers to email staff for application materials, closer to
  Rochester's "not bundled" pattern.

## Sample downloads (in `working/rye_nh/`)

- `SEPTEMBER 8 2026.pdf` — regular meeting agenda
- `_06092026-588` — June 9, 2026 minutes (no `.pdf` extension)
- `PB Legal July 14 2026 for 120 Brackett and LaMulita 15
  Sagamore_202606250903367010.pdf` — standalone Legal Notice PDF

## Open questions / not yet checked

- Whether older years' Agenda Center entries use the same URL pattern
  and stay text-extractable.
- Whether staff would provide application packets electronically if
  emailed, and whether those would be text-extractable.
- Whether the Zoning Board has a richer leads-page pattern.
- Whether "PLANNING BOARD LEGAL NOTICES" is renamed/recreated each year
  and whether prior years' equivalents remain reachable.
