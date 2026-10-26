---
name: daily-update
description: The morning protocol that brings every town up to date - re-scan every town that is due (no good scan in the last 7 days, stalest first), analyze every newly found document, find contacts for projects that have none, and finish with a DailyReport summary. Use when asked to "run the daily update", "do the morning run", "bring the towns up to date", or /daily-update.
---

# Daily Update

One run per morning. It sets the order and the limits, and relies on the
other skills for the actual work - load and follow them for each step:

- **planning-board-scanner** - permissions (one bare command per call, no
  pipes/chaining), scan logging, download/ingest tools.
- **analyze-planning-file** - the per-document analysis loop.
- **contact-search** - finding and recording contacts for projects.

Don't ask for confirmation between steps; run straight through to the
report. Only stop early if something is broken across the board (e.g. the
DB won't open, the browser session can't start).

## 0. Preflight

```bash
wwiocode/pyscript/plan_entry.py NextToAnalyze
```

If it finds a document, a previous run was interrupted mid-analysis - run
the analyze-planning-file loop until it reports nothing left before
scanning anything new, so today's report isn't mixed with leftovers.

Also check `working/project_edit/` for leftover `.md`/`.json` files from an
interrupted `ApplyProjectEdit` - finish applying them.

The browser session is opened (headed) in step 1 by the first
`scan-single-town` agent and left open for the following towns.

## 1. Scan every town that is due

```bash
wwiocode/pyscript/plan_entry.py NextToScan due_days=7 limit=0
```

This lists every town that requires a scan: never-scanned towns first,
then any whose last good scan is 7+ days old (with 6h of slack), oldest
first. It's the same rule as the report's "still due" count, so a
complete run leaves that at zero. Scan all the towns it lists - don't add
more or stop short mid-run. If it lists none, go straight to step 2.

Also note any "towninfo write-up(s) with no town row" it lists - those are
new towns that have never been scanned; include them.

For each town in the list, in order, **one at a time** (never in
parallel - they share the `planscan` browser session and the DB), launch
the **`scan-single-town`** agent (Agent tool,
`subagent_type: "scan-single-town"`) with the prompt `Scan town <slug>`.
It runs in a fresh context: reads the towninfo write-up, opens/reuses the
browser session, downloads and ingests new files, fixes towninfo if the
site changed, and opens and closes the scan log pass itself. Don't do the
scan work yourself in the main context.

It replies with a short block:

```
town: <slug>  scan_id: <id>  status: ok|FAILED
new docs: <n> (...)
towninfo updated: no | yes - ...
notes: ...
```

Keep these blocks - they feed the report highlights and final counts.

**Safety net:** if an agent errors out, or returns without a `scan_id` /
status (so its pass may be unclosed), run `DailyReport` - it marks
unclosed passes `UNCLOSED` with their scan_id - and close the town's pass
with
`EndScanLog scan_id=<id> notes="FAILED: scan agent did not finish"`, then
move on to the next town. `NextToScan` ignores FAILED passes, so the town
is retried tomorrow. Never leave a pass without an `EndScanLog`.

## 2. Analyze everything new

Run the analyze-planning-file loop until `NextToAnalyze` reports nothing
left. **The skill's default cap of 4 documents does not apply here** -
daily volume is normally 5-15 documents; analyze them all. Keep the usual
rules: check existing projects before creating, tag every project, set
`status` on every project and update it when a document moves a project
forward, `LinkProject` with
`page=`, and always `LogAnalysis`.

## 3. Find contacts for projects that have none

**This step is mandatory - never skip it**, even if no towns were due or
step 2 created no projects (e.g. a re-run after an interruption). Run the
contact-search loop over projects due for a search - that includes any
backlog from earlier runs, not just today's new ones:

```bash
wwiocode/pyscript/plan_entry.py NextForContactSearch limit=15 large_first=true
```

**Cap it at 15 projects per run** - `large_first=true` puts `large`
projects first; within the list, prefer those with a named
developer/builder or engineer, and let the rest wait for the next run or a
standalone `/contact-search`. Keep the skill's rules: check existing
contacts before creating, reuse firms across projects, don't record
guessed details, and **`LogContactSearch` every project you pick up** -
including `none_found`/`skipped` ones, or they'll be re-searched tomorrow.
Only if `NextForContactSearch` reports no projects due may you move on
with zero contacts added.

## 4. Report

```bash
wwiocode/pyscript/plan_entry.py DailyReport
```

(Covers the last 24h; pass `hours=48` etc. if the run spanned longer or
you're reporting on a missed day.) Save its output as
`working/reports/<YYYY-MM-DD>.md` with the Write tool, adding a short
**Highlights** section at the top in your own words: the 3-5 most notable
items for trades pros - new large projects, approvals, projects moving to
construction - and any towns that FAILED and why. Add a line on contacts:
projects covered (the report's "Contact searches" section has the
found / none found / skipped counts), contacts created vs reused.

End the session with a short message: the highlights, counts (towns
scanned / failed, new documents, new and updated projects, contacts added),
the path to the
saved report, and how many towns are still due (from the report's
"Outstanding" section - normally zero, or just the ones that FAILED).
