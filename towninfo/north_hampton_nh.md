# North Hampton, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://www.northhampton-nh.gov` (hyphenated domain — `northhamptonnh.gov` without the hyphen does not resolve, `net::ERR_NAME_NOT_RESOLVED`). CivicPlus **CivicEngage**, but running the older Drupal node-based template (footer credit "Government Websites by CivicPlus ®", URLs like `/node/249/agenda`, `/print/249`, `/user/login`) — same underlying platform family as Rochester and Exeter rather than the newer "Agenda Center" module seen at Hampton/Rye.
- **Cloudflare bot-challenge in headless mode**: `goto` in headless returned HTTP 403, Page Title "Just a moment...", the classic Cloudflare interstitial. Switching to `playwright-cli -s=planscan open --headed <url>` loaded the real page cleanly (HTTP 200, correct title) — same fix as documented for Rochester, no stealth/fingerprint workaround needed.

## Finding the archive

- From the homepage nav: **Boards & Committees → Planning Board** → `https://www.northhampton-nh.gov/planning-board`. The hub page has the board's charter text, staff contact (Rick Milner, Planning & Zoning Administrator), the full board roster with term-expiration years, a sidebar of sub-resource links, a mini meeting calendar widget, and inline "latest 5" teaser lists for both Agendas and Minutes with "View all" links to the full archives.
- Full archives: `https://www.northhampton-nh.gov/node/249/agenda` and `.../node/249/minutes` — flat reverse-chronological lists (not year-accordioned), one row per posted document with its date/time. `249` is the Planning Board's internal node id, discovered from the hub page rather than guessable.
- The listing mixes several meeting/committee types under the same Planning Board node: **"Planning Board PH Agenda/Minutes"** (regular Public Hearing meetings), **"Planning Board WS Agenda/Minutes"** (Work Sessions), and a very active **"Long Range Planning Committee"** sub-body posting its own agendas roughly weekly (a Master-Plan-oversight-style subcommittee, same pattern as Exeter's TRC or Master Plan Oversight Committee).
- Clicking an agenda/minutes list item does **not** land on an intermediate node page — it redirects straight to the underlying static PDF URL (e.g. `.../planning-board/agenda/planning-board-ph-agenda-113` → `.../sites/g/files/vyhlif996/f/agendas/pb_agenda_9-01-26.pdf`). No click-through/session step needed once the PDF URL is known.
- Sidebar also lists **"Meeting Document Archives (2016 and Earlier)"**, which links out to a separate static file-cabinet site, `cmsarchive.civicplus.com/North%20Hampton%20NH/index1/default.htm` — a frozen legacy archive, not part of the live CMS.

## URL structure — static and directly fetchable

```
https://www.northhampton-nh.gov/sites/g/files/vyhlif996/f/agendas/{filename}.pdf
https://www.northhampton-nh.gov/sites/g/files/vyhlif996/f/minutes/{filename}.pdf
https://www.northhampton-nh.gov/sites/g/files/vyhlif996/f/news/{filename}.pdf   (same PDFs, re-hosted under news posts)
```

- Confirmed working with plain `FetchUrl` (Python `requests`, no browser/cookie needed) — same easy tier as Rochester/Hampton/Stratham/Rye, once the exact filename is known from a listing page or news post.
- Filenames follow a loose but human-readable convention (`pb_agenda_9-01-26.pdf`, `pb_minutes_ph_08042026.pdf`) — mixed date-separator styles between agendas and minutes, so still safest to read the actual href off a listing rather than construct blind, same caveat noted for Exeter/Stratham/Rye.
- `vyhlif996` is an opaque CivicPlus per-site asset-bucket id, stable across all files on this site.

## Leads-page check: no Hampton/Stratham-style live "Active Applications" page

- The Planning Board hub's full sidebar was enumerated: 2026 Meeting Schedule, Coastal Flood Risk Summary, FEMA Flood Map Information, Master Plan, Meeting Document Archives (2016 and earlier), Ordinances/Regulations/Fees, Planning & Zoning Department, Rules of Procedure, Planning and Zoning Board Forms, Previous Master Plan Information Archive, Responsibilities & Administration. **None of these is a continuously-updated case-tracker/leads page** in the Hampton "Active Applications" or Stratham "Public Hearing Notices" sense.
- The town does post individual **"Planning Board Public Hearing {date}" news items** (`/home/news/planning-board-public-hearing-9126`, etc., one per PH meeting, ZBA gets its own equivalent) via the town-wide News & Notices feed — but each one turned out to be nothing more than a copy of that meeting's agenda PDF attached to a news post (same file, just re-hosted under `/f/news/` instead of `/f/agendas/`), not a distinct richer document. This is a thinner pattern than even Rye's stale "Legal Notices" archive page — it's not a standing archive at all, just the normal news feed noting each meeting happened.
- Conclusion: like Rye, North Hampton has **no dedicated leads page** — pending-case detail lives entirely in the (fortunately quite dense) agenda/minutes PDFs themselves, not in any standalone always-current listing.

## Document content

- **Agenda PDF** (sample: `pb_agenda_9-01-26.pdf`, Sept 1, 2026 PH meeting): 1 page, fully text-extractable (2,829 chars), Word-generated (`Microsoft® Word for Microsoft 365`, author "Rick Milner"). Despite being only 1 page, case-level detail is Exeter/Stratham/Rye-caliber — every item gives applicant name/address, property owner name/address, **Map/Lot (M/L) number**, zoning district, and a real plain-English project description. Sample cases (Sept 1, 2026 meeting):
  - Release of a site-work performance guarantee tied to a 2017 site plan approval, 227 Lafayette Road (M/L 020-012-000), I-B/R district.
  - **Lot Line Adjustment + Subdivision + Site Plan Review** for a proposed **27-unit multi-family residential development plus one commercial lot**, 165 Lafayette Road and adjacent lot (M/L 017-098-000 / 017-099-000), plus a Conditional Use Permit for building within the Aquifer Protection District — a substantial development lead.
  - Restrictive-covenant alteration request, 223 Lafayette Road (M/L 021-001-000), I-B/R and R-1 districts.
  - Minor Review to extend hours of operation for a coffee shop, 225 Atlantic Avenue (M/L 013-015-000).
  - `PdfKeywordScan` against the standard keyword list returned **8 hits** (site plan, subdivision, conditional use, lot line adjustment, residential, commercial, industrial, multi-family) from a single page — a strong hit density, reflecting the format's case-paragraph density rather than sheer length.
- **Minutes PDF** (sample: `pb_minutes_ph_08042026.pdf`, Aug 4, 2026 PH meeting): 13 pages, fully text-extractable throughout (1,100–4,360 chars/page, avg ~3,500), same Word/author metadata as the agenda. Standard motion-and-discussion narrative format, long enough to capture real back-and-forth on contested items (abutter comments, conditions imposed, vote tallies).
- **No bundled "packet"/"materials" PDF** was found for either meeting type (no such column in the listings, no packet link on the hub page) — supporting application materials are not linked from the agenda/minutes and would need to be requested from the Planning & Zoning Administrator (the hub page explicitly directs "contact the Planning & Zoning Administrator ... to review submitted applications"), same not-bundled tier as Rye/Rochester rather than Exeter's/Hampton's/Stratham's per-case document trails.

## Sample downloads (in `working/north_hampton_nh/`)

- `pb_agenda_9-01-26.pdf` — Sept 1, 2026 Public Hearing agenda (27-unit multi-family + commercial development case, plus 3 other items)
- `pb_minutes_ph_08042026.pdf` — Aug 4, 2026 Public Hearing minutes (13 pages)

## Comparison to other NH towns studied

| | Rochester | Dover | Exeter | Newmarket | Hampton | Stratham | Rye | North Hampton |
|---|---|---|---|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicEngage + CivicClerk portal | CivicPlus CivicEngage (Agenda Center) | Revize CMS | CivicPlus CivicEngage (Agenda Center) | CivicPlus CivicEngage (legacy Drupal node template) |
| Bot protection | Cloudflare hard-blocks headless | None | None | None | None | None | None | **Cloudflare hard-blocks headless, passes headed** (same fix as Rochester) |
| PDF URLs | Stable, static, guessable | Session-scoped temp URLs | Static, node-id not guessable | Static API, but TLS-blocked for this env's `requests` | Static, `FetchUrl`-able directly, id visible in listing | Static, root-relative, human-guessable date-based path | Static, `FetchUrl`-able directly, id visible in listing | Static, `FetchUrl`-able directly once filename known from listing/news post |
| Case-level detail source | Agenda | Agenda + Materials PDF | Agenda + Packet PDF | Agenda + per-file attachments | Dedicated live "Active Applications" leads page (agenda itself terse) | Both agenda and a dedicated "Public Hearing Notices" leads page | Agenda itself is dense; "Legal Notices" page is a stale archive | **Agenda itself is dense** (M/L, zoning district, real description) despite being only 1 page; no leads page at all |
| Supporting docs | Not bundled | Bundled | Bundled "Packet" PDF, mostly text-extractable | Bundled + per-file | Linked per-case from Active Applications page | Linked per-case (plan set, renderings, drainage, permits) | Not bundled or linked — email staff | **Not bundled or linked** — hub page directs inquirers to the Planning & Zoning Administrator |
| Archive scope/depth | Per-board node listing | One shared cabinet for all bodies | One shared `/meetings` table, filterable | — | Year-grouped Agenda Center table | Year-accordion, ≥2023–2026 | Year-grouped Agenda Center table, ~monthly cadence | Flat reverse-chron list per board node; PH + WS + very active Long Range Planning Committee subcommittee (near-weekly) all mixed together; pre-2017 docs frozen in a separate `cmsarchive.civicplus.com` cabinet |

## Open questions / not yet checked

- Whether the Long Range Planning Committee's near-weekly agendas carry the same case-level density as the PH/WS agendas, or are lighter procedural/master-plan-drafting content (not sampled here).
- Whether draft (pre-approval) minutes are consistently posted in the same window as the PH minutes sample, or lag further behind meeting dates.
- Whether the Zoning Board of Adjustment (also CivicEngage/Drupal on this same site, per its own recurring "ZBA Public Hearing" news posts) has any richer leads-page equivalent — not checked, but the sidebar pattern observed for Planning Board suggests it's unlikely.
- Exact cadence/depth of the pre-2017 `cmsarchive.civicplus.com` legacy archive — not explored beyond confirming the link resolves.
