# Epsom, NH — Planning Board Web Access

Investigated: 2026-09-14. Access resolved: 2026-09-15 (scan_log #3).

Merrimack County town, northeast of Pembroke. Platform: **Munibit** (see
PATTERNS.md) — no bot protection encountered.

## Platform notes — working access path

- Main site: `https://www.epsomnh.gov`. Agendas & Minutes page:
  `/agendasandminutes` — a nested accordion tree (category → year → month
  → item, four click levels total; use `playwright-cli find "Planning
  Board"` to jump straight to the right tree nodes rather than expanding
  everything top-down). Category → `Planning Board Agendas` → year (e.g.
  `2026`) → month (e.g. `September`) → item, which has a **View** button.
- Clicking **View** fires a JS request to
  `/api/blob/viewBlob?rf=t&i={token}` and renders the PDF in an embedded
  Adobe PDF viewer (`iframe-occ-adobe-dc-view`) — confirmed this token is
  **session/same-origin-bound and does not work with plain `requests`**
  even when freshly captured (still 500s, same as the stale-token
  failure from initial recon).
- ⭐ **Working extraction method**: after clicking View, run
  `playwright-cli -s=planscan requests` to find the `viewBlob` GET request
  (200 status), note its index, then
  `playwright-cli -s=planscan response-body {index}` — this pulls the
  **already-fetched in-browser response body** straight to a local PDF
  file (`.playwright-cli/response-<timestamp>.pdf`), no `FetchUrl`/base64
  workaround needed since the browser already has the bytes. Move that
  file into `working/epsom_nh/` and `IngestPdfTool` it from there.
- The **"Planning Board Minutes"** tree node currently has CSS class
  `noFiles` (visible in its `<li>` attributes) — Epsom appears to only
  post **agendas** for this board right now, not minutes. Re-check on
  future scans in case that changes.
- Sample doc downloaded: `Planning Board Agenda 9.9.2026.pdf` (1 pg).

## Scan notes (2026-09-25)

- Tree path: `find "Planning Board Agendas"` -> click -> `find "2026"` ->
  click -> `find "September"` -> click -> `find "View"` shows each item's
  `View` button ref. Two Sept items appear (9.9.2026 and 9.23.26), newest
  first. Click a View button, then `requests` (look for the 200
  `viewBlob` GET) and `response-body <index>`.
- ⚠️ While the Adobe PDF viewer dialog is open it blocks clicks on the
  rest of the tree - `goto` the page again before opening another month.
- Older months (Aug/Jul/Jun/May 2026) exist but hadn't been pulled as of
  2026-09-25.

## Scan notes (2026-10-25)

- **Planning Board Minutes now exist** (no longer `noFiles`): tree has
  2026 and 2025; 2026 has Sep, Aug, Jul, Jun... Pulled 9.9, 9.23, 8.12,
  8.26 minutes. Jul and earlier minutes/agendas not pulled yet.
- Faster clicks after `goto`: use locators, e.g.
  `click "getByRole('treeitem', { name: 'Planning Board Minutes' })"`, then
  `...getByRole('treeitem', { name: '2026' })`, month, then
  `click "getByRole('treeitem', { name: 'Planning Board Minutes 8.12.26' }).getByRole('button', { name: 'View' })"`.
  The viewBlob request was index 33 each time; `response-body 33` then
  `mv .playwright-cli/response-*.pdf working/epsom_nh/<name>.pdf` (plain mv works).

## Open items for later

- None blocking — access path fully resolved. Future scans: repeat the
  View → requests → response-body sequence per new agenda item found
  under `Planning Board Agendas`.
