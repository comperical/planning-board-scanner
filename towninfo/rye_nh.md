# Rye, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://www.ryenh.gov` — CivicPlus **CivicEngage**, same platform family as Hampton (standard Agenda Center module, `/AgendaCenter/ViewFile/...` URLs, `/DocumentCenter/View/...` for standalone attachments).
- The town is mid-migration: its old canonical hostname `www.town.rye.nh.us` redirects to `ryenh.gov`, but several old-style guessed paths (`/planning-board`, `/government/boards-commissions`) 404 on a CivicEngage-branded 404 page — a site banner even says "New Website Updates! Use Ryenh.gov to find current pages!" confirming the site was recently rebuilt/re-platformed. Don't trust guessed slugs; navigate from the nav menu.
- No Cloudflare or other bot-challenge encountered — loaded and navigated cleanly in **headless** mode, no headed fallback needed.

## Finding the archive

- From the homepage nav: **Boards → Planning Board** → `https://www.ryenh.gov/633/Planning-Board`. This hub page has a "View Most Recent Agendas and Minutes" link to `/AgendaCenter`, plus a sidebar of sub-pages (see leads-page section below), staff contacts, and the current board roster.
- `/AgendaCenter` is the same year-grouped, per-board-accordion table seen at Hampton: click "▶ Planning Board" to expand, then a `List of Agendas` table with one row per meeting date and **Agenda / Minutes / Download** cells (no separate "Media"/video column was seen for this board, unlike Hampton).
- Row density is roughly monthly (2nd Tuesday of each month, per the board's posted schedule) — much lower cadence than Exeter/Stratham's near-weekly meetings.
- Some rows carry irregular link text instead of a fixed convention ("Planning Board", "Planning Board 8-11-2026", "Planning Board Regular Meeting Agenda (PDF)", "planning board", "Planning board - canceled and rescheduled to 4-28-2026 ... `?html=true`") — same read-the-actual-href caveat as Exeter/Stratham.

## URL structure — static and directly fetchable

```
https://www.ryenh.gov/AgendaCenter/ViewFile/Agenda/_MMDDYYYY-{id}
https://www.ryenh.gov/AgendaCenter/ViewFile/Minutes/_MMDDYYYY-{id}
https://www.ryenh.gov/DocumentCenter/View/{id}/{filename}
```

- Confirmed working with plain `FetchUrl` — no browser/session/cookie needed, same easy tier as Rochester/Hampton/Stratham.
- `{id}` is a small sequential integer visible directly in the listing page's links (e.g. `_09082026-753`, `_06092026-588`) — no separate node-id lookup step needed, same as Hampton.
- `Content-Disposition` behaved inconsistently: the Sept 8 agenda fetch produced a clean `SEPTEMBER 8 2026.pdf` filename, but the June 9 minutes fetch fell back to the URL's last path segment (`_06092026-588`, no extension) — same caveat noted for Hampton, doesn't affect the PDF tools.
- `DocumentCenter/View/{id}/{filename}` links (used for standalone attachments like legal notices, the lot-merger application form, and the 2025 case/escrow-status document) are likewise static and directly `FetchUrl`-able, no session needed — same tier as Hampton's DocumentCenter links.

## Leads-page check: no Hampton/Stratham-style live "Active Applications" page

Rye's Planning Board hub sidebar lists several candidate sub-pages, none of which turned out to be a continuously-maintained leads page in the Hampton/Stratham sense:

- **"PLANNING BOARD LEGAL NOTICES 2026"** (`/641/PLANNING-BOARD-LEGAL-NOTICES-2026`) — closest analog found. It's a static CivicEngage content page with a short, manually-appended list of "Attachment" links: individual per-meeting Legal Notice PDFs (`Pb Legal for Applications Feb 10 2026.PDF`, `PB Legal July 14 2026 for 120 Brackett and LaMulita 15 Sagamore.pdf`, etc.) plus a couple of ordinance-amendment notices. Only **6 documents** were listed as of this check, the newest dated July 14, 2026 — over two months stale relative to the Sept 8, 2026 agenda already posted in the Agenda Center. Unlike Hampton's/Stratham's pages, this one is not kept current every meeting and isn't structured as a live case tracker (no status/hearing-date table, no per-case document trail across submission rounds) — it's better described as a legal-notice archive than a leads page.
- **"2025 Cases heard by the Planning Board"** (`/634/2025-Cases-heard-by-the-Planning-Board`) — turned out to be a single attached document, "2025 Pb Files and Status of Accounts" (an escrow-account/case-fee status list, not downloaded/analyzed in detail), not a prose case-description page.
- No equivalent of Hampton's "Active Applications" or Stratham's "Public Hearing Notices" page — pending-case detail for Rye lives in the **Legal Notice PDFs** (individually posted per meeting, when the board chooses to post one) and in the **agenda PDF itself**, not in a dedicated always-current listing page.

## Document content

- **Agenda PDF** (e.g. `SEPTEMBER 8 2026.pdf`, 2 pages, fully text-extractable, Word-generated): dense, Exeter/Stratham-level case detail per item — applicant name, property owner, full street address, **Tax Map and Lot number**, zoning district(s) including overlay districts (Coastal Overlay, SFHA/Zone AO, Wetlands Conservation, Aquifer & Wellhead Protection), a real plain-English project description, and the town's own case number (`Case #09-2026`). Sample (Sept 8, 2026 meeting) included:
  - Eversource utility brush-trimming application across ~25 named scenic roads (Case #08-2026) — not a development lead, but shows the agenda's level of specificity even for non-development items.
  - Minor site plan by James Holland / Ortholand, LLC, 2203 Ocean Blvd Unit C (Tax Map 5.3, Lot 28) — converting a business condo unit to residential use (Case #09-2026).
  - Preliminary conceptual consultation for a 7-lot subdivision at 701 South Rd. (Tax Map 3, Lot 2) — 6 new dwellings plus the existing house, new cul-de-sac road, in Single Residence / Wetlands Conservation / Aquifer & Wellhead Protection districts.
  - `PdfKeywordScan` against the standard keyword list returned 4 hits (site plan, residential, condominium, subdivision) — modest because this was a light meeting (2-3 items), not a weakness of the document format.
- **Legal Notice PDF** (sample: `PB Legal July 14 2026 for 120 Brackett and LaMulita 15 Sagamore.pdf`, 1 page, text-extractable, 1,705 chars): essentially the same case-paragraph format as the agenda, posted as a standalone public-hearing notice ahead of the meeting. Sample cases:
  - Minor two-lot subdivision by TFMoran for Dolores F. Lintz, 120 Brackett Road (Tax Map 22, Lot 95A) — subdividing a 6-acre lot with an existing house to create one new buildable lot (Case #05-2026).
  - **Major Site Development and Mixed-Use Development Plan** by Jones & Beach Engineers for Pruna Holdings, LLC, 15 Sagamore Rd. (Tax Map 24, Lot 22) — three new single-family dwellings on a back lot plus two mixed-use buildings on the front parcel, spanning Single Residence and Commercial zoning districts (Case #10-2022, an older case number reappearing on a current-year notice — suggests a long-running/continued application).
- **Minutes PDF** (`_06092026-588`, 2 pages, text-extractable, 2,283–1,831 chars/page, Word-generated): standard motion-and-discussion narrative.
- No bundled "materials"/"packet" PDF was found for this board (no Packet column or link in the Agenda Center rows, unlike Exeter/Dover) — supporting application materials, if posted at all, would need to be requested from staff (the Legal Notice PDF explicitly says "information submitted with the application is available for review by contacting kreed@town.rye.nh.us" rather than linking documents directly) — closer to Rochester's "not bundled" pattern than Hampton's/Stratham's per-file-attachment trail.

## Sample downloads (in `working/rye_nh/`)

- `SEPTEMBER 8 2026.pdf` — Sept 8, 2026 regular meeting agenda (Ortholand condo-to-residential conversion, 701 South Rd. 7-lot subdivision preliminary consult)
- `_06092026-588` — June 9, 2026 approved-style minutes (no `.pdf` extension, missing Content-Disposition header)
- `PB Legal July 14 2026 for 120 Brackett and LaMulita 15 Sagamore_202606250903367010.pdf` — standalone Legal Notice PDF from the Planning Board Legal Notices page (TFMoran 2-lot subdivision + Pruna Holdings mixed-use development case)

## Comparison to other NH towns studied

| | Rochester | Dover | Exeter | Newmarket | Hampton | Stratham | Rye |
|---|---|---|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicEngage + CivicClerk portal | CivicPlus CivicEngage (Agenda Center) | Revize CMS | CivicPlus CivicEngage (Agenda Center) |
| Bot protection | Cloudflare hard-blocks headless | None | None | None | None | None | None |
| PDF URLs | Stable, static, guessable | Session-scoped temp URLs | Static, node-id not guessable | Static API, but TLS-blocked for this env's `requests` | Static, `FetchUrl`-able directly, id visible in listing | Static, root-relative, human-guessable date-based path | Static, `FetchUrl`-able directly, id visible in listing (same tier as Hampton) |
| Case-level detail source | Agenda | Agenda + Materials PDF | Agenda + Packet PDF | Agenda + per-file attachments | Dedicated live "Active Applications" leads page (agenda itself terse) | Both agenda and a dedicated "Public Hearing Notices" leads page | **Agenda itself is dense** (Tax Map/Lot, zoning district, case #); a "Legal Notices" page exists but is a stale, manually-appended archive, not a live leads page |
| Supporting docs | Not bundled | Bundled | Bundled "Packet" PDF, mostly text-extractable | Bundled + per-file | Linked per-case from Active Applications page | Linked per-case (plan set, renderings, drainage, permits) | **Not bundled or linked** — notice text directs inquirers to email staff for application materials |
| Archive scope/depth | Per-board node listing | One shared cabinet for all bodies | One shared `/meetings` table, filterable | — | Year-grouped Agenda Center table | Year-accordion, ≥2023–2026 | Year-grouped Agenda Center table, ~monthly cadence (lower than Exeter/Stratham's weekly/biweekly) |

## Open questions / not yet checked

- Whether older years' Agenda Center entries (2025 and earlier, per the sidebar's "2025 Cases heard by the Planning Board" reference) use the same `ViewFile` URL pattern and are still text-extractable — only 2026 samples were pulled here.
- Whether staff, if emailed per the Legal Notice's instructions, would provide application packets electronically, and whether those would be text-extractable or scanned engineering drawings (unknown, not tested — no sample obtained).
- Whether the Zoning Board of Adjustment (`/767/Zoning-Board-of-Adjustment`, same "Boards" section) has a richer leads-page pattern than the Planning Board does — not checked.
- Whether the "PLANNING BOARD LEGAL NOTICES" page is renamed/recreated each calendar year (this one is titled "...2026") and whether prior years' equivalents remain reachable — the low document count (6) suggests either infrequent legal-notice publication or incomplete backfilling onto the page, worth periodic re-checking.
