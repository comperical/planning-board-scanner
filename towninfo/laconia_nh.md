# Laconia, NH — Planning Board Web Access

Investigated: 2026-09-14

Laconia is a small city (Belknap County seat) on Lake Winnipesaukee.
Platform: standard CivicPlus Agenda Center (see PATTERNS.md) — no bot
protection.

## Platform notes

- Main site: `https://www.laconianh.gov` (also mirrored at
  `cityoflaconianh.org`, not cross-checked for full parity).
- Direct per-board Agenda Center: `/AgendaCenter/Planning-Board-6`.
- Meeting titles carry type flags: "Regular Meeting Agenda", "Site Walk
  Agenda", "Quorum of Council, Boards and Commissions - 91-A Training",
  "Quorum - Public Information Session" — filter for "Regular Meeting" to
  get substantive case-review agendas.

## Document content

- **Agenda PDF** (Sept 1, 2026, "Regular Planning Board Meeting," 9.4KB,
  full text extracted): the richest city-scale agenda in this project —
  lists **five separate active cases**, each with case number, address,
  tax map/lot/parcel id, and a plain-English description (plus
  staff-report/submission-packet filenames referenced, not directly
  hyperlinked):
  - PB2026-022, 1206 Old North Main Street (374-404-7): subdivide into
    **5 individual lots** with an internal road.
  - PB2026-051, 371 White Oaks Road (235-241-5): site plan for a
    **16-site RV campground**, in addition to the existing single-family
    dwelling.
  - PB2026-053, Belmont Road (464-303-28): site plan for a 1,600 sq ft
    indoor self-storage building.
  - PB2026-062, 59 Doe Avenue (145-64-1): site plan for a **40-unit
    residential** development under the Performance Overlay District.
  - PB2027-001, 208 Eastman Road (313-61-1.1): site plan for a garage
    within the wetland buffer.

  A great example of a single small file carrying dense, structured
  project signal — worth using `PdfExtractText` (not just keyword scan)
  as the default here.

## Sample files downloaded

- `working/laconia_nh/09012026.pdf`
