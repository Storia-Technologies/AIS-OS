---
name: business-brief
description: Use weekly (Friday) or on-demand ("how's my business doing", "where should I focus", "business brief") to pull pipeline, cash, task load, and relationship context into one readable status report with actual recommendations on where to focus. Renders to a static HTML file James opens as his browser homepage. Trigger on "business brief", "how's my business doing", "where should I focus", "give me an overview".
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Scoped via [[.claude/skills/level-up/SKILL|/level-up]] on 2026-06-25 — full spec in [[log]]. James's own words: "I am jumping between potential leads, business opportunities, projects, managing staff, numbers and trying to find leads." Nothing currently answers "how is my business doing" in one place — the closest thing is digging through GHL, Xero, ClickUp, Storia SB, and a separate Chief of Staff project by hand, the way this got scoped in the first place (a live TeeFinder pricing mismatch between two of those systems is what surfaced the need).

This is not a numbers readout. James explicitly asked for **recommendations**, not just a data dump — the AI step has to do real synthesis: read everything, decide what actually needs attention this week, and say so with reasoning.

**Autonomy level: L2-ish, but read-only and low-stakes.** Unlike the other skills, this one writes nothing anywhere external — it only reads from every source and renders a local HTML file. There's no draft to approve before "sending" because nothing gets sent. James reviews the output by opening his browser; if something's wrong, the fix is asking for the next run with a correction, same as any other AI summary.

## Trigger

Both: a standing weekly cadence (Friday, same day as [[.claude/skills/level-up/SKILL|/level-up]]) and on-demand any time James asks.

## Inputs

- **GoHighLevel** (`scripts/ghl_pipeline.py pipelines` / `stale 3` / `triage`) — pipeline by stage/value, days since last activity
- **Xero** (`scripts/xero_data.py`, or native Xero MCP tools — `get_cash_position`, `get_financial_position`, `get_contacts_and_receivables`) — cash position, receivables, anything overdue
- **ClickUp** (MCP — `clickup_get_workspace_hierarchy`, `clickup_filter_tasks`) — open/overdue task counts per client or project
- **Storia SB** (`wiki/index.md` and relevant customer pages, at `C:\Users\James Manning\OneDrive\Vaults\Storia SB`) — relationship context, any flagged risks
- **Chief of Staff project** (`D:\Projects\claude\Chief Of Staff\pipeline.md`, `goals.md`, `contacts.md`) — James keeps a second, independently-maintained set of pipeline/relationship notes here. **Read it every time.** Don't treat GHL as automatically more authoritative — if the two disagree (e.g. the 2026-06-25 TeeFinder mismatch: $50-70K in this AIOS vs $75-110K in Chief of Staff's pipeline.md), surface the conflict in the brief rather than silently picking one. Same rule the Storia SB wiki already follows for contradictions.
- [[priorities]] — to weight recommendations against what James actually said matters this quarter

## Execution

### Step 1 — Gather the data

Run `python scripts/ghl_pipeline.py triage` and `python scripts/xero_data.py` (or the native Xero MCP tools) for structured figures. Pull ClickUp task counts via MCP. Read the Storia SB index + any customer pages flagged as active/at-risk. Read the Chief of Staff project's `pipeline.md`, `goals.md`, and `contacts.md` in full — they're short enough to read directly each time.

### Step 2 — Reconcile and flag

Cross-check GHL pipeline entries against Chief of Staff's `pipeline.md` by client name. Where they agree, use either figure. Where they disagree (value, stage, next action), note both and flag it explicitly — don't average or guess which is right.

### Step 3 — Identify what needs attention

Apply the agreed decision points:
- Stale GHL deals (3+ days untouched, same threshold as [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]])
- Deals approaching their pricing-validity deadline (Storia's standard T&Cs: 30 days from proposal date — check against proposal/quote dates in GHL or Chief of Staff's pipeline.md)
- Cash/receivables concerns (low cash position, overdue invoices)
- ClickUp overload (a client or project with an unusually high open/overdue task count relative to others)
- Relationship-risk flags already noted anywhere (e.g. Chief of Staff's "Clear Health Psychology — relationship at risk" note)
- Any GHL ↔ Chief of Staff data conflicts from Step 2

### Step 4 — Write the recommendations

This is the part that has to be genuinely useful, not generic. For each flagged item, write what it is, why it matters (tie back to [[priorities]] where relevant — e.g. "TeeFinder is one of the three named Q3 priorities"), and what James should actually do about it. Rank by urgency/impact, don't just list in the order data came in. If nothing is flagged in a category, say so briefly rather than padding the report.

### Step 5 — Render the HTML

Write a single self-contained HTML file to `business_brief.html` (repo root, gitignored — overwritten every run). Inline CSS, no external dependencies, so it opens cleanly as a local file. Use Storia's teal (#1A9E9E) and the logo at `references/storia-logo.jpg` (embed as base64 so the file works standalone if moved).

**Compact dashboard layout (James asked for minimal scrolling 2026-06-25) — keep this on every run:**
- Small header bar (logo + title + generated timestamp, single row, ~13-19px text)
- A 4-up stat-card row right under the header: cash balance, awaiting payment, payables due, overdue
- A two-column CSS grid below that: left column (wider, ~60%) holds "Where to focus this week" as compact recommendation cards (small tag + title + 1-3 sentence body, no padding to spare); right column (narrower) stacks smaller cards — GHL pipeline table, anything tracked elsewhere not in GHL, top receivables, task-load note
- Base font ~13px, table text ~11.5-12px, no wasted vertical whitespace between sections
- Don't revert to a single stacked column — the whole point was fitting more on one screen

Tell James the file path once done: `d:\Projects\storia-ai-os\business_brief.html`. He sets this as his browser's homepage/default new tab so it's always current as of the last run.

## Notes

- **Read-only everywhere except the local HTML file.** No GHL writes, no Xero writes, no ClickUp writes, nothing sent anywhere. Lowest-risk skill in the kit.
- **Don't run this on autopilot.** Phase 1 of the Bike Method — run manually (Friday or on-demand) until James has validated several rounds and decides whether to advance autonomy himself (e.g. an actual scheduled regeneration).
- **KPI this serves:**
  - Less cost: time from "how's my business doing" to having an answer — target a few seconds (open browser), down from ad hoc digging across 4+ systems.
  - More customers: stale leads and at-risk relationships get caught and actioned before going cold, instead of sitting unnoticed in a markdown file nobody re-reads.
  - See [[log]] (2026-06-25, business-brief entry) for the full spec.
- If the two-systems conflict (GHL vs. Chief of Staff) keeps recurring, that's a signal worth raising with James directly — this skill flags conflicts, it doesn't resolve the underlying duplication.

---
> *Adapted from The Three Ms of AI™ © 2026 Nate Herk. All rights reserved.*
