"""One-time OAuth2 sign-in for Xero. Opens your browser for consent, catches the
callback on a local listener, and saves tokens + tenant ID to xero_token_cache.json.
Run again any time the refresh token expires (Xero refresh tokens expire after 60 days unused).
"""
import json
import os
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ["XERO_CLIENT_ID"]
CLIENT_SECRET = os.environ["XERO_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8765/callback"
SCOPES = "openid profile email accounting.invoices.read accounting.payments.read accounting.contacts.read accounting.reports.profitandloss.read accounting.reports.balancesheet.read offline_access"
CACHE_PATH = os.path.join(os.path.dirname(__file__), "xero_token_cache.json")

auth_code = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        if "code" in params:
            auth_code["code"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Signed in. You can close this tab and return to the terminal.")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def main():
    auth_url = "https://login.xero.com/identity/connect/authorize?" + urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": "storia-aios",
    })
    print(f"Opening browser for Xero sign-in. If it doesn't open, visit:\n{auth_url}")
    webbrowser.open(auth_url)

    server = HTTPServer(("localhost", 8765), CallbackHandler)
    server.handle_request()

    if "code" not in auth_code:
        raise RuntimeError("No authorization code received.")

    token_resp = requests.post("https://identity.xero.com/connect/token", data={
        "grant_type": "authorization_code",
        "code": auth_code["code"],
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    token_resp.raise_for_status()
    tokens = token_resp.json()

    conn_resp = requests.get("https://api.xero.com/connections", headers={
        "Authorization": f"Bearer {tokens['access_token']}",
    })
    conn_resp.raise_for_status()
    connections = conn_resp.json()
    if not connections:
        raise RuntimeError("No Xero organisations connected to this app.")
    tokens["tenant_id"] = connections[0]["tenantId"]
    tokens["tenant_name"] = connections[0].get("tenantName")

    with open(CACHE_PATH, "w") as f:
        json.dump(tokens, f)
    print(f"Signed in to Xero org '{tokens['tenant_name']}'. Token cache saved to {CACHE_PATH}.")


if __name__ == "__main__":
    main()
