# Fremont, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Platform: standard CivicPlus Agenda Center
(see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.fremont.nh.gov`.
- ⚠️ Search-indexed node URLs (`/planning-board`, `/node/762/agenda`) are
  stale/404. Current Planning Board hub is `/1559/Planning-Board`, found
  via top nav → "Boards & Committees" → `/1497/Boards-Committees`.
- Agenda Center section loads **collapsed**, needs a click to expand
  (same as Newfields) — or skip that with the direct URL
  `/AgendaCenter/Planning-Board-3` (confirmed 2026-09-22).
- ⚠️ **Agendas get replaced in place under the same ViewFile id**: the
  Sept 16, 2026 agenda (`_09162026-255`) was a 1.8KB PDF stub on 9/14 and
  a full 44KB **`.docx`** by 9/22. Re-fetch any stub-sized agenda on the
  next pass; also expect mixed PDF/.docx formats.
- Also posts "Capital Improvement Program (CIP)" committee agendas in the
  same section — skip alongside the Community Facilities Subcommittee.
- Lists **multiple related boards** in one place — a "Community
  Facilities Subcommittee" also posts under a similar naming/date scheme,
  so don't assume every row under "Planning Board" is the main board's
  regular meeting; check the title text.
- ⚠️ Watch file size before assuming an agenda is empty/boilerplate: one
  sample was only 1,802 bytes — likely a stub/placeholder or
  cancelled-meeting notice.
- Meetings roughly biweekly/monthly, evenings, Town Hall.

## Document content

- **Agenda PDF** (Aug 19, 2026, 175KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Major Site Plan Review for "Flor de
  Café" (Map 2 Lot 151-2-5, applicant Ceiba Tree...) and a Lot Merger and
  Subdivision case for Montana Realty Trust (Map 2 Lots 141 and 141-1,
  continued to Sept 2, 2026).
- **Minutes PDF** (Jul 27, 2026, "Community Facilities Subcommittee
  Meeting," 47KB): 0 keyword hits — confirms this subcommittee's minutes
  aren't a useful source; prefer the main "Planning Board Meeting" rows.

## Sample files downloaded

- `working/fremont_nh/PB 20260819_Agenda.pdf` (Aug 19, 2026 — the useful
  sample)
- `working/fremont_nh/09162026.pdf` (Sept 16, 2026 — tiny/stub, not
  representative)
- `working/fremont_nh/_07272026-223` (Jul 27, 2026 subcommittee minutes —
  no extension, is a PDF, 0 keyword hits)
