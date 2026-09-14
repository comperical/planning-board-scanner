# Brentwood, NH — Planning Board Web Access

Investigated: 2026-09-14

Brentwood is the **first town in this project on the "Municipal One"
platform** (`municipalone.com` — see footer credit), not CivicPlus. It
combines two access problems seen separately in earlier towns: **hotlink
protection** (like Concord/Kingston) *and* **Word-doc output** (like
Hampton Falls) — both at once, on every file. No Cloudflare/bot-challenge
on page loads themselves.

## Platform

- Main site: `https://www.brentwoodnh.gov` — Municipal One (a smaller NH-
  focused municipal CMS vendor, distinct from CivicPlus).
- Planning Board hub: `/pview.aspx?id=594&catid=961` (or `&catid=0`, both
  work) — content page with board description/members plus a short
  "Agendas & Minutes" preview list (last 3 meetings) in a sidebar widget.
- **Full listing page**: `/agenda.aspx` → category links per board (e.g.
  "Planning Board" → `/agendalist.aspx?categoryid=12514`) — this is the
  best page to scrape: every meeting's Agenda/Minutes/Packet/Video links in
  one place, going back through the year.
- Individual meeting detail pages also exist:
  `/agendaview.aspx?aid={id}` (id matches the doc id) — not needed if
  scraping `/agendalist.aspx?categoryid=12514` directly.

## URL structure / access gotcha

- Each meeting has separate doc-type links, all sharing the meeting's
  numeric id: `/docview.aspx?doctype={agendaDoc|minuteDoc|packetDoc}&docid=
  {id}` — e.g. `/docview.aspx?doctype=agendaDoc&docid=14856`,
  `/docview.aspx?doctype=minuteDoc&docid=14847`. A `packetDoc` variant
  exists too (seen on the Feb 19, 2026 entry) but isn't posted for every
  meeting.
- **⚠️ `/docview.aspx` requires a same-origin browser fetch, not plain
  `requests`**: confirmed `FetchUrl` (plain Python `requests`, no browser)
  gets **`403 Forbidden`**, every time. Same category of problem as
  Concord's Legistar and Kingston's `/media/{id}` — use the
  `playwright-cli eval` in-page `fetch()` + base64-encode pattern instead
  (confirmed working: 200 OK on both an agenda and minutes doc this
  session, bytes fetched but not yet decoded to disk — see repo
  `TODO.txt`).
- **⚠️ Files served here are Word documents (`.docx`), not PDFs** — same
  situation as Hampton Falls. Confirmed content-type
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  on both the agenda (13,923 bytes) and minutes (24,492 bytes) sampled.
  This project's PDF tool chain can't process these directly.
- Meetings: 1st & 3rd Thursday monthly, 7pm, Town Office, plus occasional
  "Site Walk" and "Work Session" extras.

## Document content

- Not yet analyzed (blocked on both the hotlink-fetch and docx-extraction
  gaps — see `TODO.txt`). File sizes (agenda ~14-100KB range seen across
  different meetings, minutes ~24KB+) suggest normal small-town agenda/
  minutes content once those tools exist.

## Open items for later

- Same two `TODO.txt` items apply here simultaneously: (1) base64-decode-
  to-file for hotlink-protected `/docview.aspx`, and (2) `.docx` text
  extraction. Brentwood is a good test case once both are built, since it
  needs both at once.
