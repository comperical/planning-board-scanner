# Atkinson, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, near MA border. Runs CivicPlus CivicEngage with
the Agenda Center module — same shape as the other Rockingham towns this
session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.town-atkinsonnh.com` — CivicPlus CivicEngage.
- Planning Board hub: `/323/Planning-Board`.
- Agenda Center: `/agendacenter` — another busy town-wide page; same
  "plain-text `find` truncates" issue as Hampstead/Plaistow — use full
  `snapshot` + `grep "Planning Board"` to locate the section.
- Meetings sometimes link a **Video** entry hosted on Vimeo showcases
  (`vimeo.com/showcase/1893967?video=...`) alongside Agenda/Minutes.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_09162026-244`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — clean filenames via Content-Disposition
  (`PB Agenda 09-16-26.pdf`, `PB Agenda 11-19-25 - Public Hearing
  Zoning.pdf`).
- Meetings: roughly monthly, Town Hall, 19 Academy Avenue.

## Document content

- **Agenda PDF** (Sept 16, 2026, 117KB): 1 keyword hit — light in this
  sample. An older sample from search results (Nov 19, 2025, "Public
  Hearing Zoning") suggests zoning-hearing agendas run richer; worth a
  follow-up sample from an active-hearing month.

## Sample files downloaded

- `working/atkinson_nh/PB Agenda 09-16-26.pdf`
- `working/atkinson_nh/PB Agenda 11-19-25 - Public Hearing Zoning.pdf`
