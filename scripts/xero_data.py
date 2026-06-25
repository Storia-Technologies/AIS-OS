"""Query Xero Accounting API using the cached token from xero_auth.py. Refreshes silently.
Usage:
  python xero_data.py invoices [status]   # e.g. status=AUTHORISED, PAID, DRAFT
  python xero_data.py contacts [search]
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["XERO_CLIENT_ID"]
CLIENT_SECRET = os.environ["XERO_CLIENT_SECRET"]
CACHE_PATH = os.path.join(os.path.dirname(__file__), "xero_token_cache.json")
API = "https://api.xero.com/api.xro/2.0"


def get_tokens():
    if not os.path.exists(CACHE_PATH):
        raise RuntimeError("No token cache found. Run xero_auth.py first.")
    with open(CACHE_PATH) as f:
        return json.load(f)


def refresh_if_needed(tokens):
    resp = requests.post("https://identity.xero.com/connect/token", data={
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    resp.raise_for_status()
    new_tokens = resp.json()
    tokens["access_token"] = new_tokens["access_token"]
    tokens["refresh_token"] = new_tokens["refresh_token"]
    with open(CACHE_PATH, "w") as f:
        json.dump(tokens, f)
    return tokens


def headers(tokens):
    return {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Xero-tenant-id": tokens["tenant_id"],
        "Accept": "application/json",
    }


def call(tokens, path, params=None):
    resp = requests.get(f"{API}/{path}", headers=headers(tokens), params=params)
    if resp.status_code == 401:
        tokens = refresh_if_needed(tokens)
        resp = requests.get(f"{API}/{path}", headers=headers(tokens), params=params)
    resp.raise_for_status()
    return resp.json()


def list_invoices(status=None):
    tokens = get_tokens()
    params = {"where": f'Status=="{status}"'} if status else None
    return call(tokens, "Invoices", params=params).get("Invoices", [])


def list_contacts(search=None):
    tokens = get_tokens()
    params = {"where": f'Name.Contains("{search}")'} if search else None
    return call(tokens, "Contacts", params=params).get("Contacts", [])


def fmt_date(xero_date):
    if not xero_date:
        return ""
    match = re.search(r"\d+", xero_date)
    return datetime.fromtimestamp(int(match.group()) / 1000, tz=timezone.utc).strftime("%Y-%m-%d") if match else xero_date


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "invoices"
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == "invoices":
        for inv in list_invoices(arg):
            print(f"{inv['InvoiceNumber']} — {inv['Contact']['Name']} — {inv['Status']} — ${inv['Total']} — due {fmt_date(inv.get('DueDate'))}")
    elif cmd == "contacts":
        for c in list_contacts(arg):
            print(f"{c['Name']} — {c.get('EmailAddress', '')}")
    else:
        print("Usage: xero_data.py [invoices [status]|contacts [search]]")
