# Madbury, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Strafford County town near Durham. Runs the **newer CivicPlus
theme** with per-meeting detail pages and a hotlink-protected `/media/{id}`
file endpoint — same pattern as Kingston, NH (see `towninfo/kingston_nh.md`).
No Cloudflare/bot-challenge on page loads themselves.

## Platform

- Main site: `https://www.madbury.gov`.
- ⚠️ **Multiple legacy domains coexist** in search results:
  `www.madburynh.org` (`/show_pb.php` — likely an older custom PHP site)
  and `townofmadbury.com` (`/PlanningBoard.html`) — neither tested this
  session; `madbury.gov` confirmed live and current.
- Planning Board hub: `/planning-board` — lists upcoming meetings inline
  (e.g. "Planning Board, Wed, Sep 16 2026, 7-9pm") each linking to a
  per-meeting detail page.
- `/agendacenter` **404s** here — Madbury does NOT use the AgendaCenter
  module CivicPlus towns elsewhere in this project use; it's on the same
  newer per-meeting-page theme as Kingston.
- Each meeting detail page: `/planning-board/meeting/{slug}` (e.g.
  `/planning-board/meeting/planning-board-22`).

## URL structure / access gotcha

- Files are linked as `/media/{numericId}` (e.g. `/media/3281` for an
  agenda, `/media/3271` and `/media/3276` for separate "Packet" documents)
  — same shape as Kingston, and **not sequential/guessable** per meeting.
- **⚠️ `/media/{id}` requires a same-origin browser fetch, not plain
  `requests`**: confirmed `FetchUrl` (plain Python `requests`, no browser)
  gets **`403 Forbidden`** on `https://www.madbury.gov/media/1681`, every
  time.
- **Working pattern (same as Kingston/Concord)**: `playwright-cli eval`
  in-page `fetch()` against the `/media/{id}` URL, base64-encode, decode
  to disk with a one-off Python script (not run this session — same
  `TODO.txt` gap as Kingston). Confirmed working this session: `/media/
  1681` (200 OK, `application/pdf`) and `/media/3281` (200 OK, 472,559
  bytes, agenda `pb_agenda_sep_16_2026.pdf`).
- A single meeting can post **multiple separate "Packet" PDFs** (seen:
  `public_notice_16_sep_land_use-vision_mp.pdf`,
  `cottagecourt_mad_draft_ordinance_4_7.17.26.pdf`) alongside the agenda —
  the "Cottage Court" ordinance filename alone suggests an active
  cottage-court/tiny-home zoning discussion in town.
- Meetings: 1st & 3rd Wednesday monthly, 7-9pm.

## Document content

- Not yet text-analyzed this session (blocked on the decode-to-disk step,
  same as Kingston). File names alone (agenda + 2 packets, "Cottage
  Court" draft ordinance) suggest active zoning-policy work worth a
  follow-up pass once the base64-decode tooling exists.

## Open items for later

- Same as Kingston: needs the base64-decode-to-file step from `TODO.txt`
  to actually land Madbury's PDFs in `working/madbury_nh/` for analysis.
- Check whether `madburynh.org` or `townofmadbury.com` still carry live,
  different content from `madbury.gov`.
