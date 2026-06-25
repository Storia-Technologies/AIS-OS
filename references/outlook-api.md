# Outlook / Microsoft Graph

Mail connector for james@storia.tech. Auth: delegated device-code flow via MSAL, app registration "Storia AIOS" in Entra ID (tenant f2f167c5-48b1-4403-a096-64fdfe47f64b).

## One-time setup (you, in Azure portal)

1. App registration → **Authentication** → toggle **"Allow public client flows"** to **Yes**, then Save.
   (Without this, device-code sign-in fails with AADSTS7000218 — Azure assumes any app with a secret is confidential and rejects the public device flow.)
2. Confirm delegated permissions granted: `Mail.Read`, `Mail.Send`, `Calendars.Read`, `User.Read`, `offline_access` — admin consent given 2026-06-24. Teams scopes (`Chat.Read`, `ChannelMessage.Read.All`, `Team.ReadBasic.All`) and SharePoint scopes (`Sites.Read.All`, `Files.Read.All`) added and consented same day.

## Credentials

Stored in `.env` (gitignored): `OUTLOOK_CLIENT_ID`, `OUTLOOK_TENANT_ID`, `OUTLOOK_CLIENT_SECRET`. Secret isn't actually used by the device-code flow (public client) — kept for future confidential-client scenarios (e.g. app-only access without a signed-in user).

## Scripts

- `scripts/outlook_auth.py` — run once (or re-run if the token cache goes stale). Opens a device-code prompt (visit a URL, enter a code). Saves refresh token to `scripts/token_cache.json` (gitignored). Always run with `python -u` — buffered stdout hides the device code/URL until the script exits.
- `scripts/outlook_mail.py <query>` — searches `/me/messages` for the query string, prints date/sender/subject. Silently refreshes the cached token.
- `scripts/outlook_draft.py <to> <subject> <body_text_file> [attachment_path]` — creates a real draft in the Drafts folder via `POST /me/messages`, with an optional attachment. **Never sends** — James reviews and sends himself. `Mail.Send` was already a consented scope (granted 2026-06-24, just unused until now). First used 2026-06-25 for the e-Solar agreement email.
- `scripts/outlook_calendar.py [days_ahead]` — lists calendar events in the next N days (default 7), prints time/subject/organizer. Shares the same token cache — no separate auth needed.
- `scripts/teams_messages.py [name_filter]` — lists recent chats (`/me/chats`, no server-side `$orderby` support — sorted client-side) and the last 3 messages in each. **Pulls all chats, including personal 1:1s**, not just team channels — be mindful what gets surfaced from this.
- `scripts/sharepoint_files.py sites` — lists all SharePoint sites (a GBC-specific site already exists). `scripts/sharepoint_files.py search <query>` — Graph `/search/query` across driveItems; relevance is loose for multi-word queries, treat results as a starting point not an exact match.

## Common Graph endpoints

- `GET /me/messages?$search="..."` — search mail
- `GET /me/messages?$filter=...` — filtered list (e.g. by sender, date)
- `GET /me/mailFolders/{id}/messages` — mail in a specific folder
- `GET /me/calendarview?startDateTime=...&endDateTime=...` — calendar events
- `POST /me/sendMail` — send (always draft for James's review first, per [[CLAUDE]] voice rules — never auto-send external comms)

Full reference: https://learn.microsoft.com/en-us/graph/api/overview
