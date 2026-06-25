---
name: referral-checkin
description: Use weekly (or whenever Storia ships something notable — new client, workshop, case study) to check which referral partners are due for a check-in, draft a personalized message in James's voice, and create it as an Outlook draft (plus a ClickUp task) for James to review and send himself. Trigger on "check referral partners", "who's due for a check-in", "referral check-in", or after a notable win to fire an event-triggered touch.
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Scoped via [[.claude/skills/level-up/SKILL|/level-up]] on 2026-06-24 — full spec in [[log]]. Solves James's stated growth lever (a referral channel through trusted advisors) without depending on him remembering to follow up.

**Autonomy level: L2 (Drafted).** This skill never sends anything. It drafts, creates a real Outlook draft (via `scripts/outlook_draft.py`, added 2026-06-25 — see [[outlook-api]]) plus a ClickUp task for tracking, and James reviews/edits/sends manually every time.

## Inputs

- [[referral-partners]] — the partner list: name, org, status (warm / to-cultivate), last touch, next due, notes
- [[log]] — recent entries (last ~30 days) for real, specific wins to reference (not generic "just checking in")
- ClickUp (via MCP) — optionally cross-check recently completed/shipped tasks for additional win material
- [[voice]] — tone: short, casual, specific. The TeeFinder email (three sentences) is the calibration example. If a draft reads like relationship-marketing copy, it has failed — rewrite shorter and more specific.

## Execution

### Step 1 — Determine who's due

Read [[referral-partners]]. A partner is due if:
- **Cadence trigger:** today ≥ "Next due" date, OR "Next due" is blank (never contacted)
- **Event trigger:** James explicitly says "we just shipped X, check in with partners about it" — in this case, treat ALL warm partners as due regardless of cadence, using X as the hook

**Status matters:** `warm` partners get a check-in (relationship maintenance, reference a real recent win). `to-cultivate` partners get a first-touch message instead — different framing, since there's no relationship yet to "check in" on. Don't draft a to-cultivate message identical in tone to a warm one.

If nobody is due and there's no event trigger, say so and stop. Don't manufacture busywork.

### Step 2 — Gather real context

For each due partner, pull:
1. A specific recent win from [[log]] (last 30 days) or ClickUp — something concrete, not "things have been busy." If nothing genuinely relevant exists, say so rather than inventing filler.
2. The partner's `Notes` field from [[referral-partners]] for relationship context (e.g. "runs workshops," "met once, no second touch yet")

### Step 3 — Draft the message

One draft per due partner. Match James's voice exactly — short sentences, casual, specific, no em dashes, bullet points over paragraphs where it fits. Reference the real win from Step 2. For `to-cultivate` partners, the draft is a first-touch, not a check-in — introduce briefly, reference why this specific person/org is relevant (e.g. ICP overlap), no hard pitch.

**If the draft reads like marketing copy, rewrite it shorter.** This is the explicit failure mode James flagged when scoping — a polished draft means he rewrites from scratch and the system stops getting used.

### Step 4 — Create the Outlook draft

For each due partner with a known email, create a real draft via `python scripts/outlook_draft.py <to> <subject> <body_text_file>` — lands in James's Drafts folder, never sent. If no email is on file, skip this step and rely on the ClickUp task alone.

### Step 5 — Create the ClickUp task

One ClickUp task per due partner (use `mcp__clickup__clickup_create_task` in a sensible list — ask James which list the first time, then reuse it). Task title: `Referral check-in: {partner name}`. Task description: the full drafted message, a one-line note on why now (cadence due / event trigger + which win), and the Outlook draft link from Step 4 if one was created.

### Step 6 — Update the tracking file

Set `Next due` to today + 30 days for each partner a task was created for, so the cadence doesn't re-fire daily while the draft sits unreviewed. **Do not update `Last touch`** — that only reflects a message actually sent, which this skill can't confirm (sending happens outside ClickUp/Outlook). Leave a note in the partner's row like "draft queued {date}" and let James update `Last touch` himself once sent.

### Step 7 — Report back

Summarize: who got a draft and why (cadence/event), link to the Outlook draft and the ClickUp task, and a reminder that nothing was sent — these are drafts awaiting review.

## Notes

- **Read-mostly except drafts.** Writes are: the Outlook draft (never sent), the ClickUp task creation, and the `Next due` field in [[referral-partners]]. Never touch `Last touch` (see Step 6), never send anything.
- **Don't run this on autopilot.** It's Phase 1 of the Bike Method — run it manually when triggered (weekly review or a notable win), not on a hidden schedule, until James has validated several rounds of drafts and decided to advance the phase himself.
- **KPI this serves:** 2 referral-sourced signed clients by 2026-09-30, 3 active referral partners by 2026-09-30. If after a few months this isn't producing introductions, that's a signal to revisit — see the Kill Switch principle in [[3ms-framework]].

---
> *Adapted from The Three Ms of AI™ © 2026 Nate Herk. All rights reserved.*
