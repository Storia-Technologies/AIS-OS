# GoHighLevel (GHL)

Lead pipeline connector for Storia Technologies. Auth: Private Integration Token (PIT) — no OAuth flow needed since this is single sub-account, not a marketplace app.

## Credentials

Stored in `.env` (gitignored): `GHL_PIT` (the token), `GHL_LOCATION_ID` (the sub-account/location ID — found in GHL under Settings > Business Profile).

## Generating the token (one-time, done in the GHL UI, not via API)

1. In GHL, go to **Settings > Private Integrations** (enable in Labs first if the menu item isn't visible).
2. Click **Create new Integration**, name it something like `storia-aios-pipeline`.
3. Select scopes — minimum needed:
   - `contacts.readonly`
   - `contacts.write` (only if the skill should update contact notes/tags — otherwise skip)
   - `opportunities.readonly`
   - `opportunities.write` (only if the skill should ever move stages programmatically — currently it doesn't; James moves stages manually. Safe to grant for future use, since GHL Private Integrations restrict scope per-token)
4. Copy the token immediately — GHL won't show it again. Paste into `.env` as `GHL_PIT`.
5. Find the location ID under Settings > Business Profile (or in the GHL URL when viewing the sub-account) and save as `GHL_LOCATION_ID`.

Rotate the token periodically (GHL recommends ~90 days) — re-run step 2-4 and update `.env`.

## API basics

- Base URL: `https://services.leadconnectorhq.com`
- Headers on every request:
  ```
  Authorization: Bearer <GHL_PIT>
  Version: 2021-07-28
  Content-Type: application/json
  ```
- Most endpoints require `locationId` as a query param or in the request body.

## Endpoints used by `scripts/ghl_pipeline.py`

- `GET /opportunities/pipelines?locationId={id}` — list pipelines and their stages.
- `POST /opportunities/search` — body includes `location_id`, optional `pipeline_id`, `pipeline_stage_id`, `status` (`open`/`won`/`lost`/`abandoned`). Returns opportunities with `lastStatusChangeAt` / `updatedAt`-style timestamps and contact info — **verify exact field names on first real call**, GHL's public docs (Stoplight-rendered, JS-only) don't fully expose the response schema; the script logs the raw JSON on first run so field names can be confirmed and the parser adjusted.

## Notes

- GHL API v1 was deprecated end of 2025 — only use v2 (`services.leadconnectorhq.com`), not the old `rest.gohighlevel.com`.
- This connector is read-mostly by design — see [[log]] (2026-06-24 pipeline scoping entry). It never moves a stage or sends a message; it only reads opportunities and computes staleness. Drafting/sending lives in the [[.claude/skills/pipeline-checkin/SKILL|/pipeline-checkin]] skill, not this script.

Full reference: https://marketplace.gohighlevel.com/docs/
