# Chichester, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, east of Concord/Pembroke. Runs CivicPlus CivicEngage
with the Agenda Center module — same shape as other towns this session —
plain PDFs, no bot protection.

## Platform

- Main site: `https://www.chichesternh.org`.
- ⚠️ Search-indexed URLs are stale/404: `/planning-board/agenda/
  planning-board-agenda-53` and `/node/21/agenda/2026` both 404. Live
  Planning Board hub is `/1365/Planning-Board`, linking to `/AgendaCenter`.
- Agenda Center: `/AgendaCenter` — a busy town-wide page (Cemetery
  Trustees, etc. interleaved); Planning Board's own section is separate
  and loads already expanded, but filter carefully by exact board name
  (same caveat as Merrimack).

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`Planning Board Agenda September 3 2026.pdf`).
- Meetings: 1st Thursday monthly, 6:30pm, Grange Hall, 54 Main Street.

## Document content

- **Agenda PDF** (Sept 3, 2026, 319KB): real content — `PdfKeywordScan`
  found 3 hits: a standing item on updating Subdivision/Site Review
  regulations, plus a "Continued/Pending Review" case for Eric Jones, 350
  Dover Road, a Site Plan Review for a possible multi-use residential
  building with an ADU (accessory dwelling unit) as a model home/office —
  Technical Review Committee review completed Jan 29, 2026.

## Sample files downloaded

- `working/chichester_nh/Planning Board Agenda September 3 2026.pdf`
