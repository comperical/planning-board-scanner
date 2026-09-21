# Hampton, NH — Planning Board Web Access

> **Update 2026-09-21:** Agenda Center Minutes `ViewFile` responses have no Content-Disposition, so `FetchUrl dest=` names them after the URL segment (`_MMDDYYYY-NNNN`), the same name the agenda would get. Fetch without `dest=` and rename. (`FetchUrl` now refuses to overwrite.)

Investigated: 2026-09-12

Platform: standard CivicPlus Agenda Center (see PATTERNS.md). No bot
protection.

## Platform notes

- Site: `https://www.hamptonnh.gov`. Board page `/318/Planning-Board`
  links to `/AgendaCenter/Planning-Board-7`.
- Year-grouped table, columns **Agenda | Minutes | Media | Download**.
  Rows include the Planning Board's own regular meetings plus
  subcommittees filed under the same tab: **Capital Improvements Plan
  (CIP) Committee**, **Master Plan Implementation Committee**, **Plan
  Review Committee**, ad hoc **Pre-Construction Meetings**.
- "Media" links go to a Cablecast video portal
  (`reflect-hamptonnh.cablecast.tv`).

## ⭐ Key find: "Active Applications to the Planning Board" page

- `https://www.hamptonnh.gov/720/Active-Applications-to-the-Planning-Boar`
  (note: URL is truncated/typo'd by the town itself, missing the final
  `d`).
- This is a **standalone, continuously-updated leads page** — arguably
  the richest single resource found across all towns in this project
  (see PATTERNS.md). Lists every currently-pending case under headings
  (New Public Hearings / Continued Public Hearings / Attending to be
  Heard / Other Business / Plan Review Committee), each entry giving town
  case number, site address, Map/Lot, applicant name, owner of record,
  plain-English description, exact hearing date, and direct links to
  every submitted document/revision round (application form, plan sets,
  drainage analyses, stormwater O&M manuals, traffic memos, wetlands
  permits, Conservation Commission recommendation letters, town planner
  memos, etc.).
- Sample case: 44 Sweetbriar Lane — Green & Company site plan to merge
  two lots, demolish an existing house, and build a 19-unit multi-family
  condominium development with a privately-owned road.
- This page alone, kept up to date, may be a better lead-generation
  source than parsing agendas/minutes at all.

## Document content

- **Agenda PDF**: much lighter than Exeter's/Newmarket's — often just
  section headers with terse one-line item references. **The Active
  Applications page carries the real detail** the agenda itself lacks.
- **DocumentCenter files**: sample "Falcone Cir Amended Subdivision
  Application" was a normal 12-page text PDF.

## Sample downloads (in `working/hampton_nh/`)

- `09.16.2026 Agenda.pdf` — light regular-meeting agenda
- `_08192026-2057` — minutes PDF for Aug 19, 2026 (no `.pdf` extension)
- `Falcone Cir Amended Application for website.pdf` — sample case
  document pulled from the Active Applications page

## Open questions / not yet checked

- Whether other Hampton boards have an equivalent "Active Applications"
  page — if so, this pattern could generalize well.
- How far back the Agenda Center's "View More" years go.
- Whether the Active Applications page is reliably kept current (it's
  manually maintained prose, not auto-generated) — worth periodic
  re-checking.
