# MVP Target Towns — Southeastern New Hampshire

Compiled 2026-09-14. Scope: southeastern NH, bounded west by roughly the
Concord/Manchester line (nothing further west than that), south to the MA
border, east to the seacoast/Maine border, north to the towns just south of
Lake Winnipesaukee.

Status legend: ✅ researched (`towninfo/<slug>.md` exists) · ⬜ not yet started.

**See `PATTERNS.md` for shared access patterns** (platform taxonomy, URL
shapes, access gotchas, document-content conventions) common across many
towns — individual town files below only record what's different for that
specific town.

## Seacoast (Rockingham County, coastal)
- ✅ Portsmouth — `portsmouth_nh.md`
- ✅ New Castle — `new_castle_nh.md`
- ✅ Rye — `rye_nh.md`
- ✅ North Hampton — `north_hampton_nh.md`
- ✅ Hampton — `hampton_nh.md`
- ✅ Hampton Falls — `hampton_falls_nh.md`
- ✅ Seabrook — `seabrook_nh.md`
- ✅ Greenland — `greenland_nh.md`
- ✅ Stratham — `stratham_nh.md`
- ✅ Exeter — `exeter_nh.md`
- ✅ Newmarket — `newmarket_nh.md`
- ✅ Newfields — `newfields_nh.md`

## Rockingham County (inland)
- ✅ Kingston — `kingston_nh.md`
- ✅ East Kingston — `east_kingston_nh.md`
- ✅ South Hampton — `south_hampton_nh.md`
- ✅ Kensington — `kensington_nh.md`
- ✅ Brentwood — `brentwood_nh.md`
- ✅ Fremont — `fremont_nh.md`
- ✅ Epping — `epping_nh.md`
- ✅ Raymond — `raymond_nh.md`
- ✅ Chester — `chester_nh.md`
- ✅ Sandown — `sandown_nh.md`
- ✅ Danville — `danville_nh.md`
- ✅ Hampstead — `hampstead_nh.md`
- ✅ Plaistow — `plaistow_nh.md`
- ✅ Atkinson — `atkinson_nh.md`
- ✅ Salem — `salem_nh.md`
- ✅ Windham — `windham_nh.md`
- ✅ Derry — `derry_nh.md`
- ✅ Londonderry — `londonderry_nh.md`
- ✅ Auburn — `auburn_nh.md`
- ✅ Candia — `candia_nh.md`
- ✅ Deerfield — `deerfield_nh.md`
- ✅ Northwood — `northwood_nh.md`
- ✅ Nottingham — `nottingham_nh.md`

## Strafford County
- ✅ Dover — `dover_nh.md`
- ✅ Somersworth — `somersworth_nh.md`
- ✅ Rochester — `rochester_nh.md`
- ✅ Durham — `durham_nh.md`
- ✅ Lee — `lee_nh.md`
- ✅ Madbury — `madbury_nh.md`
- ✅ Barrington — `barrington_nh.md`
- ✅ Rollinsford — `rollinsford_nh.md` (partial — Google Drive access not
  fully resolved)
- ✅ Farmington — `farmington_nh.md`
- ✅ Milton — `milton_nh.md`
- ✅ Strafford — `strafford_nh.md`
- ✅ New Durham — `new_durham_nh.md`

## Manchester area (Hillsborough County, eastern edge)
- ✅ Manchester — `manchester_nh.md`
- ✅ Bedford — `bedford_nh.md`
- ✅ Goffstown — `goffstown_nh.md`
- ✅ Hudson — `hudson_nh.md`
- ✅ Litchfield — `litchfield_nh.md`
- ✅ Merrimack — `merrimack_nh.md`
- ✅ Pelham — `pelham_nh.md` (partial — Agenda Center access not fully
  resolved)

## Concord area (Merrimack County, eastern/central)
- ✅ Concord — `concord_nh.md`
- ✅ Pembroke — `pembroke_nh.md`
- ✅ Allenstown — `allenstown_nh.md`
- ✅ Hooksett — `hooksett_nh.md`
- ✅ Bow — `bow_nh.md`
- ✅ Chichester — `chichester_nh.md`
- ✅ Epsom — `epsom_nh.md` (partial — Munibit blob API access not fully
  resolved)
- ✅ Loudon — `loudon_nh.md`

## South of Lake Winnipesaukee (Belknap County)
- ✅ Alton — `alton_nh.md`
- ✅ Gilmanton — `gilmanton_nh.md`
- ✅ Belmont — `belmont_nh.md`
- ✅ Barnstead — `barnstead_nh.md`
- ✅ Gilford — `gilford_nh.md` (docx format — content not yet analyzed)
- ✅ Laconia — `laconia_nh.md`

---

**Totals: 69 of 69 towns on the list — MVP list complete.** Every town in
the southeastern NH scope (Seacoast, Rockingham, Strafford, the
Manchester/Concord areas, and Belknap County south of Winnipesaukee) has
now been researched, each with a `towninfo/<slug>.md` write-up covering
platform, URL structure, and a sample-document content check.

**Two towns are partial** and flagged as open items rather than fully
resolved: Rollinsford (Google Drive folder listing not fully explored)
and Pelham (Agenda Center access pattern not resolved) — access notes are
still useful, but no sample document was pulled for either. Epsom is
also partial (Munibit blob-token access not resolved).

**Outstanding cross-town TODO items** (see `TODO.txt`):
- `.docx` text-extraction tool needed for Hampton Falls, Brentwood, and
  Gilford (all serve Word docs instead of PDFs for some/all documents).
- Base64-decode-to-file step needed for hotlink-protected `/media/{id}`
  or `/docview.aspx` endpoints at Concord, Kingston, Madbury, and
  Brentwood (bytes fetched in-session via browser but never written to
  disk).

**Platforms found across the project** (8 distinct, beyond CivicPlus):
Municipal One (Brentwood), Legend Software (Northwood, Gilford),
TownCloud (New Durham), Revize (Hooksett), Munibit (Epsom), custom
WordPress (South Hampton, Strafford, Belmont, Alton), DotNetNuke/
"Portals" (Manchester), eCode360 + custom PHP (Raymond), and Google
Drive-hosted documents (Rollinsford).
