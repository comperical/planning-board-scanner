# Kingston, NH — Planning Board Web Access

> **Update 2026-09-21: download blocker resolved.** The site serves a Cloudflare challenge to every non-browser request (not a hotlink/Referer check). Download via a native `<a download>` click in the headed `planscan` session, then `plan_entry.py ClaimDownload` - see PATTERNS.md "Browser-only downloads". Base64 references below are historical. Confirmed: `/media/21201` = 2026-09-15 PB agenda (714,874 bytes), now at `working/kingston_nh/2026.09.15_PB_Agenda.pdf` (not yet ingested).

Investigated: 2026-09-14

Kingston runs a **newer CivicPlus theme** with per-meeting detail pages
and a hotlink-protected `/media/{id}` endpoint — see PATTERNS.md
("newer per-meeting-page theme" and "Hotlink protection" gotcha). No
Cloudflare/bot-challenge on page loads themselves. **Not yet
content-analyzed — blocked on the decode-to-disk step.**

## Platform notes

- Main site: `https://www.kingstonnh.gov`. No `/AgendaCenter` or
  `/node/{id}/agenda` routes here. A `kingstonnh.org` domain also
  surfaces in search results (older site?), not explored — `.gov` is the
  live, current one.
- Planning Board hub `/planning-board` does **not** itself list past
  agendas/minutes.
- Each meeting gets its own detail page: `/planning-board/meeting/{slug}`
  — slugs aren't sequential/guessable, must be discovered via a listing
  page.
- **Best listing page: `/meetings/recent`** — a single town-wide table of
  every board's recent meetings (filterable by board), each row showing
  direct links to every Agenda/Packet/Minutes file for that meeting —
  richer and easier to scrape than visiting each meeting detail page
  individually. Also `/calendar?boards-commissions=736` (a calendar view
  scoped to Planning Board via board id `736`), not fully explored.
- Files linked as `/media/{numericId}` — short but not sequential/
  guessable per meeting; must be scraped from a listing page.
- **Confirmed working** (per PATTERNS.md hotlink pattern): in-page
  `fetch()` against `/media/{id}` — agenda (`/media/21201`, 200 OK,
  `application/pdf`, 714,874 bytes) and minutes (`/media/21266`, 200 OK,
  583,208 bytes) both fetched and base64-encoded but not yet decoded to
  disk (blocked on the standing `TODO.txt` gap).
- Larger meetings post **multiple separate "Packet" PDFs** per meeting
  (seen up to 6-8 files for one hearing, one running 20MB) rather than
  one combined materials PDF — plan for multi-file fetches per meeting.
- Meetings: weekly-ish "Planning Board Public Hearing / Meeting" (6:45pm,
  Kingston Town Hall Main Meeting Room), plus occasional special sessions
  (CIP Committee, Master Plan Community Forum).

## Document content

- Not yet text-analyzed. Agenda file sizes (~700KB) and packet sizes (up
  to 20MB) suggest richer content than the sparser small towns (New
  Castle, Newfields) — worth a follow-up pass once the `/media/`
  fetch-and-decode step is scripted or approved.

## Open items for later

- Script (or get approval for) the base64-decode-to-file step so
  `/media/{id}` PDFs can actually land in `working/kingston_nh/`.
- Check whether `/meetings/recent` paginates/limits how far back it goes,
  or if `/calendar?boards-commissions=736` is a better source for older
  meetings.
