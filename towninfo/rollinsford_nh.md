# Rollinsford, NH — Planning Board Web Access

Investigated: 2026-09-14

Rollinsford is the only town in this project whose planning documents are
hosted entirely on **Google Drive** (see PATTERNS.md), not any town-CMS
file store. Main site is custom WordPress-style (`rollinsford.nh.us`),
but only links out to shared Drive folders. No bot protection on the town
site itself. **Partial — no sample PDF downloaded.**

## Platform notes

- Planning Board hub: `/boards-committees/planning-board/` — description/
  members only, no documents.
- **Minutes & Agendas page**: `/minutes-agendas/` — accordion, one
  section per board. Clicking "Planning Board" reveals three Google
  Drive shared-folder links (not individual document links): "Public
  Hearing Notices", "Meeting Minutes", "Site Review Documents".
- Opening a folder link loads the standard Drive folder UI (no sign-in
  required, `?usp=share_link` share type), but the file listing renders
  via client-side JS inside an iframe that didn't finish populating in
  this session's single-snapshot check — actual filenames not confirmed.
- This access pattern is fundamentally different from every other town:
  there's no direct PDF URL to `FetchUrl` — Drive's own listing/per-file
  `/uc?export=download&id=` conventions would need to be worked out.

## Open items for later

- Finish exploring the three Drive folders (wait for the file list to
  load) to get actual document names/dates and confirm whether
  individual files are downloadable via plain `FetchUrl` (Drive
  `/uc?export=download&id=` URLs are typically fetchable without a
  browser once the file id is known) or need the same in-page-fetch
  treatment as hotlink-protected towns.
