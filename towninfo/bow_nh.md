# Bow, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, south of Concord. Platform: standard CivicPlus
Agenda Center (see PATTERNS.md) — no bot protection. Page title renders
"Agenda & Minutes Center" (slightly different label than most other
towns').

## Platform notes

- Main site: `https://bownh.gov`. Direct per-board Agenda Center:
  `/AgendaCenter/Planning-Board-7`.
- Frequently posts joint "Planning Board & Conservation Commission Site
  Visit" public notices as separate entries alongside regular meeting
  agendas — filter by title when scraping.
- Meetings: 1st & 3rd Thursday-ish, 7pm, Bow Municipal Building Meeting
  Room C (or Zoom).

## Document content

- **Agenda PDF** (Jul 16, 2026, 193KB): real content — `PdfKeywordScan`
  found 3 hits: Application No. 208-26, Dennis J. Ordway Trust 2023 (on
  behalf of **Mariner Tower, LLC**), a Site Plan Application + PWSF
  (Personal Wireless Service Facility) Conditional Use Permit for a
  proposed telecommunications facility on a 100'x100' lease area,
  continued from June 18, 2026. Also references a separate property at
  1280 Route 3-A (Map 35, Block 2, Lot 99, General Industrial I-2 zone).

## Sample files downloaded

- `working/bow_nh/07162026 Planning Board Agenda.pdf`
