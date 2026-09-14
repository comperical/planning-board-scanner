# Salem, NH — Planning Board Web Access

Investigated: 2026-09-14

Salem is one of the larger, more active Rockingham towns near the MA
border. Runs CivicPlus CivicEngage with the Agenda Center module — same
shape as the other Rockingham towns this session — plain PDFs, no bot
protection.

## Platform

- Main site: `https://www.salemnh.gov` (bare `salemnh.gov` also resolves).
- Planning Board hub: `/570/Planning-Board`; also a "Planning Board
  Activity" page (`/584/Planning-Board-Activity`) not yet explored.
- Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-6`.
- Salem also runs a separate news site, `news.salemnh.gov` ("Salem Town
  Hall Times"), which publishes plain-English **meeting recaps** per
  Planning Board session (e.g. "Salem NH Planning Board Recap - March 12,
  2026") — a promising *secondary* source worth checking in a future
  session: human-written summaries of what was discussed/decided could be
  faster to mine for project signal than parsing raw agenda PDFs.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`. Agenda links
  here are titled **"Planning Board Regular Meeting Materials"** and
  consistently carry a `?html=true` suffix (safe to strip, per the pattern
  seen elsewhere).
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- ⚠️ **The "Materials" PDF at this ViewFile URL is a short index/cover
  page, not the full packet** — the Aug 25, 2026 sample was only 3.7KB /
  445 characters of text, and turned out to be a **table of contents**
  listing the titles of several separate constituent PDFs (a merged-binder
  cover sheet), e.g.:
  - "2026 Zoning Amendments Memo and Legal Notice"
  - "15-18 Manor Parkway - Bluebird Self Storage" (with sub-files
    "Bluebird Salem Revised Plans", "Response to Town Comments", a color
    rendering)
  - "9 Northeastern Boulevard - SynQor Sign CUP"

  This is already useful signal (named applicants/projects/addresses show
  up in the index alone), but the actual plan sets/staff reports these
  reference are **not linked from the index text** in what `PdfExtractText`
  recovers — likely PDF-internal bookmarks/attachments or a
  Legistar-style packet structure. Getting the full sub-documents is an
  open problem for a future session (check for PDF attachments/link
  annotations, or whether CivicPlus exposes the merged source files
  individually elsewhere).
- Meetings: 2nd & 4th Tuesday, 7pm, Knightly Meeting Room, Salem Town Hall.

## Document content

- **Agenda/Materials PDF** (Aug 25, 2026, 3.7KB, index only): names two
  concrete active projects — **Bluebird Self Storage** (15-18 Manor
  Parkway) and a sign Conditional Use Permit for **SynQor** (9
  Northeastern Boulevard) — plus a pending 2026 Zoning Amendments item.
  Strong signal density for such a small file.

## Sample files downloaded

- `working/salem_nh/08252026.pdf` (Aug 25, 2026 — index/cover page)

## Open items for later

- Figure out how to reach the individual sub-document PDFs referenced in
  Salem's "Materials" index (plan sets, staff reports, revised plans) —
  the index alone under-represents what's actually available.
- Evaluate `news.salemnh.gov` Planning Board recap posts as an alternate,
  possibly higher-signal-per-byte data source.
