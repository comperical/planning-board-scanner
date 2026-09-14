# Hudson, NH — Planning Board Web Access

Investigated: 2026-09-14

Hillsborough County town on the MA border, across the Merrimack River
from Nashua. Platform: standard CivicPlus Agenda Center (see PATTERNS.md)
— no bot protection.

## Platform notes

- Main site: `https://www.hudsonnh.gov` (logo links to
  `nh-hudson.civicplus.com`, the underlying hosting domain — cosmetic).
- ⚠️ Search-indexed `/bc-pb/page/planning-board` 404s — live path is the
  standard `/agendacenter`, section loads collapsed, needs a click.
- Meetings: 2nd & 4th Wednesday, 7pm, Buxton Community Development
  Meeting Room, Town Hall lower level.

## Document content

- **Agenda PDF** (Sept 9, 2026, 24KB): real content, terse table format
  — `PdfKeywordScan` found 2 hits: a St. Laurent Drive Lot Line
  Relocation Plan, and a Retail Site Plan + Retail Plans set for "1
  Bockes Road" (multiple related document entries for the same
  address/project).

## Sample files downloaded

- `working/hudson_nh/09092026.pdf`
