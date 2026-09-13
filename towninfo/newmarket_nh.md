# Newmarket, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Main town site: `https://www.newmarketnh.gov` — CivicPlus **CivicEngage** (same family as Rochester/Exeter's Drupal-ish CMS: `/DocumentCenter/View/{id}/...` static file store, `/169/Boards-Commissions`-style numeric paths).
- **Current agendas/packets/minutes live on a separate SPA portal**: `https://newmarketnh.portal.civicclerk.com/`, product **CivicClerk** (a different CivicPlus-family product from Dover's Treeno). Heavy client-side rendering (React/MUI) — pages show skeleton loaders, need a beat before content/refs are usable.
- No Cloudflare or bot-challenge encountered on either the CivicEngage site or the CivicClerk portal.
- The Planning Board's own CivicEngage page (`/197/Planning-Board`) links out to the portal via "Planning Board: Agendas & Packets" → `https://newmarketnh.portal.civicclerk.com/`, plus a `/507/Planning-Board-Minutes` DocumentCenter page for **pre-March-2025** minutes (older, static PDFs, not yet explored in depth).

## CivicClerk portal structure

- Home page (`/`) is a single town-wide **Events** feed — every board's meetings, past and upcoming, in one infinite-scroll list ("Load more previous/upcoming events" buttons), each row tagged with a category (e.g. "Planning Board", "Town Council", "Budget Committee").
- Clicking a meeting (or its "Go To Event Media" link) goes to `/event/{eventId}/overview`, with tabs for **Meeting Overview**, **Meeting Media** (video), **Meeting Files**, **Share Meeting**.
- **Meeting Files** tab (`/event/{eventId}/files`) lists files grouped as **Agenda**, **Agenda Packet**, **Other**, each with its own download button — plus, further down, a **per-attachment** breakdown of everything referenced by the agenda (individual site-plan PDFs, draft minutes, master-plan chapter PDFs, etc.), each independently downloadable. This is the richest per-document granularity seen in this project so far — e.g. for one meeting we saw separate buttons for "Planset 37ExeterRoad" and "SMP 37ExeterRoad" (site plan / stormwater management plan) as their own files, not buried inside one giant packet.
- Not every listed meeting has files yet — agendas are typically posted 1-2 weeks ahead (the list shows "Agenda Posted on: {date}" once available) and future-dated placeholder events show "If required, the agenda information will be here once published."

## Access method — IMPORTANT (environment-specific gotcha)

- Clicking a download button opens a **format-choice menu** (e.g. "Agenda (PDF)" / "Agenda (Plain Text)") and the actual PDF is served in-browser from a stable, discoverable API URL pattern:
  ```
  https://{town}.api.civicclerk.com/v1/Meetings/GetMeetingFileStream(fileId={id},plainText=false)
  ```
  (`{town}` = `newmarketnh` here). `{id}` is a small sequential integer visible in the button's DOM id (`downloadFilesMenu-{id}`) and in the pdf.js viewer URL once opened — not derivable from the date, but easy to read off the Meeting Files page.
- **This URL is not reachable with this environment's `FetchUrl`/`requests`** — it fails with `SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION]`, because the API host apparently requires a newer TLS stack than this environment's Python/LibreSSL 2.8.3 supports. This is a local tooling limitation, not a site block — the same URL loads fine inside the Playwright browser (confirmed via `requests`/`response-body`, HTTP 200).
- **Working pattern for Newmarket**: don't try `FetchUrl` on the API URL. Instead, click the "Download {Type} (PDF)" menu item in Playwright — this triggers a real browser download that playwright-cli saves under `.playwright-cli/{filename}.pdf` (reported in the command's console-log lines: "Downloaded file ... to ..."). Copy that file into `working/newmarket_nh/` before running the `PdfExtractText`/etc. tools (which require `working/`-rooted paths).
- Occasional flaky click targeting: MUI tooltips can linger and intercept clicks on the small icon-only download buttons — if a click times out with "subtree intercepts pointer events", re-navigate to the files page fresh (`goto` the same `/event/{id}/files` URL) rather than fighting the stale tooltip.

## Document content

- **Agenda PDF** (Aspose-generated, small): per-item structure very similar to Exeter's — full paragraph per case citing the applicant, RSA/ordinance section, tax map & lot, zoning district, project description, and any continuance status. Sample (Aug 11, 2026 meeting) had one active case: RKJ 37 Exeter LLC's minor site plan for demolishing a single-family home and building a 3-unit townhouse at 37 Exeter Road (Tax Map U3, Lot 38, VC-C zoning) — continued to the Sept 8, 2026 meeting. Also carried procedural business (master plan chapter adoption hearing, minutes approval).
- **Per-attachment files**: for a site plan case, expect a `Planset` and often a separate `SMP` (Stormwater Management Plan) PDF as their own downloadable items — likely the actual engineering drawings, worth pulling for detail beyond the agenda text.
- **Agenda Packet**: a bundled version also exists (own download button) — not successfully pulled down in this recon session (menu-selection issue after the individual-attachment discovery made it lower priority); the individual-attachment route already surfaces the same content more granularly.

## Sample downloads (in `working/newmarket_nh/`)

- `081126_PB_Agenda.pdf` — Aug 11, 2026 Planning Board agenda (RKJ 37 Exeter LLC townhouse site plan, master plan adoption hearing)

## Comparison to Exeter / Dover / Rochester, NH

| | Rochester | Dover | Exeter | Newmarket |
|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicPlus CivicEngage + **CivicClerk** portal |
| Bot protection | Cloudflare hard-blocks headless | None | None | None |
| PDF URLs | Stable, static, guessable | Session-scoped temp URLs | Static, permanent, node-id not guessable | Static REST API URL by small integer `fileId`, but **unreachable by this env's `requests`/TLS stack** — must download via browser |
| Attachment granularity | Agenda only | Agenda + one bundled Materials PDF | Agenda + one bundled Packet PDF | Agenda + bundled Packet **+ every individual submitted document as its own file** |
| Archive scope | Per-board node listing | One shared Treeno cabinet | One shared `/meetings` table | One shared town-wide Events feed on a separate SPA portal |

## Open questions / not yet checked

- Whether the `GetMeetingFileStream` API URL truly needs no auth/cookies from a plain HTTP client with a modern TLS stack (strongly suspected, based on it loading in-browser with no sign-in) — worth retesting if this environment's Python/OpenSSL is ever upgraded, since that would make Newmarket's PDFs directly `curl`-able like Rochester's.
- Whether there's a CivicClerk API endpoint that lists an event's files (and their `fileId`s) as JSON, which would let a script enumerate files without a full Playwright click-through per meeting.
- Content and structure of the pre-March-2025 `/507/Planning-Board-Minutes` DocumentCenter archive (separate, older, static-PDF system).
- Whether the Agenda Packet PDF (not successfully downloaded this session) adds anything beyond what the individual attachment files already show.
- Whether Newmarket's Planning Board Technical Review Committee (mentioned in the sidebar) posts through this same CivicClerk portal or elsewhere.
