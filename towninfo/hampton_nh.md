# Hampton, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://www.hamptonnh.gov` — CivicPlus **CivicEngage**, using the standard **Agenda Center** module (same family as other CivicPlus towns, but a different module than Exeter/Newmarket's custom `/meetings` table or CivicClerk portal).
- No Cloudflare or bot-challenge encountered.

## Finding the archive

- Board page: `hamptonnh.gov/318/Planning-Board` links to the Agenda Center, filtered to this board: `https://www.hamptonnh.gov/AgendaCenter/Planning-Board-7`.
- The Agenda Center page is a year-grouped table (`▼ Planning Board` / 2026, 2025, 2024, "View More") with columns **Agenda | Minutes | Media | Download**, one row per meeting date. "Media" links go to a Cablecast video portal (`reflect-hamptonnh.cablecast.tv`). Rows include not just the Planning Board's own regular meetings but its subcommittees filed under the same tab: **Capital Improvements Plan (CIP) Committee**, **Master Plan Implementation Committee**, **Plan Review Committee**, and ad hoc **Pre-Construction Meetings** for specific addresses.

## URL structure — static and directly fetchable

```
https://www.hamptonnh.gov/AgendaCenter/ViewFile/Agenda/_MMDDYYYY-{id}
https://www.hamptonnh.gov/AgendaCenter/ViewFile/Minutes/_MMDDYYYY-{id}
```

- Confirmed working with plain `FetchUrl` (no browser/session needed) — this is the same easy pattern as Rochester and Exeter, better than Dover's or Newmarket's session-scoped/TLS-blocked approaches.
- `{id}` is a small sequential integer, embedded directly in the listing page's links — no separate lookup step needed like Exeter's node ids.
- The `Minutes` fetch didn't carry a `Content-Disposition` filename in one test, so `FetchUrl`'s default-name fallback used the URL's last path segment (no `.pdf` extension) — rename after downloading if that matters, or just point the PDF tools at it directly (they don't care about extension).

## ⭐ Key find: "Active Applications to the Planning Board" page

- `https://www.hamptonnh.gov/720/Active-Applications-to-the-Planning-Boar` (note: URL is truncated/typo'd by the town itself, missing the final `d`).
- This is a **standalone, continuously-updated leads page** — arguably the richest single resource found across all towns studied in this project so far. It lists every currently-pending case under headings (New Public Hearings / Continued Public Hearings / Attending to be Heard / Other Business / Plan Review Committee), each entry giving:
  - Town case number (e.g. `26-028`), site address, Map/Lot, applicant name, owner of record, a plain-English project description, and the exact Planning Board hearing date.
  - Direct links to the actual submitted documents via `DocumentCenter/View/{id}/{filename}` — application form, plan sets, drainage analyses, stormwater O&M manuals, traffic memos, wetlands permits, Conservation Commission recommendation letters, town planner memos, etc. — every revision round kept (e.g. "Original PRC Submission" → "Second PRC Submission" → "Public Hearing Submission" for one case, each with its own document set).
  - Sample case: 44 Sweetbriar Lane — Green & Company site plan to merge two lots, demolish an existing house, and build a 19-unit multi-family condominium development with a privately-owned road.
- This page alone, kept up to date, may be a better lead-generation source than parsing agendas/minutes at all — it's already pre-filtered to *active* projects, with case status implicit in the submission-round documents present.

## Document content

- **Agenda PDF**: much lighter than Exeter's/Newmarket's — often just section headers (Call to Order, Public Hearings, Consideration of Minutes, Other Business) with terse one-line item references (e.g. "98 Ashworth Avenue - Request for one-year extension of Planning Board conditional site plan approval") rather than full case paragraphs. **The Active Applications page carries the real detail** that the agenda itself lacks.
- **DocumentCenter files**: confirmed working via `FetchUrl` — sample "Falcone Cir Amended Subdivision Application" was a normal 12-page text PDF, no session/auth needed.

## Sample downloads (in `working/hampton_nh/`)

- `09.16.2026 Agenda.pdf` — light regular-meeting agenda (CIP adoption, extension request, no new hearings that date)
- `_08192026-2057` — minutes PDF for Aug 19, 2026 (no `.pdf` extension due to missing Content-Disposition header)
- `Falcone Cir Amended Application for website.pdf` — sample case document pulled from the Active Applications page (amended subdivision application, 12 pages)

## Comparison to other NH towns studied

| | Rochester | Dover | Exeter | Newmarket | Hampton |
|---|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicEngage + CivicClerk portal | CivicPlus CivicEngage (Agenda Center) |
| Bot protection | Cloudflare hard-blocks headless | None | None | None | None |
| PDF URLs | Stable, static, guessable | Session-scoped temp URLs | Static, node-id not guessable | Static API, but **TLS-blocked** for this env's `requests` | Static, `FetchUrl`-able directly, id visible in listing |
| Case-level detail source | Agenda | Agenda + Materials PDF | Agenda + Packet PDF | Agenda + per-file attachments | **Dedicated live "Active Applications" leads page**, agenda itself is terse |
| Supporting docs | Not bundled | Bundled | Bundled | Bundled + per-file | Linked per-case from Active Applications page, each revision round kept |

## Open questions / not yet checked

- Whether other Hampton boards (Zoning Board of Adjustment, Conservation Commission) have an equivalent "Active Applications" page — if so, this pattern could generalize well.
- How far back the Agenda Center's "View More" years go, and whether very old entries still resolve via the same `ViewFile` URL pattern.
- Whether the Active Applications page is reliably kept current (it's manually maintained prose, not auto-generated from a case database) — worth periodic re-checking rather than treating as a one-time source.
- Video content on Cablecast — not explored, likely lower priority than the document trail already available.
