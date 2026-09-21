---
name: analyze-planning-file
description: Analyze one already-scanned planning-board document from the PLANSCAN DB to identify real development projects, record them in the projects table, and log the analysis pass. Use when asked to "analyze" a planning file/document/town, work through the analysis backlog, or find/record development projects from already-downloaded PDFs.
---

# Analyze Planning File

Works through the backlog of documents already sitting in the PLANSCAN DB
(see the `planning-board-scanner` skill for how they got there) that
haven't been analyzed yet. One document per pass of this loop:

## 1. Find the next document to analyze

```bash
wwiocode/pyscript/plan_entry.py NextToAnalyze
wwiocode/pyscript/plan_entry.py NextToAnalyze town=rochester_nh   # restrict to one town
```

Picks the most recent (`doc_date`) document with zero `analysis_log` rows -
documents with no known doc_date sort last, since recency can't be judged
for them. If it prints "Nothing left to analyze", stop - the backlog is
empty (for that town, if filtered).

## 2. Pull up everything already known about it

```bash
wwiocode/pyscript/plan_entry.py DocDetail pdf=<the pdf= path from step 1>
```

This does **not** re-run any PDF extraction - it prints town/date/size,
every `keyword_hits` row (page, keyword, count, snippet), and writes the
document's full already-extracted text to `working/OUTPUT.txt` (Read that
file - don't `cat` it, no bare `cat` grant). For a large document, skim the
keyword hits first to find which pages are worth reading closely in
`OUTPUT.txt` rather than reading the whole thing.

## 3. Decide what's a real project

A "project" is a specific development: a site plan, subdivision, lot-line
adjustment, conditional use permit, etc. tied to an address/applicant - not
routine business (minutes approval, procedural votes, a continuance with no
new information). Judgment call; when in doubt, lean toward recording it -
a thin project row can be filled in more later, a missed one is just gone.

Check whether the project is already recorded before creating a new row:
skim existing projects for that town with

```bash
wwiocode/pyscript/plan_entry.py DbStatus town=<slug>
```

(lists every project's `short_desc` and current `tags=` under that town).
Match by address/applicant, not exact wording.

## 4. Record what you found

**New project:**

```bash
wwiocode/pyscript/plan_entry.py CreateProject town=<slug>
```

prints the new `project_id`. Then write its files (see the
`planning-board-scanner`-adjacent convention in `plan_db.py`):

- `working/project_edit/<project_id>.md` - full write-up: description,
  address, applicant/owner, status, unit/sq-ft counts, anything concrete.
  Use the Write tool.
- `working/project_edit/<project_id>.json` - `{"short_desc": "one-line
  summary", "tag_set": [...]}`. Use the Write tool.

**Tags are required on every new project.** Pick them from
`PROJECT_TAGS.md` (repo root) - it defines every tag, which groups apply,
and has worked examples. In short: exactly one sector tag, exactly one
stage tag, every work-type tag that applies, housing-type tags if it
includes housing, and the `large` / `non-construction` flags when they
apply. `ApplyProjectEdit` validates the list against that file (unknown
tags, or not exactly one sector/stage, are rejected - nothing is written
and the edit files are kept, so fix the `.json` and re-run). Never invent a
tag; if nothing fits, add it to `PROJECT_TAGS.md` first and mention that in
your summary to the user.

Then apply both:

```bash
wwiocode/pyscript/plan_entry.py ApplyProjectEdit project_id=<project_id>
```

This deletes the `.md`/`.json` files once applied - `working/project_edit/`
should only ever hold edits not yet synced to the DB, never accumulate. Do
not manually delete or leave stray files there.

`CreateProject` does **not** link the project to the document it came
from - that's a separate `project_documents` row. Always follow it with,
noting the page where the project's mention starts (from the keyword-hit
page in DocDetail's output, or from reading working/OUTPUT.txt):

```bash
wwiocode/pyscript/plan_entry.py LinkProject project_id=<project_id> pdf=<path> page=<page_number>
```

**Existing project mentioned again** (this document is a later
minutes/extension/approval for a project already recorded): no new row -
link it, same page= convention:

```bash
wwiocode/pyscript/plan_entry.py LinkProject project_id=<id> pdf=<path> page=<page_number>
```

Then **bring the project's fields up to date** whenever this document adds
anything - a status change (continued, approved, extended, construction
started, surety released, withdrawn), new scope details (unit counts,
square footage, contractor/engineer names), or corrected facts:

- **Tags** - always re-check the **stage** tag against this document (e.g.
  `in-review` -> `approved` on an approval, `approved` -> `construction`
  at a preconstruction meeting, -> `complete` on a surety release), and add
  any newly revealed work-type/housing/`large` tags. `tag_set` in the
  `.json` **replaces the whole set**, so start from the current tags shown
  by `DbStatus` and edit them - don't send only the changed tag. If the
  project is still untagged (older rows), tag it fully now.
- **short_desc** - update it if it states a status or scope that is now
  out of date.
- **Write-up** - rewrite `working/project_edit/<id>.md` in full with the
  new information folded in (the `.md` replaces `full_md_text` entirely -
  read the current text first, e.g. in the Projects page or DB, so nothing
  is lost), typically adding a dated line to its Status section.

Write only the files for what changed (a `.json` with just `tag_set` is
fine), then run `ApplyProjectEdit project_id=<id>`. If the document merely
mentions the project with nothing new, linking alone is enough.

A document can yield zero, one, or several projects - create/link one at a
time for each. Every project a document yields - new or existing - must
end up `LinkProject`-ed to that document; a new project row with no
`project_documents` link back to its source document is an incomplete
step. `page=` is optional but should be supplied whenever you know which
page the mention starts on - it lets the documents page jump straight to
that page in the source PDF.

## 5. Log the analysis pass

Always do this last, even if the document had zero real projects (that's
still a completed analysis, not a skip):

```bash
wwiocode/pyscript/plan_entry.py LogAnalysis pdf=<path> notes="<short summary>"
```

`notes` should be a one-line summary of the outcome, e.g. "no new projects,
routine agenda" or "found 27-unit multifamily at 165 Lafayette Rd, created
project #4". This is what makes `NextToAnalyze` skip this document next
time - skipping this step means the same document keeps coming back up.

## Loop

Go back to step 1 for the next document. Stop when `NextToAnalyze` reports
nothing left, or when the user asks to stop / caps the number of documents
per session. If the user didn't say how many documents to analyze, default
to 4 and stop there rather than working through the whole backlog.
