# Brentwood, NH — Planning Board Web Access

> **Update 2026-09-21: download blocker resolved.** The site serves a Cloudflare challenge to every non-browser request (not a hotlink/Referer check). Download via a native `<a download>` click in the headed `planscan` session, then `plan_entry.py ClaimDownload` - see PATTERNS.md "Browser-only downloads". Base64 references below are historical. Confirmed: `docview.aspx?doctype=agendaDoc&docid=14865` = 2026-09-17 PB agenda (.docx), now at `working/brentwood_nh/2026.09.17_PB_Agenda.docx` (not yet ingested).

Investigated: 2026-09-14

Brentwood is the **only town in this project on the "Municipal One"
platform** (`municipalone.com`) — see PATTERNS.md. It combines two access
problems seen separately elsewhere: **hotlink protection** and
**Word-doc output**, both at once, on every file. No Cloudflare/bot-
challenge on page loads themselves.

## Platform notes

- Main site: `https://www.brentwoodnh.gov`.
- Planning Board hub: `/pview.aspx?id=594&catid=961` (or `&catid=0`).
- **Best scrape page**: `/agendalist.aspx?categoryid=12514` — every
  meeting's Agenda/Minutes/Packet/Video links in one place, back through
  the year. (Reached via `/agenda.aspx` → category links per board.)
- Individual meeting detail pages also exist: `/agendaview.aspx?aid={id}`
  — not needed if scraping the categoryid page directly.
- Each meeting's doc links share one numeric id:
  `/docview.aspx?doctype={agendaDoc|minuteDoc|packetDoc}&docid={id}`. A
  `packetDoc` variant exists but isn't posted every meeting.
- **⚠️ `/docview.aspx` requires a same-origin browser fetch** — plain
  `requests` gets `403 Forbidden` every time (same category as Concord's
  Legistar / Kingston's `/media/{id}`; see PATTERNS.md hotlink gotcha).
  Confirmed working via in-page `fetch()` + base64-encode (200 OK on both
  an agenda and minutes doc), bytes fetched but not yet decoded to disk.
- **⚠️ Files served are Word documents (`.docx`), not PDFs** — same
  situation as Hampton Falls. Confirmed content-type
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  on both the agenda (13,923 bytes) and minutes (24,492 bytes) sampled.
- Meetings: 1st & 3rd Thursday monthly, 7pm, Town Office, plus occasional
  "Site Walk" and "Work Session" extras.

## Document content

- Not yet analyzed (blocked on both the hotlink-fetch and docx-extraction
  gaps — see PATTERNS.md TODOs). File sizes (agenda ~14-100KB across
  different meetings, minutes ~24KB+) suggest normal small-town content
  once those tools exist.

## Open items for later

- Both `TODO.txt` items apply here simultaneously: base64-decode-to-file,
  and `.docx` text extraction. Brentwood is a good test case once both
  are built, since it needs both at once.
