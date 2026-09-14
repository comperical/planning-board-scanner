# Lee, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town, along Route 4/155 between Durham and Northwood.
Platform: node-based CivicPlus (see PATTERNS.md). No bot protection.

## Platform notes

- Main site: `https://www.leenh.org`. Planning Board hub:
  `/planning-board`.
- Agendas index: `/node/34/agenda`, years, `/node/34/agenda/2026` for
  current year. A pre-CivicPlus archive link also exists:
  `cmsarchive.civicplus.com/Lee%20NH/default.htm`.
- ⚠️ The 2026 listing mixes **Planning Board entries with other boards'
  meetings under the same node/category** — "Conservation Comm" and
  "Tustees of Trust Funds" [sic] rows appeared interleaved. Filter by
  title text, not just URL prefix.
- Entry title/slug styles are inconsistent across meetings: "Planning
  Board Meeting" (`-meeting-84`), plain "Planning Board" (`-2`, `-1`,
  `-0`), "Planning Board Agenda" (`-agenda-0`) all appear for what are
  presumably the same recurring meeting type.
- Static PDF path: `sites/g/files/vyhlif776/f/agendas/{M-D-YYYY}_agenda_.pdf`.
- Meetings: roughly monthly-to-biweekly, 6pm (one outlier 10:00am entry —
  possibly a site walk or special session).

## Document content

- **Agenda PDF** (Sept 9, 2026, 70KB): rich — `PdfKeywordScan` found 3
  hits describing an active multi-phase commercial buildout: **Lee
  Circle Development**, case P2627-02, an accepted Site Plan Review
  Application proposing a 3,600 sq ft commercial building (Phase 4) and
  another 3,600 sq ft commercial building (Phase 5), plus a subdivision
  application splitting a 7.2808-acre parcel out of an existing
  33.04-acre parcel. Strong, well-specified signal.

## Sample files downloaded

- `working/lee_nh/9-9-2026_agenda_.pdf`
