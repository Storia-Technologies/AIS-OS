"""Query GoHighLevel opportunities and flag stale leads using the Private Integration Token.
Usage:
  python ghl_pipeline.py pipelines              # list pipelines + stage IDs
  python ghl_pipeline.py stale [days]           # open opportunities untouched >= days (default 3)
  python ghl_pipeline.py triage                 # one-time backlog report: likely-spam vs needs-review
  python ghl_pipeline.py create <name> <value> <contact_name> <contact_email> <pipeline_id> <stage_id>
                                                 # create a contact + opportunity (e.g. a manually-flagged lead from /lead-scan)
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

PIT = os.environ["GHL_PIT"]
LOCATION_ID = os.environ["GHL_LOCATION_ID"]
API = "https://services.leadconnectorhq.com"

HEADERS = {
    "Authorization": f"Bearer {PIT}",
    "Version": "2021-07-28",
    "Content-Type": "application/json",
}


def get_pipelines():
    resp = requests.get(f"{API}/opportunities/pipelines", headers=HEADERS, params={"locationId": LOCATION_ID})
    resp.raise_for_status()
    return resp.json().get("pipelines", [])


def search_opportunities(pipeline_id=None):
    # GHL rejects an explicit "status" field (422 — "property status should not exist");
    # opportunities/search returns open opportunities by default. "limit" raised to 300
    # to fetch the whole account in one call instead of paging (confirmed via live testing
    # that startAfter/startAfterId/searchAfter are all rejected or silently ignored — "page"
    # and "limit" are the only pagination params that actually work).
    body = {"locationId": LOCATION_ID, "limit": 300}
    resp = requests.post(f"{API}/opportunities/search", headers=HEADERS, json=body)
    resp.raise_for_status()
    opps = resp.json().get("opportunities", [])
    if pipeline_id:
        opps = [o for o in opps if o.get("pipelineId") == pipeline_id]
    return opps


SPAM_STAGE_NAMES = {"spam"}


def is_spam_stage(opp, stage_name_by_id):
    stage_name = stage_name_by_id.get(opp.get("pipelineStageId"), "").lower()
    return stage_name in SPAM_STAGE_NAMES


SPAM_DOMAINS = {"hot.com", "neonet.com", "neonet.us", "neonet.au", "info.com", "net.com", "xcellerateit.com", "xcellerateit.comt", "cellerateit.com"}


def looks_like_spam(opp):
    """Heuristic only — flags for human review, doesn't move/delete anything by itself."""
    name = (opp.get("name") or "").strip()
    parts = name.split()
    if len(parts) == 2 and parts[0].lower() == parts[1].lower():
        return True  # bot pattern: "Wallyphype Wallyphype"
    if re.search(r"[^\x00-\x7F]", name):
        return True  # non-Latin script in a name field on an English-language site
    contact = opp.get("contact", {}) or {}
    email = (contact.get("email") or "").lower()
    domain = email.split("@")[-1] if "@" in email else ""
    if domain in SPAM_DOMAINS:
        return True  # throwaway-domain bot pattern seen across this account's backlog
    return False


def delete_opportunity(opp_id):
    resp = requests.delete(f"{API}/opportunities/{opp_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def upsert_contact(name, email):
    resp = requests.post(f"{API}/contacts/upsert", headers=HEADERS, json={"locationId": LOCATION_ID, "name": name, "email": email})
    resp.raise_for_status()
    return resp.json()["contact"]["id"]


def create_opportunity(name, value, contact_id, pipeline_id, stage_id):
    body = {
        "locationId": LOCATION_ID,
        "pipelineId": pipeline_id,
        "pipelineStageId": stage_id,
        "name": name,
        "status": "open",
        "monetaryValue": value,
        "contactId": contact_id,
    }
    resp = requests.post(f"{API}/opportunities/", headers=HEADERS, json=body)
    resp.raise_for_status()
    return resp.json()["opportunity"]


def update_opportunity(opp_id, name=None, value=None, stage_id=None, status=None):
    body = {}
    if name is not None:
        body["name"] = name
    if value is not None:
        body["monetaryValue"] = value
    if stage_id is not None:
        body["pipelineStageId"] = stage_id
    if status is not None:
        body["status"] = status
    resp = requests.put(f"{API}/opportunities/{opp_id}", headers=HEADERS, json=body)
    resp.raise_for_status()
    return resp.json()["opportunity"]


def days_since(timestamp_str):
    if not timestamp_str:
        return None
    dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def stage_name_lookup():
    lookup = {}
    for pipeline in get_pipelines():
        for stage in pipeline.get("stages", []):
            lookup[stage["id"]] = stage["name"]
    return lookup


CLOSED_STAGE_NAMES = {"won", "closed", "lost", "abandoned", "spam"}


def stale_opportunities(min_days=3):
    stage_names = stage_name_lookup()
    stale = []
    for opp in search_opportunities():
        stage_name = stage_names.get(opp.get("pipelineStageId"), "").lower()
        if stage_name in CLOSED_STAGE_NAMES or looks_like_spam(opp):
            continue  # closed-stage opps (e.g. "Won") don't need a follow-up draft regardless of status field
        last_touch = opp.get("lastStatusChangeAt") or opp.get("updatedAt")
        age = days_since(last_touch)
        if age is not None and age >= min_days:
            stale.append({**opp, "_days_stale": age, "_stage_name": stage_names.get(opp.get("pipelineStageId"), "")})
    return stale


def triage():
    stage_names = stage_name_lookup()
    spam, review = [], []
    for opp in search_opportunities():
        stage_name = stage_names.get(opp.get("pipelineStageId"), "")
        entry = {**opp, "_stage_name": stage_name}
        if is_spam_stage(opp, stage_names) or looks_like_spam(opp):
            spam.append(entry)
        else:
            review.append(entry)
    return spam, review


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stale"
    if cmd == "pipelines":
        for p in get_pipelines():
            print(f"{p['name']} ({p['id']})")
            for stage in p.get("stages", []):
                print(f"  - {stage['name']} ({stage['id']})")
    elif cmd == "stale":
        min_days = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        results = stale_opportunities(min_days)
        if not results:
            print(f"No opportunities stale >= {min_days} days.")
        for opp in results:
            name = opp.get("name", "(unnamed)")
            contact = opp.get("contact", {}) or {}
            email = contact.get("email", "")
            value = opp.get("monetaryValue", 0)
            print(f"{name} <{email}> | stage: {opp['_stage_name']} | stale {opp['_days_stale']}d | ${value}")
    elif cmd == "delete-spam":
        spam, _ = triage()
        print(f"Deleting {len(spam)} opportunities flagged as spam...")
        for opp in spam:
            contact = opp.get("contact", {}) or {}
            try:
                delete_opportunity(opp["id"])
                print(f"  deleted: {opp.get('name', '(unnamed)')} <{contact.get('email', '')}>")
            except requests.exceptions.HTTPError as e:
                print(f"  FAILED: {opp.get('name', '(unnamed)')} — {e}")
        print("Done. GHL keeps deleted opportunities recoverable for 60 days (Bulk Actions / Audit Logs) if anything needs undoing.")
    elif cmd == "triage":
        spam, review = triage()
        print(f"=== Likely spam ({len(spam)}) — heuristic only, review before deleting in GHL ===")
        for opp in spam:
            contact = opp.get("contact", {}) or {}
            print(f"{opp.get('name', '(unnamed)')} <{contact.get('email', '')}> | stage: {opp['_stage_name']}")
        print(f"\n=== Needs human review ({len(review)}) ===")
        for opp in review:
            contact = opp.get("contact", {}) or {}
            age = days_since(opp.get("lastStatusChangeAt") or opp.get("updatedAt"))
            print(f"{opp.get('name', '(unnamed)')} <{contact.get('email', '')}> | stage: {opp['_stage_name']} | {age}d since last activity | ${opp.get('monetaryValue', 0)}")
    elif cmd == "create":
        name, value, contact_name, contact_email, pipeline_id, stage_id = sys.argv[2:8]
        contact_id = upsert_contact(contact_name, contact_email)
        opp = create_opportunity(name, float(value), contact_id, pipeline_id, stage_id)
        print(f"Created: {opp['name']} (id {opp['id']}) — ${opp['monetaryValue']} — contact {contact_name} <{contact_email}>")
    elif cmd == "update":
        opp_id, name, value, stage_id, status = sys.argv[2:7]
        opp = update_opportunity(
            opp_id,
            name=name or None,
            value=float(value) if value else None,
            stage_id=stage_id or None,
            status=status or None,
        )
        print(f"Updated: {opp['name']} (id {opp['id']}) — ${opp['monetaryValue']} — stage {opp['pipelineStageId']} — status {opp['status']}")
    else:
        print("Usage: ghl_pipeline.py [pipelines|stale [days]|triage|create ...|update <id> <name|''> <value|''> <stage_id|''> <status|''>]")
