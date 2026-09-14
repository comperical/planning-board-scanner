# Hampstead, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town. Runs CivicPlus CivicEngage with the Agenda Center
module — same shape as the other Rockingham towns this session — plain
PDFs, no bot protection.

## Platform

- Main site: `https://www.hampsteadnh.us` — CivicPlus CivicEngage.
- Planning Board hub: `/263/Planning-Board`.
- Agenda Center: `/AgendaCenter` — town-wide page listing every board; the
  Planning Board section shows only the **current year by default**, with
  "Planning Board 2025", "Planning Board 2024" and a "View More" link as
  separate JS-triggered year loads (`javascript:changeYear(2025, 4,
  'a1')`) — same lazy-year pattern seen elsewhere, but this page is busy
  enough (many boards, ~115 ViewFile links total) that a plain text `find`
  for "Planning Board" alone missed the actual row data; needed a full
  snapshot + grep for the section to locate current rows.
- Sample agenda titles are plain ("09/08/2026 PB Agenda (PDF)") — no
  embedded project detail in the title itself here, unlike Danville/
  Kensington.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs (`09.08.2026 Agenda.pdf`, 44KB).
- Some meetings also link a **Media/Video** entry (hosted on
  `cloud.castus.tv`) alongside Agenda/Minutes.

## Document content

- **Agenda PDF** (Sept 8, 2026, 44KB): 1 keyword hit — light content in
  this sample; not yet clear if that's typical or an off month. A follow-up
  session should sample 2-3 more meetings before concluding Hampstead is
  generally sparse.

## Sample files downloaded

- `working/hampstead_nh/09.08.2026 Agenda.pdf`
