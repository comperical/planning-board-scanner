# Concord, NH — Planning Board Web Access

Investigated: 2026-09-12

Concord (the state capital, a city not a small town) is notably more complex than every other NH municipality studied in this project so far — it runs **Legistar** (a Granicus legislative-management product used by larger cities/councils), not a CivicPlus/Drupal/WordPress town site. This write-up documents the extra steps that requires.

## Platform

- Main city site: `https://www.concordnh.gov` — CivicPlus CivicEngage, same family as other NH towns (Rochester, Exeter's cousin platforms). The Planning Board hub page is `/273/Planning-Board`.
- **Current agendas (Feb 2017–present) are hosted entirely on a separate system**: `https://concordnh.legistar.com` (Legistar/Granicus). Pre-2017 agendas, and it turns out **all years of minutes including current**, are mirrored on CivicPlus's own **Archive Center** module (`concordnh.gov/Archive.aspx`).
- No Cloudflare or bot-challenge on either system — both load fine headless.

## Legistar structure (agendas)

- `https://concordnh.legistar.com/Calendar.aspx` — one town-wide meeting calendar (all boards/commissions), filterable by "Departments Dropdown" (misleadingly labeled; it's actually the body/committee filter) and date range. Columns: Name, Meeting Date, Time, Location, Meeting Details, Agenda, Minutes, Video.
- Each meeting row links to:
  - `MeetingDetail.aspx?ID={meetingId}&GUID={guid}&Options=info|&Search=` — an HTML agenda with one row per item, each linking to `LegislationDetail.aspx?ID={matterId}&GUID={guid}` — Legistar's per-"Matter" (case) detail page, with its own file number (e.g. `26-343`), type, status, and history.
  - `View.ashx?M=A&ID={meetingId}&GUID={guid}` — the same agenda as a single flattened PDF (this is what CivicEngage's Planning Board page links to under "Agendas").
- Legistar's `LegislationDetail.aspx` page for an individual matter did **not** show a populated attachments list during this recon (renders "0 records" in its grid) — the actual attachment documents (Staff Report, Civil Plans, Architectural Plans, Landscape Plans, Supplemental, Record of Recommendation, Application, Zoning Compliant Submission, etc.) are named as plain text under each item's "Attachments:" heading **inside the agenda PDF itself**, presumably as clickable link annotations in the PDF that weren't resolved to URLs in this session (our PDF tools extract text only, not link annotations). **Getting the individual attachment PDFs is an open problem for a future session** — likely solvable via a Legistar `MatterAttachment`-style endpoint or by parsing PDF link annotations directly, but not solved here.

## ⚠️ Access gotcha: Legistar's `View.ashx` needs a same-origin browser fetch, not plain `requests`

- `FetchUrl` (plain Python `requests`, no browser) gets **`410 Gone`** on every `View.ashx?...` URL, every time — confirmed reproducible, not transient.
- Comparing headers: the browser's successful request carried `referer: https://concordnh.legistar.com/Calendar.aspx`; a bare `requests.get()` with no referer is what gets the 410. This looks like a deliberate anti-hotlinking/anti-scraping check on Legistar's file-serving handler.
- **Playwright's own automatic file-download flow doesn't cleanly capture the bytes either** here: Chrome's native PDF viewer intercepts the navigation, and `response-body` on the "obvious" request in the log can return the PDF-viewer's wrapper HTML shell instead of the actual PDF bytes (a red herring — check `file <path>` / look for `%PDF` magic bytes before trusting a saved response).
- **Working pattern that succeeded**: use `playwright-cli eval` to run an in-page `fetch()` (same-origin, so it automatically carries the right `Referer`/cookies) against the `View.ashx` URL, base64-encode the response body, and decode it back into a file:
  ```
  playwright-cli -s=planscan eval "async () => { const resp = await fetch('<View.ashx URL>'); const buf = await resp.arrayBuffer(); const bytes = new Uint8Array(buf); let bin=''; for (let i=0;i<bytes.length;i++) bin += String.fromCharCode(bytes[i]); return { status: resp.status, len: bytes.length, b64: btoa(bin) }; }"
  ```
  then decode the returned `b64` field with a small Python/`base64` snippet into `working/concord_nh/...pdf`. Verify `len` matches the file size before trusting it. This is the same category of problem as Newmarket's CivicClerk API (`GetMeetingFileStream`), but a different root cause (anti-hotlink header check vs. a TLS-stack incompatibility) and a different fix (in-page `fetch` vs. click-and-copy-from-downloads).

## Archive Center (minutes, and pre-2017 agendas) — the easy path

- `https://concordnh.gov/Archive.aspx?AMID=48` = Planning Board **Minutes**, and it is **not** a stale/legacy-only archive — confirmed current through Aug 19, 2026 (drafts included, e.g. "August 19, 2026 (Draft)"). Each entry links to `Archive.aspx?ADID={id}`, which redirects straight to a static PDF.
- `https://concordnh.gov/ArchiveCenter/ViewFile/Item/{id}` is the same underlying document store (same `{id}` numbering as `ADID`) and — unlike Legistar's `View.ashx` — **works fine with plain `FetchUrl`, no browser needed**. Confirmed: fetched a 390KB, 32,000-character, fully text-extractable April 15, 2026 minutes PDF this way with zero friction.
- `https://concordnh.gov/Archive.aspx?AMID=49` = Planning Board **Agendas**, but is explicitly labeled "Agendas - Prior to February 2017" on the Planning Board hub page — i.e. **current agendas are NOT mirrored here**, only on Legistar. So: use the easy Archive Center path for minutes (any date) and pre-2017 agendas; use the harder Legistar `eval`-fetch path for any agenda from Feb 2017 onward.

## Document content

- **Agenda PDF** (via Legistar `View.ashx?M=A`): the richest, most structured agenda content found in this entire project. Sample (Sept 16, 2026, 9 pages) organized into Consent Agenda (Design Review / Determination-of-Completeness items), non-consent Design Review Applications, Public Hearings, and "Site Plan, Subdivision and Conditional Use Permit Applications" — each item giving applicant + owner/property-owner names, a precise project description (square footage, unit counts, building stories), Tax Map/Lot, zoning district(s), the city's own case number(s) (e.g. `PL-SPR-2026-0068`, `2026-092`), continuance status, and a named list of every attachment filed for that case. Real projects in the sample: a 110-unit, 4-story, 133,600-sq-ft multifamily building at 270 Loudon Road; a 24-lot major subdivision off Mooreland Avenue/Heather Lane; a car-dealership conversion at 110 Manchester Street; an 8,160-sq-ft micro-data-center/office/garage building at 52 Locke Road.
- **Minutes PDF** (via Archive Center): sample was 32,000 characters of standard motion-and-discussion narrative, fully text-extractable.

## Sample downloads (in `working/concord_nh/`)

- `09.16.2026_PB_Agenda.pdf` — Sept 16, 2026 agenda, 9 pages, fetched via the Legistar `eval`-fetch workaround (see above)
- `20260415.pdf` — April 15, 2026 minutes, fetched via the plain, `FetchUrl`-able Archive Center path

## Comparison to other NH towns studied

| | Typical CivicPlus town (Rochester/Exeter/Hampton/etc.) | Concord |
|---|---|---|
| Platform | Drupal / Agenda Center / WordPress | **Legistar** (Granicus) for current agendas + CivicPlus Archive Center for minutes |
| Bot protection | Varies (Cloudflare on some) | None on either system |
| PDF access | Static `FetchUrl`, or a browser click-through | **Split**: minutes are plain `FetchUrl`-able; agendas need an in-page `fetch()`+base64 workaround due to a Referer check |
| Case-level detail | Ranges from terse (Hampton, Seabrook) to rich (Exeter, Stratham) | Extremely rich and uniformly structured — case numbers, tax map/lot, zoning, attachment names, all in every item |
| Attachment documents | Usually a single bundled packet, or per-file links | Named per-case in the agenda text but **individual attachment PDFs not yet successfully retrieved** — open problem |

## Open questions / not yet checked

- How to retrieve the individual named attachments (Staff Report, Civil Plans, Architectural Plans, etc.) referenced inside each agenda item — likely requires either extracting PDF link-annotation URLs (not currently in this project's PDF toolset) or finding a Legistar `MatterAttachment`/API endpoint that lists them by matter ID.
- Whether Legistar's search page (`Legislation.aspx`) offers a way to query/filter matters by type (e.g. all major site plan applications) across meetings, which could be a more efficient scan method than paging through individual meeting agendas.
- Whether the `eval`-based fetch-and-base64-decode approach could be simplified into a small reusable helper rather than a one-off snippet each time.
- Whether Concord has anything resembling Hampton's/Stratham's standalone "Active Applications" leads page — not checked this session given time spent on the Legistar access mechanics.
