# Hampstead, NH — Planning Board Web Access

Investigated: 2026-09-14

Rockingham County town. Platform: standard CivicPlus Agenda Center (see
PATTERNS.md) — no bot protection.

## Platform notes

- Main site: `https://www.hampsteadnh.us`. Planning Board hub:
  `/263/Planning-Board`.
- Agenda Center shows only the current year by default (older years via
  JS-triggered loads) — busy page (~115 ViewFile links total), a plain
  text `find` for "Planning Board" missed the actual rows; needed a full
  snapshot + grep.
- Sample agenda titles are plain ("09/08/2026 PB Agenda (PDF)") — no
  embedded project detail in the title itself here, unlike
  Danville/Kensington.
- Some meetings also link a Media/Video entry (`cloud.castus.tv`).
- **CHANGE 2026-09-24:** plain `FetchUrl` now 403s (Cloudflare) on
  ViewFile URLs. Browser `<a download>` + `ClaimDownload` works. Rows can
  be pulled without a snapshot by filtering `tr` elements whose enclosing
  `.listing` h2 matches /planning/i.
- Meetings roughly 1st & 3rd Monday, but frequently skipped (none posted
  between 8/3 and 9/8 2026).

## Document content

- **Agenda PDF** (Sept 8, 2026, 44KB): 1 keyword hit — light content in
  this sample; not yet clear if typical or an off month. A follow-up
  session should sample 2-3 more meetings.

## Sample files downloaded

- `working/hampstead_nh/09.08.2026 Agenda.pdf`
