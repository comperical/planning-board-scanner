# Greenland, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town between Portsmouth and Stratham. Platform:
standard CivicPlus Agenda Center (see PATTERNS.md) — real PDFs (not Word
docs). No bot protection.

## Platform notes

- Main site: `https://www.greenland.nh.gov`.
- ⚠️ **Two other domains surface and both still resolve**: bare
  `greenland.nh.gov` (same site) and legacy `www.greenland-nh.com` (older
  theme, e.g. `/node/96/agenda/2022` for pre-2025 archives). Use
  `www.greenland.nh.gov` as canonical; the `-nh.com` domain worth a look
  only if older agendas are needed.
- Planning Board Agenda Center: `/AgendaCenter/Planning-Board-4` — single
  page, year-filterable via in-page JS, not a separate URL per year.
- "Agendas & Minutes prior to 2025" are in a separate Document Center
  archive (`/DocumentCenter/Index/32`), not explored.
- Board meets roughly biweekly (1st & 3rd — sometimes shifted)
  Wednesday/Thursday, 6:30pm, Town Hall Conference Room.

## Document content

- **Agenda PDF** (Sept 17, 2026, 60KB, 1 page): real substance —
  `PdfKeywordScan` found 3 hits: a new Site Plan Review (143 Post Road,
  applicant City of Portsmouth) and a continued Subdivision of Land
  (Moulton Avenue, Map R9 Lot 8K-1, owner Michael Gill), plus a standing
  "Projects of Regional Impact" agenda item — good signal that
  Greenland's agendas alone carry actionable project details.
- **Minutes PDF** (Aug 20, 2026, 220KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/greenland_nh/A 09.17.26 PB.pdf` (Sept 17, 2026 agenda)
- `working/greenland_nh/_08202026-130` (Aug 20, 2026 minutes — no
  extension in the saved filename; it is a PDF)
