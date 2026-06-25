---
name: pipeline-checkin
description: Use weekly (or on-demand "check my pipeline") to scan GoHighLevel for leads going cold, draft a follow-up per stale lead, and create it as an Outlook draft (plus a ClickUp task) for James to review and send himself. Trigger on "check my pipeline", "any stale leads", "pipeline check-in".
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Scoped via [[.claude/skills/level-up/SKILL|/level-up]] on 2026-06-24 — full spec in [[log]]. Solves James's stated growth lever (leads going cold because the pipeline lives in his head + email) by making GoHighLevel the system of record and surfacing anything untouched.

**Autonomy level: L2 (Drafted).** This skill never sends anything and never moves a GHL stage. It drafts a follow-up, creates a real Outlook draft (via `scripts/outlook_draft.py`, added 2026-06-25 — see [[outlook-api]]) plus a ClickUp task for tracking, and James reviews/edits/sends and moves the stage himself.

## Inputs

- GoHighLevel (via `scripts/ghl_pipeline.py`) — open opportunities, pipeline stages, days since last activity. See [[gohighlevel-api]] for auth setup and endpoint notes.
- Outlook (via MCP) — optional thread context for the lead, especially referral-sourced ones (cross-check [[referral-partners]] for the source relationship)
- [[voice]] — tone: short, casual, specific. No em dashes, bullets over paragraphs.

## Execution

### Step 1 — Pull stale opportunities

Run `python scripts/ghl_pipeline.py stale 3` (3-day threshold, per the Method scoping — adjust only if James asks). If `GHL_PIT` / `GHL_LOCATION_ID` aren't set in `.env` yet, stop and point James to [[gohighlevel-api]] to generate the Private Integration Token first.

If nothing is stale, say so and stop. Don't manufacture busywork.

### Step 2 — Gather context per stale lead

For each stale opportunity:
1. Pull the contact name, opportunity name/value, current stage, and days stale from the script output.
2. If the lead came from a referral partner (check [[referral-partners]]), note that — it changes the tone of the follow-up (warmer, can reference the referrer).
3. Check Outlook for the most recent thread with that contact, if any, so the draft doesn't repeat something already said.

### Step 3 — Draft the follow-up

One draft per stale lead, in James's voice ([[voice]]) — short, casual, specific, no em dashes. Reference real context (their stated need, last thing discussed) — never generic "just checking in." If a referral partner sourced the lead, the draft can lean on that warmth; if cold/direct, keep it brief and value-forward.

**If the draft reads like sales copy, rewrite it shorter.** Same failure mode as `referral-checkin` — a polished draft means James rewrites from scratch and stops trusting the system.

### Step 4 — Create the Outlook draft

For each stale lead with a known contact email, create a real draft via `python scripts/outlook_draft.py <to> <subject> <body_text_file>` — this lands in James's Drafts folder, never sent. If no contact email is available, skip this step and rely on the ClickUp task alone.

### Step 5 — Create the ClickUp task

One ClickUp task per stale lead (`mcp__clickup__clickup_create_task` — ask James which list the first time, then reuse it). Task title: `Pipeline follow-up: {contact/opportunity name}`. Description: the drafted message, current stage, days stale, a one-line note on source (referral partner name, or "direct/cold"), and the Outlook draft link from Step 4 if one was created.

### Step 6 — Report back

Summarize: how many stale leads found, one line each (name, days stale, stage), link to the Outlook draft and the ClickUp task. Remind James nothing was sent and no stage was moved — drafts await review, stage moves happen manually in GHL.

## Notes

- **Read-mostly except drafts.** Writes are: the Outlook draft (never sent) and the ClickUp task creation. Never writes to GHL, never sends anything.
- **Don't run this on autopilot.** Phase 1 of the Bike Method — run manually (weekly review or on-demand) until James has validated several rounds of drafts and decided to advance the phase himself.
- **KPI this serves:** no open opportunity untouched >3 days (leading), lead → signed client conversion rate (lagging, once GHL data accumulates). If after a few months this isn't catching real stale leads or the drafts aren't useful, that's a signal to revisit — see the Kill Switch principle in [[3ms-framework]].

---
> *Adapted from The Three Ms of AI™ © 2026 Nate Herk. All rights reserved.*
