# Hooksett, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town on the Merrimack River, south of Manchester.
**First town in this project on Revize** (`revize.com` — a seventh
distinct municipal CMS vendor found across this project). No bot
protection.

## Platform

- Main site: `https://www.hooksett.gov` — Revize (PHP-based, e.g.
  `.../agendas_minutes.php`).
- Planning Board hub: `/government/boards_committees/planning_board/
  index.php`. Also has "Current Project Applications" and "Public
  Notices" sub-pages — both potentially higher-signal summary sources,
  not explored this session.
- Agendas & Minutes page:
  `/government/boards_committees/planning_board/agendas_minutes.php` — an
  **accordion tree**, not a flat list: click a year heading (e.g. "2026 —
  33 documents") to reveal **Agendas / Minutes sub-headings**, then click
  one of those to reveal the actual file links. Three levels of clicking
  needed to reach a document link (year → type → file) — the deepest
  nesting seen in this project so far. The 2026 year alone already showed
  17 agenda + 16 minutes documents.
- Files are also mirrored on a separate `cms3.revize.com` subdomain
  (`cms3.revize.com/revize/hooksett/Documents/Government/Board%20&%20
  Committees/Planning%20Board/Agendas%20and%20Minutes/{YYYY}/{filename}.pdf`)
  — this direct path bypasses the accordion UI entirely and was used to
  confirm access this session (older 2024 filenames match a simple
  `MMDDYYYY.pdf` pattern, though naming isn't guaranteed consistent
  across years).

## URL structure

- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  documents directly** from the `cms3.revize.com` static path — no
  referer/cookie gate.
- Meeting titles inline in agenda text use ALL-CAPS section headers:
  "COMPLETENESS REVIEW & PUBLIC HEARING", "CONTINUED PUBLIC HEARING" —
  useful for parsing case status.

## Document content

- **Agenda PDF** (Oct 21, 2024 sample, 71KB): very rich —
  `PdfKeywordScan` found 4 hits: **Richmond Technology Drive, LLC**
  proposing a Major Subdivision *and* a separate Site Plan at 400
  Technology Drive (Map 29, Lot 76-1) — including a **100-dock** proposal
  (likely a marina/boat storage facility given the town's riverfront);
  a Minor Subdivision Plan splitting a parcel bisected by Merrimack
  Street (117/118 Merrimack St., Map 5 Lots 12/13); and a Lot Line
  Adjustment reconfiguring two parcels on Londonderry Turnpike (Map 32,
  Lots 23/24).

## Sample files downloaded

- `working/hooksett_nh/10212024.pdf` (Oct 21, 2024 — older sample used to
  confirm platform access; a current-2026 sample not yet pulled through
  the accordion UI)

## Open items for later

- Work out the exact 2026 file-naming pattern via the accordion UI (the
  `MMDDYYYY.pdf` guess worked for the 2024 sample but wasn't re-confirmed
  for 2026) to pull a current agenda.
