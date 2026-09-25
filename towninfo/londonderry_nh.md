# Londonderry, NH — Planning Board Web Access

Investigated: 2026-09-14

Londonderry is a larger, industrially-active Rockingham town near
Manchester-Boston Regional Airport. Platform: standard CivicPlus Agenda
Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.londonderrynh.gov`. Planning Board hub:
  `/365/Planning-Board`. Direct per-board Agenda Center:
  `/AgendaCenter/Planning-Board-16/`.
- Two distinct agenda title styles alternate: plain **"Planning Board
  Regular Meeting Agenda (PDF)"** (compact, text-only — see below) vs.
  **"Planning Board Regular Meeting Materials"** (likely a larger merged
  packet, not sampled this session — see Salem's write-up and
  PATTERNS.md for the caveat that a "Materials" file can sometimes be
  only a cover/index page).
- Meetings: weekly-ish "Regular Meeting" sessions, 7pm, Moose Hill
  Conference Room, 268B Mammoth Road.

## Document content

- **Agenda PDF** (Sept 9, 2026, 9KB — the "Agenda (PDF)" style, not
  "Materials"): despite the tiny file size, this is **full plain-text
  agenda content**, not scanned or a bare index — the richest single
  document read in this entire project so far. Four full public
  hearings, each with complete legal-notice-style detail:
  - A lot-line-adjustment review, 16 & 22 Delta Drive (Map 14, Lots
    21-4/21-11, Industrial-2), owner/applicant "16 Delta Drive Owner LLC"
    and "17 & 22 Delta Drive Owner LLC".
  - A site plan for an **existing industrial building** expanding/
    reconfiguring trailer parking, security fencing, controlled-access
    gates, and a mobile loading dock, 10 & 12 Industrial Drive (Map 28,
    Lots 21C-7/21-7), applicant Austin Schimming CCB, Inc., owner Aero
    Manchester Fee LLC.
  - A subdivision + lot-line adjustment creating 3 residential lots at 36
    Pillsbury Road (Map 10, Lot 42, Woodmont Commons PUD / AR-1 zoning),
    owner Pillsbury Realty Development LLC, applicant Procopio
    Enterprises, Inc.
  - A **condo conversion** of the same newly-created lot (Map 10, Lot
    42-2), same owner/applicant pair.

  Every item gives full owner + applicant names, tax map/lot, zoning
  district, and a plain-English description — no packet or PDF-rendering
  needed at all. Strong argument that `PdfExtractText` alone on
  Londonderry's plain "Agenda (PDF)" links is enough for full signal
  extraction.

## Sample files downloaded

- `working/londonderry_nh/9.9.2026 agenda.pdf`

## Open items for later

- ~~Sample a "Materials" link.~~ Done 2026-09-24: the plain "Materials"
  ViewFile is the **full agenda text** (1-2pp, rich), not an index. Each
  row also has a `?packet=true` link for the merged packet (plans/staff
  reports) - not taken routinely.
- **CHANGE 2026-09-24:** plain `FetchUrl` now 403s (Cloudflare); browser
  `<a download>` + `ClaimDownload` works (saves as `{MMDDYYYY}.pdf`).
- No minutes posted in the Agenda Center section for 2026. Agendas go up
  ~2 weeks ahead.
