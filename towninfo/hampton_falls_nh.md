# Hampton Falls, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town, runs CivicPlus CivicEngage like its
neighbors, but uses the **Agenda Center** module (`/AgendaCenter/...`)
rather than the node-based agenda/minutes pages seen in New Castle/Rye/
Exeter. No bot protection encountered.

## Platform

- Main site: `https://www.hamptonfalls.org` — CivicPlus CivicEngage.
- Planning Board hub: `/250/Planning-Board`.
- Agenda Center for this board: `/AgendaCenter/Planning-Board-4` — a single
  page listing all agenda/minutes entries (not paginated by year in the
  URL; older entries presumably load via in-page pagination/JS).

## URL structure

- Each agenda/minutes row links to
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`
  (e.g. `/AgendaCenter/ViewFile/Agenda/_08252026-162`,
  `/AgendaCenter/ViewFile/Minutes/_06232026-147}`) — date-plus-sequential-id,
  guessable in *shape* but the numeric id isn't derivable without scraping
  the index page.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** — no referer/cookie gate, unlike Concord's Legistar.
- **⚠️ Files served here are Word documents (`.docx`), not PDFs** — first
  town in this project where that's the case. Content-Type comes back as
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
  This project's PDF tool chain (`PdfExtractText`, `PdfKeywordScan`, etc.)
  won't work on these directly — analyzing Hampton Falls documents will need
  either a docx→text step or an upstream conversion, not yet built.
  - Also note: when `FetchUrl`'s response lacks a `Content-Disposition`
    filename, it falls back to the URL's last path segment, which for these
    URLs is just `_{date}-{id}` with **no file extension** (saved as
    `_06232026-147`) — check/rename before assuming file type downstream.

## Document content

- Not yet analyzed (docx, not text-extractable with current tools). Sample
  files pulled for a future docx-handling pass:
  - `working/hampton_falls_nh/2026-08-25 PB Agenda.docx` (Aug 25, 2026
    agenda — this one kept its real filename via Content-Disposition)
  - `working/hampton_falls_nh/_06232026-147` (Jun 23, 2026 minutes, no
    extension — is actually a .docx, rename before use)
- Board meets 4th Tuesday monthly (3rd Tuesday in Nov/Dec).

## Open items for later

- Build/borrow a `.docx` text-extraction tool if Hampton Falls (or other
  towns using Agenda Center with Word output) needs full analysis.
- Confirm whether *all* entries in this town's Agenda Center are `.docx`,
  or whether some meeting types post PDFs instead.
