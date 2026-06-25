"""Create a draft email in Outlook via Microsoft Graph, using the cached token from outlook_auth.py.
Never sends — always creates a draft in the Drafts folder for James to review and send himself.

Usage: python outlook_draft.py <to_email[,to_email2,...]> <subject> <body_text_file> [attachment_path]
"""
import base64
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


def create_draft(to_email, subject, body_text, attachment_path=None):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    to_addresses = [addr.strip() for addr in to_email.split(",") if addr.strip()]
    body = {
        "subject": subject,
        "body": {"contentType": "Text", "content": body_text},
        "toRecipients": [{"emailAddress": {"address": addr}} for addr in to_addresses],
    }

    if attachment_path:
        with open(attachment_path, "rb") as f:
            content_bytes = base64.b64encode(f.read()).decode()
        body["attachments"] = [{
            "@odata.type": "#microsoft.graph.fileAttachment",
            "name": os.path.basename(attachment_path),
            "contentBytes": content_bytes,
        }]

    resp = requests.post(f"{GRAPH}/me/messages", headers=headers, json=body)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    to_email, subject, body_file = sys.argv[1:4]
    attachment_path = sys.argv[4] if len(sys.argv) > 4 else None
    with open(body_file, "r", encoding="utf-8") as f:
        body_text = f.read()
    draft = create_draft(to_email, subject, body_text, attachment_path)
    print(f"Draft created: {draft['webLink']}")
