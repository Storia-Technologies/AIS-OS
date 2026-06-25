---
name: client-onboarding
description: Use on-demand when a GHL deal goes Closed/Won ("draft agreement for X") and again once it's signed ("onboard X"). Drafts the engagement agreement and the post-signature kickoff (ClickUp project + welcome email), creates each as a real Outlook draft — never sends anything without explicit approval. Trigger on "draft agreement for <client>", "onboard <client>", "set up <client>".
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Scoped via [[.claude/skills/level-up/SKILL|/level-up]] on 2026-06-25 — full spec in [[log]]. e-Solar's deal went Closed/Won the same day, and the agreement doc + (eventual) ClickUp setup got built ad hoc, from scratch, in one long session. Nothing breaks if that keeps happening manually, but it's real recurring cost (rebuilding the same structure every time) and inconsistent customer experience (the customer's first impression of "working with Storia" depends on whatever James remembers to do that day). This skill makes the two real moments — *deal won* and *deal signed* — repeatable instead of reinvented.

These are genuinely two separate moments, often days apart, with a real precondition between them (signed or not). Don't try to collapse them into one "smart" trigger that guesses which phase applies — that would require watching GHL for signature status, which James has explicitly ruled out for now ("I am not going to live in GHL too much"). Two explicit on-demand triggers instead.

**Autonomy level: L2 (Drafted).** Matches `pipeline-checkin`/`lead-scan`. AI drafts the agreement and the kickoff email; James reviews and sends both himself, every time, no exceptions. The ClickUp project setup and any GHL note are mechanical (not customer-facing) and can run as part of generating the draft, without a separate approval step.

## Trigger A — "draft agreement for `<client>`" (deal won, not yet signed)

Run when a GHL opportunity moves to Closed/Won, or whenever James says a deal is agreed verbally and needs paperwork.

### Step 1 — Pull deal context
- GHL: opportunity name, value, contact, pipeline/stage (`python scripts/ghl_pipeline.py` — add a `find <query>` style lookup if one doesn't exist yet, or search by name/contact email).
- Scope context: the email thread or Storia SB customer page for this client — what was actually agreed (rate/value, deliverables, fixed-scope vs. T&M).
- A reference proposal/agreement doc with current Storia branding (find the most recent one in the client's SharePoint folder, or another recent client's, if this is a first engagement).

### Step 2 — Generate the doc
- Copy the reference doc (don't edit the original) into the client's SharePoint folder, named for the new agreement (e.g. `<Client> - <Engagement type> Agreement.docx`).
- Edit via python-docx, same pattern used for e-Solar's T&M agreement (2026-06-25): keep the cover-page layout, keep the **Terms & Conditions section verbatim, unchanged** (never rewrite legal boilerplate without being asked), keep the "Go-Ahead" sign-off page. Replace only the body sections — why this approach, scope, investment/rate, assumptions — with content grounded in this specific deal's actual scope and rate. Don't invent a rate or scope detail that wasn't confirmed; ask James if anything's missing rather than guessing.
- Update the Go-Ahead checkbox(es) and cover-page Focus/Engagement-type fields to match.

### Step 3 — Present for approval
Show the full doc content (or the changed sections) before saving as final. Get an explicit yes. Apply any requested changes before calling it done — don't ship first and fix after.

### Step 4 — Create the Outlook draft
Once approved, draft the covering email in [[voice]] (short, casual, specific to the deal) and create a real Outlook draft with the agreement doc attached, via `python scripts/outlook_draft.py <to> <subject> <body_text_file> <attachment_path>` (added 2026-06-25 — see [[outlook-api]]). **James still sends it himself** — this only creates the draft, it never sends.

## Trigger B — "onboard `<client>`" (agreement signed)

Run once James confirms the agreement is signed back.

### Step 1 — ClickUp project setup
- Create a ClickUp project/list for the client (mirror the structure of an existing client's setup — check `clickup_get_workspace_hierarchy` for the pattern).
- Add the client contact as a guest, if ClickUp's permission model supports it cleanly without exposing other clients' work.

### Step 2 — Draft the kickoff email
- Grounded in [[voice]], the signed scope, and the ClickUp guest-invite link. Plain, short, sets expectation for how updates will flow (ClickUp, not email threads).

### Step 3 — Present for approval, then create the Outlook draft
Same rule as Trigger A — show the drafted email, get an explicit yes, then create the real Outlook draft via `scripts/outlook_draft.py` (no attachment needed unless there's something to send beyond the ClickUp invite link). James reviews and pushes send himself.

### Step 4 — Sync
- Update GHL with an onboarding note if useful (optional — don't add noise for its own sake).
- Update the relevant Storia SB customer page per the standing-sync rule in [[CLAUDE]] — note the signed date, ClickUp project link, and kickoff status.

## Notes

- **Drafts only — no send, ever, without explicit approval.** Outlook drafts created by this skill sit in James's Drafts folder until he sends them himself. The only unconditional actions are the deal-context lookups (read-only) and ClickUp project creation (internal, not customer-facing).
- **Don't run this on autopilot.** Phase 1 of the Bike Method — run manually until James has validated a few rounds and decides whether to advance autonomy himself.
- **KPI this serves** (bucket: less cost + more value per customer):
  - Less cost: time from "draft agreement for X" to a ready-for-review doc — target minutes, not a full session (e-Solar's was built from scratch, took most of a working session).
  - More value per customer: % of signed deals with a ClickUp project + kickoff email drafted within 24 hours of "onboard X" being run — currently 0% systematic (e-Solar was the first, built ad hoc).
  - See [[log]] (2026-06-25, client onboarding entry) for the full spec.
- Revisit the trigger design (currently two explicit on-demand commands) if James later wants GHL-stage-watching — that was explicitly deferred, not ruled out forever.

---
> *Adapted from The Three Ms of AI™ © 2026 Nate Herk. All rights reserved.*
