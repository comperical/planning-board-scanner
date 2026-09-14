# Newfields, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town next to Exeter/Newmarket. Runs CivicPlus
CivicEngage with the Agenda Center module — same pattern as Hampton Falls
and Greenland — but with real PDFs (like Greenland). No bot protection
encountered.

## Platform

- Main site: `https://www.newfieldsnh.gov` — CivicPlus CivicEngage.
- Planning Board hub page: `/235/Planning-Board` (a plain content page with
  board members / meeting schedule; agendas/minutes are *not* embedded here
  — it links out to the shared `/AgendaCenter` instead).
  - ⚠️ A URL surfaced in search results, `/bc-planningboard`, **404s** — not
    a valid page path (looks like a leftover/incorrect link somewhere on
    the web, not the real route). Use `/235/Planning-Board`.
- Agenda Center: `https://www.newfieldsnh.gov/agendacenter` — lists every
  board; **Planning Board's section loads collapsed** and had to be
  expanded with a click (`getByRole('button', { name: '► Planning Board'
  }).click()`) before its rows became visible/scrapable — unlike Hampton
  Falls/Greenland where the Planning Board Agenda Center had its own direct
  per-board URL (`/AgendaCenter/Planning-Board-4`). Worth trying
  `/AgendaCenter/Planning-Board-{n}` directly here too in a future session
  to skip the click step, but not confirmed.

## URL structure

- Same file-serving shape as Hampton Falls/Greenland:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_09102026-188`,
  `/AgendaCenter/ViewFile/Minutes/_08132026-173`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs. Some agenda links append `?html=true`
  (e.g. `_03122026-80?html=true`) — meaning: opens an inline HTML preview
  instead of triggering a download; the same `?html=true` URL still appears
  to resolve to the PDF content via `FetchUrl` (not separately re-tested
  this session, but the pattern is consistent with CivicPlus's other
  towns) — strip the query param if unsure.
- Meetings are monthly, 2nd Thursday, 7pm, Newfields Town Hall. Some months
  add an extra "Work Session" agenda (e.g. May 28, 2026).

## Document content

- **Agenda PDF** (Sept 10, 2026, 179KB): light — `PdfKeywordScan` found 1
  hit ("subdivision" — "Oaklands Rd Subdivision" listed under an "Updates"
  item, plus a "Muddy River Smokehouse mylar" update). Small-town cadence,
  similar sparseness to New Castle.
- **Minutes PDF** (Aug 13, 2026, 70KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/newfields_nh/pb agenda 09.10.2026.pdf`
- `working/newfields_nh/_08132026-173` (Aug 13, 2026 minutes — no extension
  in the saved filename; it is a PDF)
