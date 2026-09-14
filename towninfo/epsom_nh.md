# Epsom, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, northeast of Pembroke. **First town in this
project on Munibit** (`munibit.com` — an eighth distinct municipal CMS
vendor found across this project, per the "Powered By Munibit" footer
credit). No bot protection encountered.

## Platform

- Main site: `https://www.epsomnh.gov`.
- Agendas & Minutes page: `/agendasandminutes` — a **nested tree widget**
  (React-style accordion), not a flat list: expand "Agendas" → "Planning
  Board Agendas" → a year (e.g. "2026") → a month (e.g. "September") to
  reveal individual dated entries, each with a "View" button (not a plain
  `<a href>` link) — the deepest UI nesting found in this project
  (year → month → item, four click levels total including the top
  category).
- Clicking "View" does **not** navigate to a visible new URL in this
  session's checks (page stayed at `/agendasandminutes#occdrw`) — the
  actual document is very likely opened via a JS-driven fetch to
  `/api/blob/viewBlob?rf=t&i={token}` (confirmed as the underlying
  endpoint shape from a search-indexed URL) rather than a plain anchor
  navigation, so the URL never showed up in the page's static link list.

## URL structure / access gotcha

- The blob endpoint is `https://www.epsomnh.gov/api/blob/viewBlob?rf=t&i={token}`
  — the `{token}` appears to be a **long, opaque, possibly time-limited or
  single-use** identifier tied to the page session it was generated in.
  **Confirmed a token pulled from a stale search-engine-cached URL
  returned `500 Internal Server Error`** via `FetchUrl` — meaning old
  tokens don't stay valid, and a fresh token must be captured from a live
  page interaction (e.g. intercepting the network request the "View"
  button triggers) rather than reused across sessions.
- Not yet confirmed whether a fresh token (captured via `playwright-cli
  eval` intercepting the underlying `fetch`/XHR call, or via browser
  network-log inspection) is fetchable with plain `requests`, or requires
  the same-origin browser treatment seen at Kingston/Madbury/Brentwood.

## Document content

- Not sampled this session — blocked on obtaining a valid, live blob
  token. Board/committee list confirms a normal small-town lineup
  (Planning Board, Conservation Commission, ZBA, etc.), each with its own
  Agendas + Minutes tree branch.

## Open items for later

- Capture a fresh `/api/blob/viewBlob` token by intercepting the network
  request the "View" button fires (e.g. via `playwright-cli` response
  logging) rather than reusing a stale search-cached URL, then confirm
  whether `FetchUrl` (plain `requests`) works with a fresh token or needs
  the in-page-fetch treatment.
