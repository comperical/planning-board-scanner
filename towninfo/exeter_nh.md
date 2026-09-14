# Exeter, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: Drupal ("municodeWEB" design, footer credit "ahaconsulting.com"
— see PATTERNS.md). No bot protection.

## Platform notes

- Site: `https://www.exeternh.gov`.
- Per-board static pages (`bcc/planning-board`, etc.) are really just a
  single meeting node, not useful as an archive entry point.
- **The real archive is the town-wide `/meetings` page** — one master
  table of every board/committee's meetings, each row showing Date,
  Meeting, and (when available) direct Agenda/Minutes/Packets/Video
  links, plus "View Details". Has server-side filter controls (didn't
  resolve the exact query-string param this session) — paging through the
  unfiltered list (`?page=1`, `?page=2`, …) and scanning for "Planning
  Board" works fine given the board's near-weekly density.
- Video links point to YouTube (Exeter TV channel).
- Static file paths:
  `sites/default/files/fileattachments/planning_board/meeting/{node_id}/{filename}`
  (packets under a `.../packets/{node_id}/{filename}` sub-path). `{node_id}`
  is opaque, not derivable from the date — get it from `/meetings` or a
  per-meeting node page. Filenames are inconsistent, no fixed convention.
- Planning Board's **Technical Review Committee (TRC)** and **Master Plan
  Oversight Committee** sub-meetings are filed under the same
  `planning_board` folder — worth including when scanning.
- Draft minutes sometimes posted as `.docx` rather than PDF (not tested
  with the PDF tools).

## Document content

- **Agenda PDF** ("Legal Notice"/"Revised Agenda" style): richer than a
  bare-bones agenda — full paragraph per case (applicant, tax
  map/parcel, zoning district, real description). Sample (Aug 27, 2026):
  - Site plan review for demolition of a dry-cleaner + new 4-story,
    22-room hotel (Map 65-125, PB Case #26-3).
  - Minor site plan review for 3 new duplexes (faculty housing, Phillips
    Exeter Academy) + a voluntary lot merger (PB Case #26-7).
  - Lot line adjustment + minor subdivision + site plan review for
    redevelopment into 8 residential condo units at 5 Brentwood Drive,
    with new roadway/utilities (PB Case #26-11).
- **Packet PDF** ("Mtg Packet"): large bundled submission set. Sample was
  143 pages / 43 MB, Word-generated (searchable text throughout — only 6
  of 143 pages lack selectable text, presumably scanned site-plan
  drawings). `PdfKeywordScan` returned **120 hits** — a rich,
  text-extractable source, not a scanned image dump. Worth pulling
  routinely when available.

## Sample downloads (in `working/exeter_nh/`)

- `pb-leg.08-27-26_legal_notice.pdf` — Aug 27, 2026 agenda
- `pb-08-27-26_pb_mtg_packet.pdf` — corresponding 143-page packet

## Open questions / not yet checked

- The exact filter query-string parameter for
  `Boards and Commissions=Planning Board` on `/meetings`.
- Whether minutes PDFs (vs. draft `.docx` minutes) are consistently
  available for older meetings, and their URL pattern.
- Earliest date covered by `/meetings` (year dropdown goes back to 1976).
- Whether `.doc`/`.docx` agenda/minutes files need separate handling.
