# Fremont, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Runs CivicPlus CivicEngage with the Agenda
Center module — same shape as Newfields/East Kingston/Kensington — plain
PDFs, no bot protection.

## Platform

- Main site: `https://www.fremont.nh.gov` — CivicPlus CivicEngage.
- ⚠️ Search-indexed node URLs (`/planning-board`, `/node/762/agenda`) are
  **stale/404** — same pattern seen in East Kingston. Current Planning
  Board hub is `/1559/Planning-Board`, found via top nav → "Boards &
  Committees" → `/1497/Boards-Committees` listing page.
- Agenda Center: `https://www.fremont.nh.gov/AgendaCenter` — Planning
  Board section loads **collapsed** and needs a click to expand (same as
  Newfields): `getByRole('button', { name: '► Planning Board' }).click()`.
- Fremont's Agenda Center lists **multiple related boards** in one place —
  in this sample, a "Community Facilities Subcommittee" also posts under a
  similar naming/date scheme, so don't assume every row under "Planning
  Board" is the main board's regular meeting; check the title text.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_08192026-227`,
  `/AgendaCenter/ViewFile/Minutes/_07272026-223`. Some agenda links append
  `?html=true` (inline preview variant, same as Newfields) — safe to strip.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs. Filenames vary in quality: one agenda
  came through with a full descriptive name (`PB 20260819_Agenda.pdf`),
  another with just the date (`09162026.pdf`), and minutes fell back to
  the bare `_{date}-{id}` with no extension (the recurring AgendaCenter
  quirk — it is a PDF).
- ⚠️ Watch file size before assuming an agenda is empty/boilerplate: one
  sample (Sept 16, 2026) was only 1,802 bytes — likely a stub/placeholder
  or cancelled-meeting notice, not representative. The substantive sample
  used below (Aug 19, 2026) was 175KB.
- Meetings roughly biweekly/monthly, evenings, Town Hall.

## Document content

- **Agenda PDF** (Aug 19, 2026, 175KB): real project detail —
  `PdfKeywordScan` found 2 hits: a Major Site Plan Review for "Flor de
  Café" (Map 2 Lot 151-2-5, applicant Ceiba Tree...) and a Lot Merger and
  Subdivision case for Montana Realty Trust (Map 2 Lots 141 and 141-1,
  continued to Sept 2, 2026).
- **Minutes PDF** (Jul 27, 2026, "Community Facilities Subcommittee
  Meeting," 47KB): 0 keyword hits — confirms this subcommittee's minutes
  aren't a useful source for development-project signal; prefer the main
  "Planning Board Meeting" rows instead.

## Sample files downloaded

- `working/fremont_nh/PB 20260819_Agenda.pdf` (Aug 19, 2026 agenda — the
  useful sample)
- `working/fremont_nh/09162026.pdf` (Sept 16, 2026 agenda — tiny/stub, not
  representative)
- `working/fremont_nh/_07272026-223` (Jul 27, 2026 subcommittee minutes —
  no extension, is a PDF, 0 keyword hits)
