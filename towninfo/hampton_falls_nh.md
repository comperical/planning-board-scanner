# Hampton Falls, NH — Planning Board Web Access

Investigated: 2026-09-14

Small Rockingham County town, runs standard CivicPlus Agenda Center (see
PATTERNS.md), but serves **`.docx` instead of PDF** — the first town in
this project where that's the case. No bot protection.

## Platform notes

- Main site: `https://www.hamptonfalls.org`. Planning Board hub:
  `/250/Planning-Board`. Agenda Center for this board:
  `/AgendaCenter/Planning-Board-4`.
- Content-Type comes back as
  `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
  — this project's PDF toolchain won't work on these directly (see
  PATTERNS.md TODOs).
- Board meets 4th Tuesday monthly (3rd Tuesday in Nov/Dec).

## Document content

- Not yet analyzed (docx, not text-extractable with current tools).
  Sample files pulled for a future docx-handling pass:
  - `working/hampton_falls_nh/2026-08-25 PB Agenda.docx` (kept its real
    filename via Content-Disposition)
  - `working/hampton_falls_nh/_06232026-147` (Jun 23, 2026 minutes, no
    extension — is actually a .docx, rename before use)

## Open items for later

- Confirm whether *all* entries in this town's Agenda Center are `.docx`,
  or whether some meeting types post PDFs instead.
