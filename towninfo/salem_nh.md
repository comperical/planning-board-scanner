# Salem, NH — Planning Board Web Access

Investigated: 2026-09-14

Salem is one of the larger, more active Rockingham towns near the MA
border. Platform: standard CivicPlus Agenda Center (see PATTERNS.md) —
no bot protection.

## Platform notes

- Main site: `https://www.salemnh.gov` (bare domain also resolves).
  Planning Board hub: `/570/Planning-Board`; also a "Planning Board
  Activity" page (`/584/Planning-Board-Activity`) not yet explored.
  Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-6`.
- Separate news site `news.salemnh.gov` ("Salem Town Hall Times")
  publishes plain-English **meeting recaps** per Planning Board session —
  a promising secondary source worth checking in a future session.
- Agenda links titled **"Planning Board Regular Meeting Materials"**,
  consistently carry `?html=true` (safe to strip).
- ⚠️ **The "Materials" PDF at this ViewFile URL is a short index/cover
  page, not the full packet** (see PATTERNS.md gotcha) — the Aug 25, 2026
  sample was only 3.7KB / 445 characters, a table of contents listing
  the titles of several separate constituent PDFs (a merged-binder cover
  sheet), e.g. "2026 Zoning Amendments Memo and Legal Notice", "15-18
  Manor Parkway - Bluebird Self Storage" (with sub-files), "9
  Northeastern Boulevard - SynQor Sign CUP". Already useful signal, but
  the referenced plan sets/staff reports are **not linked** in what
  `PdfExtractText` recovers — likely PDF-internal bookmarks/attachments
  or a Legistar-style packet structure. Getting the full sub-documents is
  an open problem.
- **RESOLVED 2026-09-24: full packet = `ViewFile/Agenda/_{date}-{id}?packet=true`**
  (a second link on the same listing row). It merges the index plus every
  constituent PDF - e.g. 9/22/2026 packet was 100MB / 186pp, 10/13 was
  10MB / 17pp. Downloads as `{MMDDYYYY}Plus.pdf`. Large packets take a
  while; poll the session (`eval "() => 1"`) until the "Downloaded file"
  event appears before `ClaimDownload`.
- **CHANGE 2026-09-24:** plain `FetchUrl` now 403s (Cloudflare) on
  ViewFile URLs. Browser `<a download>` + `ClaimDownload` works.
- Agendas are posted ~3 weeks ahead (10/13 materials up on 9/24).
- Meetings: 2nd & 4th Tuesday, 7pm, Knightly Meeting Room, Salem Town
  Hall.

## Document content

- **Agenda/Materials PDF** (Aug 25, 2026, 3.7KB, index only): names two
  concrete active projects — **Bluebird Self Storage** (15-18 Manor
  Parkway) and a sign Conditional Use Permit for **SynQor** (9
  Northeastern Boulevard) — plus a pending 2026 Zoning Amendments item.
  Strong signal density for such a small file.

## Sample files downloaded

- `working/salem_nh/08252026.pdf` (Aug 25, 2026 — index/cover page)

## Open items for later

- ~~Figure out how to reach the individual sub-document PDFs referenced in
  Salem's "Materials" index.~~ Done - use `?packet=true` (see above).
- Evaluate `news.salemnh.gov` Planning Board recap posts as an alternate,
  possibly higher-signal-per-byte data source.
