# AIS-OS Intake

This is the source-of-truth file for your AIOS. Fill it in by typing, voice-pasting (Wispr Flow / OS dictation), or running [[.claude/skills/onboard/SKILL|/onboard]] for a guided conversation. Whichever mode, this file is what [[.claude/skills/onboard/SKILL|/onboard]] reads to scaffold your Day-1 setup.

**Hard cap: 7 questions.** Each answerable in under 60 seconds. Don't overthink — you can edit and re-run [[.claude/skills/onboard/SKILL|/onboard]] any time.

---

## Q1 — Who are you, what do you sell, who do you sell it to?

Identity, offer, ICP. One paragraph each is fine.

```
Who we are: Storia Technologies is a Perth-based AI consulting and development studio. We're a small, senior team — four people — which means every engagement gets real attention, not a junior handed the brief.

What we sell: We help businesses identify where AI can save the most time or money, then we build and implement it. That ranges from a focused 10-hour advisory sprint ($2,995) through to ongoing retainers where we act as an embedded AI team. We also build custom software — apps, integrations, automation — when the problem calls for it.

Who we sell it to: Professional services businesses and owner-operators who know AI is relevant to them but don't have the internal capability to act on it. Typically 5–50 people, already running well, and losing hours every week to manual processes they suspect could be automated. They're not looking for hype — they want someone to show them what's actually possible and then build it.
```

---

## Q2 — Paste 1-2 things you've written recently. Don't edit them.

An email, a LinkedIn post, a DM, a doc — anything that sounds like you when you're not trying. **Paste verbatim.** Do not type these mid-conversation with Claude — chat-shaped samples are worse than no samples (voice contamination).

```
Option 1 — TeeFinder reply to Jate/Jaz (23 Jun, professional but warm)

Hi Jate and Jaz,
Thanks for sending this through! Some interesting stuff in there, especially around the group payments flow, it's great you defined the core of the product.
I've got a rough number and a couple of questions on the MiClub side. Got 15 mins for a quick call this week so I can clarify?
```

```
Option 2 — Earlier TeeFinder reply to Jaz (19 Jun, more direct/technical)

Hi Jaz,
Good to hear Teefinder's kept moving. Sounds like the UI and pitch deck work has paid off.
Happy to quote the MVP build, but the slide you sent through is more positioning than scope. There's no actual feature list or wireframes for me to size against. Could you send over the wireframes/designs, the feature list, which platforms you're targeting, and any integrations needed (we've already got context on the tee time APIs from last time)? Once I've got that I can turn around a number quickly.
Given the history on this one, happy to jump on a call instead of going back and forth over email too. Whatever's easiest for you.
```

```
Option 3 — Security alert to Sonja (23 Jun, client-facing, structured)

Hi Sonja,
I wanted to let you know that Microsoft Defender has raised a high-priority security alert relating to Karen's laptop.
The alert occurred at approximately 1:54 PM on Monday and appears to be linked to a suspicious phishing page being accessed through Microsoft Edge. I have started a remote antivirus scan and automated investigation through Microsoft Defender, but the laptop currently appears to be offline, so these actions may not complete until the device is powered on and connected to the internet.
Could you please help with the following tomorrow: [numbered list of actions]...
```

---

## Q3 — What are your 2-3 biggest priorities for the next 90 days?

Quarterly priorities. Not yearly aspirations. Things that, if not done by July, would make you say "I wasted Q2."

```
1. Lock in the GBC retainer upgrade — signed agreement at Option A ($7,280/month) or better by July 31. Already in motion with John and David; fastest revenue move available (+$27K+ ARR with no new client acquisition). If not signed by end of July, chase harder — don't let it drift into Q4.

2. Close one new meaningful project (TeeFinder or equivalent) — signed SOW + deposit by end of July, work underway by August. Q4 target is $400K ARR, can't get there on existing clients alone. TeeFinder is live and sized at $50-70K; if it falls through, priority stays the same — close something of real scale before September.

3. Run the first AI Launch Lab workshop with paying attendees — one workshop completed before September 30, minimum 6 paying participants at $550 each. Has been "in planning" too long without a date or registration link. Goal isn't profit, it's proof of concept — testimonials and a base to sell the next one from.
```

---

## Q4 — Where does revenue actually land, and where is it tracked?

Multiple answers OK. Stripe? Skool? GoHighLevel? QuickBooks? A spreadsheet?

```
Xero — primary accounting system, where invoices are issued and payments are recorded (source of truth).
Stripe — for online payments (hosting subscriptions at $249/month, potentially workshop registrations).
Direct bank transfer — most client project invoices are paid via EFT, reconciled in Xero.
```

---

## Q5 — Where do you talk to customers, your team, and the outside world day-to-day?

Email (which one — Gmail / Outlook)? Slack? Teams? DMs (Skool / Discord / iMessage)? Phone?

```
Email — Outlook (james@storia.tech) — primary client communication.
Microsoft Teams — internal team (Kevin, Meliton, Jordan).
WhatsApp — some clients.
Phone/iMessage — ad hoc.
```

---

## Q6 — Where do meeting recordings, notes, and important docs live?

Granola? Otter? Fireflies? Google Drive? Notion? Dropbox? A folder on your desktop you keep meaning to organize?

```
Fireflies — meeting recordings and transcripts.
SharePoint — important docs (proposals, contracts, etc.).
```

---

## Q7 — What's the one task that eats your week, and where do you currently track work?

The single biggest time-suck or recurring drudgery. Plus where tasks/projects live (ClickUp / Asana / Linear / Notion / a notebook).

```
Task/project tracking — ClickUp.
Biggest time-suck — lead generation anxiety (the mental overhead of not knowing where the next client is coming from).
```

---

When this file is filled, run [[.claude/skills/onboard/SKILL|/onboard]] (or re-run it) and the wizard will scaffold your Day-1 file set: `context/`, [[voice]], populated [[connections]], and a filled [[CLAUDE]].
