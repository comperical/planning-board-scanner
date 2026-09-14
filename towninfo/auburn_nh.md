# Auburn, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town near Manchester. Platform: standard CivicPlus
Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- ⚠️ **Two domains coexist** (see PATTERNS.md domain-gotcha list):
  `https://www.auburnnh.us` (older, node-based `/node/2421/agenda` links)
  and `https://auburnnh.gov` (newer; `AgendaCenter/ViewFile/...` confirmed
  live this session). Treat `.gov` as canonical; `.us` not confirmed
  retired or in sync.
- Planning Board hub (on `.us`): `/planning-board`. Agenda Center (on
  `.gov`): `/agendacenter`, section at `/AgendaCenter/Planning-Board-{n}`
  (exact n not confirmed — reached via a direct `ViewFile` URL from search
  results).
- Uses a **case-number system** (e.g. "P26-03", "P26-05") tagging each
  agenda item — useful for tracking one application across meetings.

## Document content

- **Agenda PDF** (May 20, 2026, 276KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Minor Site Plan Review for "...&
  Pizzeria" (case P26-03, owner Dan Cronin, 5 Dartmouth Dr, Tax Map 6 Lot
  18-3) and a Minor Subdivision for William & Joyce McEvoy (case P26-05,
  30 McEvoy Drive, Tax Map 9 Lot 16-20). An "Other Business" section also
  references ongoing items (15 King Street surety, Jeff Wenzel at 81
  Pri...).

## Sample files downloaded

- `working/auburn_nh/5-20-2026.pdf`

## Open items for later

- Confirm whether `auburnnh.us` and `auburnnh.gov` are the same underlying
  site (a domain migration) or genuinely parallel/stale content.
