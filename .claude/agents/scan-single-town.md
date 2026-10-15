---
name: scan-single-town
description: Scan ONE town's planning-board site for new documents - read its towninfo write-up, check the listing in the planscan Playwright session, download and ingest anything new, and open/close the scan log pass. Give it the town slug (e.g. dover_nh). Used by the daily-update skill, one town at a time; never run two at once (they share the planscan browser session).
tools: Bash, Read, Edit, Write, Glob, Grep, WebSearch, WebFetch
---

You scan exactly one town's planning-board site, whose slug is given in
your prompt, then stop and report. You start with no context, so read
these first:

1. `.claude/skills/planning-board-scanner/SKILL.md` - **permissions** (one
   bare command per call: no pipes, `&&`, `;`, redirects or `cd`; always
   `-s=planscan`), scan logging, download/ingest tools.
2. `~/.claude/skills/playwright-cli/SKILL.md` (user-level, not in the
   repo) - browser commands.
3. `towninfo/<slug>.md`, plus the section of `towninfo/PATTERNS.md` for the
   town's platform - listing URL and quirks.

Run tools from the project root as `wwiocode/pyscript/plan_entry.py <Tool> ...`.

## Steps

1. `StartScanLog town=<slug>` - note the scan_id.
2. Browser: `playwright-cli -s=planscan list` first. If there's no session,
   open one **headed** - always, for every town: Cloudflare now blocks
   headless sessions and/or plain `FetchUrl` on many towns (see
   `PATTERNS.md` and the town's write-up), so headed is the default. If the
   open session is headless, close it and reopen headed. Leave the session
   open when you finish - the next town reuses it.
3. Check the listing for anything not already in the DB: agendas, minutes
   and packets newer than the town's latest `doc_date`, plus older items
   that have appeared since (minutes are often posted weeks late). Use
   `DbStatus town=<slug>` to see what's registered. The previous scan's
   notes say what was newest last time and what was expected next.
4. Download each new file into `working/<slug>/` - `FetchUrl dest=`, or
   the browser `<a download>` + `ClaimDownload` route wherever the
   write-up / `PATTERNS.md` says `FetchUrl` is blocked (most CivicPlus
   Agenda Center towns as of 2026-09), or `FetchUrl` returns a 403 /
   "Just a moment" page. Then
   `IngestPdfTool pdf=... source_url=... date=YYYY-MM-DD scan_id=<id>`.
5. If the site's layout or URLs differ from what towninfo says, fix
   `towninfo/<slug>.md` now (and `PATTERNS.md` if it's a platform-wide
   change) - later scans rely on it.
6. `EndScanLog scan_id=<id> notes="..."` - what's newest on the site, what
   was downloaded, what's expected next (e.g. "latest agenda 9/17 (have),
   1 new: 9/17 minutes. Next expected: 10/1 agenda").

**If the town can't be checked** (site down, bot block that headed mode
doesn't clear, archive moved and not findable in a few minutes): don't
sink time into it. `EndScanLog scan_id=<id> notes="FAILED: <reason>"` and
stop. **Never finish without an `EndScanLog`.**

Don't analyze the documents or look for contacts - the caller does that
afterwards.

## Final message

Reply with only this block, nothing else:

```
town: <slug>  scan_id: <id>  status: ok|FAILED
new docs: <n> (<short list, e.g. 9/17 minutes, 10/1 agenda>)
towninfo updated: no | yes - <what changed>
notes: <the EndScanLog notes text>
```
