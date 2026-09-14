# East Kingston, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Runs CivicPlus CivicEngage with the Agenda
Center module (same shape as Hampton Falls/Greenland/Newfields/Kingston's
neighbor towns) — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.eknh.org` — CivicPlus CivicEngage.
- ⚠️ Search-indexed node URLs (`/node/1811/agenda`, `/planning-board`) are
  **stale/404** — the site was apparently renumbered since those were
  crawled. Current Planning Board hub is `/1205/Planning-Board`, found via
  the top nav → "Boards" menu → `/1195/Boards` listing page. Always verify
  a cached node id/slug against live navigation rather than trusting a
  search result directly.
- Agenda Center: `https://www.eknh.org/AgendaCenter` — the Planning Board
  section loads **already expanded** by default here (unlike Newfields,
  which needed a click), so all rows are visible on first load.

## URL structure

- Same shape as the other Agenda Center towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_09172026-100`,
  `/AgendaCenter/ViewFile/Minutes/_08202026-98`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — agenda file got a sane filename via
  Content-Disposition (`09172026 EKPB Agenda.pdf`); minutes fell back to
  the bare `_{date}-{id}` with no extension (same quirk as other
  AgendaCenter towns — it is a PDF).
- Meetings: 3rd Thursday monthly at 7pm, plus occasional extra sessions
  ("Planning Board Site Visit" seen for Apr 28, 2026).

## Document content

- **Agenda PDF** (Sept 17, 2026, 303KB): substantial — `PdfKeywordScan`
  found 4 hits with real, actionable project detail: a site-plan proposal
  at 33 Haverhill Road (The Green Cocoon LLC, PB Case# 2026-07, storage
  of insulation products in a commercial building plus a mobile home) and
  a 17-lot subdivision proposal at 14 Tilton Lane (Pappalardo Family
  Realty Trust, PB Case# 2026-02) — both with case numbers, applicant
  names, and addresses right in the agenda text, no packet needed.
- **Minutes PDF** (Aug 20, 2026, 461KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/east_kingston_nh/09172026 EKPB Agenda.pdf`
- `working/east_kingston_nh/_08202026-98` (Aug 20, 2026 minutes — no
  extension in the saved filename; it is a PDF)
