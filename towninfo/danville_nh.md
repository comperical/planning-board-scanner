# Danville, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Runs CivicPlus CivicEngage with the Agenda
Center module — same shape as the other Rockingham towns this session —
plain PDFs, no bot protection.

## Platform

- Main site: `https://www.townofdanville.org` — CivicPlus CivicEngage.
- Planning Board hub: `/1301/Planning-Board`.
- Agenda Center: `/agendacenter` — Planning Board section loads already
  expanded.
- Danville's meeting **titles themselves carry the project/applicant**, like
  Kensington: "Planning Board Meeting - Preliminary Discussion for a
  possible subdivision at 79 Emerald Drive" (Sept 10, 2026), "Planning
  Board Meeting for discussion of Zoning requested by Jeff & Joelle Stone
  of 17 Quimby Court" (Aug 27, 2026) — real signal visible from the listing
  page alone.
- ⚠️ Two different `docid` numbering series appear for the same date (Jan
  22, 2026 has both `_01222026-144` and `_01222026-84`, one from an older
  Planning Board series and one newer, likely a site/module migration
  artifact) — dedupe by date+title when scraping, not by docid alone.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs (`September 10 2026 Agenda.pdf`, 18KB).
- Meetings: 2nd & 4th Thursday, 7:30pm, Town Hall, 210 Main Street.

## Document content

- **Agenda PDF** (Sept 10, 2026, 18KB): short — 1 keyword hit, consistent
  with a small-town preliminary-discussion agenda (not yet a formal
  subdivision application). The listing-page title itself already carried
  more signal than the PDF body in this sample.

## Sample files downloaded

- `working/danville_nh/September 10 2026 Agenda.pdf`
