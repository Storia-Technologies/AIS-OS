# Connections

Registry of every system your AIOS can reach. Filled by [[.claude/skills/onboard/SKILL|/onboard]] from Q4-Q7 answers; expanded over time as you wire new tools. [[.claude/skills/audit/SKILL|/audit]] checks this file for domain coverage and freshness.

| # | Domain | Tool | Mechanism | Auth | Last checked |
|---|---|---|---|---|---|
| 1 | Revenue / Financials | Xero (primary), Stripe (online payments), direct EFT reconciled in Xero | mcp (native, financial snapshots) + script (Accounting API, scripts/xero_data.py, contact/invoice lookup) — Xero live; Stripe not yet | OAuth (live, both paths) | 2026-06-24 |
| 2 | Customer interactions | Outlook email (james@storia.tech), WhatsApp, Phone/iMessage | mcp (native, read-only) for search/read — script (scripts/outlook_mail.py search, scripts/outlook_draft.py create-draft+attachment) for writes, since the native connector can't send/draft | OAuth (live) | 2026-06-25 |
| 3 | Calendar | Outlook Calendar (inferred from Outlook email) | mcp (native, primary) — script (scripts/outlook_calendar.py) kept as fallback | OAuth (live) | 2026-06-24 |
| 4 | Communication | Microsoft Teams (internal — Kevin, Meliton, Jordan) | mcp (native, primary) — script (scripts/teams_messages.py) kept as fallback | OAuth (live) | 2026-06-24 |
| 5 | Project / task tracking | ClickUp | mcp | OAuth (live) | 2026-06-24 |
| 6 | Meeting intelligence | Fireflies (recordings/transcripts), SharePoint (docs, proposals, contracts) | mcp (native, primary — full transcript access) — script (scripts/fireflies_transcripts.py) kept as fallback | OAuth/API key (live) | 2026-06-24 |
| 7 | Knowledge / files | SharePoint | mcp (native, primary) — script (scripts/sharepoint_files.py) kept as fallback | OAuth (live) | 2026-06-24 |
| 8 | Lead pipeline / sales | GoHighLevel (GHL) | script (scripts/ghl_pipeline.py, opportunities/pipelines API) | Private Integration Token (live) | 2026-06-24 |

**Mechanism options:** `mcp` (MCP server), `script` (Python/Bash hitting an API, in `scripts/`), `export` (CSV/JSON dump pipeline), `key+ref` (`.env` key + `references/{tool}-api.md` guide), `not yet connected`.

When you wire a new tool, also save `references/{tool}-api.md` capturing endpoints, auth flow, and common queries — researched-once-saved-forever. See [[outlook-api]], [[xero-api]], [[fireflies-api]], [[gohighlevel-api]] for the ones already written.
