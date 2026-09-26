# Rollinsford, NH — Planning Board Web Access

Investigated: 2026-09-14. Access resolved: 2026-09-15 (scan_log #2).

Rollinsford is the only town in this project whose planning documents are
hosted entirely on **Google Drive** (see PATTERNS.md), not any town-CMS
file store. Main site is custom WordPress-style (`rollinsford.nh.us`),
but only links out to shared Drive folders. No bot protection on the town
site itself.

## Platform notes — working access path

- Planning Board hub: `/boards-committees/planning-board/` — description/
  members only, no documents.
- **Minutes & Agendas page**: `/minutes-agendas/` — accordion, one section
  per board. The "Planning Board" section link must actually be **clicked**
  (its content isn't in the static page load) to reveal three Google Drive
  shared-folder links: **Public Hearing Notices**, **Meeting Minutes**,
  **Site Review Documents**.
- **Meeting Minutes** folder nests by year as subfolders (`2008-2011 All
  PB Files`, `2014_ PB Minutes` ... `2026: PB Mintues` [sic, typo in the
  folder name itself]) — open the year subfolder to reach actual PDFs.
  Filenames are inconsistent/free-text (e.g. `RPB Mins 7.14. 2026
  DRAFT.pdf`, `RPB Non Public 3.3.26.pdf`).
- **Downloading a file**: click the file row to select it, then click the
  "Download" icon button that appears. **The first click per session
  often 503s** behind a Google reCAPTCHA challenge
  (`drive.usercontent.google.com/download?...&confirm=t` returns 503) —
  clicking Download a second time on the same file succeeds and
  `playwright-cli` auto-saves it to `.playwright-cli/<name>.pdf`, same as
  a normal browser download. No `FetchUrl`/base64 workaround needed once
  past that hiccup.
- **Public Hearing Notices** folder was **empty** as of 2026-09-15 (no
  sign-in wall issue - genuinely no files in it right now, confirmed via
  screenshot). Worth re-checking on future scans in case it starts
  getting used, since it's the folder most likely to carry rich per-
  project detail (site plans, applicant info) if the town starts filling
  it.
- Sample doc downloaded: `RPB Mins 7.14.2026 DRAFT.pdf` (3 pg, from the
  2026 Meeting Minutes subfolder).

## Direct folder URLs (confirmed 2026-09-25 - no accordion click needed)

The Drive links ARE in the static HTML of `/minutes-agendas/` (`eval` over
`a[href*="drive.google"]`; the Planning Board trio is the last group before
the second "Public Hearing Notices"). Planning Board folders:

- Meeting Minutes: `https://drive.google.com/drive/folders/1qDRJ0czQGW4JF3vhdQ6DXMHvxH3pwy9C`
  - 2026 subfolder: `.../folders/1SPuXwhQf-zGrqE-RBokfLuWQ8bjJbZ6H`
    (has `RPB Mins {M.D.YY}.pdf` for 1/6, 2/4, 3/3 (+Non Public), 4/7, 6/2,
    7/14 DRAFT; nothing later as of 9/25 - minutes lag ~1 week+)
- Site Review Documents: `.../folders/1D_bpMWApqK007_rYjgO42qhttyu5ZWBr` -
  checked 2026-09-25: only two old project subfolders ("15 Pease Lane
  (Cantwell)" Nov 2025, "Dover Gaming 2024"), nothing current.
- Public Hearing Notices: `.../folders/1uuBZywqaufT-xcTeFt8ck9r1RiCTOJ0e` -
  still EMPTY on 2026-09-25.
- List a folder without screenshots: `goto` it, then `eval` over
  `[data-id]` and read `innerText` (file name, date, size). Subfolder ids
  are the `data-id` values. No agendas are posted for this board at all.

## Open items for later

- Haven't yet checked the **Site Review Documents** folder (likely the
  richest source of per-project detail, similar to other towns'
  "materials packet" documents) - do this on the next scan pass.
- Filenames don't reliably carry the meeting date in a parseable format
  (compare `RPB Mins 7.14. 2026 DRAFT.pdf` vs `RPB Mins 6.2.26.pdf`) -
  `doc_date` will likely need to be read out of each PDF by hand rather
  than parsed from the filename.
