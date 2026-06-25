"""Search/list SharePoint sites and files via Microsoft Graph using the cached token from outlook_auth.py.
Usage:
  python sharepoint_files.py sites
  python sharepoint_files.py search <query>
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


def list_sites():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{GRAPH}/sites?search=*", headers=headers)
    resp.raise_for_status()
    return resp.json().get("value", [])


def search_files(query, top=10):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"$top": top}
    resp = requests.post(f"{GRAPH}/search/query", headers=headers, json={
        "requests": [{
            "entityTypes": ["driveItem"],
            "query": {"queryString": query},
            "from": 0,
            "size": top,
        }]
    })
    resp.raise_for_status()
    hits = []
    for container in resp.json().get("value", []):
        for hc in container.get("hitsContainers", []):
            hits.extend(hc.get("hits", []))
    return hits


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sites"
    if cmd == "sites":
        for s in list_sites():
            print(f"{s['displayName']} — {s['webUrl']}")
    elif cmd == "search":
        query = " ".join(sys.argv[2:])
        for h in search_files(query):
            res = h.get("resource", {})
            print(f"{res.get('name')} — {res.get('webUrl')}")
    else:
        print("Usage: sharepoint_files.py [sites|search <query>]")
