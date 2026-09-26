# Pelham, NH — Planning Board Web Access

Investigated: 2026-09-14. Access resolved: 2026-09-15 (scan_log #1).

Hillsborough County town on the MA border, southeast of Nashua. Main site
runs CivicPlus (mixed classic `.aspx` + newer CivicEngage pages), but
**Planning Board agendas/minutes are NOT served by CivicPlus's own Agenda
Center** — they're a **CivicClerk** portal (`pelhamnh.portal.civicclerk.com`)
embedded on a CivicPlus page. No bot protection encountered.

## Platform notes — working access path

- Go to `https://www.pelhamweb.com/866/Planning-Board-Agendas-and-Minutes`
  (via Planning Board hub `/165/Planning-Board`). The page embeds a
  CivicClerk widget: a small navigation calendar plus a scrollable
  "Events by date" list (Past Events / Coming Up), pre-filtered to the
  Planning Board category.
- Each event row has a "Download Files from this Event" icon button
  (`id="downloadFilesMenu-{eventId}"`). Clicking it opens a dropdown menu
  with whichever of these are available for that meeting: **Agenda
  (PDF)**, **Agenda (Plain Text)**, **Minutes (PDF)**, **Minutes (Plain
  Text)**.
- Clicking a PDF menu item triggers a **direct browser download** (no
  intermediate navigable URL, no static/guessable link pattern) —
  `playwright-cli` saves it straight to `.playwright-cli/<name>.pdf`
  automatically (no in-page-fetch/base64 workaround needed, unlike the
  hotlink-blocked towns in TODO.txt). Move the file into `working/pelham_nh/`
  and `IngestPdfTool` it from there.
- Sample docs downloaded: `9_10_26 Planning Board Agenda.pdf` (1 pg,
  9/10/2026 meeting) and `07.20.2026 PB Minutes Approved.pdf` (6 pg,
  7/20/2026 meeting).

## Dead ends (from initial recon — do not retry)

- `/agendacenter` (CivicPlus's own Agenda Center): loads, but only shows a
  search form with a single "All Categories" checkbox — searching with no
  date range returns "No results found in All categories", and this isn't
  actually where Planning Board files live anyway (see above).
- Node-based URL guesses `/node/3851/agenda/2026`, `/node/4536/agenda`,
  and `/129` all 404 or dead-end.
- `/223/Meetings` lists only the meeting **schedule** (1st & 3rd Mondays),
  not individual agendas/minutes.

## Working recipe (confirmed 2026-09-25)

The widget renders a few seconds after load - `find`/`eval` return nothing
until it does (re-run, or take one `snapshot`). Then:

1. `playwright-cli -s=planscan eval "Array.from(document.querySelectorAll('[id^=downloadFilesMenu-]')).filter(b=>!/-menu/.test(b.id)).map(b=>b.id+' | '+b.closest('li').innerText.replace(/\s+/g,' ').slice(0,60)).join('\n')"`
   lists one `downloadFilesMenu-{eventId}` button per event, with its date.
   Menus with 2 items = agenda only (PDF/Text); 4 items = agenda + minutes.
2. `click "#downloadFilesMenu-{id}"`, then
   `click "getByRole('menuitem', { name: 'Agenda (PDF)' })"` (or
   `'Minutes (PDF)'`). The PDF lands in `working/playwright_output/`.
3. ⚠️ The menu **stays open** after a download and its backdrop blocks the
   next click (5s timeout) - `press Escape` before opening another event.
4. `ClaimDownload file=working/playwright_output/<f> dest=working/pelham_nh
   name=<new>.pdf`, then `IngestPdfTool` (use the /866/ page as source_url).
- Refs from `snapshot` go stale after every click; the id locators don't.
- Cancelled meetings still list a file ("CANCELED Planning Board Agenda
  8_17_26.pdf") - skip those.

## Open items for later

- No stable per-event URL was found (download is a JS click-through, not a
  navigable link) — every future scan of this town needs the same
  browser click-through via `/866/Planning-Board-Agendas-and-Minutes`,
  there's no `FetchUrl`-only shortcut.
