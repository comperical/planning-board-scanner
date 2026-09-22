# Project Tags

Controlled vocabulary for the `projects.tag_set` column (see
`wwiocode/pyscript/plan_db.py`). Tags classify each development project so
the Projects page can sort and filter leads for trades pros.

## Format

- `tag_set` is a comma-separated set of tags, e.g.
  `residential,multifamily,new-construction,approved,large`.
- Tags are lowercase, hyphenated, and never contain commas or spaces.
- No duplicates; order doesn't matter (write them in the group order below
  for readability).
- Empty string `''` = not yet tagged.
- Only use tags from this file. To add a new tag, add it here first.
- This file is machine-read: `ApplyProjectEdit` (via `load_tag_vocabulary`
  in `plan_db.py`) takes the vocabulary from the backticked first-column
  entries of the tables under each `### <N>. ...` heading, and requires
  exactly one tag from group 1 (sector) and group 4 (stage). Keep that
  table layout when editing.

## Tag groups

A project typically gets 4-6 tags total. Groups 1 (one sector) and 4 (one
stage) apply to every project; group 3 to every project with physical work
(a `non-construction` project may have none); group 2 only to projects
that include housing; group 5 only when the flag applies.

### 1. Sector - who/what the project is for

Pick the one that best describes the end use. Use `mixed-use` only when a
single project deliberately combines residential and commercial space.

| Tag | Meaning | Examples |
|---|---|---|
| `residential` | Homes, apartments, condos, residential lots | #57 701 South Rd 7-lot subdivision; #111 559 Winnacunnet Rd teardown/rebuild |
| `commercial` | Retail, office, restaurants, auto, medical, hospitality, private recreation | #72 Gilford ER/medical center; #38 110 Manchester St car dealership |
| `industrial` | Warehouse, light manufacturing, storage, contractor yards, data centers | #55 121 Technology Dr warehouses; #83 7 Marshall Rd self-storage |
| `mixed-use` | One project combining residential with commercial space | #18 15 Sagamore Rd; #58 97 Portsmouth Ave |
| `institutional` | Private schools, churches, nonprofits, assisted-care operators | #104 Phillips Exeter faculty duplexes; #35 St. Paul's School mail center; #108 Exeter Presbyterian Church |
| `municipal` | Town/city-owned facilities and public works (usually public bid) | #86 Madbury public works facility; #98 Peverly Hill Rd reconstruction; #56 Churchill Rink |
| `utility` | Electric, water, gas, telecom company projects | #96 Eversource transmission structures; #112 Aquarion water mains; #113 Aquarion water tank |

### 2. Housing type - residential projects only

Apply alongside `residential` (or `mixed-use` / `institutional` when the
project includes housing). A project can carry more than one of these,
e.g. `multifamily,condo,affordable`.

| Tag | Meaning | Examples |
|---|---|---|
| `single-family` | Detached single-family homes, including lots created for them | #90 89 Stark Ave; #95 238 Austin St; #105 Exeter Country Club cluster subdivision |
| `small-multi` | 2-4 units per building: duplexes, triplexes, small townhouse groups | #45 210 Portsmouth Ave duplexes; #114 37 Exeter Rd 3-unit townhouse; #104 PEA duplexes |
| `multifamily` | 5+ units: apartment buildings, larger townhouse developments | #36 270 Loudon Rd 110 units; #51 90 Wakefield St 35 units; #82 Liberty Common |
| `condo` | Condominium ownership, including condo conversions of existing buildings | #9 Parmenter Place; #31 Cottages at Back River Rd; #59 5 Brentwood Rd |
| `senior-housing` | Age-restricted housing, assisted living, continuing care | #52 Riverwoods Phase II; #10 Benchmark assisted care |
| `affordable` | Income-restricted or explicitly affordable/workforce housing | #31 Cottages at Back River Rd; #51 Community Action Partnership |

### 3. Work type - what physically gets built

Tag every kind of work the project involves; this group is the main
filter for matching leads to trades. Multiple tags are normal, e.g. a
teardown-and-rebuild is `demolition,new-construction`.

| Tag | Meaning | Examples |
|---|---|---|
| `new-construction` | New building(s) or home(s) | #36 270 Loudon Rd; #86 public works facility; #101 0 Elm St new home |
| `addition` | Enlarging an existing building | #15 16 Whitaker Way; #79 444 Route 125 6,000 SF addition; #5 313 Loudon Rd |
| `conversion` | Change of use or reconfiguring an existing building (office-to-residential, co-living, recreation use) | #6 103 North State St office to 21 units; #61 38 Milton Rd batting cages; #103 1-15 Congress St co-living |
| `renovation` | Renovating an existing building without enlarging it or changing its use - facade/storefront replacement, exterior lighting, interior fit-out, roof/HVAC upgrades | #143 38 South Main St storefront; #161 80 Storrs St facade lighting |
| `demolition` | Tearing down an existing structure | #58 dry cleaner; #95 238 Austin St; #113 old water tank |
| `subdivision` | Dividing land into new lots (usually precedes home building) | #53 73 Piscataqua Rd; #57 701 South Rd; #109 121 High St |
| `lot-line-adjustment` | Moving a boundary between existing lots, or merging lots; little construction by itself | #42 109 Hoit Rd; #80 95/97 Prescott Rd; #117 Ocean Blvd |
| `sitework` | Parking lots, paving, grading, drainage/stormwater, site lighting | #92 77 Long Hill Rd; #107 109 Epping Rd; #119 NHSPCA parking |
| `road-infrastructure` | New/rebuilt roads, sidewalks, water/sewer mains, subdivision roads | #98 Peverly Hill Rd; #112 Aquarion water mains; #88 Peterson Rd |
| `accessory` | Garages, decks, pools, sheds, driveways, stone-wall/driveway cuts | #27 in-ground pool; #94 105 Spur Rd garage + deck; #81 175 South Rd driveway |
| `landscaping` | Plantings, buffer restoration, tree work, landscape regrading | #99 224 Cate St; #110 26 Wadleigh St; #102 361 Hanover St |

### 4. Stage - where the project is in the approval process

Exactly one per project, reflecting the **latest** document linked to it.
These go stale as projects move forward - update the stage tag whenever a
new analysis pass links a later document to the project.

| Tag | Meaning | Examples |
|---|---|---|
| `concept` | Design review, preliminary/conceptual consultation - no formal application yet | #116 6 Airfield Dr; #115 14 Elm St; #29 Birch Rd |
| `in-review` | Formal application filed, hearing pending or continued, TRC review | #82 Liberty Common; #105 Exeter Country Club; #92 77 Long Hill Rd |
| `approved` | Board approval granted (possibly with conditions); construction not yet confirmed | #51 90 Wakefield St; #85 32 Nute Rd; #111 559 Winnacunnet Rd |
| `extension` | Approval extended because the project hasn't started or met conditions | #50 Farmington Rd; #108 73 Winter St; #23 EV charging station |
| `construction` | Pre-construction meeting held or construction reported underway | #113 5R Falcone Circle; #11 Airfield Dr Phase I |
| `complete` | Surety/bond release or other sign that the work is finished | #68 29 Wadleigh Rd; #87 18 Sterling Dr; #49 Aldi's |
| `withdrawn` | Application withdrawn or denied | #19 94 Langdon / 98 Cornwall St |

### 5. Lead-quality flags - optional

Add only when the flag applies.

| Tag | Meaning | Examples |
|---|---|---|
| `large` | 20+ dwelling units, or 20,000+ SF of building, or a major public/utility job | #82 Liberty Common (140 units); #55 2 x 162,000 SF warehouses; #83 72,300 SF self-storage; #98 1-mile road rebuild |
| `non-construction` | Purely administrative - little or no trades work expected (rezoning, covenants, escrow payments, rental/use permits, signage) | #22 375 Banfield Rd rezoning; #26 restrictive covenant; #10-#13 escrow payments; #70 short-term rental CUP; #16 billboard |

## Worked examples

| Project | `tag_set` |
|---|---|
| #82 Liberty Common, 140-unit condo development, hearing continued | `residential,multifamily,condo,new-construction,subdivision,road-infrastructure,in-review,large` |
| #111 559 Winnacunnet Rd, teardown + new single-family home, approved | `residential,single-family,demolition,new-construction,approved` |
| #113 5R Falcone Circle, water tank replacement, preconstruction held | `utility,demolition,new-construction,construction` |
| #92 77 Long Hill Rd, church parking lot rebuild, TRC review | `institutional,sitework,in-review` |
| #22 375 Banfield Rd rezoning | `commercial,in-review,non-construction` |
