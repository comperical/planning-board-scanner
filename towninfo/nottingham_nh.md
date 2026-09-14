# Nottingham, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town (northwest border, near Strafford County). Runs
standard **node-based CivicPlus CivicEngage** (not Agenda Center) — same
family as New Castle/Derry. No bot protection.

## Platform

- Main site: `https://www.nottingham-nh.gov` — CivicPlus CivicEngage.
- Planning Board hub: `/planning-board`.
- **Agendas index**: `https://www.nottingham-nh.gov/node/176/agenda` —
  lists years; click into `/node/176/agenda/2026` for current-year
  entries (same as Derry's pattern).
- Nottingham also maintains a **"Current Applications Before the Board"**
  page (`/planning-board/pages/current-applications-board`) — not explored
  this session, but likely a high-signal summary page worth checking in a
  future pass (a plain-English running list of active applications, akin
  to Salem's news recaps).

## URL structure

- Each entry links to `/planning-board/agenda/planning-board-meeting-agenda-{MDYY}`
  (e.g. `-9926` for Sept 9, 2026) or `-joint-meeting-agenda-{...}` for
  joint sessions — and **redirects straight to a static PDF**:
  `https://www.nottingham-nh.gov/sites/g/files/vyhlif3611/f/agendas/pb_agenda_{M-D-YYYY}.pdf`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the PDF directly** — no referer/cookie gate.
- Meetings appear frequent, including joint sessions with other boards.

## Document content

- **Agenda PDF** (Sept 9, 2026, 175KB): real project detail —
  `PdfKeywordScan` found 2 hits: a 2-lot conventional subdivision
  application, filed by an engineering firm ("...Associates, Inc.") on
  behalf of Christopher Lydon, 151 Round Pond Rd (Tax Map 61, Lot 2), plus
  a standing agenda item referencing the town's Subdivision and Site Plan
  Regulations under RSA 675:7.

## Sample files downloaded

- `working/nottingham_nh/pb_agenda_9-9-2026.pdf`

## Open items for later

- Check `/planning-board/pages/current-applications-board` as a possible
  higher-signal summary source (plain list of active applications), same
  idea flagged for Salem's news recaps.
