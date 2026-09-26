# Alton, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, "Gateway to Lake Winnipesaukee." Platform: custom
WordPress (see PATTERNS.md), not CivicPlus (despite stale `/planning-
event/...` search results). No bot protection.

## Platform notes

- Main site: `https://alton.nh.gov`. ⚠️ Search-indexed `/planning-event/
  planning-board-1` and similar URLs **404** — use the paths below instead.
- Minutes archive by year: `/documents/planning-board-minutes-{YYYY}/` — a
  flat page listing every minutes PDF for that year directly.
- Static media path: `/wp-content/uploads/{YYYY}/{MM}/{M-D-YY}-PB-
  {Approved|Draft}.pdf` — upload-date folder, not necessarily matching the
  meeting date's own year/month.

## Document content

- **Minutes PDF** (Jul 21, 2026, 290KB, 16 pages): the richest single
  document sampled in this entire project — `PdfKeywordScan` found 16 hits
  across at least 4 separate cases, each with real narrative detail (full
  meeting transcripts, not terse tables):
  - A Minor Site Plan for a Bed & Breakfast with a small antique shop,
    Joyce McGuirk Trust, 117 Hayes Road (Map 19, Lot 47), Rural Zone.
  - A Lot Line Adjustment between 208 and 238 Fort Point Road (Map 18,
    Lots 5 & 5-2), Lakeshore Residential Zone.
  - A Final Minor Subdivision, Case #P26-19, Michelle Penland (owner),
    Jesus Valley Road (Map 14, Lot 1-1) — subdividing a 50.97-acre lot
    into two lots, **approved** by board vote (motion/second/unanimous
    recorded in the minutes).
  - A separate commercial development discussion referencing drainage and
    right-of-way plans.

  Alton's minutes read like verbatim meeting transcripts (numbered lines,
  board-member names, direct quotes) — a strong candidate for full-text
  analysis rather than keyword-scan alone.

## Scan notes (2026-09-25)

- Alton posts **minutes only** - no agenda archive found (`/documents/
  planning-board-agendas-2026/` 404s; `/document-category/pb/` has only
  forms, regs and minutes-by-year categories). Newest minutes lag the
  meeting by ~4 weeks (7/21 was the latest on 9/25; 8/18 not yet up).
- On the yearly minutes page, link *text* can be wrong (the 2-17-26 file
  was labelled "7-21-26 PB Minutes Approved") - trust the filename/href.
- Files `wp-content/uploads/2026/03/{M-D-YY}-PB-Approved.pdf` - all 2026
  minutes so far sit in the `2026/03` upload folder.

## Sample files downloaded

- `working/alton_nh/7-21-26-PB-Approved.pdf`
