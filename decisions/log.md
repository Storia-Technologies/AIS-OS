# Decisions Log

Append-only record of meaningful decisions and why they were made. [[.claude/skills/level-up/SKILL|/level-up]] Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-06-24 — Native MCP as primary for Outlook/Calendar/Teams/SharePoint/Fireflies; keep Xero script alongside native Xero tools

**Decision:** Use the native claude.ai MCP connectors (Microsoft 365, Fireflies) as the default path for Outlook mail, Calendar, Teams, SharePoint, and Fireflies going forward. Keep the custom `scripts/xero_data.py` running alongside the native Xero MCP tools rather than replacing it. ClickUp is unaffected — already native MCP.

**Why:** The native connectors appeared mid-session and are strictly more capable for the Microsoft 365 + Fireflies set: natural-language date filters, delegated/shared mailbox search, KQL for Teams, and — critically — `fireflies_get_transcript` gives full sentence-by-sentence transcript content, which the custom Fireflies script couldn't do (it only had access to AI-generated summaries). Native also needs no OAuth token-refresh maintenance. Neither path can send/write on Outlook or Teams, so there's no functional regression. For Xero, native tools (`get_cash_position`, `get_financial_position`, `get_profit_and_loss`, `get_top_customers_by_revenue`, receivables snapshot) are better for financial-health questions, but don't support raw contact-name lookup or arbitrary invoice-status filtering — which is how "Gold Buyers Central" was found by name earlier today. The script fills that gap.

**Alternatives considered:** Keep all custom scripts as-is and ignore the native connectors (rejected — duplicates maintenance for no benefit, misses the Fireflies full-transcript capability). Replace everything including Xero (rejected — native Xero lacks contact/invoice-level search).

**Owner:** James.

---

## 2026-06-24 — Scope: Referral-partner relationship system (/level-up)

**Decision:** Build a weekly referral-partner check-in system. Tracks warm and to-cultivate partners (Anthea, BNI Coastal Sands, future accountants/bookkeepers serving Perth's 5-50 person professional services firms), drafts a personalized check-in message on a 30-day cadence or when Storia ships something notable, and queues the draft as a ClickUp task for James to review and send manually — never auto-sent.

**Why (constraint/lever):** James's stated growth lever ("what would give you 500 more clients tomorrow") is a referral channel through trusted advisors, not cold outreach — Storia's ICP trusts advisor recommendations more than direct pitches. Currently zero system exists for this; it's fully dependent on James's memory, which is also his stated constraint ("the whole pipeline runs through me"). Email triage and proposal writing were considered and ranked lower leverage — they cut cost/time, this one drives new client acquisition (his actual top pain: lead-gen anxiety).

**EAD:** Eliminate ruled out — the relationships still need tending or they decay (BNI/Anthea go cold, the 10-hour pack stays a one-on-one pitch instead of an advisor recommendation). Automate at roughly 60/30/10: ~60% deterministic (cadence tracking, due-date logic, ClickUp task creation), ~30% AI-drafted (the check-in message itself, grounded in real recent wins + relationship notes + James's voice), ~10% manual (deciding weekly priority, the actual relationship-building/calls/BNI presence). Delegate not applicable — too relationship-specific to hand to someone else.

**Process map:**
- Trigger: 30-day cadence per partner, OR manual fire when Storia ships something notable (new client, workshop, case study)
- Data sources: [[referral-partners]] (new, created during scoping), [[log]] + ClickUp for recent wins, [[voice]] for tone
- Data transformations: partner context + recent wins + voice → drafted check-in message
- Decision points: cadence due? warm vs to-cultivate (different tone/cadence — to-cultivate is first-touch, not a check-in); did a manual event just fire?
- Destination: ClickUp task, draft in the task description, actioned during James's weekly review

**Autonomy level: L2 (Drafted).** AI drafts every message; James reviews and edits before send, every time, no exceptions — explicitly rejected L3 (periodic batch review) because a slightly-off message to a referral partner costs more than no message at all.

**KPI (bucket: more customers):**
- Lagging: 2 new clients signed (not just leads) sourced from referral partners by 2026-09-30, blended ~$10K value each (~$20K attributable Q3 revenue)
- Leading: 3 active referral partners (made ≥1 introduction) by 2026-09-30 — Anthea counts as 1, need 2 more

**Owner:** James.

---

## 2026-06-24 — Scope: Lead pipeline tracker + stale-lead flagging (/level-up)

**Decision:** Build a pipeline check-in system on top of GoHighLevel. GHL becomes the system of record for lead stages (new → qualified → proposal → won/lost). The skill scans GHL opportunities (cross-referencing Outlook for context on referral-sourced leads), flags any opportunity untouched for 3+ days, drafts a follow-up message per stale lead, and queues each as a ClickUp task for review — never auto-sends, never auto-moves a stage.

**Why (constraint/lever):** Directly answers James's growth-lever question — the pipeline currently lives in his head + email with no system, and he's confirmed leads get missed. This is his stated top pain (lead-gen anxiety) made structural instead of memory-dependent. Eliminate was ruled out — leads still need tracking or they go cold for real. Automate at roughly 60/30/10: ~60% deterministic (GHL API fetch, staleness calculation, last-touch comparison), ~30% AI-drafted (the follow-up message itself, grounded in lead context + James's voice), ~10% manual (deciding which stale leads actually matter this week, the real follow-up call/email, any stage moves). Delegate not applicable — too judgment-heavy and relationship-specific for now.

**Process map:**
- Trigger: weekly review, or on-demand ("check my pipeline")
- Data sources: GoHighLevel (`opportunities/search`, `opportunities/pipelines` via Private Integration Token, see [[gohighlevel-api]]), Outlook (thread context for referral-sourced leads), [[voice]]
- Data transformations: pull all open opportunities per pipeline → compute days since last activity → filter to ≥3 days stale
- Decision points: stale (≥3 days) → draft a follow-up; not stale → no action. Stage moves are never automatic — flagged as a suggestion only, James moves the stage himself in GHL
- Destination: drafted follow-ups queued as ClickUp tasks (same pattern as [[.claude/skills/referral-checkin/SKILL|/referral-checkin]]), nothing sent or moved automatically

**Autonomy level: L2 (Drafted).** AI drafts the follow-up, James reviews/edits/sends and moves stages manually. Explicitly rejected auto-stage-movement (would require reading email replies and inferring intent — too risky to get wrong silently) and rejected pure flag-only (adds review overhead without saving the actual drafting time).

**KPI (bucket: more customers):**
- Leading: no open opportunity goes untouched >3 days (staleness count trending to zero week over week)
- Lagging: lead → signed client conversion rate, tracked monthly once GHL data accumulates

**Owner:** James.

---

## 2026-06-24 — Scope: Inbox lead-scan (flag-only) feeding GHL

**Decision:** Build a second pipeline-adjacent skill — scans Outlook Inbox + Sent (last 30 days), flags emails that look like genuine inbound leads not already represented as a GHL opportunity, and reports the list. It does **not** create anything in GHL. James decides which flagged emails become real opportunities and creates them himself.

**Why (constraint/lever):** Follows directly from the GHL cleanup — the chatbot that used to feed GHL was generating pure spam (236 opportunities, ~230 of them junk), and nothing replaced it as a real lead source. James confirmed two real sources exist: a scorecard tool on the website (in progress, not yet built — out of scope until it exists) and his own inbox, where leads currently arrive and get missed because nothing surfaces them into the pipeline. This directly serves the same growth lever as [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]] — leads going cold from lack of a system — but on the *intake* side rather than the *follow-up* side.

**EAD:** Eliminate doesn't apply — inbound leads are real revenue signal. Automate: deliberately low automation share here versus [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]]. ~30% deterministic (inbox scan, de-dupe against existing GHL contacts), ~40% AI-judgment (does this email actually read as a lead, vs. a vendor pitch or internal thread), ~30% manual (James decides which flagged items become real GHL opportunities — explicitly NOT automated, see autonomy below).

**Process map:**
- Trigger: weekly review, or on-demand ("scan my email for leads")
- Data sources: Outlook Inbox + Sent (last 30 days, via MCP), GHL contacts/opportunities (via `scripts/ghl_pipeline.py`) to skip anything already represented
- Data transformations: filter inbox to externally-sourced threads with inquiry/interest language, cross-reference sender against existing GHL contacts, check Sent for whether James already replied (informational only — doesn't suppress the flag, since "replied but never entered in GHL" is exactly the gap this closes)
- Decision points: already in GHL → skip; looks like vendor/cold-outreach spam (same patterns as the GHL chatbot junk) → skip; genuine lead signal → flag
- Destination: a report back to James (chat + optionally one ClickUp task summarizing the batch) — never a GHL write

**Autonomy level: L1 (Suggested).** Deliberately one notch lower than [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]]'s L2. Creating a real opportunity in GHL is the exact mistake that caused the original mess (chatbot auto-creating junk) — James explicitly chose "flag only, you create it" over having the AI even draft the GHL entry. Revisit only after L1 has run clean for a few weeks.

**KPI (bucket: more customers):**
- Leading: every flagged email gets actioned (created in GHL or explicitly dismissed) within a week of the scan — no flagged lead sits unactioned
- Lagging: shares the [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]] lagging KPI — lead → signed client conversion rate, now measured against a pipeline that actually reflects real inbound volume instead of chatbot noise

**Owner:** James.

---

## 2026-06-25 — `/lead-scan` upgraded L1 → L2

**Decision:** `/lead-scan` now drafts a proposed GHL contact + opportunity per flagged lead (name, value estimate if inferable, suggested pipeline/stage) and waits for explicit approval before creating anything — matching `/pipeline-checkin`'s L2. Previously flag-only (L1): James had to build every GHL entry himself.

**Why:** James asked for the upgrade directly, right after using the new `ghl_pipeline.py create` path to add TeeFinder to GHL himself and realizing he wants this habit to stick going forward. The original reason for capping at L1 — the chatbot-spam incident — doesn't apply to a drafted-then-approved flow; the risk was *auto-creating* without review, not drafting.

**Owner:** James.

---

## 2026-06-25 — Storia SB made a standing reference, kept in sync automatically

**Decision:** Storia SB (the separate Obsidian vault at `C:\Users\James Manning\OneDrive\Vaults\Storia SB`) is now treated as a standing reference, checked the same way as [[connections]] — not something only looked up when explicitly asked. Whenever documentation/context in this repo changes in a way that overlaps with client, project, or people knowledge (new lead, deal update, new contact), the corresponding Storia SB page(s) get updated in the same turn.

**Why:** James asked for this directly after a session where several real leads (TeeFinder, e-Solar, White Chalk Road, Aestus) got created in GHL and the wiki updates happened as an afterthought rather than a built-in step. Splitting "operate the business" (this repo) from "know the business" (Storia SB) only works if the second one actually stays current without being asked every time.

**Owner:** James.

---

## 2026-06-25 — Outlook draft/send capability unlocked (scripts/outlook_draft.py)

**Decision:** Added `scripts/outlook_draft.py` — creates a real Outlook draft (with optional attachment) via `POST /me/messages` on the Graph API, using the existing "Storia AIOS" app registration and token cache. Never sends — only drafts, James reviews and sends himself, same as the voice rule for all external comms.

**Why:** The native claude.ai Microsoft 365 MCP connector is read-only — confirmed via ToolSearch when James asked for a drafted email to be created directly in Outlook and it wasn't possible. Turned out to be a non-issue: `Mail.Send` was already a consented delegated scope on the custom app registration (granted 2026-06-24 alongside `Mail.Read`), just never used by a script. No new Azure AD consent or app changes needed — just code. First live use: the e-Solar T&M agreement email, drafted with the signed-agreement `.docx` attached.

**Alternatives considered:** Request broader native-connector write scopes (not controllable from this side — claude.ai's connector permissions aren't something James can edit) or keep doing this by hand (rejected, this was the whole point of asking).

**Owner:** James.

---

## 2026-06-25 — TeeFinder re-engaged after failed MVP attempt elsewhere

**Decision/update:** TeeFinder (Jate/Jaz) came back to Storia for a quote as of 19 Jun, after attempting to get an MCP MVP built elsewhere and failing. Surfaced via a Fireflies catch-up transcript (internal team standup, not a TeeFinder-facing meeting) and cross-confirmed with James on 25 Jun — "T Finder" in that transcript is the same deal as TeeFinder, the $50-70K Q3 priority in [[priorities]].

**Why this matters:** TeeFinder going elsewhere and coming back is a meaningful signal — the competing build attempt failed, which strengthens Storia's negotiating position and removes "they might just go build it cheaper elsewhere" as a live risk to the Q3 target (signed SOW + deposit by end of July). James still owes them a quote as of this writing.

**Owner:** James.

---

## 2026-06-25 — Scope: Client onboarding (agreement drafting + post-signature kickoff) (/level-up)

**Decision:** Build [[.claude/skills/client-onboarding/SKILL|/client-onboarding]] — two on-demand triggers. "Draft agreement for X" (deal Closed/Won, not yet signed): pulls deal context from GHL + scope context, generates a Storia-branded agreement doc by editing a copy of a recent template via python-docx (cover page + scope/investment sections rewritten, Terms & Conditions kept verbatim), presents for approval. "Onboard X" (signed): creates a ClickUp project, drafts a kickoff/welcome email, presents for approval. Neither trigger ever sends or shares anything — James reviews and sends both himself, always.

**Why (constraint/lever):** Directly prompted by e-Solar's win the same day — the agreement doc got built from scratch in one long ad hoc session, with no consistent next step for ClickUp or kickoff. James named both growth-lever buckets: less cost (re-deriving the same structure every time) and more value per customer (consistent, fast onboarding instead of "whatever James remembers to do").

**EAD:** Eliminate ruled out — onboarding has to happen for every won deal, skipping it isn't a real option, and the cost is recurring rework, not waste. Delegate ruled out — James confirmed it's 100% him right now, no one else on the four-person team currently does this, so there's no one to hand it to. Automate at roughly 60/30/10: ~60% deterministic (GHL/ClickUp lookups, copying the template doc, filling cover-page fields, ClickUp project creation), ~30% AI-drafted (the agreement's scope/investment sections, which vary per deal, and the kickoff email), ~10% manual (James's review and the actual send of both).

**Process map:**
- Trigger: on-demand only, two separate commands — "draft agreement for X" and "onboard X" (assumes signed). Explicitly **not** a GHL-watching/auto-detecting trigger — James doesn't want to live in GHL, and a single smart trigger would need to poll for signature status to know which phase applies, which is exactly the background-watching he ruled out.
- Data sources: GHL (`scripts/ghl_pipeline.py`) for deal name/value/contact/stage, the client's email thread or Storia SB customer page for confirmed scope, a recent branded proposal/agreement `.docx` as the structural template, ClickUp (`clickup_get_workspace_hierarchy`) for project structure, [[voice]] for the kickoff email tone
- Data transformations: deal context + confirmed scope → agreement doc body sections (Why This Approach, Scope & Focus Areas, Investment & Options, Assumptions) via python-docx editing of a template copy; deal context + voice → kickoff email draft
- Decision points: which template structure fits (fixed-scope vs. T&M, per the e-Solar precedent on 2026-06-25); agreement approved?; email approved? Never invent a rate or scope detail that wasn't actually confirmed — ask rather than guess.
- Destination: agreement doc saved to the client's SharePoint folder, presented to James for review (he sends/shares it himself); ClickUp project + guest invite created directly (mechanical, not customer-facing); kickoff email drafted, James sends

**Autonomy level: L2 (Drafted).** Matches `pipeline-checkin`/`lead-scan`. Both customer-facing outputs (agreement, email) require explicit approval before James sends them himself — no auto-send, ever. The ClickUp setup underneath isn't customer-facing, so it runs as part of generating the draft without a separate approval gate.

**KPI (buckets: less cost + more value per customer):**
- Less cost: time from "draft agreement for X" to a ready-for-review doc — target minutes, not a full session (e-Solar's was built from scratch and took most of one).
- More value per customer: % of signed deals with a ClickUp project + kickoff email drafted within 24 hours of "onboard X" being run — currently 0% systematic (e-Solar was the first, built ad hoc).

## 2026-06-25 — Scope: Business brief skill (`/level-up`)

James's own words: "I am jumping between potential leads, business opportunities, projects, managing staff, numbers and trying to find leads." No single place answers "how is my business doing" or "where should I focus" — closest thing was digging through GHL, Xero, ClickUp, Storia SB, and the separate Chief of Staff project by hand, which is exactly how today's TeeFinder pricing mismatch ($50-70K here vs. $75-110K there) got found.

**Constraint:** visibility, not capacity. The cost of not having this is real (time spent digging, risk of acting on stale/wrong numbers) — not an Eliminate candidate. Delegate ruled out — synthesizing cross-system numbers into "where to focus" isn't in the team's lane (Kevin/Meliton/Jordan are delivery, not ops).

**Automate split (revised from 60/30/10 after James asked for actual recommendations, not a readout):** ~50% deterministic data pulls (GHL, Xero, ClickUp), ~40% AI-synthesized recommendations (what needs attention and why), ~10% manual (James decides what to act on).

**Process map:**
- Trigger: both — weekly (Friday) and on-demand.
- Data sources: GHL (`scripts/ghl_pipeline.py`), Xero (script or native MCP), ClickUp (MCP), Storia SB wiki, and the Chief of Staff project's `pipeline.md`/`goals.md`/`contacts.md` — read every time, conflicts flagged not silently resolved.
- Decision points: stale GHL deals (3+ days), pricing-validity deadlines, cash/receivables concerns, ClickUp overload, relationship-risk flags, GHL↔Chief-of-Staff conflicts.
- Destination: self-contained HTML file (`business_brief.html`, repo root, gitignored) — James sets it as his browser homepage so it's always current as of the last run.

**Autonomy level:** L2-ish but lowest-risk in the kit — read-only everywhere except the local HTML output, nothing sent or written externally.

**KPI (buckets: less cost + more customers):**
- Less cost: time from "how's my business doing" to having an answer — target a few seconds (open browser), down from ad hoc digging across 4+ systems.
- More customers: stale leads and at-risk relationships caught and actioned before going cold, instead of sitting unnoticed in a markdown file nobody re-reads.

**Machine handoff:** AI-assisted skill (lowest tier that solves it — pure deterministic can't generate judgment-based recommendations). Built as `.claude/skills/business-brief/SKILL.md`.

**Owner:** James.

## 2026-06-25 — GBC retainer added to GHL (first `/business-brief` finding, acted on)

First run of `/business-brief` immediately surfaced that GBC — Storia's #1 named Q3 priority ($7,280-$10,920/month, deadline 31 Jul) — had no GHL opportunity and no Storia SB commercial entry at all; it only existed in the separate Chief of Staff project's files. James asked to fix it on the spot.

Created GHL opportunity "GBC - Retainer Upgrade ($7,280-$10,920/mo)" (id `ACx0LqDt8uJZPvChuxUD`), Marketing Pipeline / Negotiation, value set to $7,280 (the committed lower-bound figure — GHL only holds one number, upside noted in the name). Added a "Commercial — GBC retainer upgrade" section to `wiki/customers/great-southern-bullion.md` in Storia SB with full context.

TeeFinder's GHL-vs-Chief-of-Staff value/stage conflict (also surfaced by the same first run) is still open, not yet resolved.

**Owner:** James.

## 2026-06-25 — TeeFinder pricing reconciled ($65K-$85K range)

GHL had $60K/Contacted; the Chief of Staff project's file had $75K-$110K/Proposal Out — neither was sourced. Re-scoped bottom-up: pulled the original Mar 2025 full-build proposal (`TeeFinder - App Development Proposal.docx`, ~$103K-$121K for a much bigger native+web+AI+social+travel vision) as a pricing reference, then sized down against Jate's actual 22 Jun feature list (web-only/mobile-first, no AI/social/travel — but group split payments is explicitly the core feature and the MiClub SOAP integration carries real risk, so it isn't a cheap MVP).

Landed on **$65K-$85K**. GHL updated: opportunity renamed to include the range, value set to $65K (floor), stage corrected back to **Contacted** (no quote has gone out — James asked for a clarifying call on 23 Jun, still no reply as of 25 Jun). Storia SB's `wiki/customers/teefinder.md` updated with full reasoning. James is holding the range open until he's actually spoken to Jate/Jaz — no single number locked yet.

Kept regardless of the value fix: Hyper Startup Studio is a competing bid (time-sensitive), recommended approach is a paid discovery sprint ($3-5K) as foot-in-the-door rather than quoting cold, don't lead with equity — all from the Chief of Staff file, not contradicted by anything else.

**Owner:** James.
