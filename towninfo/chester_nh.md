# Chester, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town, active planning board (meets 1st, 3rd & often 4th
Wednesday). Runs CivicPlus CivicEngage with the Agenda Center module —
same shape as Fremont/East Kingston/Kensington/Epping — plain PDFs, no bot
protection.

## Platform

- Main site: `https://www.chesternh.org` (bare `chesternh.org` also
  resolves and redirects/serves fine).
- Planning Board hub: `/1392/Planning-Board` (also `/planning-department`
  — the department and board are closely linked on this site).
- Agenda Center: `https://chesternh.org/agendacenter` — Planning Board
  section loads **already expanded**.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}` — e.g.
  `/AgendaCenter/ViewFile/Agenda/_09092026-345`,
  `/AgendaCenter/ViewFile/Minutes/_08262026-338`. Some agenda titles append
  `?html=true` (inline preview variant, seen elsewhere too) — safe to
  strip.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — agenda got a sane filename via
  Content-Disposition (`09-09-26 PB Draft Agenda.pdf`); minutes fell back
  to the bare `_{date}-{id}` with no extension (recurring AgendaCenter
  quirk — it is a PDF).
- Meeting titles carry useful status flags right in the title text: "(Public
  Hearing)", "(Hearing Continued)", "(Meeting Cancelled)", "(No Agenda)" —
  worth parsing to skip cancelled/no-agenda meetings when scraping in bulk.
  Chester is unusually active: near-weekly meetings, many marked as public
  hearings.
- Meetings: 1st, 3rd, and (per search) sometimes 4th Wednesday, 7pm, Main
  Conference Room, Municipal Complex, 84 Chester Street.

## Document content

- **Agenda PDF** (Sept 9, 2026, 340KB): real project detail —
  `PdfKeywordScan` found 3 hits: a continued Subdivision Application
  hearing for David Haddad (owner, 107 Windham Road, Derry NH), continued
  until 9/30/26 by request of the applicant. The agenda also defines its
  own case-type abbreviation key (APT, CD, CUP, HB, LLA, PH, PHC, SPR,
  SUB) — useful if building a parser, since case types are consistently
  coded this way.
- **Minutes PDF** (Aug 26, 2026, 243KB): downloaded but not yet
  content-analyzed in this session.

## Sample files downloaded

- `working/chester_nh/09-09-26 PB Draft Agenda.pdf`
- `working/chester_nh/_08262026-338` (Aug 26, 2026 minutes — no extension
  in the saved filename; it is a PDF)
