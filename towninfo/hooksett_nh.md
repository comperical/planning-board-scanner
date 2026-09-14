# Hooksett, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town on the Merrimack River, south of Manchester.
Platform: **Revize** (see PATTERNS.md). No bot protection.

## Platform notes

- Main site: `https://www.hooksett.gov` (PHP-based, `agendas_minutes.php`).
- Planning Board hub: `/government/boards_committees/planning_board/
  index.php`. Also "Current Project Applications" and "Public Notices"
  sub-pages — potentially higher-signal, not explored this session.
- Agendas & Minutes page is an **accordion tree**: click a year heading →
  reveal Agendas/Minutes sub-headings → click one to reveal file links —
  three levels of clicking, the deepest nesting seen alongside Munibit.
  2026 alone showed 17 agenda + 16 minutes documents.
- Files also mirrored on `cms3.revize.com/revize/hooksett/Documents/
  Government/Board%20&%20Committees/Planning%20Board/Agendas%20and%20
  Minutes/{YYYY}/{filename}.pdf` — bypasses the accordion UI entirely
  (older 2024 filenames match a simple `MMDDYYYY.pdf` pattern, not
  guaranteed consistent across years).
- Meeting titles inline in agenda text use ALL-CAPS section headers:
  "COMPLETENESS REVIEW & PUBLIC HEARING", "CONTINUED PUBLIC HEARING" —
  useful for parsing case status.

## Document content

- **Agenda PDF** (Oct 21, 2024 sample, 71KB): very rich —
  `PdfKeywordScan` found 4 hits: **Richmond Technology Drive, LLC**
  proposing a Major Subdivision *and* a separate Site Plan at 400
  Technology Drive (Map 29, Lot 76-1) — including a **100-dock** proposal
  (likely a marina/boat storage facility given the town's riverfront); a
  Minor Subdivision Plan splitting a parcel bisected by Merrimack Street
  (117/118 Merrimack St., Map 5 Lots 12/13); and a Lot Line Adjustment
  reconfiguring two parcels on Londonderry Turnpike (Map 32, Lots 23/24).

## Sample files downloaded

- `working/hooksett_nh/10212024.pdf` (older sample used to confirm
  platform access; a current-2026 sample not yet pulled)

## Open items for later

- Work out the exact 2026 file-naming pattern via the accordion UI (the
  `MMDDYYYY.pdf` guess worked for 2024 but wasn't re-confirmed for 2026).
