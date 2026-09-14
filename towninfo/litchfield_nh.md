# Litchfield, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town, along the Merrimack River south of Manchester.
Runs CivicPlus CivicEngage with the Agenda Center module — same shape as
other towns this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://litchfieldnh.gov` (also `www.litchfieldnh.gov`).
- Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-6/`.
- Search results also surfaced `planning.litchfieldnh.gov` — a possible
  separate planning-department microsite, not explored this session.
- Meeting titles vary: "Planning Board Meeting", "Planning Board Hearing",
  "Planning Board SIte Walk" [sic, typo preserved from the site].

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — descriptive filename via
  Content-Disposition (`_Public Notice PB 20260901.pdf`).
- Meetings: 1st & 3rd Tuesday monthly, 7pm, Litchfield Town Hall
  Conference Room.

## Document content

- **Agenda PDF** (Sept 1, 2026, "Planning Board Hearing," 290KB): 1
  keyword hit — a public hearing on proposed **zoning/regulation
  amendments** (Private Road Design Requirements, Stormwater Regulations
  Appendix D, Site Plan Review Regulations) rather than a specific
  development project. Confirms this town's hearings include
  regulation-amendment sessions distinct from individual-case reviews —
  worth sampling a plain "Planning Board Meeting" entry in a follow-up
  pass for project-level signal.

## Sample files downloaded

- `working/litchfield_nh/_Public Notice PB 20260901.pdf`
