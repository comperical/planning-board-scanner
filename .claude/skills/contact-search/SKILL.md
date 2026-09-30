---
name: contact-search
description: Find contact info for development projects that have none - pull the names of people and companies (applicant, owner, developer, engineer, surveyor, architect, attorney) out of the project write-up and its linked documents, web-search each one for phone/email/web site, and record them as contacts linked to the project. Use when asked to "find contacts", "do the contact search", fill in contacts for projects, or /contact-search.
---

# Contact Search

Works through projects that have no linked contacts (`contact_project`
rows). One project per pass of this loop. Follow the permission rules in
the `planning-board-scanner` skill (one bare `plan_entry.py` call per
Bash command). `WebSearch` and `WebFetch` are both pre-approved - fetch a
firm's own contact page when the search snippet lacks a phone number.

## 1. Pick the next project

```bash
wwiocode/pyscript/plan_entry.py NextForContactSearch
wwiocode/pyscript/plan_entry.py NextForContactSearch limit=15 large_first=true   # daily-update priority
```

Lists projects with no linked contacts that are **due** for a search:
never searched, or last searched `retry_days=` (default 30) or more ago,
or linked to a new document since the last search (new minutes often
name the engineer or developer the first agenda didn't). Never-searched
projects come first, newest first - they're the freshest leads;
`large_first=true` puts `large` projects ahead of everything. Retries
print the last search's outcome and notes - read them before searching
the same names again. `non-construction` projects (rezonings, permits)
are skipped by default; pass `include_noncon=true` only if asked.
`town=<slug>` restricts to one town.

## 2. Pull out the names

Read the project's write-up and linked documents:

```sql
SELECT full_md_text FROM projects WHERE id = <id>;
SELECT d.file_path, pd.page_number FROM project_documents pd
JOIN documents d ON d.id = pd.document_id WHERE pd.project_id = <id>;
```

The write-up usually names the parties already. If it doesn't, run
`DocDetail pdf=<path>` on a linked document and read
`working/OUTPUT.txt` around the linked page. (Some very large packets
have had their page text trimmed to save DB space - `text_pages=0` in
`DbStatus` - fall back to the other linked documents.)

List every **person or company** involved: applicant, owner (LLCs
included), developer/builder, engineer, surveyor, architect, wetland
scientist, attorney. For a trades pro the most useful are the
developer/builder and the engineer/surveyor of record - prioritize those.
Skip town staff, board members and abutters.

## 3. Check for existing contacts first

The same firms (Jones & Beach, Berry Surveying, Lavelle Associates, Keach-
Nordstrom, the Dubay Group, ...) show up across many projects and towns.
Before creating anything, search the whole table:

```bash
wwiocode/pyscript/plan_entry.py FindContact q=lavelle                              # substring, all fields
wwiocode/pyscript/plan_entry.py FindContact "name=Ryan Lavelle" "company=Lavelle Associates"   # fuzzy duplicate check
```

`ShowContactForTown town=<slug>` also lists contacts already used in that
town. If a match exists, reuse it with `LinkContact` - don't create a
duplicate. If the firm exists but the named person doesn't, create a new
row for the person with the same company/phone/web site (that's the
existing convention - see the several Jones & Beach rows).

`CreateContact` runs the same fuzzy check itself (a shared distinctive
company word or surname) and **refuses** when it finds possible matches,
listing them. Reuse one, or re-run with `force=true` when it really is
new - e.g. a new person at a firm already on file.

## 4. Web search the rest

`WebSearch` each remaining name, adding the town/state and role to
disambiguate, e.g. `"Lavelle Associates" surveyor New Hampshire phone`
or `"Q&G Development LLC" Raymond NH`. Take phone, email and web site
from the search results.

- Record only details that clearly belong to that person/firm. Don't
  guess email addresses or copy a similarly named firm in another state.
- A bare LLC often has no public presence; a registered agent or
  manager's name from a business-registry result is fine to record as
  `name=`, but don't spend more than a couple of searches on it.
- If nothing useful turns up for a name, skip it.

## 5. Record and link

```bash
wwiocode/pyscript/plan_entry.py CreateContact "name=Jane Smith, PE" "company=Acme Engineering, LLC" "phone=(603) 555-1234" email=jane@acme.com web_site=https://www.acme.com
wwiocode/pyscript/plan_entry.py LinkContact project_id=<id> contact_ids=<new id>,<existing id>
```

`name=` is the person (with credentials, e.g. "PE", "LLS"), `company=`
the firm; for an organization with no known person, leave `name=` blank.
Put a role hint in parentheses when the company name doesn't make it
obvious, e.g. `company=Gallagher, Callahan & Gartrell, PC (attorneys)`.
Link every contact found - new and reused - to the project.

### Fixing mistakes

- Wrong or incomplete details on a contact: write `working/UPSERT.json`
  with its `"id"` and the corrected fields, then
  `Upsert table=contact_info` (only the given fields change).
- Linked to the wrong project: `UnlinkContact project_id=<id> contact_ids=<id>`.
- Two rows for the same person/firm: `MergeContacts keep=<id> drop=<id>` -
  moves drop's project links to keep, fills keep's blank fields from
  drop, deletes drop.

### Batches

When working through many projects, write the creates, links and logs
for a whole batch to `working/CONTACT_OPS.json` and apply them with one
`BatchContactOps` call instead of dozens of separate calls. Everything is
validated first (projects/contacts exist, outcomes valid, duplicate check
on creates) and applied in one transaction - a bad batch writes nothing.
A create's `"ref"` stands in for its new id in later link ops:

```json
[
  {"op": "create", "ref": "cornerstone", "name": "Kevin Hatch, LLS",
   "company": "Cornerstone Survey Associates", "phone": "(603) 887-6647"},
  {"op": "link", "project_id": 295, "contact_ids": ["cornerstone"]},
  {"op": "link", "project_id": 294, "contact_ids": ["cornerstone", 161]},
  {"op": "log", "project_ids": [295, 294], "outcome": "found", "notes": "Cornerstone Survey (new)"},
  {"op": "log", "project_ids": [502, 501, 486], "outcome": "skipped", "notes": "non-construction"}
]
```

Add `"force": true` to a create the duplicate check wrongly flags.

## 6. Log the search pass

Always do this last for every project you picked up, whatever happened -
same principle as `LogAnalysis`:

```bash
wwiocode/pyscript/plan_entry.py LogContactSearch project_id=<id> outcome=found "notes=Jones & Beach (reused), NTV Builders (new)"
wwiocode/pyscript/plan_entry.py LogContactSearch project_id=<id> outcome=none_found "notes=KV Partners ambiguous - only NH match is a municipal engineer"
wwiocode/pyscript/plan_entry.py LogContactSearch project_id=<id> outcome=skipped "notes=bare trust name on a lot line adjustment"
wwiocode/pyscript/plan_entry.py LogContactSearch project_ids=<id>,<id>,<id> outcome=skipped "notes=private homeowners"   # same outcome for several
```

- `found` - at least one contact created or linked.
- `none_found` - searched, nothing usable. Say *why* in `notes` (which
  names were tried, what the near-misses were) so a retry in 30 days
  doesn't repeat the same searches.
- `skipped` - not worth searching (no named party, a bare trust/LLC on a
  lot line adjustment, an out-of-town regional-impact notice).

A `none_found`/`skipped` project drops out of `NextForContactSearch` until
the retry window passes or a new document is linked to it - so an
unlogged dead end would clog the head of the list every run.

## Loop

Go back to step 1. Stop when the list is empty, or when the user asks to
stop / caps the number of projects. If the user didn't say how many,
default to 10 projects per session. End with a short summary: projects
covered, contacts created vs reused, and projects where nothing was found.
