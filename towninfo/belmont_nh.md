# Belmont, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, south of Laconia/Gilford. Platform: custom WordPress
(see PATTERNS.md), not CivicPlus. No bot protection.

## Platform notes

- Main site: `https://belmontnh.gov`. ⚠️ Not the same as `belmont.gov`
  (Belmont, MA — a different town), don't confuse domains.
- Each meeting gets its own page: `/meetings/{YYYY-MM-DD}-planning-board-
  meeting/`, embedding direct download links for Agenda and (once posted)
  Minutes. Also a calendar/events version at `/events/planning-board-
  meeting-{date}/` (not cross-checked for content parity).
- Static media path: `/wp-content/uploads/sites/38/{YYYY}/{MM}/
  {YYMMDD}PBAgenda.pdf` (agenda) / `.../{YYMMDD}-PB-MInutes.pdf` [sic,
  typo preserved] (minutes) — `sites/38/` is a WordPress multisite id,
  constant across Belmont's pages.
- Live meetings streamed at `youtube.com/@belmontlive`; Zoom links posted
  per-meeting at the bottom of each agenda.

## Scan notes (2026-09-25)

- ⚠️ `/meetings/` (no date) 404s and `/boards/archives/` and
  `/boards/planning-board/` only show the *upcoming* meeting (no past-
  meeting list without JS). Reliable route: open the per-meeting page
  directly, `/meetings/{YYYY-MM-DD}-planning-board-meeting/`, and `eval`
  its `a[href*=".pdf"]` links. PB meets the 4th Monday (9/28, 8/24, 7/27,
  6/22, ...) - guess the date and check.
- ⚠️ The slug date can differ from the meeting date: the `2026-08-24` page
  is titled "2026-08-31" (rescheduled) and carries `260824PBAgenda.pdf`
  plus `260831-PB-Minutes.pdf`. Upload folders (`2026/05`, `2026/06`) do
  not track the meeting month either - read hrefs from the page.
- Each meeting page has agenda + (later) minutes; minutes are 5-16 pages.

## Document content

- **Agenda PDF** (Feb 23, 2026, 159KB): real content — `PdfKeywordScan`
  found 3 hits: a Site Plan Review application by the Susan
  Condodemetraky Revocable Trust to expand an existing contractor's yard
  to include towing and temporary vehicle storage; and a Boundary Line
  Adjustment between the Paroma Condominium Association and Mallard's
  Landing Association, transferring a small parcel between the two.

## Sample files downloaded

- `working/belmont_nh/260223PBAgenda.pdf`
- `working/belmont_nh/PLANNING-BOARD-PBAgenda-2025-05-19.pdf` (older
  sample, used to first confirm platform access)
