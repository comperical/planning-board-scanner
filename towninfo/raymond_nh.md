# Raymond, NH — Planning Board Web Access

Investigated: 2026-09-14

Raymond's main town site is a plain custom PHP site, but it hosts
agendas/minutes on **eCode360** (see PATTERNS.md), not seen elsewhere in
this project. No bot protection on either domain.

## Platform notes

- Main site: `https://www.raymondnh.gov` (custom PHP, `.../index.php`),
  not CivicPlus.
- ⚠️ Search-indexed `/meeting-minutes-agendas` 404s — the real path is
  off-site: footer link "Agendas & Minutes" →
  `https://ecode360.com/RA1135/document/types` (`RA1135` = Raymond's
  eCode360 client id).
- eCode360 Planning Board category: `ecode360.com/RA1135/documents/
  Planning_Board` — a single page with three subsections (Agendas,
  Meeting Documents, Meeting Minutes), each broken out by year via
  in-page anchors, not separate URLs — whole year loads on one page.
- Every document is a static numeric PDF: `/RA1135/document/{id}.pdf` —
  no query params, no session token.
- Posts far more than monthly agendas: individual **"Site Walk Notice"**
  PDFs are filed per-project (e.g. "Site Walk Notice PB-2026-003
  Evergreen", "...PB-2025-012 Houston Subdivision", "...PB-2025-022 King
  Meadow Subdivision") — these alone name real, in-progress subdivisions
  by name and case number, a strong direct signal source independent of
  the main agenda text. Separate "Meeting Documents" category too.
- Meetings frequent: near-weekly, plus separate "Work Session" agendas.

## Document content

- **Agenda PDF** (Sept 3, 2026, 318KB): very rich —
  `PdfKeywordScan` found 4 hits spanning multiple active, named,
  multi-phase projects with case numbers: **Onway Lake Development**
  (Phase IV site plan review + special permit, applicant Jones & Beach
  Engineering; Phase I subdivision application by Shiv Shrestha and Matt
  Silverstein, PB-2023-008; Phase II referenced for an Oct 1 hearing,
  PB-2024-011), plus a residential/agricultural zone item at 18
  Nottingham Road (Tax Map 35 Lot 1), and a rundown of upcoming case
  numbers (PB-2026-003 Evergreen, PB-2025-012 Houston Subdivision) on
  page 2. One of the strongest single-document samples found in the
  project.

## Sample files downloaded

- `working/raymond_nh/Planning Board - Agendas - 2026 - 09.03.2026
  Planning Board Agenda.pdf` (note: saved with literal `%20` in the
  filename since `FetchUrl` didn't URL-decode the Content-Disposition
  value — cosmetic only)
