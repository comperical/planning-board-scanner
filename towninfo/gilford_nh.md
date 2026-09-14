# Gilford, NH — Planning Board Web Access

Investigated: 2026-09-14

Belknap County town, on Lake Winnipesaukee's south shore, adjacent to
Laconia. Runs **Legend Software** (same platform as Northwood, NH — see
`towninfo/northwood_nh.md`). No bot protection.

## Platform

- Main site: `https://www.gilfordnh.gov`.
- Planning Board entity page: `/entity/Planning-Board-22`.
- Town-wide agendas listing, filterable: `/agendas/-{entityId}` — e.g.
  `/agendas/-22` for Planning Board, `/agendas/-9` for the **separate**
  "Planning and Land Use Department" (staff-level "Site Study" entries,
  a different thing from Planning Board meetings — don't conflate the
  two when scraping; entity 9 ≠ entity 22).
- Each meeting gets its own page: `/agenda/{Type}-{id}` (e.g.
  `/agenda/Regular-Meeting-3453`, `/agenda/Public-Hearing-3428`) — same
  per-meeting-page shape as Northwood.
- Meeting titles carry status: "CANCELLED - Regular Meeting" appears
  directly in the title for cancelled sessions — easy to filter out.

## URL structure / access gotcha

- ⚠️ **Some meeting pages have no agenda file at all** (only "Attached
  Meeting Minutes: Please check back later" with nothing else) — same
  quirk observed at Northwood. A Public Hearing page did have a document:
  linked as `https://www.gilfordnh.gov/file/{fileId}/{filename}` — same
  `/file/{id}/...` pattern as Northwood's agenda links.
- **⚠️ The file found was a Word document (`.docx`), not a PDF** —
  `PB_Notice_for_August_17_2026_jba.docx`, content-type
  `application/msword`. This is at least the third town in the project
  serving Word docs instead of PDFs (alongside Hampton Falls and
  Brentwood) — needs the same docx-extraction tool from `TODO.txt`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  the file directly** — no referer/cookie gate (unlike the hotlink-
  protected `/media/{id}` pattern at Kingston/Madbury; Gilford/
  Northwood's `/file/{id}/...` endpoint is openly fetchable).

## Document content

- Not yet text-analyzed this session (blocked on docx extraction, same
  `TODO.txt` gap as Hampton Falls/Brentwood).

## Sample files downloaded

- `working/gilford_nh/PB_Notice_for_August_17_2026_jba.docx` (Aug 17,
  2026 Public Hearing notice)

## Open items for later

- Same as Hampton Falls/Brentwood: needs the `.docx` text-extraction tool
  from `TODO.txt` before Gilford's documents can be analyzed.
- Confirm whether Regular Meeting pages (vs. Public Hearing pages)
  consistently lack agenda files, or whether that was specific to the
  one sampled this session.
