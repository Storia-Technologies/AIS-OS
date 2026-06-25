"""List/search Fireflies meeting transcripts via their GraphQL API.
Usage: python fireflies_transcripts.py [search_title] [limit]
"""
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["FIREFLIES_API_KEY"]
API_URL = "https://api.fireflies.ai/graphql"

LIST_QUERY = """
query Transcripts($title: String, $limit: Int) {
  transcripts(title: $title, limit: $limit) {
    id
    title
    date
    duration
    summary {
      action_items
      overview
    }
  }
}
"""


def list_transcripts(title=None, limit=10):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    variables = {"limit": limit}
    if title:
        variables["title"] = title
    resp = requests.post(API_URL, headers=headers, json={"query": LIST_QUERY, "variables": variables})
    resp.raise_for_status()
    data = resp.json()
    if "errors" in data:
        raise RuntimeError(data["errors"])
    return data["data"]["transcripts"]


if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else None
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    for t in list_transcripts(title, limit):
        print(f"--- {t['title']} ({t['date']}, {t['duration']} min) ---")
        if t["summary"] and t["summary"].get("overview"):
            print(f"  {t['summary']['overview'][:200]}")
        if t["summary"] and t["summary"].get("action_items"):
            print(f"  Action items: {t['summary']['action_items'][:200]}")
