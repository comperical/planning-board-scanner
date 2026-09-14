# Allenstown, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, adjacent to Suncook/Pembroke. Platform: standard
CivicPlus Agenda Center (see PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.allenstownnh.gov`. Planning Board hub:
  `/1289/Planning-Board`.
- ⚠️ `/AgendaCenter/Planning-Board` (no numeric suffix) **404s** — needs the
  numeric id (not captured this session); use `/agendacenter` and expand
  the section manually.
- Some agenda links carry a `?packet=true` query param (seen on a
  Selectmen example, not confirmed for Planning Board).

## Document content

- **Minutes PDF** (Mar 18, 2026, 361KB): `PdfKeywordScan` found 0 hits —
  either an administrative-only session or the keyword set missed this
  meeting's content; worth a follow-up sample from an agenda (not
  minutes), and a different date, before concluding Allenstown is
  low-signal.

## Sample files downloaded

- `working/allenstown_nh/_03182026-310` (Mar 18, 2026 minutes — no
  extension in the saved filename; it is a PDF)
