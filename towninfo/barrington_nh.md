# Barrington, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town. Platform: node-based CivicPlus (see PATTERNS.md).
No bot protection.

## Platform notes

- Main site: `https://www.barrington.nh.gov`. Planning Board hub:
  `/planning` / `/land-use-department/links/planning-board`.
- Agendas index: `/node/34/agenda`, `/node/34/agenda/2026` for current
  year.
- ⚠️ Entry URL slugs are **inconsistent** across meetings: some are short
  custom slugs at site root (`/pbagenda20260915`), others follow
  `/planning-board/agenda/{slug}` — no single guessable pattern, always
  scrape the year-listing page.
- Meetings: 1st & 3rd Tuesday monthly, 6:30pm. Also streamed via Teams,
  archived on YouTube (`youtube.com/BarrNHGov`) — possible secondary
  source for sparse-agenda towns.

## Document content

- **Agenda PDF** (Sept 15, 2026, 227KB): `PdfKeywordScan` found 0 hits.
  Confirmed via `PdfInfo` this is **not** a scanned/image PDF (2,954
  selectable text chars, Word-generated) — genuinely administrative-only
  for this date. Sample another meeting before concluding low-signal.

## Sample files downloaded

- `working/barrington_nh/2026_0915_pb_0.pdf` (0 keyword hits — confirmed
  genuine, not a scan)
