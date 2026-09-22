# Newfields, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town next to Exeter/Newmarket. Platform:
standard CivicPlus Agenda Center (see PATTERNS.md), real PDFs. No bot
protection.

## Platform notes

- Main site: `https://www.newfieldsnh.gov`. Planning Board hub:
  `/235/Planning-Board` (a plain content page; agendas/minutes are *not*
  embedded here — links out to the shared `/agendacenter`).
- Agenda Center's **Planning Board section loads collapsed**, had to be
  expanded with a click before rows became visible — unlike Hampton
  Falls/Greenland which have a direct per-board URL
  (`/AgendaCenter/Planning-Board-{n}`). **Confirmed 2026-09-22**: the
  direct URL `/AgendaCenter/Planning-Board-7` works and loads the board's
  rows already expanded — use it instead of the collapsed town-wide page.
- Some agenda links append `?html=true` (opens an inline HTML preview
  instead of downloading) — strip if unsure.
- Meetings monthly, 2nd Thursday, 7pm. Some months add an extra "Work
  Session" agenda.

## Document content

- **Agenda PDF** (Sept 10, 2026, 179KB): light — `PdfKeywordScan` found 1
  hit ("subdivision" — "Oaklands Rd Subdivision" listed under an
  "Updates" item, plus a "Muddy River Smokehouse mylar" update).
  Small-town cadence, similar sparseness to New Castle.
- **Minutes PDF** (Aug 13, 2026, 70KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/newfields_nh/pb agenda 09.10.2026.pdf`
- `working/newfields_nh/_08132026-173` (Aug 13, 2026 minutes — no
  extension in the saved filename; it is a PDF)
