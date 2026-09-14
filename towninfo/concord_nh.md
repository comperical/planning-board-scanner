# Concord, NH — Planning Board Web Access

Investigated: 2026-09-12

Concord (state capital, a city not a small town) is the most complex
municipality in this project — it runs **Legistar** (Granicus) for
current agendas, not a CivicPlus/Drupal/WordPress town site (see
PATTERNS.md). No Cloudflare/bot-challenge on either system.

## Platform notes

- Main city site: `https://www.concordnh.gov` — CivicPlus CivicEngage
  (Planning Board hub `/273/Planning-Board`), but this is only used for
  minutes/older agendas (Archive Center) — see below.
- **Current agendas (Feb 2017–present) are hosted entirely on
  `https://concordnh.legistar.com`.** Pre-2017 agendas, and *all* years of
  minutes including current, are mirrored on CivicPlus's own **Archive
  Center** (`concordnh.gov/Archive.aspx`).

## Legistar structure (agendas)

- `Calendar.aspx` — one town-wide meeting calendar (all boards), a
  "Departments Dropdown" filter (actually the body/committee filter).
  Columns: Name, Meeting Date, Time, Location, Meeting Details, Agenda,
  Minutes, Video.
- Each row links to `MeetingDetail.aspx?ID={meetingId}&GUID={guid}` (HTML
  agenda, each item linking to `LegislationDetail.aspx?ID={matterId}` —
  Legistar's per-"Matter" detail page with its own file number, e.g.
  `26-343`) and `View.ashx?M=A&ID={meetingId}&GUID={guid}` (the same
  agenda as one flattened PDF — what CivicEngage's own Planning Board page
  links to).
- `LegislationDetail.aspx`'s attachments grid renders "0 records" during
  this recon — the actual attachment documents (Staff Report, Civil
  Plans, etc.) are named as plain text under each item's heading **inside
  the agenda PDF**, presumably as PDF link annotations not resolved by
  this project's text-only PDF tools. **Getting individual attachment
  PDFs is an open problem.**

## ⚠️ Access gotcha: `View.ashx` needs a same-origin browser fetch

- Plain `requests` gets **`410 Gone`** on every `View.ashx?...` URL —
  reproducible, not transient. The browser's successful request carries a
  `Referer`; this looks like a deliberate anti-hotlinking check (see
  PATTERNS.md). Playwright's own download flow doesn't cleanly capture
  the bytes either — Chrome's native PDF viewer can intercept the
  navigation and return wrapper HTML instead of the PDF; check for `%PDF`
  magic bytes before trusting a saved response.
- **Working pattern**: `playwright-cli eval` in-page `fetch()`,
  base64-encode, decode to a file with a small Python script (see
  PATTERNS.md hotlink-gotcha for the exact snippet). Confirmed working
  this session; the decode-to-disk step itself is the standing `TODO.txt`
  gap.

## Archive Center (minutes, and pre-2017 agendas) — the easy path

- `Archive.aspx?AMID=48` = Planning Board **Minutes**, confirmed current
  through Aug 19, 2026 (drafts included). Each entry links to
  `Archive.aspx?ADID={id}`, redirecting to a static PDF.
- `ArchiveCenter/ViewFile/Item/{id}` is the same document store (same
  `{id}` as `ADID`) and — unlike Legistar — **works fine with plain
  `FetchUrl`**. Confirmed: fetched a 390KB, fully text-extractable minutes
  PDF this way with zero friction.
- `Archive.aspx?AMID=49` = Planning Board **Agendas**, but explicitly
  labeled "prior to February 2017" — current agendas are NOT mirrored
  here, only on Legistar.

## Document content

- **Agenda PDF** (via Legistar `View.ashx?M=A`): the richest, most
  structured agenda content found in this entire project. Sample (Sept
  16, 2026, 9 pages) organized into Consent Agenda, Design Review
  Applications, Public Hearings, and "Site Plan, Subdivision and
  Conditional Use Permit Applications" — each item giving applicant +
  owner name, precise project description, Tax Map/Lot, zoning
  district(s), the city's own case number(s) (e.g. `PL-SPR-2026-0068`),
  continuance status, and a named list of every attachment filed. Real
  projects: a 110-unit, 4-story, 133,600-sq-ft multifamily building at
  270 Loudon Road; a 24-lot major subdivision off Mooreland
  Avenue/Heather Lane; a car-dealership conversion at 110 Manchester
  Street; an 8,160-sq-ft micro-data-center/office/garage building at 52
  Locke Road.
- **Minutes PDF** (via Archive Center): 32,000 characters of standard
  motion-and-discussion narrative, fully text-extractable.

## Sample downloads (in `working/concord_nh/`)

- `09.16.2026_PB_Agenda.pdf` — via the Legistar `eval`-fetch workaround
- `20260415.pdf` — via the plain, `FetchUrl`-able Archive Center path

## Open questions / not yet checked

- How to retrieve the individual named attachments referenced inside each
  agenda item — likely needs PDF link-annotation extraction (not in this
  project's toolset) or a Legistar `MatterAttachment`-style endpoint.
- Whether Legistar's `Legislation.aspx` search page can filter matters by
  type across meetings — a more efficient scan method than paging
  meeting-by-meeting.
- Whether Concord has anything resembling Hampton's/Stratham's standalone
  "Active Applications" leads page — not checked this session.
