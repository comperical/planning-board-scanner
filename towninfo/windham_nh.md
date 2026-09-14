# Windham, NH — Planning Board Web Access

Investigated: 2026-09-14

Windham is a larger, actively-developing Rockingham town. Runs CivicPlus
CivicEngage with the Agenda Center module — same shape as the other
Rockingham towns this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.windhamnh.gov` — CivicPlus CivicEngage.
- Planning Board hub: `/327/Planning-Board` — description notes the board
  "deals primarily with Site Plan and Subdivision reviews."
- Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-15`.
- Meetings held at the "Community Development Meeting Room," 3 N Lowell
  Road.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs — got a full descriptive filename via
  Content-Disposition (`01-07-26 PB Agenda Revised.pdf`).
- Meetings: 7pm, roughly biweekly.

## Document content

- **Agenda PDF** (Jan 7, 2026, 227KB): very rich — `PdfKeywordScan` found
  8 hits across multiple substantial items: a **Preliminary Site Plan
  Application** on a Historic Cultural Resource List property (Parcels
  11-A-570/580, Village Center District & WWPD, applicant partially named
  "Jo..."); a **Conceptual Site Plan & Conceptual Subdivision** at Wall
  Street (Parcels 11-C-700/800, Professional Business District, applicant
  Karl Dubay...); and — most notably — a discussion of a **100-acre master
  plan** proposing subdivision and site plans for retail, commercial,
  services, a school, industrial, and open-space/residential/conservation
  land uses, with a limited extension of Wall Street to complete its
  cul-de-sac. This is one of the largest-scale single projects surfaced in
  the project so far. A rescheduled Zoning Amendments public hearing (to
  Jan 14, 2026) is also flagged.

## Sample files downloaded

- `working/windham_nh/01-07-26 PB Agenda Revised.pdf`
