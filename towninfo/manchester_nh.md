# Manchester, NH — Planning Board Web Access

Investigated: 2026-09-14

Manchester is NH's largest city, on a custom DotNetNuke/"Portals" CMS
(see PATTERNS.md). No bot protection.

## Platform notes

- Main site: `https://www.manchesternh.gov`. Planning Board Agendas page:
  `/Departments/Planning-and-Comm-Dev/Planning-Board/Agendas` — a single
  page listing every agenda PDF filename directly (no per-meeting detail
  page), plus a year-filter combobox (options back to 2002).
- This is the most **directly scrapable listing** found in the project so
  far: plain, dated, linked straight to the PDF, no intermediate HTML
  page, no JS-rendered table.
- Static path: `/Portals/2/Departments/pcd/BoardsCommissions/
  PlanningBoard/Agendas2/{YYYY-MM-DD}_PB_AGENDA{_REV._{date}}.PDF` —
  revised agendas keep the original meeting date but add a `_REV._{date}`
  suffix, multiple revisions can coexist (e.g. three separate files for
  the Jan 8, 2026 meeting alone) — take the latest revision.
- Meetings: twice monthly (1st & 3rd, roughly), 6pm, Aldermanic Chambers,
  3rd Floor, City Hall.

## Document content

- **Agenda PDF** (Sept 3, 2026, 299KB): rich, city-scale content —
  `PdfKeywordScan` found 3 hits: a subdivision application at Wellington
  Road (Tax Map 860, Lot 30) creating **34 new buildable lots** with new
  public roads; a **school-building-to-36-unit-affordable-housing
  conversion** (York Hallsville Building, LLC and Fuss & O'Neill,
  representing the City of Manchester itself as applicant — impact fee
  waivers under discussion); and a 6-month extension request on a
  conditionally-approved subdivision of a 31.04-acre parcel with existing
  wetlands.

## Sample files downloaded

- `working/manchester_nh/2026-09-03_PB_AGENDA.PDF`
