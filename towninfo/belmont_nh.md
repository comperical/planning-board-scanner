# Belmont, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, south of Laconia/Gilford. Runs a **custom WordPress
site**, not CivicPlus. No bot protection.

## Platform

- Main site: `https://belmontnh.gov` — WordPress.
- Each meeting gets its own page: `/meetings/{YYYY-MM-DD}-planning-board-meeting/`
  (e.g. `/meetings/2026-02-23-planning-board-meeting/`), each embedding
  direct download links for the Agenda and (once posted) the Minutes.
- Also has a calendar/events version: `/events/planning-board-meeting/`
  and `/events/planning-board-meeting-{date}/` for individual occurrences
  — not cross-checked against `/meetings/...` for content parity.
- A "Public Meetings and Resources" page also surfaced at
  `belmont.gov/departments/meetings-agendas-minutes` in search results —
  that's a different town (Belmont, MA / generic city), not this NH town;
  don't confuse domains.

## URL structure

- Static WordPress media uploads:
  `https://belmontnh.gov/wp-content/uploads/sites/38/{YYYY}/{MM}/
  {YYMMDD}PBAgenda.pdf` (agenda) and `.../{YYMMDD}-PB-MInutes.pdf`
  [sic, typo capitalization preserved] (minutes) — the `sites/38/`
  segment is a WordPress multisite id, constant across Belmont's pages.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** — no referer/cookie gate.
- Live meetings streamed at `youtube.com/@belmontlive`; Zoom links posted
  per-meeting at the bottom of each agenda.

## Document content

- **Agenda PDF** (Feb 23, 2026, 159KB): real content — `PdfKeywordScan`
  found 3 hits: a Site Plan Review application by the Susan
  Condodemetraky Revocable Trust to expand an existing contractor's yard
  to include towing and temporary storage of vehicles; and a Boundary
  Line Adjustment between the Paroma Condominium Association and
  Mallard's Landing Association, transferring a small parcel between the
  two associations.

## Sample files downloaded

- `working/belmont_nh/260223PBAgenda.pdf`
- `working/belmont_nh/PLANNING-BOARD-PBAgenda-2025-05-19.pdf` (older
  sample, used to first confirm platform access)
