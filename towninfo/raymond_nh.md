# Raymond, NH — Planning Board Web Access

Investigated: 2026-09-14

Raymond is **not** CivicPlus — its main town site (`raymondnh.gov`) is a
plain custom PHP site, and it hosts agendas/minutes/support documents on
**eCode360** (General Code's document/code publishing platform,
`ecode360.com`), a system not seen elsewhere in this project yet. No bot
protection encountered on either domain.

## Platform

- Main site: `https://www.raymondnh.gov` (also resolves bare at
  `raymondnh.gov`) — custom PHP site (`.../index.php` paths), not
  CivicPlus.
- ⚠️ A search-indexed `/meeting-minutes-agendas` URL **404s** — the real
  path to documents is off-site entirely. From the homepage: footer link
  "Agendas & Minutes" → `https://ecode360.com/RA1135/document/types`, a
  General Code eCode360 portal scoped to Raymond (`RA1135` = the town's
  eCode360 client id).
- Planning & Development department page (board info, not documents):
  `https://raymondnh.gov/town_departments/planning___development/index.php`.
- eCode360 Planning Board document category:
  `https://ecode360.com/RA1135/documents/Planning_Board` — a single page
  with three subsections (Agendas, Meeting Documents, Meeting Minutes),
  each broken out by year via in-page anchors
  (`#category-752819398-year-2026` etc.), not separate URLs — the whole
  year's documents load on one page load, so no per-year navigation
  needed to scrape everything visible.

## URL structure

- Every document is a **static, sequential-looking numeric PDF** under
  `/RA1135/document/{id}.pdf` — e.g.
  `https://ecode360.com/RA1135/document/753278587.pdf` — no query params,
  no session token.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** — got a full descriptive filename via
  Content-Disposition (`Planning Board - Agendas - 2026 - 09.03.2026
  Planning Board Agenda.pdf`).
- Raymond posts **far more than just monthly agendas**: individual
  **"Site Walk Notice"** PDFs are filed per-project (e.g. "Site Walk Notice
  PB-2026-003 Evergreen", "Site Walk Notice PB-2025-012 Houston
  Subdivision", "Site Walk Notice PB-2025-022 King Meadow Subdivision") —
  these alone name real, in-progress subdivisions by name and case number,
  a strong direct signal source independent of the main agenda text.
  There's also a separate "Meeting Documents" (support materials/packets)
  category per meeting, parallel to Agendas and Minutes.
- Meetings are frequent: near-weekly ("Planning Board Agenda" entries
  roughly every 1-2 weeks, plus separate "Work Session" agendas).

## Document content

- **Agenda PDF** (Sept 3, 2026, 318KB): very rich —
  `PdfKeywordScan` found 4 hits spanning multiple active, named,
  multi-phase projects with case numbers: **Onway Lake Development**
  (Phase IV site plan review + special permit, applicant Jones & Beach
  Engineering; Phase I subdivision application by Shiv Shrestha and Matt
  Silverstein, PB-2023-008; Phase II referenced for an Oct 1 hearing,
  PB-2024-011), plus a residential/agricultural zone item at 18 Nottingham
  Road (Tax Map 35 Lot 1), and a rundown of upcoming case numbers
  (PB-2026-003 Evergreen, PB-2025-012 Houston Subdivision) on page 2. This
  is one of the strongest single-document samples found in the project so
  far.

## Sample files downloaded

- `working/raymond_nh/Planning Board - Agendas - 2026 - 09.03.2026
  Planning Board Agenda.pdf` (note: saved with literal `%20` in the
  filename since `FetchUrl` didn't URL-decode the Content-Disposition
  value — cosmetic only, file opens fine)
