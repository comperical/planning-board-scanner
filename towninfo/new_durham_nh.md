# New Durham, NH — Planning Board Web Access

Investigated: 2026-09-14

New Durham is the **first town in this project on TownCloud** (`towncloud.io`
— a fifth distinct municipal CMS vendor found this session, alongside
CivicPlus, Municipal One, Legend Software, and custom WordPress sites). No
bot protection.

## Platform

- Main site: `https://www.newdurhamnh.us`.
- Town-wide agendas page (all boards mixed together, most recent first):
  `/agendas` — each entry shows a board name heading, meeting date/time,
  and three links: **View Agenda** (an HTML view on `towncloud.io`),
  **Agenda PDF**, and **Packet PDF**.
- ⚠️ No dedicated Planning-Board-only filtered URL found this session —
  the page lists every board's meetings interleaved by date. Must scrape
  and filter by heading text (e.g. "Planning Board Business Meeting",
  "Planning Board Workshop", "Planning Board Site Walk").
- ⚠️ **Do not assume a numeric agenda id belongs to whichever heading
  looks nearby in an isolated `find`-tool match snippet** — each `find`
  result block independently re-renders the pruned tree around just that
  one match, so headings and PDF links from *different* `find` calls
  don't line up positionally. Take one full-page `snapshot` instead and
  read the heading → link association directly from that single
  consistent tree (confirmed this the hard way: two ids grabbed from
  separate `find` results both turned out to belong to unrelated
  "Supervisors of the Checklist" meetings, not Planning Board).

## URL structure

- `https://towncloud.io/go/{town-slug}/agendas/{id}/PDF/get_agenda_document_link`
  — the bare agenda PDF.
- `https://towncloud.io/go/{town-slug}/agendas/{id}/pdf_packet/get_agenda_document_link`
  — a (usually larger) packet PDF for the same meeting.
- `https://towncloud.io/go/{town-slug}/agendas/{id}` — an HTML view (not
  fetched this session).
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  both PDF variants directly** — no referer/cookie gate. Filename
  fallback is generic (`get_agenda_document_link`, no extension/date) —
  rename immediately after each fetch or it will silently overwrite the
  previous file, since the URL's last path segment is identical across
  every document on this platform.
- Meetings: e.g. "Planning Board Workshop" 3rd Monday-ish, 7pm.

## Document content

- **Planning Board Workshop agenda** (Sept 15, 2026, 37KB, id 651): real
  content — `PdfKeywordScan` found 2 hits: a Site Plan Review & Special
  Permit application by **Green Mountain Holdings of NH, LLC** (Map 209,
  Lot 034, 320 Kings Highway) for construction and operation of a
  wireless telecommunications service facility in the Residential/
  Agricultural/Recreational Zoning District, submitted by attorney Brian
  S. Grossman, Esq. — consistent with the town's own "cell-tower-info"
  page naming convention seen at neighboring Strafford, NH.

## Sample files downloaded

- `working/new_durham_nh/get_agenda_document_link` (Sept 15, 2026
  Planning Board Workshop agenda, id 651 — rename before reuse, filename
  is generic)
