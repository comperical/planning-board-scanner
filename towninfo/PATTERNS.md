# Shared Access Patterns — NH Planning Board Sites

This file holds everything that's true across many towns: platform
taxonomy, URL shapes, access gotchas, and document-content conventions.
Individual `towninfo/<slug>.md` files should **not** repeat this material —
they should link back here (e.g. "Platform: CivicPlus AgendaCenter, see
PATTERNS.md") and only record what's different, broken, or notable for that
specific town, plus the town's own document-content findings.

Default assumption unless a town's file says otherwise: **no bot
protection, plain `FetchUrl`/`requests` downloads PDFs directly, no
browser/session needed.**

## Platform taxonomy

### CivicPlus CivicEngage — by far the most common platform (~55 of 69 towns)

CivicPlus has (at least) three distinct URL shapes in this project — the
module in use matters more than "it's CivicPlus":

1. **Agenda Center module** (the majority shape): town-wide `/AgendaCenter`
   (or `/agendacenter`) page groups every board into a collapsible section
   (some pre-expanded, some need a click); a direct per-board URL often
   works too: `/AgendaCenter/Planning-Board-{n}`. Each row links to
   `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`, sometimes with
   a harmless `?html=true` suffix (safe to strip). `{id}` is an opaque
   incrementing item id, not derivable from the date — scrape it from the
   listing. Confirmed `FetchUrl`-able directly on every town using this
   module. Recurring quirks:
   - When `Content-Disposition` is missing, the saved filename falls back
     to the bare `_{date}-{id}` with **no extension** — it's still a real
     PDF, just rename/inspect before assuming otherwise. Seen at: chester,
     candia, east_kingston, epping, fremont, greenland, kensington,
     newfields, sandown, allenstown.
   - Some towns' Agenda Center page is too busy for a plain-text `find` to
     resolve the right section — take a full `snapshot` + `grep` instead
     (hampstead, plaistow).
   - Board section sometimes loads collapsed and needs a click to expand
     (deerfield, fremont, goffstown, newfields).
   - Watch for other same-named-ish sections (a Planning Board
     "Appointment Committee," a "Community Facilities Subcommittee," etc.)
     interleaved under similar titles — filter by exact title text, not
     substring (merrimack, fremont, lee, durham, hampton, north_hampton).
   - Watch file size before concluding an agenda is empty: some are
     genuine 1-page stubs/cancelled notices under 2KB (fremont); others are
     small but text-dense and richer than the file size implies (laconia,
     londonderry, salem's index page).

2. **Node-based (older Drupal template)**: `/node/{id}/agenda` (or
   `/minutes`) lists years; drill into `/node/{id}/agenda/{year}` for a flat
   list of entries; each entry has its own detail-page slug (not always
   sequential/guessable — sometimes date-based, sometimes a counter, styles
   can be inconsistent even within one town). The detail page embeds (or,
   for minutes, redirects straight to) a static PDF under
   `/sites/g/files/{opaque-bucket-id}/f/{agendas|minutes}/{filename}.pdf`.
   Filenames are hand-typed by town staff, no fixed convention — always
   read the href off the listing. Confirmed `FetchUrl`-able directly, no
   session needed. Towns: derry, new_castle, nottingham, somersworth,
   barrington, lee, milton, durham (pre-2025 archive only — current
   Durham uses Agenda Center), north_hampton, rochester (Cloudflare-gated,
   see below), exeter (via a town-wide `/meetings` table rather than a
   per-board node listing).

3. **Newer per-meeting-page theme with a hotlink-protected `/media/{id}`
   endpoint**: no `/AgendaCenter` or `/node/.../agenda` routes. Planning
   Board hub links to individual meeting detail pages
   (`/planning-board/meeting/{slug}`), each linking files as `/media/{id}`
   — short but not sequential/guessable, and **not `FetchUrl`-able**: plain
   `requests` gets `403 Forbidden` every time. See "Hotlink protection"
   gotcha below for the fix. Towns: kingston, madbury.

Cloudflare sits in front of a few CivicPlus sites and specifically blocks
**headless** browser sessions (not plain `curl`/`requests` against the
static PDF paths themselves): rochester, north_hampton. Fix: use a headed
Playwright session to enumerate/navigate pages, then hand PDF URLs to plain
`curl`/`FetchUrl` for the actual download.

### Non-CivicPlus platforms (one-off vendors, 14 towns)

| Platform | Towns | Shape |
|---|---|---|
| **Legistar** (Granicus) | concord (current agendas only; minutes still on CivicPlus Archive Center) | `Calendar.aspx` town-wide meeting list; `View.ashx?M=A&ID=...` serves the PDF but needs same-origin fetch (see hotlink gotcha) |
| **Treeno** (DMS) | dover | One shared `Public_Meetings` cabinet for every board; session-scoped temp URLs (`/TempFiles/{token}_{name}.pdf`) generated only on click — must drive a browser to obtain each link, then plain `curl` works on the resulting temp URL |
| **CivicClerk** (CivicPlus-family SPA portal) | newmarket | React/MUI SPA; per-meeting `/event/{id}/files` page lists Agenda/Packet/individual attachments; the underlying `GetMeetingFileStream` API URL is TLS-incompatible with this env's `requests` — download via Playwright's browser click instead |
| **Legend Software** | northwood, gilford | `/entity/Planning-Board-{id}` hub; `/agendas/-{entityId}` listing; per-meeting page `/agenda/{Type}-{id}` (flat id counter shared across all boards); files at `/file/{fileId}/{filename}` — openly `FetchUrl`-able, no hotlink gate |
| **Municipal One** | brentwood | `/agendalist.aspx?categoryid={n}` is the best single scrape page; files at `/docview.aspx?doctype={agendaDoc\|minuteDoc\|packetDoc}&docid={id}` — hotlink-protected (403 on plain `requests`) *and* served as `.docx` |
| **TownCloud** | new_durham | Town-wide `/agendas` page mixes all boards; files at `towncloud.io/go/{slug}/agendas/{id}/{PDF|pdf_packet}/get_agenda_document_link` — openly fetchable, but the URL's last path segment is identical for every document, so the filename fallback silently collides; rename immediately after each fetch |
| **Munibit** | epsom | Deep nested accordion (year → month → item); "View" doesn't navigate to a visible URL — actual doc is served via `/api/blob/viewBlob?rf=t&i={token}`, and stale/cached tokens return `500` — must capture a fresh token from a live network request |
| **Revize** | hooksett, stratham | PHP-based (`agendas_minutes.php`); openly `FetchUrl`-able static paths, sometimes mirrored on a `cms3.revize.com`/`cms6.revize.com` subdomain that bypasses the accordion UI |
| **eCode360** (General Code) | raymond | `ecode360.com/{clientId}/documents/Planning_Board`, one page per category with in-page year anchors; files at `/​{clientId}/document/{id}.pdf` — openly fetchable |
| **DotNetNuke / "Portals"** | manchester | Single flat listing page, no per-meeting detail page; files under `/Portals/2/.../{date}_PB_AGENDA{_REV._{date}}.PDF` — openly fetchable; multiple `_REV.` revisions can coexist for one date, take the latest |
| **Custom WordPress** | south_hampton (files on Google Cloud Storage, not the WP media store), belmont, alton, strafford, seabrook | Standard `/wp-content/uploads/{YYYY}/{MM}/{filename}` media paths (except south_hampton), openly fetchable; upload-date folder doesn't always match meeting date |
| **Google Drive-hosted docs** | rollinsford | No town-CMS file store at all — Planning Board page links out to shared Drive folders; no direct PDF URL without working out Drive's own listing/file-id conventions |
| **Custom / other** | portsmouth (custom CMS + a plain static file host), exeter ("municodeWEB" on Drupal) | See individual files |

## Access gotchas (cross-town)

- **Browser-only downloads (Cloudflare challenge)**: kingston & madbury
  (`/media/{id}`) and brentwood (`/docview.aspx`) serve a Cloudflare
  "Just a moment..." 403 to *every* non-browser request - listing pages
  as well as files - so `FetchUrl` can't be used at all, with or without a
  Referer. An in-page `fetch()` gets challenged too. **Fix** (confirmed
  2026-09-21 on all three): in the headed `planscan` session, on any page of
  the town's site, click a native download link:
  `playwright-cli -s=planscan eval "() => { const a = document.createElement('a'); a.href = '/media/21201'; a.download = ''; document.body.appendChild(a); a.click(); }"`
  The browser saves the file (real filename) to `working/playwright_output/`
  - then `plan_entry.py ClaimDownload file=working/playwright_output/<f> dest=working/<town> [name=...]`
  checks it's a real PDF/.docx and moves it in, ready for `IngestPdfTool`.
  (Concord was previously listed here too; its 410s were an argument-
  parsing bug, now fixed - plain `FetchUrl` works for Legistar `View.ashx`.)
- **`.docx` instead of PDF**: hampton_falls (all documents), brentwood (all
  documents, in addition to the hotlink issue), gilford (at least some
  documents). Content-Type
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  (or bare `application/msword`). This project's PDF toolchain
  (`PdfExtractText`, `PdfKeywordScan`) can't process these directly — a
  **`.docx` text-extraction tool is a standing `TODO.txt` item**, not yet
  built. exeter also occasionally posts draft minutes as `.docx`.
- **Dual/legacy domains resolving to the same or a stale site**: bedford
  (`.gov`/`.org`, confirmed interchangeable), auburn (`.us`/`.gov`, *not*
  confirmed in sync), greenland (`.nh.gov` vs. legacy `-nh.com`), gilmanton
  (`.gov` vs. legacy `.org`), madbury (two more legacy domains, untested),
  deerfield (legacy `townofdeerfieldnh.com`), kingston (`.gov` vs. `.org`,
  untested), belmont NH vs. Belmont MA (different towns, don't confuse),
  milton NH vs. Milton MA/NY (different towns, don't confuse). Rye and
  Durham both note a full domain migration where the *old* hostname now
  404s/redirects — don't trust a cached old domain.
- **Stale/404 search-indexed URLs, live path is the standard one**:
  recurring across nearly every AgendaCenter town whose search-indexed hub
  page or node link no longer resolves (candia, chichester, east_kingston,
  epping, fremont, hudson, loudon, merrimack, allenstown). Always verify a
  cached node id/slug against live top-nav rather than trusting a search
  result directly; the live path is consistently `/agendacenter` +
  discovering the real Planning Board hub via top-nav → "Boards"-style
  listing page.
- **SPA / heavy client-side rendering**: newmarket's CivicClerk portal and
  epsom's Munibit accordion both need a beat before content/refs are
  usable — skeleton loaders or JS-driven fetches, not plain anchors.
- **Deep click-through nesting**: Munibit (epsom, 4 levels: category →
  year → month → item), Revize (hooksett, 3 levels: year → type → file).
  Most towns need at most one click (expand a collapsed board section).
- **A "Materials"/"Packet" file can be a short index/cover page, not the
  full packet**: salem's "Materials" ViewFile was a 3.7KB table of
  contents naming sub-documents without linking them; durham's "Meeting
  Material" link was similarly just a filename-listing cover sheet.
  Londonderry flags the same risk for its own "Materials" agendas (not yet
  sampled). Don't assume "Materials"/"Packet" == the actual packet without
  checking file size/content first.
- **Meeting-title metadata is free signal, parseable without opening a
  PDF**: status flags embedded directly in listing titles — "CANCELLED",
  "(Public Hearing)", "(Hearing Continued)", "(No Agenda)" (chester,
  bedford, laconia, gilford, northwood); some towns go further and put the
  applicant/address right in the title (danville, kensington, sandown,
  raymond's "Site Walk Notice" filings). Worth pre-filtering a scrape by
  title text alone before opening any PDF.
- **Case-type abbreviation keys**: some agendas define their own
  consistent case-type coding worth parsing (chester: APT/CD/CUP/HB/LLA/
  PH/PHC/SPR/SUB; auburn/raymond/lee/salem/laconia/sandown use a
  `{prefix}##-###`-style case number consistently).

## Document content patterns

- **Dominant case types** across all keyword scans: subdivision and site
  plan review are by far the most common (>70 combined hits across
  samples), then Conditional Use Permit, then condominium/lot-line-
  adjustment/special-exception. The standard `PdfKeywordScan` keyword list
  is well-tuned to what's actually in these agendas.
- **Richness varies enormously by town, independent of platform** — small
  file size does not mean low signal (laconia's 9.4KB agenda and
  londonderry's 9KB agenda were among the richest in the project; several
  small-town agendas under 50KB carried 0 hits and were genuinely
  administrative-only). Always sample more than one meeting/date before
  concluding a town is low-signal.
- **Three tiers of "where the real case detail lives"**:
  1. **Agenda/minutes alone is enough** — most towns. Case paragraphs give
     applicant + owner name, address, tax map/lot, zoning district, and a
     plain-English description directly (exeter, stratham, rye, north_hampton,
     concord's Legistar agendas, durham, most AgendaCenter towns).
  2. **A bundled "Packet"/"Materials" PDF** adds engineering drawings/
     exhibits beyond the agenda (exeter's Packet, dover's Agenda Materials,
     portsmouth's Packet, stratham's per-case plan sets) — often large
     (tens of MB) and partly-to-fully text-extractable; large CAD-exported
     plan sets are often partly rasterized (no selectable text on drawing
     pages) and better suited to `PdfRenderPages` on targeted sheets than
     bulk text extraction.
  3. **A dedicated, continuously-updated "leads" page** exists independent
     of any single meeting's agenda — the richest source type found:
     hampton's "Active Applications to the Planning Board" and stratham's
     "Public Hearing Notices" both list every currently-pending case with
     full detail and links to every submitted document/revision round.
     Rye's and north_hampton's closest analogs turned out to be stale/thin
     legal-notice archives, not true leads pages — check staleness (last
     document date vs. today) before trusting one as current. Salem and
     nottingham have unexplored candidate pages of this type
     ("Planning Board Activity", "Current Applications Before the Board")
     worth checking in a future pass.
- **Minutes are usually richer than agendas** (full narrative, motions,
  vote outcomes, approval conditions) but published later (rochester,
  portsmouth, north_hampton) — pair agenda (earliest signal of a new
  filing) with minutes (confirmation of approval status/scope) when both
  are available.

## Outstanding cross-project TODOs

- `.docx` text-extraction tool — needed for hampton_falls, brentwood,
  gilford (see gotcha above).
- Base64-decode-to-file step for hotlink-protected endpoints — needed for
  concord, kingston, madbury, brentwood (see gotcha above).
- Individual attachment/exhibit retrieval from Legistar (concord) and
  Salem's Materials index — case text names each attachment but no
  extractable link/URL was found for either.
- Confirm whether `auburnnh.us`/`.gov`, `kingstonnh.gov`/`.org`, and the
  legacy domains at greenland/gilmanton/madbury/deerfield are in sync or
  genuinely diverging content.

## Partial/unresolved towns (see `mvp_town_list.md` for status)

Rollinsford (Google Drive folder listing not fully explored), Pelham
(Agenda Center access pattern not resolved — the category/calendar-widget
click sequence needed wasn't worked out), Epsom (Munibit blob-token access
not resolved — needs a freshly-captured token, see gotcha above).
