# Pelham, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town on the MA border, southeast of Nashua. Runs
CivicPlus (mixed classic `.aspx` + newer CivicEngage pages). No bot
protection encountered, but the Agenda Center here behaves differently
from every other CivicPlus town in this project. **Partial — no sample
PDF downloaded.**

## Platform notes

- Main site: `https://www.pelhamweb.com`. Planning Board hub:
  `/165/Planning-Board` → `/866/Planning-Board-Agendas-and-Minutes`,
  which renders as an **inline calendar widget** rather than a per-board
  list of dated agenda links like every other CivicPlus town sampled.
- `/agendacenter` exists and loads, but unlike other AgendaCenter towns it
  shows **only a search form** (date range + keyword + "Select a
  Category" dropdown) with no pre-expanded per-board list visible in
  static markup — clicking "Select a Category" didn't surface visible
  options in this session's checks.
- ⚠️ Several plausible node-based URLs guessed from the pattern seen
  elsewhere **404'd**: `/node/3851/agenda/2026`, `/node/4536/agenda`,
  `/129` (redirects to `/129/Agendas-Minutes`, also a dead end for
  Planning Board specifically).
- `/223/Meetings` lists the meeting **schedule** (1st & 3rd Mondays) and
  a schedule-of-dates PDF, but not individual meeting agendas/minutes.
  `/237/Planning-Department` and the Document Center (`/522`) hold
  reference documents (Master Plan, Zoning Ordinance, Buildout Analysis)
  but not dated meeting agendas.

## Open items for later

- Finish working out the Agenda Center category-selection flow (or find
  the per-board direct URL, likely `/AgendaCenter/Planning-Board-{n}`
  following the pattern from other CivicPlus towns, though a numeric
  guess wasn't tried).
- Alternatively, try clicking a specific date on the `/866/...` calendar
  widget to see if it surfaces a document link per meeting.
