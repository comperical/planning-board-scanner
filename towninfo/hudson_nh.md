# Hudson, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town on the MA border, across the Merrimack River
from Nashua. Runs CivicPlus CivicEngage with the Agenda Center module —
same shape as other towns this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.hudsonnh.gov` — CivicPlus CivicEngage (logo
  links to `nh-hudson.civicplus.com`, the underlying CivicPlus hosting
  domain — cosmetic, not a separate live site).
- ⚠️ Search-indexed `/bc-pb/page/planning-board` **404s** — same recurring
  stale-link pattern (East Kingston, Fremont, etc.). Live path is the
  standard `/agendacenter`.
- Agenda Center: `/agendacenter` — Planning Board section loads
  collapsed, needs a click to expand.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`, with
  `?html=true` on agenda links (safe to strip).
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Meetings: 2nd & 4th Wednesday, 7pm, Buxton Community Development
  Meeting Room, Town Hall lower level.

## Document content

- **Agenda PDF** (Sept 9, 2026, 24KB): real content, in a terse table
  format — `PdfKeywordScan` found 2 hits: a St. Laurent Drive Lot Line
  Relocation Plan, and a Retail Site Plan + Retail Plans set for "1
  Bockes Road" (multiple related document entries for the same address/
  project, table-style listing rather than narrative prose).

## Sample files downloaded

- `working/hudson_nh/09092026.pdf`
