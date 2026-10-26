# East Kingston, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Platform: standard CivicPlus Agenda Center
(see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.eknh.org`.
- ⚠️ Search-indexed node URLs (`/node/1811/agenda`, `/planning-board`) are
  stale/404 — site was renumbered. Current Planning Board hub is
  `/1205/Planning-Board`, found via top nav → "Boards" → `/1195/Boards`.
- Agenda Center section loads **already expanded** by default here
  (unlike Newfields, which needed a click).
- Meetings: 3rd Thursday monthly at 7pm, plus occasional extra sessions
  ("Planning Board Site Visit" seen for Apr 28, 2026).

## Scan notes (2026-10-25)

- Listing: `/AgendaCenter`, scrape with the `tr` eval from PATTERNS.md; every
  row carries both Agenda and Minutes links (minutes can be posted within
  days - 10/15 minutes were up by 10/25). Download via browser
  `<a download>` + `ClaimDownload` (works; FetchUrl not tried).
- DB holds agendas only for 9/17 and 10/15; 6/18, 7/16, 8/20 are minutes
  (extension-less `_MMDDYYYY-id` names); the 6/18-8/20 agendas were never
  downloaded.

## Document content

- **Agenda PDF** (Sept 17, 2026, 303KB): substantial — `PdfKeywordScan`
  found 4 hits with real, actionable project detail: a site-plan proposal
  at 33 Haverhill Road (The Green Cocoon LLC, PB Case# 2026-07, storage
  of insulation products in a commercial building plus a mobile home) and
  a 17-lot subdivision proposal at 14 Tilton Lane (Pappalardo Family
  Realty Trust, PB Case# 2026-02) — both with case numbers, applicant
  names, and addresses right in the agenda text.
- **Minutes PDF** (Aug 20, 2026, 461KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/east_kingston_nh/09172026 EKPB Agenda.pdf`
- `working/east_kingston_nh/_08202026-98` (Aug 20, 2026 minutes — no
  extension in the saved filename; it is a PDF)
