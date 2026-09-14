# Loudon, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, northeast of Concord (home to New Hampshire Motor
Speedway). Runs CivicPlus CivicEngage with the Agenda Center module —
same shape as other towns this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.loudonnh.org`.
- ⚠️ `/planning-board` **404s** (stale link pattern seen repeatedly this
  session). Live path is `/agendacenter`, Planning Board section
  pre-expanded.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.
- Meetings: 3rd Wednesday-ish, evenings.

## Document content

- **Agenda PDF** (Sept 17, 2026, "Planning Board Public Meeting," 126KB):
  real content — `PdfKeywordScan` found 2 hits: a joint reference to a ZBA
  agenda item (Application #Z26-07, Eric & Rainie Lady, Special Exception
  for Setback Reduction; #Z26-08, Next Gen Properties) plus a Planning
  Board Public Hearing, Application #26-07, Boynton/Wittenburg, a Lot Line
  Adjustment on South Village Road (Map 20, Lots 4 & 5).

## Sample files downloaded

- `working/loudon_nh/091726 Agenda.pdf`
