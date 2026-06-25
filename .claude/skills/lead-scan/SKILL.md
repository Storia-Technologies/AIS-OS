---
name: lead-scan
description: Use weekly (or on-demand "scan my email for leads") to find inbound emails from the last 7 days that look like genuine leads and aren't yet in GoHighLevel. Drafts a GHL contact/opportunity per lead and waits for approval before creating anything. Trigger on "scan my email for leads", "any new leads in my inbox", "lead scan".
bike-method-phase: 1  # Phase 1 — Training wheels. Run manually first.
three-ms-attribution: |
  Adapted from The Three Ms of AI™ © 2026 Nate Herk.
---

## What this skill does

Scoped via [[.claude/skills/level-up/SKILL|/level-up]] on 2026-06-24 — full spec in [[log]]. The chatbot that used to feed GHL was generating pure spam (a 236-opportunity backlog, ~230 of it junk — see the earlier pipeline-checkin scoping entry). Nothing replaced it as a real intake source, so genuine leads sitting in James's inbox never make it into the pipeline at all. This skill closes that gap on the intake side, while [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]] handles the follow-up side.

**Autonomy level: L2 (Drafted), upgraded from L1 on 2026-06-25.** Matches `pipeline-checkin` now. For each flagged lead, draft the proposed GHL contact + opportunity (name, estimated value if inferable from the email, suggested pipeline/stage) and present it for approval — in chat, or as one ClickUp task per batch if there are several. **Never create the GHL entry without an explicit yes from James first**, every time, no exceptions — same reasoning as `referral-checkin`'s L2: a wrong auto-created entry costs more than no entry. The L1→L2 move happened only after James had a working `ghl_pipeline.py create` path and asked for it directly — don't read this as license to push further to L3 without the same kind of explicit ask.

## Inputs

- Outlook Inbox + Sent, last **7 days** (via MCP `outlook_email_search`) — narrow window deliberately, scoped to match the weekly cadence so the full window can be read thoroughly instead of keyword-sampled. (Tested against 30 days first: ~550 emails, dominated by ClickUp bot notifications and vendor spam — too much to scan exhaustively, and keyword search alone misses leads that don't happen to use the sampled words. 7 days is small enough to read in full.) Sent is checked only to note whether James already replied, not to suppress a flag (a lead he replied to but never entered in GHL is still a gap this should catch)
- GoHighLevel contacts/opportunities (via `scripts/ghl_pipeline.py`) — to skip anything already represented

## Execution

### Step 1 — Pull existing GHL contacts

Get current GHL opportunities/contacts so known leads can be excluded. If `GHL_PIT`/`GHL_LOCATION_ID` aren't set, point to [[gohighlevel-api]].

### Step 2 — Scan the inbox

Pull Inbox (and Sent, for reply context) for the last 7 days, full list — don't rely on a keyword `query` filter, it misses leads that phrase things differently than expected. Read every result in the window. Look for genuine inbound-lead signals: someone asking about services, pricing, a project, a referral introduction ("X suggested I reach out"). Exclude:
- Senders already matching a GHL contact email
- Internal team threads (Kevin, Meliton, Jordan @ storia.tech) and known recurring noise senders (`notifications@tasks.clickup.com`, `no-reply@coreplus.com.au`, `admin@storia.tech` automated digests)
- Anything already tracked elsewhere — check against known active threads (e.g. TeeFinder, referral partners in [[referral-partners]]) before flagging as "new"
- Obvious vendor/cold-outreach spam — same fingerprint as the GHL chatbot junk (gibberish names, SEO/link-building pitches, throwaway domains). See `looks_like_spam()` in `scripts/ghl_pipeline.py` for the pattern reference, applied here to senders instead of GHL records.
- Newsletters/announcements (e.g. "New Leadership at X!") — these aren't leads even if the sender once looked like a contact

### Step 3 — Draft a GHL entry per candidate

For each flagged email: sender name/email, subject, one-line why-it-looks-like-a-lead, whether James already replied (per Sent search), and a proposed GHL draft — opportunity name, an estimated value if one can reasonably be inferred (else leave blank, don't invent a number), and the best-fit pipeline/stage from `python scripts/ghl_pipeline.py pipelines`. Check the contact's email against existing GHL contacts first (GET `/contacts/?query=`) — skip drafting if already represented.

### Step 4 — Get explicit approval, then create

Present the draft(s) and wait for a yes. Once approved, create via `python scripts/ghl_pipeline.py create <name> <value> <contact_name> <contact_email> <pipeline_id> <stage_id>`. If James wants changes (different stage, different value), apply those before creating — don't create first and fix after.

If nothing looks like a genuine new lead, say so and stop.

## Notes

- **Drafts only — no GHL write without approval.** The only unconditional write is the contact-lookup read (checking for duplicates).
- **Don't run this on autopilot.** Phase 1 of the Bike Method — run manually until James has validated several rounds and decides whether to advance autonomy further himself.
- **KPI this serves:** every flagged email gets actioned (created in GHL or explicitly dismissed) within a week — no flagged lead sits unactioned. See [[log]] (2026-06-24, inbox lead-scan entry) for the full spec.
- When the scorecard tool on the Storia website ships, it becomes a second intake source — revisit this skill (or scope a new one) once that's live and its output shape is known.

---
> *Adapted from The Three Ms of AI™ © 2026 Nate Herk. All rights reserved.*
