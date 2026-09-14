# Seabrook, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: WordPress, Divi-family theme, unusual `.info` TLD — see
PATTERNS.md. No bot protection.

## Platform notes

- Site: `https://seabrooknh.info`.
- ⚠️ **The obvious page is stale, a different page is current**:
  Google/web-search and the site's own old permalinks point to
  `/planning-board-agendas/` and `/planning-board-minutes/`, whose
  "current year" sections are **stuck at February/March 2023** despite
  the town clearly still holding meetings. **The actually-current listing
  is `/boards-and-committees/planning-board/`**, a tabbed interface
  (Meeting Agendas / Meeting Minutes / Relevant Links) showing agendas up
  to Sept 14, 2026. Always use this page, not the two stale ones — worth
  checking for this same "one page abandoned mid-migration" split on any
  WordPress town site before concluding a town's agendas end in some old
  year.
- Static path: `wp-content/uploads/{YYYY}/{MM}/{filename}.pdf` —
  `{filename}` has no consistent convention and the upload month folder
  doesn't always match the meeting month — read the actual link rather
  than guessing the path.
- Older years (2007–2025) archived under per-year sub-pages with
  inconsistent slug patterns — expect to open each year's page
  separately.

## Document content

- **Agenda PDF**: short and plain-text, no letterhead formatting. Gives
  case number, applicant/business name, project type (CUP, site plan,
  etc.), address, and Tax Map/Lot — less narrative detail than
  Exeter's/Newmarket's. Sample (Sept 14, 2026): a Master Plan update
  hearing, a new CUP case for VRP Cleaning LLC at 1 Eaton Lane (Tax Map
  7, Lot 34-4), and a release of site security for the already-built
  Aldi's Grocery Store case.
- No separate "packet"/bundled materials PDF found — the agenda appears
  to be the only document type published per meeting (plus eventual
  minutes).

## Sample downloads (in `working/seabrook_nh/`)

- `September-14th.pdf` — Sept 14, 2026 agenda
- `June15th.pdf` — Jun 15, 2026 minutes

## Open questions / not yet checked

- Whether there's any bundled "materials"/packet PDF per case.
- Whether Seabrook has an equivalent to Hampton's "Active Applications"
  leads page.
- Whether the Zoning Board/Selectmen pages have the same stale-vs-current
  page split.
