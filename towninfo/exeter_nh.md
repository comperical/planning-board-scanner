# Exeter, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://www.exeternh.gov` — a **municodeWEB** design (footer credit: "a municodeWEB design | ahaconsulting.com"), running on Drupal (node-based URLs, `/user/login`, `/print/{nid}`).
- No Cloudflare or other bot-challenge encountered — loaded cleanly, no headed-vs-headless distinction needed.

## Finding the archive

- Per-board static pages exist (`bcc/planning-board`, `bcc/planning-board-agenda`, `bcc-pb/planning-board-minutes`) but each of these is really just a **single meeting node** (e.g. the minutes page returned a Sept 2012 minutes doc, not a list) — not useful as an archive entry point on its own.
- The real archive is the **town-wide `/meetings` page**: `https://www.exeternh.gov/meetings`. It's one master table of *every* board/committee's meetings, each row showing Date, Meeting, and (when available) direct **Agenda / Minutes / Packets / Video** links, plus a "View Details" link to that meeting's own node page.
- The table has server-side filter controls (From/To date range, Department, **Boards and Commissions** dropdown with a "Planning Board" option) submitted via a normal form — but I did not resolve the exact query-string parameter (native `<select>` didn't cooperate with the CLI's `select` command in the time available). Not required in practice: paging through the unfiltered `/meetings` list (`?page=1`, `?page=2`, …) and scanning for "Planning Board" rows works fine, and the board's row density is high enough (roughly weekly) that a few pages cover a couple months.
- Video links, when present, point to YouTube (Exeter TV channel).

## URL structure — static and guessable-ish

All documents are plain static files, no session/cookie needed:

```
https://www.exeternh.gov/sites/default/files/fileattachments/planning_board/meeting/{node_id}/{filename}
https://www.exeternh.gov/sites/default/files/fileattachments/planning_board/meeting/packets/{node_id}/{filename}
```

- `{node_id}` is an opaque internal id (e.g. `63845`), not derivable from the date — you need the `/meetings` listing (or a per-meeting node page) to learn it. Once known, the PDF URL is permanent and `curl`/`FetchUrl`-able directly.
- The Planning Board's **Technical Review Committee (TRC)** and **Master Plan Oversight Committee** sub-meetings are filed under this same `planning_board` folder — worth including when scanning for that board's activity.
- Filenames are inconsistent (`pb-leg.08-27-26_legal_notice.pdf`, `09-10-26_pbb_mtg_packet.pdf`, sometimes `.doc`/`.docx` instead of `.pdf` for agendas or draft minutes) — no fixed naming convention to exploit, always read the link text/href from the listing.

## Document content

- **Agenda PDF** ("Legal Notice" / "Revised Agenda" style): richer than a bare-bones agenda — each case gets a full paragraph with applicant name, tax map/parcel, zoning district, and a real description of the proposal. Sample (Aug 27, 2026 meeting) included:
  - Site plan review for demolition of a dry-cleaner + new 4-story, 22-room hotel (Map 65-125, PB Case #26-3)
  - Minor site plan review for 3 new duplexes (faculty housing, Phillips Exeter Academy) + a voluntary lot merger (Tax Maps 83-01/72-99, PB Case #26-7)
  - Lot line adjustment + minor subdivision + site plan review for redevelopment into 8 residential condo units at 5 Brentwood Drive, with new roadway/utilities (Map 62 Parcel 111, PB Case #26-11)
  - This alone is enough to identify development projects worth surfacing — no packet needed just to find leads.
- **Packet PDF** ("Mtg Packet"): large bundled submission set. Sample was **143 pages / 43 MB**, Word-generated (searchable text throughout — only 6 of 143 pages lack selectable text, presumably scanned site-plan drawings). A keyword scan (`PdfKeywordScan`) returned **120 hits** across site-plan/subdivision/residential/commercial terms — this is a rich, text-extractable source, not a scanned image dump like some other towns' packets. Worth pulling routinely when available.
- Draft minutes are sometimes posted as `.docx` rather than PDF (not yet tested with the PDF tools — would need conversion or a text-extraction path for that format).

## Sample downloads (in `working/exeter_nh/`)

- `pb-leg.08-27-26_legal_notice.pdf` — Aug 27, 2026 agenda (3 active site plan/subdivision cases, see above)
- `pb-08-27-26_pb_mtg_packet.pdf` — corresponding 143-page meeting packet

## Comparison to Rochester / Dover, NH

| | Rochester, NH | Dover, NH | Exeter, NH |
|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom site + Treeno DMS | Drupal (municodeWEB) |
| Bot protection | Cloudflare hard-blocks headless | None | None |
| PDF URLs | Stable, static, guessable from listing HTML | Session-scoped temp URLs | Static, permanent, but node-id not guessable — needs the `/meetings` listing to discover |
| Supporting materials | Not bundled | Bundled "Agenda Materials" PDF per meeting | Bundled "Packet" PDF per meeting, mostly text-extractable |
| Archive scope | Per-board node listing | One shared cabinet for all bodies | One shared `/meetings` table for all boards/committees, filterable |

## Open questions / not yet checked

- The exact filter query-string parameter for `Boards and Commissions=Planning Board` on `/meetings` (would let a fetch target Planning Board rows directly instead of paging through the full town-wide list).
- Whether minutes PDFs (vs. draft `.docx` minutes) are consistently available for older meetings, and their URL pattern.
- Earliest date covered by the `/meetings` archive (year dropdown on the filter form goes back to 1976, suggesting a long — possibly sparsely populated — history).
- Whether `.doc`/`.docx` agenda/minutes files need separate handling from the PDF-focused tool chain here.
