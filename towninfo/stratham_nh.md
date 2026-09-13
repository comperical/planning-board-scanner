# Stratham, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://www.strathamnh.gov` — **Revize CMS** (footer: "Powered by revize., government website experts", login portal at `cms6.revize.com/revize/security/...`). PHP-based URLs (`boards/planning_board/agendas_minutes.php`, etc.), not Drupal/CivicPlus.
- No Cloudflare or other bot-challenge encountered — loaded and navigated cleanly in **headless** mode, no headed fallback needed.

## Finding the archive

- Planning Board hub: `https://www.strathamnh.gov/boards/planning_board/index.php`, with a "Related Pages" sidebar linking every sub-resource:
  - `Agendas & Minutes` — the meeting-by-meeting archive (see below).
  - `Public Hearing Notices` — the ⭐ leads page (see below).
  - `Technical Review Committee`, `Route 108 Corridor Study Committee`, `Age Friendly Communities Project` — Planning Board sub-bodies, same pattern as Exeter's TRC.
  - `Planning Board Meeting Schedule` — a direct link to a static PDF meeting calendar.
- **Agendas & Minutes** page (`boards/planning_board/agendas_minutes.php`) is a year-accordion (2026: 23 documents, 2025: 26, 2024: 23, 2023: 22 — consistent ~biweekly cadence, archive covers at least 2023–2026). Each meeting-date row expands to show whatever's posted for it: Agenda / Minutes columns, with cells simply blank when a document type isn't available yet. A "Search for file name" box sits above the accordion for text search across the whole set.

## URL structure — static, root-relative, directly fetchable

```
https://www.strathamnh.gov/Documents/Boards and Committees/Planning Board/Agendas and Minutes/{year}/Agenda/{YYYY.MM.DD} PB Agenda.pdf
https://www.strathamnh.gov/Documents/Boards and Committees/Planning Board/Agendas and Minutes/{year}/Minutes/{YYYY.MM.DD} approved minutes.pdf
https://www.strathamnh.gov/Documents/Boards and Committees/Planning Board/Public Hearing Notices/{filename}.pdf
```

- Confirmed working with plain `FetchUrl` — no browser/session/cookie needed, same easy tier as Rochester/Hampton. Links in the page HTML carry a `?t={timestamp}` cache-busting query string, but it's not required — fetching the bare path works fine.
- The date/type pattern is human-guessable once you know a meeting date and its title case ("PB Agenda", "approved minutes"), but filenames aren't perfectly uniform (draft vs. approved minutes wording could vary) — safest to read the exact href off the `agendas_minutes.php` listing rather than constructing paths blind, same caveat as Exeter's inconsistent filenames.
- Note for scripted downloads: paths contain literal spaces (`Documents/Boards and Committees/...`) — URL-encode as `%20` when fetching (Stratham's own site does not consistently do this itself, since the raw href in the page HTML contains literal spaces resolved by the browser).

## ⭐ Key find: "Public Hearing Notices" page — Hampton-style leads page

- `https://www.strathamnh.gov/boards/planning_board/public_hearing_notices.php`
- Like Hampton's "Active Applications" page, this is a **standalone, continuously-updated leads page** listing every case coming up for public hearing, in prose form, each with:
  - Applicant/owner name, exact street address, **Tax Map and Lot number**, zoning district, hearing date, and a real plain-English project description.
  - Direct links to the actual submitted materials: full plan sets, architectural renderings/floor plans, drainage analyses, NRCS soils reports, NHDOT driveway permits, etc. — comparable breadth to Hampton's per-case document trail.
  - Also carries non-project business, e.g. a pending public hearing on amendments to the town's own Site Plan Regulations, with the draft amendment PDF linked.
- Sample cases pulled from the page (both live as of Sept 2026):
  - **Packer Brook Holdings LLC / "Mighty Roots"**, 170 Portsmouth Avenue (Tax Map 17, Lot 86) — final site plan approval for a ±6,110 sq ft light-manufacturing office/shop behind an existing single-family home, Route 33 Legacy Highway Heritage District.
  - **Red Barn Property LLC**, 210 Portsmouth Avenue (Tax Map 21, Lot 81) — major subdivision + Conditional Use Permits for a shared driveway, well, barn, and multi-duplex residential development (4 duplex buildings) in wetland setback/buffer areas; continued across at least three meetings (Aug 19 → Sept 2 → Sept 16, 2026).
- Unlike Hampton's page, Stratham's regular agenda PDFs are *not* terse — they carry essentially the same case-level narrative and the same document links as the Public Hearing Notices page (see below), so here the two sources are largely redundant rather than the agenda being a stub that only the leads page fills in. Still very much worth checking as the single place to see everything currently pending, without paging through the accordion.

## Document content

- **Agenda PDF** ("Legal Notice"-style, e.g. `2026.09.16 PB Agenda.pdf`): 1 page, fully text-extractable, dense case detail on par with Exeter's — applicant/owner name, full street address, Tax Map/Lot, zoning district, a real project description (not just a case number), and inline links to that case's plan set/renderings/drainage/permit documents. `PdfKeywordScan` against the standard keyword list returned only 2 hits (one `subdivision`, one `conditional use`) for this particular sample — reflects that this meeting had only one active case, not a weakness of the document; Exeter-style richer meetings would score higher.
- **Minutes PDF** (`{date} approved minutes.pdf`): 5 pages, fully text-extractable (2,600–4,900 chars/page), standard motion-and-discussion narrative format.
- **Public Hearing Notices plan-set PDF** (sample: `5613 - Mighty Roots World Headquaters Plan Set - 8.6.26.pdf`, 22 pages, **39 MB**): CAD-exported engineering drawing set (title block metadata references AutoCAD/Civil3D project files), large-format pages (34"×22" and similar). Mixed extractability — most pages carry a few hundred characters of selectable title-block text, one page (11) has 3,322 chars (likely a notes/legend sheet), but 4 of 22 pages have **zero extractable text** (fully rasterized drawings). This is a "packet" in the Exeter/Dover sense but for engineering plan sets specifically — worth `PdfRenderPages` on targeted sheets rather than bulk text extraction, same guidance as the skill's default for scanned materials packets.
- No separate bundled "meeting packet" PDF was seen the way Exeter/Dover produce one — supporting materials are instead linked individually (plan set, renderings, drainage, permits) from the agenda/hearing-notice text itself, closer to Newmarket's or Hampton's per-file-attachment pattern than Exeter's single bundled packet.

## Sample downloads (in `working/stratham_nh/`)

- `2026.09.16 PB Agenda.pdf` — Sept 16, 2026 regular meeting agenda (Red Barn Property LLC subdivision/CUP case, continued item)
- `2026.08.19 approved minutes.pdf` — Aug 19, 2026 approved minutes (5 pages)
- `5613 - Mighty Roots World Headquaters Plan Set - 8.6.26.pdf` — 22-page CAD plan set for the Packer Brook Holdings/Mighty Roots case, pulled from the Public Hearing Notices page

(Note: files saved via `FetchUrl` with `dest=` kept the literal `%20`-encoded spelling from the URL rather than decoding to spaces, since no `Content-Disposition` filename was returned — cosmetic only, the PDF tools don't care.)

## Comparison to other NH towns studied

| | Rochester | Dover | Exeter | Newmarket | Hampton | Stratham |
|---|---|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicEngage + CivicClerk portal | CivicPlus CivicEngage (Agenda Center) | Revize CMS |
| Bot protection | Cloudflare hard-blocks headless | None | None | None | None | None |
| PDF URLs | Stable, static, guessable | Session-scoped temp URLs | Static, node-id not guessable | Static API, but TLS-blocked for this env's `requests` | Static, `FetchUrl`-able directly, id visible in listing | Static, root-relative, `FetchUrl`-able directly, human-guessable date-based path (once filename convention known) |
| Case-level detail source | Agenda | Agenda + Materials PDF | Agenda + Packet PDF | Agenda + per-file attachments | Dedicated live "Active Applications" leads page (agenda itself terse) | **Both** the agenda itself *and* a dedicated "Public Hearing Notices" leads page carry full case detail |
| Supporting docs | Not bundled | Bundled | Bundled "Packet" PDF, mostly text-extractable | Bundled + per-file | Linked per-case from Active Applications page | Linked per-case (plan set, renderings, drainage, permits) from agenda/hearing-notice text; plan-set PDFs are large CAD exports, partly rasterized |
| Archive scope/depth | Per-board node listing | One shared cabinet for all bodies | One shared `/meetings` table, filterable | — | Year-grouped Agenda Center table | Year-accordion, ≥2023–2026, ~22-26 docs/year, with filename search |

## Open questions / not yet checked

- Whether Stratham's other boards (Zoning Board of Adjustment, Conservation Commission) have an equivalent Public Hearing Notices leads page — the URL pattern (`boards/{board}/public_hearing_notices.php`) suggests it may be a site-wide Revize template feature worth checking.
- Exact minutes filename convention for meetings where minutes are still in draft (not yet "approved") — only an approved-minutes sample was pulled here.
- How far back the Agendas & Minutes accordion goes before 2023, and whether pre-2023 documents use the same URL structure.
- Whether the Public Hearing Notices page is manually pruned after each hearing resolves (i.e., how far back stale entries linger) — worth periodic re-checking like Hampton's equivalent page.
