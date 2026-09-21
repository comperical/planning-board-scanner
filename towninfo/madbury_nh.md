# Madbury, NH — Planning Board Web Access

> **Update 2026-09-21: download blocker resolved.** The site serves a Cloudflare challenge to every non-browser request (not a hotlink/Referer check). Download via a native `<a download>` click in the headed `planscan` session, then `plan_entry.py ClaimDownload` - see PATTERNS.md "Browser-only downloads". Base64 references below are historical. Note: `/media/1681` is actually a 2019-11-20 file, not the Sep 16 agenda as recorded below - re-identify current media IDs from the meeting pages.

Investigated: 2026-09-14

Small Strafford County town near Durham. Runs the newer CivicPlus theme
with a hotlink-protected `/media/{id}` endpoint — same pattern as
Kingston (see PATTERNS.md). No Cloudflare/bot-challenge on page loads
themselves. **Not yet content-analyzed — blocked on the decode-to-disk
step.**

## Platform notes

- Main site: `https://www.madbury.gov`.
- ⚠️ Multiple legacy domains coexist in search results: `madburynh.org`
  (`/show_pb.php`, likely an older custom PHP site) and
  `townofmadbury.com` (`/PlanningBoard.html`) — neither tested;
  `madbury.gov` confirmed live and current.
- Planning Board hub: `/planning-board` — lists upcoming meetings inline,
  each linking to a per-meeting detail page. `/agendacenter` **404s**
  here — Madbury does NOT use the AgendaCenter module.
- Each meeting detail page: `/planning-board/meeting/{slug}`.
- Files linked as `/media/{numericId}` — not sequential/guessable.
- **Confirmed** (per PATTERNS.md hotlink pattern): in-page `fetch()`
  against `/media/{id}` — `/media/1681` and `/media/3281` both 200 OK
  (472,559 bytes, `pb_agenda_sep_16_2026.pdf`), bytes fetched but decode
  step not run this session (same standing `TODO.txt` gap as Kingston).
- A single meeting can post **multiple separate "Packet" PDFs** (seen:
  `public_notice_16_sep_land_use-vision_mp.pdf`,
  `cottagecourt_mad_draft_ordinance_4_7.17.26.pdf`) alongside the agenda
  — the "Cottage Court" ordinance filename alone suggests an active
  cottage-court/tiny-home zoning discussion in town.
- Meetings: 1st & 3rd Wednesday monthly, 7-9pm.

## Document content

- Not yet text-analyzed. File names alone (agenda + 2 packets, "Cottage
  Court" draft ordinance) suggest active zoning-policy work worth a
  follow-up pass once the base64-decode tooling exists.

## Open items for later

- Needs the base64-decode-to-file step (see PATTERNS.md TODOs) to
  actually land Madbury's PDFs in `working/madbury_nh/` for analysis.
- Check whether `madburynh.org` or `townofmadbury.com` still carry live,
  different content from `madbury.gov`.
