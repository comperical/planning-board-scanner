# Greenland, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town between Portsmouth and Stratham. Runs CivicPlus
CivicEngage with the **Agenda Center** module, same pattern as Hampton
Falls, but here documents are plain PDFs (not Word docs). No bot protection
encountered.

## Platform

- Main site: `https://www.greenland.nh.gov` — CivicPlus CivicEngage.
- ⚠️ **Two other domains surface in search results and both still resolve**:
  `https://greenland.nh.gov` (bare, no `www`, same site) and a legacy
  `https://www.greenland-nh.com` (older CivicPlus theme, e.g.
  `/node/96/agenda/2022` for pre-2025 archives). Use `www.greenland.nh.gov`
  as canonical; the `-nh.com` domain is worth a look only if older agendas
  are needed and the "Document Center" link (below) doesn't cover them.
- Planning Board Agenda Center: `/AgendaCenter/Planning-Board-4` — single
  page, year-filterable via an in-page JS control (`changeYear(2025, 4,
  'a1')`), not a separate URL per year.
- Page note: "Agendas & Minutes prior to 2025 can be found in
  [Document Center](https://www.greenland.nh.gov/DocumentCenter/Index/32)"
  — a separate archive module for older records, not yet explored.

## URL structure

- Same shape as Hampton Falls: each row links to
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`
  (e.g. `/AgendaCenter/ViewFile/Agenda/_09172026-135`,
  `/AgendaCenter/ViewFile/Minutes/_08202026-130`).
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — `Content-Disposition` gives a sane
  filename for agendas (e.g. `A 09.17.26 PB.pdf`) but not always for minutes
  (fell back to the URL's bare `_{date}-{id}` with no extension in one
  sample — same quirk as Hampton Falls, rename/inspect before trusting the
  file type).
- Board meets roughly biweekly (1st & 3rd — sometimes shifted) Wednesday/
  Thursday, 6:30pm, Town Hall Conference Room.

## Document content

- **Agenda PDF** (Sept 17, 2026, 60KB, 1 page): real substance —
  `PdfKeywordScan` found 3 hits: a new Site Plan Review (143 Post Road,
  applicant City of Portsmouth) and a continued Subdivision of Land
  (Moulton Avenue, Map R9 Lot 8K-1, owner Michael Gill), plus a standing
  "Projects of Regional Impact" agenda item — good signal that Greenland's
  agendas alone (without needing a fuller "materials" packet) carry
  actionable project details: address, applicant/owner, map/lot.
- **Minutes PDF** (Aug 20, 2026, 220KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/greenland_nh/A 09.17.26 PB.pdf` (Sept 17, 2026 agenda)
- `working/greenland_nh/_08202026-130` (Aug 20, 2026 minutes — no
  extension in the saved filename; it is a PDF)
