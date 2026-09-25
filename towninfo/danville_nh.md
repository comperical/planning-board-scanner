# Danville, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town. Platform: standard CivicPlus Agenda Center
(see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.townofdanville.org`. Planning Board hub:
  `/1301/Planning-Board`. Agenda Center section loads already expanded.
- Meeting **titles themselves carry the project/applicant**, like
  Kensington: "Planning Board Meeting - Preliminary Discussion for a
  possible subdivision at 79 Emerald Drive" (Sept 10, 2026), "...for
  discussion of Zoning requested by Jeff & Joelle Stone of 17 Quimby
  Court" (Aug 27, 2026) — real signal visible from the listing page
  alone.
- ⚠️ Two different `docid` numbering series appear for the same date (Jan
  22, 2026 has both `_01222026-144` and `_01222026-84`, likely a
  site/module migration artifact) — dedupe by date+title, not docid
  alone.
- Meetings: 2nd & 4th Thursday, 7:30pm, Town Hall, 210 Main Street.
- **CHANGE 2026-09-24:** plain `FetchUrl` now 403s (Cloudflare) on
  ViewFile URLs. Browser `<a download>` + `ClaimDownload` works.
- Agendas are now posted as **`.docx`** (Aug-Sep 2026), minutes as PDF.
  Browser-downloaded minutes save as `-{MMDDYYYY}-{id}.pdf` - rename on
  `ClaimDownload` (`name=YYYY.MM.DD_PB_Minutes.pdf`).

## Document content

- **Agenda PDF** (Sept 10, 2026, 18KB): short — 1 keyword hit, consistent
  with a small-town preliminary-discussion agenda (not yet a formal
  subdivision application). The listing-page title itself already carried
  more signal than the PDF body in this sample.

## Sample files downloaded

- `working/danville_nh/September 10 2026 Agenda.pdf`
