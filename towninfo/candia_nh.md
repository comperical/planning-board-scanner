# Candia, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town. Runs CivicPlus CivicEngage with the Agenda Center
module — same shape as the other Rockingham towns this session — plain
PDFs, no bot protection.

## Platform

- Main site: `https://www.candianh.org` — CivicPlus CivicEngage.
- ⚠️ Search results surfaced a legacy non-CivicPlus path structure
  (`/meeting_documents/`, `/docs/minutes/pb_2025_05_21.pdf`,
  `/docs/misc/pb_rules_of_procedure.pdf`) — `/meeting_documents/` **404s**
  on the current site (`Custom404 • Candia, NH • CivicEngage` — the
  current CivicPlus theme's own 404 page, confirming this is a genuine
  dead link rather than a different live platform). The `/docs/...` direct
  file paths may still resolve individually (not tested), but the current
  live browse path is the standard CivicPlus **Agenda Center**:
  `https://www.candianh.org/AgendaCenter`.
- Planning Board Rules of Procedure and other static docs may still be
  reachable at their old `/docs/misc/...` paths even if the browse/index
  page that used to link them is gone — worth a direct-URL check before
  assuming a `/docs/` link is fully dead.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Minutes/_05202026-555`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Meetings: 1st & 3rd Wednesday monthly, 6:30pm, Candia Town Hall, 74 High
  Street. Unapproved minutes are posted with an asterisk and replaced once
  approved.

## Document content

- **Minutes PDF** (May 20, 2026, 221KB): real project detail —
  `PdfKeywordScan` found 5 hits: Case #26-001, a MAJOR Subdivision
  application by DAR Builders, LLC (722 East Industrial Park Drive Unit
  17, Manchester NH), property on Crowley Road, Candia, Map 414 Lot 152 &
  152-10 — creating a single-family residential lot with the remainder
  deeded to the Town of Chester for access/right-of-way. A second section
  discusses Master Plan survey results (residential growth management,
  diverse housing) and a "zero lot line" condominium-style layout concept
  — town-planning-policy content rather than a specific case, but still
  useful context.

## Sample files downloaded

- `working/candia_nh/_05202026-555` (May 20, 2026 minutes — no extension
  in the saved filename; it is a PDF)
