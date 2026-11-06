# Milton, NH — Planning Board Web Access

Investigated: 2026-09-14

Strafford County town, Maine border, north of Farmington. Platform:
node-based CivicPlus (see PATTERNS.md). **Cloudflare since ~2026-10-03**:
listing pages 403 headless, pass headed; static `sites/g/files` PDFs
still `FetchUrl`-able.

## Platform notes

- Main site: `https://www.miltonnh-us.com`. Planning Board hub:
  `/planning-board`. Agendas index: `/node/107/agenda`,
  `/node/107/agenda/2026` for current year.
- ⚠️ Search results also surfaced `miltonma.gov` (Milton,
  *Massachusetts*) and `miltonny.gov` — don't confuse domains;
  `miltonnh-us.com` is the correct NH town.
- Entry slugs mostly follow `/planning-board/agenda/planning-board-
  meeting-agenda-{n}` (sequential counter), with an occasional
  differently-named entry (`notice-public-hearings`) interleaved.
- Static PDF path: `sites/g/files/vyhlif916/f/agendas/milton_pb_agenda_
  {MM-DD-YY}.pdf`. Meetings: 1st & 3rd Tuesday monthly, 6pm.

## Minutes (as of 2026-10-27)

- Minutes index: `/node/107/minutes/2026`; entries at
  `/planning-board/minutes/planning-board-draft-meeting-minutes-{n}`.
  Visiting an entry URL in the headed browser triggers an immediate file
  download (redirect to file), e.g. `working/playwright_output/...`.
- Newer minutes (10/6 approved, 10/20 draft) are legacy binary `.doc`
  (OLE), NOT pdf/.docx: `ClaimDownload` and `IngestPdfTool` reject them.
  Older ones were PDFs (`..._draft_minutes-bww_rev.pdf`). Needs a .doc
  to .docx/.pdf conversion step (or tool support) to ingest.
- Agenda entries often carry no usable file for non-regular items; 10/6
  had only a public hearing notice (no agenda PDF).

## Document content

- **Agenda PDF** (Sept 15, 2026, 156KB): light — `PdfKeywordScan` found 3
  hits, but all administrative/procedural (a discussion item on the list
  of zoning/subdivision/site-plan regulations requiring public-hearing
  scheduling, plus the town's own address "55 Industrial Way" matching
  the "industrial" keyword) rather than an active development case. No
  named applicant in this sample — worth trying another meeting date.

## Sample files downloaded

- `working/milton_nh/milton_pb_agenda_09-15-26.pdf`
