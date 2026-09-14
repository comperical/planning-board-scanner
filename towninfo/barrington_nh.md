# Barrington, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town. Runs node-based CivicPlus CivicEngage. No bot
protection.

## Platform

- Main site: `https://www.barrington.nh.gov` — CivicPlus CivicEngage.
- Planning Board hub: `/planning` (department page) / `/land-use-
  department/links/planning-board`.
- **Agendas index**: `https://www.barrington.nh.gov/node/34/agenda` —
  lists years; `/node/34/agenda/2026` for current-year entries.
- ⚠️ Entry URL slugs are **inconsistent** across meetings: some are short
  custom slugs at the site root (`/pbagenda20260915`,
  `/pbagenda20260811`), others follow the standard
  `/planning-board/agenda/{slug}` pattern
  (`/planning-board/agenda/2026planning-board-agenda-0`) — no single
  guessable pattern; always scrape the year-listing page.

## URL structure

- Each detail page embeds a static PDF:
  `https://www.barrington.nh.gov/sites/g/files/vyhlif2766/f/agendas/{YYYY_MMDD}_pb{_N}.pdf`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the PDF directly** — no referer/cookie gate.
- Meetings: 1st & 3rd Tuesday monthly, 6:30pm, Town Hall, 4 Signature
  Drive. Also streamed via Microsoft Teams and archived on YouTube
  (`youtube.com/BarrNHGov`) — a possible secondary source (recorded
  discussion) for towns where the agenda text alone is sparse.

## Document content

- **Agenda PDF** (Sept 15, 2026, 227KB): `PdfKeywordScan` found 0 hits.
  Confirmed via `PdfInfo` this is **not** a scanned/image PDF (2,954
  selectable text characters on 1 page, Word-generated) — genuinely an
  administrative-only agenda for this particular date, not a
  keyword-scan/OCR failure. Sample another meeting before concluding
  Barrington is generally low-signal.

## Sample files downloaded

- `working/barrington_nh/2026_0915_pb_0.pdf` (0 keyword hits — confirmed
  genuine, not a scan)
