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

## Open items for later

- None blocking — access path fully resolved. Future scans: repeat the
  View → requests → response-body sequence per new agenda item found
  under `Planning Board Agendas`.
