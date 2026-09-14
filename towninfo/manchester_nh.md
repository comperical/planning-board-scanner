# Manchester, NH — Planning Board Web Access

Investigated: 2026-09-14

Manchester is NH's largest city and runs its own **custom .gov site on a
DotNetNuke/"Portals" CMS** — the sixth distinct platform found in this
project (alongside CivicPlus, Municipal One, Legend Software, custom
WordPress, and TownCloud). No bot protection.

## Platform

- Main site: `https://www.manchesternh.gov`.
- Planning Board Agendas page:
  `/Departments/Planning-and-Comm-Dev/Planning-Board/Agendas` — a single
  page listing every agenda PDF filename directly (no per-meeting detail
  page to click through), plus a year-filter combobox (options back to
  2002) and a separate "Planning Board Links" section.
- This is the most **directly scrapable listing** found in the project so
  far: filenames are plain, dated, and linked straight to the PDF — no
  intermediate HTML page, no JS-rendered table, no `?html=true` variants.

## URL structure

- Static PDFs under a `/Portals/2/...` DotNetNuke file-storage path:
  `https://www.manchesternh.gov/Portals/2/Departments/pcd/
  BoardsCommissions/PlanningBoard/Agendas2/{YYYY-MM-DD}_PB_AGENDA{_REV._
  {date}}.PDF` — revised agendas keep the original meeting date in the
  filename prefix but add a `_REV._{revision-date}` suffix, and multiple
  revisions can coexist for the same meeting (e.g. three separate `_REV.`
  files for the Jan 8, 2026 meeting alone) — take the latest revision
  when several exist for one date.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** — no referer/cookie gate.
- Meetings: twice monthly (1st & 3rd, roughly), 6pm, Aldermanic Chambers,
  3rd Floor, City Hall.

## Document content

- **Agenda PDF** (Sept 3, 2026, 299KB): rich, city-scale content —
  `PdfKeywordScan` found 3 hits: a subdivision application at Wellington
  Road (Tax Map 860, Lot 30) creating **34 new buildable lots** with new
  public roads; a **school-building-to-36-unit-affordable-housing
  conversion** (York Hallsville Building, LLC and Fuss & O'Neill,
  representing the City of Manchester itself as an applicant — impact fee
  waivers under discussion); and a 6-month extension request on a
  conditionally-approved subdivision of a 31.04-acre parcel with existing
  wetlands. Strong, large-scale signal typical of a city rather than a
  small town.

## Sample files downloaded

- `working/manchester_nh/2026-09-03_PB_AGENDA.PDF`
