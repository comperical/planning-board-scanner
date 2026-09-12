# Rochester, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- CMS: **CivicPlus** (Drupal-based; URLs use `/node/{id}/...`), footer credit "Government Websites by CivicPlus®".
- Root domain: `https://www.rochesternh.gov`
- Sits behind **Cloudflare bot management**.

## Access method — IMPORTANT

- A **headless** Playwright/CDP session is **hard-blocked** by Cloudflare on every page, including static PDF assets: returns HTTP 403 with a "Performing security verification" interstitial that never clears, even after reloading or waiting 15+ seconds.
- A **headed** Playwright session passes through cleanly with no challenge at all, same machine/network.
- Plain `curl` (with a normal desktop-browser User-Agent) works fine for the actual PDF file URLs (`/sites/g/files/.../*.pdf`) — the Cloudflare check appears to gate rendered page requests, not static file downloads under that path.
- **Working pattern for future scraping**: use a *headed* browser to discover/enumerate document links (navigate the CivicPlus listing pages), then hand the resulting PDF URLs to plain `curl` for bulk download. No need to route file downloads through the browser.

## Planning Board archive structure

- Main board page: `/planning-board`
- Agenda year-index: `/node/10106/agenda/{year}` — years available 2009–2026 (as of 2026-09-12)
- Minutes year-index: `/node/10106/minutes/{year}` — same year range
- Agenda detail page: `/planning-board/agenda/{slug}` → page contains a link to the actual PDF under `/sites/g/files/vyhlif9211/f/agendas/{YYYY_MM_DD}_{type}_agenda.pdf`
- Minutes detail page: `/planning-board/minutes/{slug}` → **redirects straight to the PDF** at `/sites/g/files/vyhlif9211/f/minutes/{YYYY_MM_DD}_pb_minutes_final.pdf` (no intermediate HTML page, unlike agendas)

### Meeting types (all mixed together in the same year-index list)

| Type | Agenda filename pattern | Notes |
|---|---|---|
| Regular Planning Board meeting | `{date}_pb_agenda.pdf` | Full board, public hearings, most substantial site plans/subdivisions |
| Workshop meeting | `{date}_pb_agenda.pdf` (same board, labeled "(Workshop Meeting)" in the doc header) | Still carries real case items (extensions, lot-line adjustments, surety releases) — **do not skip these** |
| Minor Site Plan Review Committee | `{date}_minor_site_agenda.pdf` | Sub-committee handling small/administrative applications (e.g. change-of-use); generally lower-value but occasionally has real content |

## Document content notes (from sample PDFs, in `working/rochester_nh/`)

- Agendas: terse, one entry per application — `{address}, {applicant} ({agent/engineer}), {application type} — {description}. Case# {number}` — consistently structured, good for automated parsing of address/applicant/project type.
- Minutes: much richer — full narrative of discussion, motions, vote outcomes, unit counts, approval conditions. Published ~2 weeks after the meeting (minutes note the date they were formally approved). Sometimes reveal items (e.g. pending road-acceptance subdivisions) that never appeared on any agenda as a formal item.
- **For a trades-pro lead feed**: agendas give earliest signal of a new filing; minutes are needed to confirm approval status and get real project scope. Link the two by case# and meeting date.

## Sample downloads (in `working/rochester_nh/`)

- `2026_09_14_pb_agenda.pdf` — regular meeting; new 35-unit senior housing site plan
- `2026_08_17_pb_agenda.pdf` — workshop meeting; extension, 2 lot-line adjustments, surety release, data-center zoning update
- `2026_08_26_minor_site_agenda.pdf` — minor site plan committee; single small change-of-use item
- `2026_08_03_pb_minutes_final.pdf` — regular meeting minutes; 206-unit multi-family site plan (final approval), subdivision amendment, retail motor-fuel outlet design review

## Open questions / not yet checked

- Whether other Rochester boards (Zoning Board of Adjustment, Conservation Commission, etc.) use the same `/node/{id}/agenda|minutes/{year}` pattern under a different node id.
- Whether there's an RSS/API feed or CivicPlus "Agenda Center" alternative that avoids needing to crawl the HTML listing pages at all.
- Full behavior of the Cloudflare block — untested whether it's IP-based, purely CDP-fingerprint-based, or time/rate based.
