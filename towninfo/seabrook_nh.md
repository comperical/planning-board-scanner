# Seabrook, NH — Planning Board Web Access

Investigated: 2026-09-12

## Platform

- Site: `https://seabrooknh.info` — note the unusual `.info` TLD (not `.gov`), a WordPress site (Divi-family theme with an accessiBe accessibility widget bolted on). Static PDFs live under a normal WordPress `wp-content/uploads/{year}/{month}/{file}.pdf` structure.
- No Cloudflare or bot-challenge encountered — everything loads/fetches cleanly, including plain `FetchUrl`.

## ⚠️ Important gotcha: the obvious page is stale, a different page is current

- Google/web-search and the site's own old permalinks point to two standalone pages — `https://seabrooknh.info/planning-board-agendas/` and `https://seabrooknh.info/planning-board-minutes/` — whose "current year" sections are **stuck at February/March 2023**. These look like the canonical archive pages but have not been updated in ~3.5 years, despite the town clearly still holding Planning Board meetings (confirmed via the site's own event calendar showing meetings scheduled through at least Sept 2026).
- **The actually-current listing lives on a different page**: `https://seabrooknh.info/boards-and-committees/planning-board/`, which has a tabbed interface (**Meeting Agendas** / **Meeting Minutes** / **Relevant Links**) showing agendas up to Sept 14, 2026 and minutes up to Jun 15, 2026 (minutes lag behind agendas by a meeting or two, as expected pending board approval).
- **Always use the `/boards-and-committees/planning-board/` page, not `/planning-board-agendas/` or `/planning-board-minutes/`.** The latter two still exist and rank in search, but are effectively dead pages frozen at a past redesign point. This kind of split (one page abandoned mid-migration, another quietly taking over) is worth checking for on any WordPress-based town site before concluding "this town's agendas end in [old year]."
- The town calendar's individual event pages (`/events/planning-board-...`) carry only date/time/location — no agenda attachment — so they're not a substitute source.

## URL structure — static and directly fetchable

```
https://seabrooknh.info/wp-content/uploads/{YYYY}/{MM}/{filename}.pdf
```

- Confirmed working with plain `FetchUrl`, no browser needed — same ease as Rochester/Exeter/Hampton.
- `{filename}` has no consistent convention (`September-14th.pdf`, `Feb-23rd.pdf`, `June-1stdocx.pdf`, `March-9th.pdf`) and the upload month folder doesn't always match the meeting month (e.g. a June 15 minutes PDF was uploaded into the `2026/08` folder) — always read the actual link from the listing page rather than guessing the path.
- Older years (2007–2025) are archived under per-year sub-pages (`/planning-board-agendas/2022-agendas/`, `/planning-board-minutes/2020-2/`, etc., with inconsistent slug patterns across years) rather than one continuous list — expect to open each year's page separately for historical research.

## Document content

- **Agenda PDF**: short and plain-text, no letterhead formatting. Gives case number, applicant/business name, project type (Conditional Use Permit, site plan, etc.), address, and Tax Map/Lot — enough to identify a lead but with much less narrative detail than Exeter's or Newmarket's agendas. Sample (Sept 14, 2026): a Master Plan update hearing, a new Conditional Use Permit case for VRP Cleaning LLC at 1 Eaton Lane (Tax Map 7, Lot 34-4), and a release of site security for the (already-built) Aldi's Grocery Store case.
- No separate "packet" or bundled materials PDF was found for Seabrook — the agenda appears to be the only document type published per meeting (plus the eventual minutes).

## Sample downloads (in `working/seabrook_nh/`)

- `September-14th.pdf` — Sept 14, 2026 Planning Board agenda (Master Plan hearing, new CUP case, Aldi's security release)
- `June15th.pdf` — Jun 15, 2026 Planning Board minutes

## Comparison to other NH towns studied

| | Rochester | Dover | Exeter | Newmarket | Hampton | Seabrook |
|---|---|---|---|---|---|---|
| CMS | CivicPlus (Drupal) | Custom + Treeno | Drupal (municodeWEB) | CivicEngage + CivicClerk | CivicPlus CivicEngage | WordPress (Divi), `.info` domain |
| Bot protection | Cloudflare hard-blocks headless | None | None | None | None | None |
| PDF URLs | Stable, static, guessable | Session-scoped | Static, node-id not guessable | Static API, TLS-blocked here | Static, `FetchUrl`-able | Static, `FetchUrl`-able, filenames irregular |
| Current listing findability | Straightforward | Straightforward | Straightforward | Straightforward | Straightforward | **Two competing pages — the search-indexed one is 3.5 years stale** |
| Case-level detail | Agenda only | Agenda + Materials | Agenda + Packet | Agenda + per-file | Terse agenda; rich separate leads page | Terse agenda; case #, applicant, tax map/lot only |

## Open questions / not yet checked

- Whether there's any bundled "materials"/packet PDF per case (not found so far — may simply not exist, or may be available on request/in person only).
- Whether Seabrook has an equivalent to Hampton's "Active Applications" leads page — worth a targeted search, given the terse agendas here would benefit from one.
- Whether the Zoning Board and Board of Selectmen pages on this same site have the same "stale standalone page vs. current tabbed page" split — if so, that's a site-wide pattern to watch for when this WordPress site was restructured.
- Exact date of the site restructuring that left the old pages orphaned (agendas page stops in March 2023; tabbed page presumably started around then) — not critical, but would confirm the theory.
