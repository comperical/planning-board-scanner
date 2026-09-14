# Nottingham, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town (northwest border, near Strafford County).
Platform: node-based CivicPlus (see PATTERNS.md), same family as New
Castle/Derry. No bot protection.

## Platform notes

- Main site: `https://www.nottingham-nh.gov`. Planning Board hub:
  `/planning-board`. Agendas index: `/node/176/agenda`, drill into
  `/node/176/agenda/2026` (same as Derry's pattern).
- Also maintains a **"Current Applications Before the Board"** page
  (`/planning-board/pages/current-applications-board`) — not explored,
  but likely a high-signal summary page (akin to Salem's news recaps).
- Entries link to `/planning-board/agenda/planning-board-meeting-agenda-
  {MDYY}` or `-joint-meeting-agenda-{...}` and redirect straight to a
  static PDF at `sites/g/files/vyhlif3611/f/agendas/pb_agenda_
  {M-D-YYYY}.pdf`. Meetings appear frequent, including joint sessions
  with other boards.

## Document content

- **Agenda PDF** (Sept 9, 2026, 175KB): real project detail —
  `PdfKeywordScan` found 2 hits: a 2-lot conventional subdivision
  application, filed by an engineering firm ("...Associates, Inc.") on
  behalf of Christopher Lydon, 151 Round Pond Rd (Tax Map 61, Lot 2),
  plus a standing agenda item referencing the town's Subdivision and Site
  Plan Regulations under RSA 675:7.

## Sample files downloaded

- `working/nottingham_nh/pb_agenda_9-9-2026.pdf`

## Open items for later

- Check `/planning-board/pages/current-applications-board` as a possible
  higher-signal summary source, same idea flagged for Salem's news
  recaps.
