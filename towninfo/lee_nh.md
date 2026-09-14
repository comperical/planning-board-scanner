# Lee, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town, along Route 4/155 between Durham and Northwood.
Runs node-based CivicPlus CivicEngage. No bot protection.

## Platform

- Main site: `https://www.leenh.org` — CivicPlus CivicEngage.
- Planning Board hub: `/planning-board`.
- **Agendas index**: `https://www.leenh.org/node/34/agenda` — lists years;
  `/node/34/agenda/2026` for current-year entries. A link to a pre-CivicPlus
  archive also exists: `https://cmsarchive.civicplus.com/Lee%20NH/default.htm`.
- ⚠️ The 2026 listing mixes **Planning Board entries with other boards'
  meetings under the same node/category** — "Conservation Comm" (Jul 2,
  2026) and "Tustees of Trust Funds" [sic] (Jun 4, 2026) rows appeared
  interleaved with Planning Board rows on the same `/node/34/agenda/2026`
  page. Filter by title text, not just by URL prefix, when scraping.
- Entry title/slug styles are inconsistent across meetings: "Planning
  Board Meeting" (`-meeting-84`), plain "Planning Board" (`-2`, `-1`,
  `-0`), and "Planning Board Agenda" (`-agenda-0`) all appear for what are
  presumably the same recurring meeting type.

## URL structure

- Each detail page embeds a static PDF:
  `https://www.leenh.org/sites/g/files/vyhlif776/f/agendas/{M-D-YYYY}_agenda_.pdf`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the PDF directly** — no referer/cookie gate.
- Meetings: roughly monthly-to-biweekly, 6pm (one outlier entry at
  10:00am for Jul 22, 2026 — possibly a site walk or special session).

## Document content

- **Agenda PDF** (Sept 9, 2026, 70KB): rich — `PdfKeywordScan` found 3
  hits describing an active multi-phase commercial buildout: **Lee Circle
  Development**, case P2627-02, an accepted Site Plan Review Application
  proposing a 3,600 sq ft commercial building (Phase 4) and another 3,600
  sq ft commercial building (Phase 5), plus a subdivision application
  splitting a 7.2808-acre parcel out of an existing 33.04-acre parcel.
  Strong, well-specified signal — named development, phase numbers, exact
  square footage and acreage.

## Sample files downloaded

- `working/lee_nh/9-9-2026_agenda_.pdf`
