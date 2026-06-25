"""List recent Microsoft Teams chats/channel activity via Microsoft Graph using the cached token from outlook_auth.py.
Usage: python teams_messages.py [team_name_filter]
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
        raise RuntimeError("Token refresh failed. Run outlook_auth.py again (scopes may have changed).")

    with open(CACHE_PATH, "w") as f:
        f.write(cache.serialize())
    return result["access_token"]


def list_recent_chats(top=10):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$top": top}
    resp = requests.get(f"{GRAPH}/me/chats", headers=headers, params=params)
    resp.raise_for_status()
    chats = resp.json().get("value", [])
    return sorted(chats, key=lambda c: c.get("lastUpdatedDateTime") or "", reverse=True)


def list_chat_messages(chat_id, top=10):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$top": top}
    resp = requests.get(f"{GRAPH}/chats/{chat_id}/messages", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json().get("value", [])


if __name__ == "__main__":
    name_filter = sys.argv[1] if len(sys.argv) > 1 else None
    chats = list_recent_chats()
    for c in chats:
        topic = c.get("topic") or c.get("chatType")
        if name_filter and name_filter.lower() not in (topic or "").lower():
            continue
        print(f"--- {topic} (id: {c['id']}, updated: {c.get('lastUpdatedDateTime')}) ---")
        for m in list_chat_messages(c["id"], top=3):
            sender = (m.get("from") or {}).get("user", {}).get("displayName", "?")
            body = (m.get("body") or {}).get("content", "")[:150]
            print(f"  [{m.get('createdDateTime')}] {sender}: {body}")
