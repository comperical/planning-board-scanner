# Atkinson, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, near MA border. Platform: standard CivicPlus
Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.town-atkinsonnh.com`. Planning Board hub:
  `/323/Planning-Board`.
- Agenda Center is a busy town-wide page — same "plain-text `find`
  truncates" issue as Hampstead/Plaistow, use full `snapshot` + `grep`.
- Meetings sometimes link a **Video** entry on Vimeo showcases
  (`vimeo.com/showcase/1893967?video=...`) alongside Agenda/Minutes.
- Meetings: roughly monthly, Town Hall, 19 Academy Avenue.

## Document content

- **Agenda PDF** (Sept 16, 2026, 117KB): 1 keyword hit — light in this
  sample. An older sample from search results (Nov 19, 2025, "Public
  Hearing Zoning") suggests zoning-hearing agendas run richer; worth a
  follow-up sample from an active-hearing month.

## Sample files downloaded

- `working/atkinson_nh/PB Agenda 09-16-26.pdf`
- `working/atkinson_nh/PB Agenda 11-19-25 - Public Hearing Zoning.pdf`
