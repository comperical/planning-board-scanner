# Durham, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: standard CivicPlus Agenda Center (see PATTERNS.md).

## Platform notes

- Root domain: `https://www.durhamnh.gov` — town migrated off the old
  `ci.durham.nh.us` domain; that domain (and search results pointing at
  `/boc_planning/planning-board-agendas-minutes`) now 404s/redirects.
  Always start from `/agendacenter`.
- No bot protection encountered — Cloudflare is present at the edge
  (`server: cloudflare` header) but did not challenge page loads or
  direct PDF fetches.
- Agendas/minutes **prior to 2025** are not in Agenda Center at all — the
  page says they live in `/DocumentCenter/Index/1556` instead (not
  explored).

### Meeting types (all under one "Planning Board" section, mixed by date)

| Type | Notes |
|---|---|
| Planning Board Meeting | Regular meeting — full agenda with real case items, each with map/lot, district, applicant/engineer, and a "Recommended action". |
| Planning Board Workshop | Same board, still carries real items. |
| Planning Board Site Walk | Short single-purpose notice, low content value. |
| Planning Board Meeting Material | **Misleading name**: a 1-page cover sheet just listing the filenames of the actual supporting PDFs, not the packet itself (see PATTERNS.md "Materials"-page gotcha). |

## Document content

- **Agendas are unusually rich on their own** — no separate "materials
  packet" needed. Each item gives address/location, project description
  (unit counts, square footage, building count), applicant/owner name,
  engineer/surveyor firm, Map/Lot, zoning district, and a "Recommended
  action" — noticeably more detailed than Rochester's terse one-line
  entries.
- Minutes are Word-generated, fully selectable text, multi-page
  narrative.

## Sample downloads (in `working/durham_nh/`)

- `2026.09.09_PlanningBoard.Agenda.pdf` — 3 pages: Riverwoods Phase II
  senior-housing modification (55 units), a 3-lot subdivision at 73
  Piscataqua Road, a 3-lot subdivision at 4 Smith Park Lane, a
  two-building light-industrial/warehouse site plan (162,000 sq ft each)
  at 121 Technology Drive, and a rink/community-center renovation
  discussion.
- `2026.08.26_PlanningBoard.Minutes.pdf` — 11 pages.
- `2026.02.21_PlanningBoard.SiteWalk.pdf` — 1 page, low content.
- `2026.03.25_PlanningBoard.Materials.pdf` — 1 page cover sheet only
  (see note above).

## Open questions / not yet checked

- Whether the documents listed inside a "Meeting Material" cover sheet
  are independently reachable via their own Agenda Center URLs.
- Pre-2025 archive structure under `/DocumentCenter/Index/1556`.
