---
name: daily-update
description: The morning protocol that brings every town up to date - re-scan each town whose last good scan is 7+ days old, analyze every newly found document, find contacts for the new projects, and finish with a DailyReport summary. Use when asked to "run the daily update", "do the morning run", "bring the towns up to date", or /daily-update.
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

The browser session is opened lazily in step 1 only when a town needs it
(`playwright-cli -s=planscan list` first; open headed for Cloudflare towns -
kingston, madbury, brentwood, rochester - see their towninfo files).

## 1. Scan every town that's due

```bash
wwiocode/pyscript/plan_entry.py NextToScan due_days=7 limit=25
```

`due_days=7` returns only towns whose last *good* scan is at least 7 days
old (never-scanned towns first, then oldest). `limit=25` is the daily cap:
steady state is ~10 towns/day (68 towns / 7 days), so 25 absorbs a missed
day or two and still clears the backlog. If more than 25 are due, the rest
come up tomorrow, oldest first - don't raise the cap mid-run.

Also note any "towninfo write-up(s) with no town row" it lists - those are
new towns that have never been scanned; include them.

For each town in the list, in order:

1. `StartScanLog town=<slug>` - note the scan_id.
2. Read `towninfo/<slug>.md` (and `towninfo/PATTERNS.md` for its platform)
   - it has the listing URL and quirks. The previous scan's notes (shown in
   `DailyReport` / `scan_log.wisp`) say what was newest last time and what
   meeting is expected next.
3. Check the listing for anything not already in the DB: agendas, minutes,
   and packets newer than the town's latest `doc_date`, plus older items
   that have appeared since (minutes are often posted weeks late). Use
   `DbStatus town=<slug>` if unsure what's already registered.
4. Download each new file into `working/<slug>/` (`FetchUrl dest=`, or the
   `ClaimDownload` route for Cloudflare towns), then
   `IngestPdfTool pdf=... source_url=... date=YYYY-MM-DD scan_id=<id>`.
5. If the site's layout or URLs differ from what towninfo says, fix the
   towninfo file now.
6. `EndScanLog scan_id=<id> notes="..."` - what's newest on the site, what
   was downloaded, and what's expected next (e.g. "latest agenda 9/17
   (have), 1 new: 9/17 minutes. Next expected: 10/1 agenda").

**If a town can't be checked** (site down, bot block that headed mode
doesn't clear, archive moved and can't be found in a few minutes): don't
sink time into it. Close the pass with notes starting `FAILED:` -
`EndScanLog scan_id=<id> notes="FAILED: <reason>"` - and move on.
`NextToScan` ignores FAILED passes, so the town is retried tomorrow. Never
leave a pass without an `EndScanLog`; unclosed passes are flagged in the
report.

## 2. Analyze everything new

Run the analyze-planning-file loop until `NextToAnalyze` reports nothing
left. **The skill's default cap of 4 documents does not apply here** -
daily volume is normally 5-15 documents; analyze them all. Keep the usual
rules: check existing projects before creating, tag every project, update
stage tags when a document moves a project forward, `LinkProject` with
`page=`, and always `LogAnalysis`.

## 3. Find contacts for today's new projects

Run the contact-search loop over the projects created in step 2 (the
report's "New projects" list; highest `project_id`s first, which is the
skill's default order). **Cap it at 15 projects per run** - on a heavy day
prioritize `large` projects and those with a named developer/builder or
engineer, and let the rest wait for the next run or a standalone
`/contact-search`. Keep the skill's rules: check existing contacts before
creating, reuse firms across projects, and don't record guessed details.

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
projects covered, contacts created vs reused.

End the session with a short message: the highlights, counts (towns
scanned / failed, new documents, new and updated projects, contacts added),
the path to the
saved report, and how many towns are still due (from the report's
"Outstanding" section).
