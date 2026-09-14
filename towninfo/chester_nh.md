# Chester, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, active planning board (1st, 3rd & often 4th
Wednesday). Platform: standard CivicPlus Agenda Center (see PATTERNS.md)
— no bot protection.

## Platform notes

- Main site: `https://www.chesternh.org`. Planning Board hub:
  `/1392/Planning-Board` (also `/planning-department`).
- Agenda Center: `/agendacenter` — Planning Board section loads already
  expanded.
- Meeting titles carry useful status flags right in the title text:
  "(Public Hearing)", "(Hearing Continued)", "(Meeting Cancelled)",
  "(No Agenda)" — worth parsing to skip cancelled/no-agenda meetings.
  Unusually active: near-weekly meetings, many marked public hearings.
- Meetings: 1st, 3rd, sometimes 4th Wednesday, 7pm, Main Conference Room,
  Municipal Complex, 84 Chester Street.

## Document content

- **Agenda PDF** (Sept 9, 2026, 340KB): real project detail —
  `PdfKeywordScan` found 3 hits: a continued Subdivision Application
  hearing for David Haddad (owner, 107 Windham Road, Derry NH), continued
  until 9/30/26. The agenda also defines its own case-type abbreviation
  key (APT, CD, CUP, HB, LLA, PH, PHC, SPR, SUB) — useful if building a
  parser.
- **Minutes PDF** (Aug 26, 2026, 243KB): downloaded but not yet
  content-analyzed.

## Sample files downloaded

- `working/chester_nh/09-09-26 PB Draft Agenda.pdf`
- `working/chester_nh/_08262026-338` (Aug 26, 2026 minutes — no extension
  in the saved filename; it is a PDF)
