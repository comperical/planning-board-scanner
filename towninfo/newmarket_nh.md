# Newmarket, NH — Planning Board Web Access

> **Update 2026-09-21 - better method:** skip the portal UI. From any `newmarketnh.portal.civicclerk.com` page, in-page `fetch('https://newmarketnh.api.civicclerk.com/v1/Events?$filter=startDateTime ge 2026-07-01T00:00:00Z&$orderby=startDateTime desc')` (CORS-open) lists events with `publishedFiles` (type + fileId). Download each via in-page `fetch(.../v1/Meetings/GetMeetingFileStream(fileId={id},plainText=false))` -> blob -> `<a download>` click -> `ClaimDownload`. The portal's home feed only shows from the current month on.

Investigated: 2026-09-12

Platform: **CivicClerk** SPA portal (see PATTERNS.md), a different
CivicPlus-family product from Dover's Treeno. No bot protection.

## Platform notes

- Main town site: `https://www.newmarketnh.gov` — CivicPlus CivicEngage
  (`/DocumentCenter/View/{id}/...`, `/169/Boards-Commissions`-style
  paths). Current agendas/packets/minutes live on the separate SPA
  portal: `https://newmarketnh.portal.civicclerk.com/`. The Planning
  Board's own CivicEngage page (`/197/Planning-Board`) links out to the
  portal, plus a `/507/Planning-Board-Minutes` DocumentCenter page for
  **pre-March-2025** minutes (older, static PDFs, not explored in depth).
- Home page (`/`) is a single town-wide **Events** feed. Clicking a
  meeting → `/event/{eventId}/overview`, tabs for Overview / Media /
  **Meeting Files** / Share. **Meeting Files** (`/event/{eventId}/files`)
  lists Agenda / Agenda Packet / Other, plus a **per-attachment**
  breakdown of everything referenced (individual site-plan PDFs, draft
  minutes, master-plan chapter PDFs, etc.), each independently
  downloadable — the richest per-document granularity seen in this
  project (e.g. separate "Planset" / "SMP" buttons for one meeting's site
  plan case).
- Agendas typically posted 1-2 weeks ahead; future-dated placeholder
  events show "If required, the agenda information will be here once
  published."

## ⚠️ Access method — environment-specific gotcha

- Clicking a download button opens a format-choice menu; the actual PDF
  is served from `{town}.api.civicclerk.com/v1/Meetings/
  GetMeetingFileStream(fileId={id},plainText=false)`. `{id}` is a small
  sequential integer visible in the button's DOM id
  (`downloadFilesMenu-{id}`).
- **This URL is not reachable with this environment's `FetchUrl`** —
  fails with `SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION]` (the API
  host needs a newer TLS stack than this environment's
  Python/LibreSSL 2.8.3 supports — a local tooling limitation, not a site
  block; loads fine in-browser).
- **Working pattern**: click the "Download {Type} (PDF)" menu item in
  Playwright — triggers a real browser download saved under
  `.playwright-cli/{filename}.pdf`; copy into `working/newmarket_nh/`
  before running the PDF tools.
- Occasional flaky click targeting: MUI tooltips can linger and intercept
  clicks — if a click times out with "subtree intercepts pointer events",
  re-navigate to the files page fresh rather than fighting the stale
  tooltip.

## Document content

- **Agenda PDF** (Aspose-generated, small): per-item structure similar to
  Exeter's — full paragraph per case citing applicant, RSA/ordinance
  section, tax map & lot, zoning district, project description, and
  continuance status. Sample (Aug 11, 2026 meeting): RKJ 37 Exeter LLC's
  minor site plan for demolishing a single-family home and building a
  3-unit townhouse at 37 Exeter Road (Tax Map U3, Lot 38, VC-C zoning) —
  continued to Sept 8, 2026. Also procedural business (master plan
  chapter adoption hearing, minutes approval).
- **Per-attachment files**: for a site plan case, expect a `Planset` and
  often a separate `SMP` (Stormwater Management Plan) PDF as their own
  downloadable items.
- **Agenda Packet**: a bundled version also exists — not successfully
  pulled down this session (menu-selection issue; the individual-
  attachment route already surfaces the same content more granularly).

## Sample downloads (in `working/newmarket_nh/`)

- `081126_PB_Agenda.pdf` — Aug 11, 2026 agenda (RKJ 37 Exeter LLC
  townhouse site plan, master plan adoption hearing)

## Open questions / not yet checked

- Whether `GetMeetingFileStream` truly needs no auth from a plain HTTP
  client with a modern TLS stack — worth retesting if this environment's
  Python/OpenSSL is ever upgraded.
- Whether a CivicClerk API endpoint lists an event's files as JSON.
- Content of the pre-March-2025 `/507/Planning-Board-Minutes` archive.
- Whether the Agenda Packet PDF adds anything beyond the individual
  attachment files.
- Whether Newmarket's Technical Review Committee posts through this same
  portal or elsewhere.
