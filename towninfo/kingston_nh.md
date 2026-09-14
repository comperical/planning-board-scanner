# Kingston, NH — Planning Board Web Access

Investigated: 2026-09-14

Kingston is notably more complex than the neighboring Seacoast towns
studied so far — it runs a **newer CivicPlus theme** with per-meeting detail
pages and a `/media/{id}` file-serving endpoint that's **hotlink-protected**
(same category of problem as Concord's Legistar, different root system). No
Cloudflare/bot-challenge on page loads themselves.

## Platform

- Main site: `https://www.kingstonnh.gov` — CivicPlus, but a different
  (newer-looking) theme/module set than the node-based CivicEngage seen in
  New Castle/Rye/Exeter and the AgendaCenter seen in Hampton Falls/
  Greenland/Newfields. No `/AgendaCenter` or `/node/{id}/agenda` routes here.
  - A `kingstonnh.org` domain also surfaces in search results (older site?)
    — not explored this session; `kingstonnh.gov` is the live, current one.
- Planning Board hub: `/planning-board` — content page (board description,
  meeting info) plus an upcoming-meetings widget; does **not** itself list
  past agendas/minutes.
- Each individual meeting gets its own detail page:
  `/planning-board/meeting/{slug}` (e.g.
  `/planning-board/meeting/planning-board-public-hearing-meeting-6`) —
  slugs aren't sequential/guessable, so meetings must be discovered via a
  listing page, not constructed directly.
- **Best listing page found: `/meetings/recent`** — a single town-wide table
  of every board's recent meetings (filterable by a "Boards, Commissions,
  Committees" dropdown, value `Planning Board`), each row showing
  date/time, meeting title, and **direct links to every Agenda/Packet/
  Minutes file** for that meeting — richer and easier to scrape than
  visiting each meeting detail page individually.
  - Also found: `/calendar?boards-commissions=736` (a calendar view scoped
    to Planning Board via a numeric board id, `736`) — not fully explored,
    `/meetings/recent` was more directly useful.

## URL structure / access gotcha

- Files are linked as `/media/{numericId}` (e.g. `/media/21201` for an
  agenda, `/media/21266` for minutes) — short, clean, but **not
  sequential/guessable per meeting**; must be scraped from a listing page.
- **⚠️ `/media/{id}` requires a same-origin browser fetch, not plain
  `requests`**: confirmed `FetchUrl` (plain Python `requests`, no browser)
  gets **`403 Forbidden`** on `https://www.kingstonnh.gov/media/21201`,
  every time.
- **Working pattern (same as Concord's Legistar `View.ashx` fix)**: use
  `playwright-cli eval` to run an in-page `fetch()` against the `/media/
  {id}` URL (relative path, so it carries the right origin/referer/cookies
  automatically), base64-encode the response body, and decode it back into
  a file with a small Python/base64 snippet. Confirmed working for both an
  agenda (`/media/21201`, 200 OK, `content-type: application/pdf`,
  714,874 bytes) and minutes (`/media/21266`, 200 OK, 583,208 bytes) in
  this session — bytes fetched and base64-encoded but not yet decoded to
  disk (that last step needs a one-off Python call outside this project's
  pre-approved command set, so it wasn't run this session).
- Larger meetings post **multiple separate "Packet" PDFs** per meeting
  (seen up to 6-8 packet files for one hearing, one running 20MB) rather
  than one combined materials PDF — plan for multi-file fetches per meeting
  if packets are wanted, not just the agenda.
- Meetings: weekly-ish "Planning Board Public Hearing / Meeting" (6:45pm,
  Kingston Town Hall Main Meeting Room), plus occasional special sessions
  (CIP Committee, Master Plan Community Forum).

## Document content

- Not yet text-analyzed this session (blocked on the decode-to-disk step
  above). Agenda file sizes (~700KB) and packet sizes (up to 20MB) suggest
  richer content than the sparser small towns (New Castle, Newfields) —
  worth a follow-up pass once the `/media/` fetch-and-decode step is
  scripted or approved.

## Open items for later

- Script (or get approval for) the base64-decode-to-file step so `/media/
  {id}` PDFs can actually land in `working/kingston_nh/` for
  `PdfKeywordScan`/`PdfExtractText` analysis.
- Check whether `/meetings/recent` paginates/limits how far back it goes,
  or if `/calendar?boards-commissions=736` is a better source for older
  meetings.
