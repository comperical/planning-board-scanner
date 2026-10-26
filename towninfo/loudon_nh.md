# Loudon, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, northeast of Concord (home to New Hampshire Motor
Speedway). Platform: standard CivicPlus Agenda Center (see PATTERNS.md)
— no bot protection.

## Platform notes

- Main site: `https://www.loudonnh.org`.
- ⚠️ `/planning-board` 404s (stale link pattern). Live path is
  `/agendacenter`, Planning Board section pre-expanded.
- Meetings: 3rd Wednesday-ish, evenings.

- Scanned 2026-10-25: plain `FetchUrl` works on `/AgendaCenter/ViewFile/...`
  (no Cloudflare). Minutes link exists on every row back to Jan 2026.
  Minutes save with no extension (`_{MMDDYYYY}-{id}`); agendas as
  `MMDDYY Agenda.pdf`; Work Session / Master Plan Subcommittee agendas
  are ~1.7KB stub PDFs (HTML/PDF/Packet links).

## Document content

- **Agenda PDF** (Sept 17, 2026, "Planning Board Public Meeting", 126KB):
  real content — `PdfKeywordScan` found 2 hits: a joint reference to a
  ZBA agenda item (Application #Z26-07, Eric & Rainie Lady, Special
  Exception for Setback Reduction; #Z26-08, Next Gen Properties) plus a
  Planning Board Public Hearing, Application #26-07, Boynton/Wittenburg,
  a Lot Line Adjustment on South Village Road (Map 20, Lots 4 & 5).

## Sample files downloaded

- `working/loudon_nh/091726 Agenda.pdf`
