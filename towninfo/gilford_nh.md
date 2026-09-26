# Gilford, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, on Lake Winnipesaukee's south shore, adjacent to
Laconia. Platform: **Legend Software** (see PATTERNS.md; same platform as
Northwood). No bot protection. **Partial — docx content not yet
analyzed.**

## Platform notes

- Main site: `https://www.gilfordnh.gov`. Planning Board entity page:
  `/entity/Planning-Board-22`.
- Town-wide agendas listing: `/agendas/-{entityId}` — e.g. `/agendas/-22`
  for Planning Board, `/agendas/-9` for the **separate** "Planning and
  Land Use Department" (staff-level "Site Study" entries — don't
  conflate; entity 9 ≠ entity 22).
- Meeting titles carry status: "CANCELLED - Regular Meeting".
- ⚠️ **Some meeting pages have no agenda file at all** (same quirk as
  Northwood). A Public Hearing page did have a document, linked as
  `/file/{fileId}/{filename}`.
- **⚠️ The file found was `.docx`, not PDF** —
  `PB_Notice_for_August_17_2026_jba.docx`. At least the third town in the
  project serving Word docs (alongside Hampton Falls and Brentwood) —
  needs the docx-extraction tool (see PATTERNS.md TODOs).
- `/file/{id}/...` is openly `FetchUrl`-able, no hotlink gate (unlike
  Kingston/Madbury's `/media/{id}`).

## Scan notes (2026-09-25)

- `IngestPdfTool` now accepts `.docx` - Gilford's docx notices/agendas ingest
  fine (`pdf=working/gilford_nh/<file>.docx`); the extraction blocker is gone.
- `/agendas/-22` lists meetings (rows: type, "Planning Board", date) but the
  link text has no date - read each row's text to map `Regular-Meeting-NNNN`
  slugs to dates. Future meetings are pre-listed through December.
- Only **Public Hearing** meetings (and an occasional Regular Meeting, e.g.
  Aug 31 `8-31-26_PB_Agenda.docx`) carry a file; most Regular Meeting pages
  (9/7, 9/21, 10/5 checked) have no attachment. So the routine is: open each
  meeting page since the last scan and `eval` `a[href*="/file/"]`.
- Files: `/file/{id}/{name}.docx`, `FetchUrl` works (content-type reported as
  application/msword but they ingest as docx).

## Document content

## Sample files downloaded

- `working/gilford_nh/PB_Notice_for_August_17_2026_jba.docx` (Aug 17,
  2026 Public Hearing notice)

## Open items for later

- Needs the `.docx` text-extraction tool before Gilford's documents can
  be analyzed.
- Confirm whether Regular Meeting pages (vs. Public Hearing pages)
  consistently lack agenda files, or whether that was specific to the
  one sampled this session.
