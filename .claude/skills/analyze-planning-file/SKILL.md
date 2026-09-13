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

Picks the oldest (`doc_date`) document with zero `analysis_log` rows. If it
prints "Nothing left to analyze", stop - the backlog is empty (for that
town, if filtered).

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

(lists every project's `short_desc` under that town). Match by
address/applicant, not exact wording.

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
  summary"}`. Use the Write tool.

Then apply both:

```bash
wwiocode/pyscript/plan_entry.py ApplyProjectEdit project_id=<project_id>
```

This deletes the `.md`/`.json` files once applied - `working/project_edit/`
should only ever hold edits not yet synced to the DB, never accumulate. Do
not manually delete or leave stray files there.

**Existing project mentioned again** (this document is a later
minutes/extension/approval for a project already recorded): just link it,
no new row:

```bash
wwiocode/pyscript/plan_entry.py LinkProject project_id=<id> pdf=<path>
```

A document can yield zero, one, or several projects - create/link one at a
time for each.

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
per session.
