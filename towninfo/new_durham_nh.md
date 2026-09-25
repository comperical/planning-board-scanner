# New Durham, NH — Planning Board Web Access

Investigated: 2026-09-14

New Durham is the only town in this project on **TownCloud** (see
PATTERNS.md). No bot protection.

## Platform notes

- Main site: `https://www.newdurhamnh.us`. Town-wide agendas page (all
  boards mixed): `/agendas` — each entry shows a board heading, date/
  time, and three links: **View Agenda** (HTML on `towncloud.io`),
  **Agenda PDF**, **Packet PDF**.
- ⚠️ No dedicated Planning-Board-only filtered URL — must scrape and
  filter by heading text ("Planning Board Business Meeting", "Planning
  Board Workshop", "Planning Board Site Walk").
- ⚠️ **Do not assume a numeric agenda id belongs to whichever heading
  looks nearby in an isolated `find`-tool match snippet** — each `find`
  result independently re-renders the pruned tree around just that one
  match, so headings and PDF links from *different* `find` calls don't
  line up positionally. Take one full-page `snapshot` instead. (Confirmed
  the hard way: two ids grabbed from separate `find` results both turned
  out to belong to unrelated "Supervisors of the Checklist" meetings.)
- File URLs use a **generic last path segment**
  (`get_agenda_document_link`) identical across every document on the
  platform — rename immediately after each fetch or it will silently
  overwrite the previous file.
- Meetings: "Business Meeting" 1st Tuesday, "Workshop" 3rd Tuesday, 7pm,
  plus frequent per-case "Site Walk" entries (thin notices - skip).
- **Filename-collision workaround (2026-09-24):** write a placeholder
  `working/new_durham_nh/{agendaId}/.keep`, then
  `FetchUrl ... dest=working/new_durham_nh/{agendaId}` - one folder per
  agenda id keeps each `get_agenda_document_link` distinct. (Browser
  `<a download>` doesn't work here: towncloud.io is cross-origin.)
- To pull only PB rows without a snapshot: `eval` over
  `a[href*=towncloud]`, walking up to the nearest ancestor whose short
  innerText matches /planning/i.
- No minutes found on `/agendas` (agendas + packets only).

## Document content

- **Planning Board Workshop agenda** (Sept 15, 2026, 37KB, id 651): real
  content — `PdfKeywordScan` found 2 hits: a Site Plan Review & Special
  Permit application by **Green Mountain Holdings of NH, LLC** (Map 209,
  Lot 034, 320 Kings Highway) for construction and operation of a
  wireless telecommunications service facility in the
  Residential/Agricultural/Recreational Zoning District, submitted by
  attorney Brian S. Grossman, Esq. — consistent with the town's own
  "cell-tower-info" page naming convention seen at neighboring Strafford.

## Sample files downloaded

- `working/new_durham_nh/get_agenda_document_link` (Sept 15, 2026
  Planning Board Workshop agenda, id 651 — rename before reuse)
