# Epsom, NH — Planning Board Web Access

Investigated: 2026-09-14

Merrimack County town, northeast of Pembroke. Platform: **Munibit** (see
PATTERNS.md) — no bot protection encountered. **Partial — access not
fully resolved.**

## Platform notes

- Main site: `https://www.epsomnh.gov`. Agendas & Minutes page:
  `/agendasandminutes` — a nested accordion (year → month → item, four
  click levels total) — the deepest UI nesting found in this project.
- Clicking "View" does **not** navigate to a visible URL — the document is
  very likely opened via a JS-driven fetch to
  `/api/blob/viewBlob?rf=t&i={token}`. A token pulled from a stale
  search-engine-cached URL returned `500 Internal Server Error` — old
  tokens don't stay valid; a fresh token must be captured from a live
  page interaction.
- Not yet confirmed whether a *fresh* token is fetchable with plain
  `requests`, or requires the same-origin browser treatment (see
  PATTERNS.md hotlink gotcha).

## Document content

- Not sampled this session — blocked on obtaining a valid, live blob
  token. Board/committee list confirms a normal small-town lineup
  (Planning Board, Conservation Commission, ZBA, etc.), each with its own
  Agendas + Minutes tree branch.

## Open items for later

- Capture a fresh `/api/blob/viewBlob` token by intercepting the network
  request the "View" button fires, then confirm whether plain `requests`
  works with a fresh token or needs in-page-fetch treatment.
