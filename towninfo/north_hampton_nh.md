# North Hampton, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: node-based CivicPlus (see PATTERNS.md), older Drupal template.

## Platform notes

- Site: `https://www.northhampton-nh.gov` (hyphenated domain —
  `northhamptonnh.gov` without the hyphen does not resolve).
- **Cloudflare bot-challenge in headless mode**: `goto` headless returned
  HTTP 403 ("Just a moment..." interstitial). `--headed` loaded cleanly
  (same fix as Rochester, no stealth/fingerprint workaround needed).
- Board hub: `/planning-board` — full charter text, staff contact, board
  roster, sidebar of sub-resource links, mini calendar widget, inline
  "latest 5" teaser lists with "View all" links.
- Full archives: `/node/249/agenda` and `.../minutes` — flat
  reverse-chronological lists (not year-accordioned). `249` is the
  Planning Board's internal node id.
- The listing mixes several meeting/committee types under the same node:
  "Planning Board PH Agenda/Minutes" (regular Public Hearing meetings),
  "Planning Board WS Agenda/Minutes" (Work Sessions), and a very active
  **"Long Range Planning Committee"** sub-body posting its own agendas
  roughly weekly (Master-Plan-oversight-style, same pattern as Exeter's
  TRC).
- Clicking a list item redirects straight to the static PDF, no
  intermediate node page. Sidebar also links a frozen pre-2016 legacy
  archive at `cmsarchive.civicplus.com/North%20Hampton%20NH/...`.
- Static PDF paths: `sites/g/files/vyhlif996/f/{agendas|minutes|news}/
  {filename}.pdf` (same PDFs re-hosted under news posts too). Filenames
  loosely readable but mixed date-separator styles — read the actual
  href rather than guessing.

## No live "Active Applications"-style leads page

- Full sidebar enumerated (2026 Meeting Schedule, Coastal Flood Risk
  Summary, FEMA Flood Map Information, Master Plan, Meeting Document
  Archives, Ordinances/Regulations/Fees, Planning & Zoning Department,
  Rules of Procedure, Forms, Previous Master Plan Archive, Responsibilities
  & Administration) — **none is a continuously-updated case-tracker** in
  the Hampton/Stratham sense. Individual "Planning Board Public Hearing
  {date}" news posts turned out to just re-host that meeting's agenda
  PDF, not a distinct richer document. Like Rye, North Hampton has no
  dedicated leads page — pending-case detail lives entirely in the
  agenda/minutes PDFs.

## Document content

- **Agenda PDF** (sample: `pb_agenda_9-01-26.pdf`, Sept 1, 2026 PH
  meeting): 1 page, fully text-extractable, Word-generated. Despite being
  only 1 page, case-level detail is Exeter/Stratham/Rye-caliber — every
  item gives applicant name/address, property owner name/address,
  **Map/Lot (M/L) number**, zoning district, and a real project
  description. Sample cases:
  - Release of a site-work performance guarantee tied to a 2017 site plan
    approval, 227 Lafayette Road (M/L 020-012-000), I-B/R district.
  - **Lot Line Adjustment + Subdivision + Site Plan Review** for a
    proposed **27-unit multi-family residential development plus one
    commercial lot**, 165 Lafayette Road and adjacent lot (M/L
    017-098-000 / 017-099-000), plus a Conditional Use Permit for
    building within the Aquifer Protection District — a substantial
    development lead.
  - Restrictive-covenant alteration request, 223 Lafayette Road (M/L
    021-001-000), I-B/R and R-1 districts.
  - Minor Review to extend hours of operation for a coffee shop, 225
    Atlantic Avenue (M/L 013-015-000).
  - `PdfKeywordScan` returned **8 hits** from a single page — strong hit
    density, reflecting case-paragraph density rather than sheer length.
- **Minutes PDF** (sample: `pb_minutes_ph_08042026.pdf`): 13 pages, fully
  text-extractable, same narrative format as other towns' minutes.
- **No bundled "packet"/"materials" PDF** — the hub page explicitly
  directs inquirers to "contact the Planning & Zoning Administrator ...
  to review submitted applications" — same not-bundled tier as
  Rye/Rochester.

## Sample downloads (in `working/north_hampton_nh/`)

- `pb_agenda_9-01-26.pdf` — 27-unit multi-family + commercial development
  case, plus 3 other items
- `pb_minutes_ph_08042026.pdf` — 13 pages

## Open questions / not yet checked

- Whether the Long Range Planning Committee's near-weekly agendas carry
  the same case-level density as the PH/WS agendas.
- Whether draft (pre-approval) minutes are consistently posted promptly.
- Whether the Zoning Board of Adjustment has any richer leads-page
  equivalent.
- Exact cadence/depth of the pre-2017 legacy archive.
