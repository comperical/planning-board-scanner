# Rochester, NH — Planning Board Web Access

Investigated: 2026-09-12

Platform: node-based CivicPlus (Drupal, `/node/{id}/...`), footer credit
"Government Websites by CivicPlus®". Sits behind **Cloudflare bot
management** — see PATTERNS.md.

## Platform notes

- Root domain: `https://www.rochesternh.gov`.
- A **headless** Playwright/CDP session is **hard-blocked** by Cloudflare
  on every page, including static PDF assets: HTTP 403, "Performing
  security verification" interstitial that never clears. A **headed**
  session passes through cleanly. Plain `curl` (normal desktop UA) works
  fine for the actual PDF file URLs — the check appears to gate rendered
  page requests, not static file downloads under that path. **Working
  pattern**: headed browser to discover/enumerate document links, plain
  `curl` for bulk download.
- Main board page: `/planning-board`. Agenda year-index:
  `/node/10106/agenda/{year}` (years 2009–2026 as of 2026-09-12). Minutes
  year-index: `/node/10106/minutes/{year}`.
- Agenda detail page → PDF at `sites/g/files/vyhlif9211/f/agendas/
  {YYYY_MM_DD}_{type}_agenda.pdf`. Minutes detail page **redirects
  straight to the PDF** (no intermediate page, unlike agendas) at
  `.../f/minutes/{YYYY_MM_DD}_pb_minutes_final.pdf`.

### Meeting types (all mixed in the same year-index list)

| Type | Filename pattern | Notes |
|---|---|---|
| Regular meeting | `{date}_pb_agenda.pdf` | Full board, public hearings, most substantial site plans/subdivisions |
| Workshop meeting | `{date}_pb_agenda.pdf` ("(Workshop Meeting)" in header) | Still carries real case items (extensions, lot-line adjustments, surety releases) — do not skip |
| Minor Site Plan Review Committee | `{date}_minor_site_agenda.pdf` | Sub-committee, small/administrative applications; generally lower-value but occasionally has real content |

## Document content

- Agendas: terse, one entry per application —
  `{address}, {applicant} ({agent/engineer}), {application type} —
  {description}. Case# {number}` — consistently structured, good for
  automated parsing.
- Minutes: much richer — full narrative, motions, vote outcomes, unit
  counts, approval conditions. Published ~2 weeks after the meeting.
  Sometimes reveal items (e.g. pending road-acceptance subdivisions)
  never on any agenda as a formal item.
- **For a trades-pro lead feed**: agendas give earliest signal of a new
  filing; minutes confirm approval status and real project scope. Link
  by case# and meeting date.

## Sample downloads (in `working/rochester_nh/`)

- `2026_09_14_pb_agenda.pdf` — regular meeting; new 35-unit senior
  housing site plan
- `2026_08_17_pb_agenda.pdf` — workshop; extension, 2 lot-line
  adjustments, surety release, data-center zoning update
- `2026_08_26_minor_site_agenda.pdf` — minor site plan committee, single
  small change-of-use item
- `2026_08_03_pb_minutes_final.pdf` — regular meeting minutes; 206-unit
  multi-family site plan (final approval), subdivision amendment, retail
  motor-fuel outlet design review

## Open questions / not yet checked

- Whether other Rochester boards use the same
  `/node/{id}/agenda|minutes/{year}` pattern under a different node id.
- Whether there's an RSS/API feed or Agenda Center alternative that
  avoids crawling HTML listing pages.
- Full behavior of the Cloudflare block — untested whether IP-based,
  CDP-fingerprint-based, or time/rate based.
