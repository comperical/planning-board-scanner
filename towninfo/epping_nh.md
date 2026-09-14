# Epping, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town along Route 101/125, larger than the small Kingston-
area towns (has real industrial/commercial development pressure). Runs
CivicPlus CivicEngage with the Agenda Center module — plain PDFs, no bot
protection.

## Platform

- Main site: `https://www.eppingnh.gov` — CivicPlus CivicEngage.
- ⚠️ Search-indexed `/minutes-and-agendas` is **stale/404** — same recurring
  pattern (East Kingston, Fremont). Live Planning Board hub is
  `/217/Planning-Board-Code-Enforcement` (board is combined with Code
  Enforcement here), found via top nav → "Boards & Commissions" →
  `/208/Government`.
- Agenda Center: `https://www.eppingnh.gov/AgendaCenter` — the Planning
  Board section here is labeled **"Planning Board Agenda"** (not just
  "Planning Board") and loads **already expanded**.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_09102026-148`,
  `/AgendaCenter/ViewFile/Minutes/_06112026-110`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — agenda got a compact real filename
  (`091026pbag.pdf`); minutes fell back to the bare `_{date}-{id}` with no
  extension (recurring AgendaCenter quirk — it is a PDF).
- Meetings: 2nd Thursday monthly, 6pm.

## Document content

- **Agenda PDF** (Sept 10, 2026, 251KB): rich, real project detail —
  `PdfKeywordScan` found 5 hits across multiple cases: **SIG SAUER, INC.**
  (major regional firearms manufacturer headquartered in Epping) applying
  for a Site Plan + Conditional Use to build a two-story classroom/shooting
  structure; a separate site plan/conditional-use item at 46 Martin Road
  (Tax Map 036, Lot 023, Industrial Commercial Zoning District); and a Lot
  Line Adjustment for Matthew Harvey at French Road / Nottingham Square
  Road (Tax Map 002). Epping is a good example of a town where a named,
  recognizable applicant shows up directly in agenda text — useful signal
  strength for this project's purpose.
- **Minutes PDF** (Jun 11, 2026, 70KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/epping_nh/091026pbag.pdf` (Sept 10, 2026 agenda)
- `working/epping_nh/_06112026-110` (Jun 11, 2026 minutes — no extension
  in the saved filename; it is a PDF)
