# Allenstown, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, adjacent to Suncook/Pembroke. Runs CivicPlus
CivicEngage with the Agenda Center module — same shape as other towns
this session — plain PDFs, no bot protection.

## Platform

- Main site: `https://www.allenstownnh.gov`.
- Planning Board hub: `/1289/Planning-Board`.
- ⚠️ `/AgendaCenter/Planning-Board` (no numeric suffix) **404s** — the
  per-board Agenda Center URL needs the numeric id (not captured this
  session); use `/agendacenter` and expand the Planning Board section
  manually, or scrape directly via known `ViewFile` ids from search
  results.
- Some agenda links carry a `?packet=true` query param (seen on a
  Selectmen example) — likely toggles a fuller packet view; not confirmed
  for Planning Board specifically this session.

## URL structure

- Same shape as other AgendaCenter towns:
  `/AgendaCenter/ViewFile/{Agenda|Minutes}/_{MMDDYYYY}-{id}`.
- **Confirmed `FetchUrl` (plain `requests`, no browser/session) downloads
  these directly** as real PDFs.

## Document content

- **Minutes PDF** (Mar 18, 2026, 361KB): `PdfKeywordScan` found 0 hits —
  either an administrative-only session or the keyword set missed this
  meeting's specific content; worth a follow-up sample from an agenda
  (not minutes) PDF, and from a different date, before concluding
  Allenstown is low-signal.

## Sample files downloaded

- `working/allenstown_nh/_03182026-310` (Mar 18, 2026 minutes — no
  extension in the saved filename; it is a PDF)
