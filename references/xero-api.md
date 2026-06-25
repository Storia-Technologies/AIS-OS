# Xero

Revenue/financials connector for Storia Technologies Pty Ltd. Auth: OAuth2 authorization-code flow (Xero has no device-code flow — needs a redirect URI), app "Storia AIOS" registered at developer.xero.com.

## Credentials

Stored in `.env` (gitignored): `XERO_CLIENT_ID`, `XERO_CLIENT_SECRET`. Redirect URI registered on the app: `http://localhost:8765/callback`.

## Scopes — use the new granular ones, not the deprecated bundles

Xero deprecated `accounting.transactions`, `accounting.transactions.read`, and `accounting.reports.read` in favor of granular scopes (requesting a deprecated scope throws a generic "invalid scope" error on the consent page, not a clear message — see https://developer.xero.com/documentation/guides/oauth2/scopes/ for the current mapping). This connector requests:

```
openid profile email accounting.invoices.read accounting.payments.read accounting.contacts.read accounting.reports.profitandloss.read accounting.reports.balancesheet.read offline_access
```

Add more granular scopes (e.g. `accounting.banktransactions.read`, `accounting.reports.aged.read`) if a future query needs them — requires re-running `xero_auth.py`.

## Scripts

- `scripts/xero_auth.py` — run once (or when the refresh token expires — Xero refresh tokens expire after 60 days of inactivity). Opens your browser for Xero login + org consent, catches the callback on `localhost:8765`, saves tokens + tenant ID to `scripts/xero_token_cache.json` (gitignored).
- `scripts/xero_data.py invoices [status]` — lists invoices, optionally filtered by status (`AUTHORISED`, `PAID`, `DRAFT`, etc.)
- `scripts/xero_data.py contacts [search]` — searches contacts by name substring. Note: client/org names in Xero use legal entity names, not nicknames — GBC is **Gold Buyers Central PTY LTD** in Xero (contact: creynolds@gbcentral.com.au), searching "GBC" returns nothing.

## Notes

- Xero dates come back as `/Date(1234567890000+0000)/` (.NET JSON format) — `xero_data.py` has a `fmt_date()` helper that converts to `YYYY-MM-DD`, reuse it for any new date fields.
- Access tokens expire in 30 min; `xero_data.py`'s `call()` auto-refreshes on a 401.

Full reference: https://developer.xero.com/documentation/api/accounting/overview
