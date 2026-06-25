"""One-time device-code sign-in for Outlook/Graph access. Run this once to create token_cache.json, then outlook_mail.py reuses/refreshes it silently."""
import json
import os

import msal
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["OUTLOOK_CLIENT_ID"]
TENANT_ID = os.environ["OUTLOOK_TENANT_ID"]
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "User.Read", "Chat.Read", "ChannelMessage.Read.All", "Team.ReadBasic.All", "Sites.Read.All", "Files.Read.All"]
CACHE_PATH = os.path.join(os.path.dirname(__file__), "token_cache.json")


def main():
    cache = msal.SerializableTokenCache()
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise RuntimeError(f"Failed to create device flow: {flow}")
    print(flow["message"])

    result = app.acquire_token_by_device_flow(flow)
    if "access_token" not in result:
        raise RuntimeError(f"Auth failed: {result.get('error_description', result)}")

    with open(CACHE_PATH, "w") as f:
        f.write(cache.serialize())
    print(f"Signed in as {result.get('id_token_claims', {}).get('preferred_username')}. Token cache saved to {CACHE_PATH}.")


if __name__ == "__main__":
    main()
