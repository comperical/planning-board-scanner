# Auburn, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town near Manchester. Runs CivicPlus CivicEngage with
the Agenda Center module — same shape as the other Rockingham towns this
session — plain PDFs, no bot protection.

## Platform

- ⚠️ **Two domains coexist**: `https://www.auburnnh.us` (older, shows up in
  search alongside node-based `/node/2421/agenda` links) and
  `https://auburnnh.gov` (newer; `/AgendaCenter/ViewFile/...` links resolve
  here and were confirmed live/fetchable this session). Treat `.gov` as
  canonical going forward; `.us` may be a legacy/parallel site not fully
  retired — not cross-checked for content parity this session.
- Planning Board hub (on `.us`): `/planning-board`.
- Agenda Center (on `.gov`): `/agendacenter`, Planning Board section at
  `/AgendaCenter/Planning-Board-{n}` (exact n not confirmed — reached via
  a direct `ViewFile` URL from search results rather than browsing the
  index page this session).

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `https://auburnnh.gov/AgendaCenter/ViewFile/Agenda/_05202026-152`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Auburn's agendas use a **case-number system** (e.g. "P26-03", "P26-05")
  tagging each item — useful for tracking a specific application across
  multiple meetings.

## Document content

- **Agenda PDF** (May 20, 2026, 276KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Minor Site Plan Review for "...& Pizzeria"
  (case P26-03, owner Dan Cronin, 5 Dartmouth Dr, Tax Map 6 Lot 18-3) and a
  Minor Subdivision for William & Joyce McEvoy (case P26-05, 30 McEvoy
  Drive, Tax Map 9 Lot 16-20). An "Other Business" section also references
  ongoing items (15 King Street surety, Jeff Wenzel at 81 Pri...).

## Sample files downloaded

- `working/auburn_nh/5-20-2026.pdf`

## Open items for later

- Confirm whether `auburnnh.us` and `auburnnh.gov` are the same underlying
  CivicPlus site (a domain migration) or genuinely parallel/stale content
  — don't assume both stay in sync.
