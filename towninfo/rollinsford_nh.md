# Rollinsford, NH — Planning Board Web Access

Investigated: 2026-09-14

Rollinsford is the **first town in this project whose planning documents
are hosted entirely on Google Drive**, not any town-CMS file store. Main
site is a custom WordPress-style site (`rollinsford.nh.us`), but it only
links out to shared Drive folders for actual documents. No bot protection
on the town site itself.

## Platform

- Main site: `https://rollinsford.nh.us` — custom WordPress-family site,
  not CivicPlus.
- Planning Board hub: `/boards-committees/planning-board/` — board
  description/members only, no documents.
- **Minutes & Agendas page**: `/minutes-agendas/` — an accordion-style page
  with one section per board (Select Board, Budget Committee, Planning
  Board, Zoning Board). Clicking "Planning Board" reveals three **Google
  Drive shared-folder links**, not individual document links:
  - "Public Hearing Notices" →
    `https://drive.google.com/drive/folders/1uuBZywqaufT-xcTeFt8ck9r1RiCTOJ0e`
  - "Meeting Minutes" →
    `https://drive.google.com/drive/folders/1qDRJ0czQGW4JF3vhdQ6DXMHvxH3pwy9C`
  - "Site Review Documents" →
    `https://drive.google.com/drive/folders/1D_bpMWApqK007_rYjgO42qhttyu5ZWBr`

## Access notes

- The town page itself has no per-document URLs to scrape — everything
  routes through these three Drive folders.
- Opening a folder link in the browser loads the standard Google Drive
  folder UI (no sign-in required to view, per the `?usp=share_link` share
  type), but the file listing renders via client-side JS inside an iframe
  that didn't finish populating in this session's single-snapshot check —
  did not confirm actual file names/PDFs this pass.
- This access pattern is fundamentally different from every other town in
  this project: there's no direct PDF URL to `FetchUrl`, and Google
  Drive's own API/UI conventions (folder listing, per-file `/view` or
  `/export` URLs) would need to be worked out rather than reusing the
  CivicPlus/Legend Software/Municipal One patterns seen elsewhere.

## Open items for later

- Finish exploring the three Drive folders (wait for the file list to
  load, or find Drive's public-folder listing pattern) to get actual
  document names/dates and confirm whether individual files are
  downloadable via plain `FetchUrl` (Drive file `/uc?export=download&id=`
  URLs are typically fetchable without a browser once the file id is
  known) or need the same in-page-fetch treatment as hotlink-protected
  towns.
- No sample PDF downloaded this session — Rollinsford has no
  `working/rollinsford_nh/` content yet beyond this write-up.
