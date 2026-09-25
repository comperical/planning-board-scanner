---
name: contact-search
description: Find contact info for development projects that have none - pull the names of people and companies (applicant, owner, developer, engineer, surveyor, architect, attorney) out of the project write-up and its linked documents, web-search each one for phone/email/web site, and record them as contacts linked to the project. Use when asked to "find contacts", "do the contact search", fill in contacts for projects, or /contact-search.
---

# Contact Search

Works through projects that have no linked contacts (`contact_project`
rows). One project per pass of this loop. Follow the permission rules in
the `planning-board-scanner` skill (one bare `plan_entry.py` call per
Bash command; `WebSearch` is pre-approved, `WebFetch` is not - ask before
fetching a page).

## 1. Pick the next project

There's no dedicated tool; use `RunQuery`. Write `working/QUERY.sql`
with the Write tool:

```sql
SELECT p.id, t.slug, p.short_desc
FROM projects p JOIN town t ON t.id = p.town_id
WHERE NOT EXISTS (SELECT 1 FROM contact_project cp WHERE cp.project_id = p.id)
  AND p.tag_set NOT LIKE '%non-construction%'
ORDER BY p.id DESC
LIMIT 10;
```

```bash
wwiocode/pyscript/plan_entry.py RunQuery
```

Newest projects first - they're the freshest leads. `non-construction`
projects (lot line adjustments, rezonings, permits) are skipped by
default; include them only if asked.

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

```sql
SELECT id, name, company, phone, email, web_site FROM contact_info
WHERE company LIKE '%<firm word>%' OR name LIKE '%<surname>%';
```

`ShowContactForTown town=<slug>` also lists contacts already used in that
town. If a match exists, reuse it with `LinkContact` - don't create a
duplicate. If the firm exists but the named person doesn't, create a new
row for the person with the same company/phone/web site (that's the
existing convention - see the several Jones & Beach rows).

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

A project where nothing could be found stays contact-less and will come
up again; note it in your summary so it can be skipped next time (move
down the list past it).

## Loop

Go back to step 1. Stop when the list is empty, or when the user asks to
stop / caps the number of projects. If the user didn't say how many,
default to 10 projects per session. End with a short summary: projects
covered, contacts created vs reused, and projects where nothing was found.
