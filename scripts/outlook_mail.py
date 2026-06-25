"""Query Outlook mail via Microsoft Graph using the cached token from outlook_auth.py.
Usage: python outlook_mail.py [search terms...]
"""
import os
import sys

import msal
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["OUTLOOK_CLIENT_ID"]
TENANT_ID = os.environ["OUTLOOK_TENANT_ID"]
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Mail.Read", "Mail.Send", "Calendars.Read", "User.Read", "Chat.Read", "ChannelMessage.Read.All", "Team.ReadBasic.All", "Sites.Read.All", "Files.Read.All"]
CACHE_PATH = os.path.join(os.path.dirname(__file__), "token_cache.json")
GRAPH = "https://graph.microsoft.com/v1.0"


def get_token():
    cache = msal.SerializableTokenCache()
    if not os.path.exists(CACHE_PATH):
        raise RuntimeError("No token cache found. Run outlook_auth.py first.")
    cache.deserialize(open(CACHE_PATH).read())

    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)
    accounts = app.get_accounts()
    if not accounts:
        raise RuntimeError("No cached account. Run outlook_auth.py again.")

    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if not result:
        raise RuntimeError("Token refresh failed. Run outlook_auth.py again.")

    with open(CACHE_PATH, "w") as f:
        f.write(cache.serialize())
    return result["access_token"]


def search_mail(query, top=10):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$search": f'"{query}"', "$top": top}
    resp = requests.get(f"{GRAPH}/me/messages", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("value", [])


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "GBC"
    messages = search_mail(query)
    for m in messages:
        print(f"[{m['receivedDateTime']}] {m['from']['emailAddress']['address']}: {m['subject']}")
