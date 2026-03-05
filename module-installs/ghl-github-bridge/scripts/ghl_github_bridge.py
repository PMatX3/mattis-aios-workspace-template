#!/usr/bin/env python3
"""
GHL → GitHub Bridge
====================
Polls GoHighLevel for opportunities in the "White-Label Agency Clients" pipeline
at the "Payment 1 Received" stage and creates a GitHub issue for each new one.

Deduplication: embeds the GHL opportunity ID as a hidden HTML comment in the
issue body and searches GitHub for it before creating — safe across multiple runs.

Usage:
    python ghl_github_bridge.py              # Normal run
    python ghl_github_bridge.py --dry-run    # Preview without creating anything
    python ghl_github_bridge.py --setup      # Only create required GitHub labels
"""

import os
import sys
import time
import logging
from urllib.parse import quote

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

load_dotenv()

GHL_API_KEY       = os.getenv("GHL_API_KEY")
GHL_LOCATION_ID   = os.getenv("GHL_LOCATION_ID")
GITHUB_TOKEN      = os.getenv("GITHUB_TOKEN")
GITHUB_REPO       = os.getenv("GITHUB_REPO")       # full "owner/repo" e.g. "acme/delivery-projects"
GITHUB_OWNER      = os.getenv("GITHUB_OWNER")      # used only as a fallback; GITHUB_REPO already contains owner

# Which GHL pipeline and stage triggers issue creation.
# Set these in your .env file to match your pipeline names exactly.
PIPELINE_NAME     = os.getenv("GHL_TRIGGER_PIPELINE", "Sales Pipeline")
STAGE_NAME        = os.getenv("GHL_TRIGGER_STAGE",    "Payment Received")

GHL_BASE          = "https://services.leadconnectorhq.com"
GITHUB_BASE       = "https://api.github.com"

REQUIRED_LABELS = [
    {"name": "ghl-linked",           "color": "0075ca", "description": "Linked to a GHL opportunity"},
    {"name": "payment-received",     "color": "0e8a16", "description": "Payment 1 has been received"},
    {"name": "ready-for-onboarding", "color": "e4e669", "description": "Ready for client onboarding"},
]

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("ghl_bridge")

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_env():
    missing = [k for k in ("GHL_API_KEY", "GHL_LOCATION_ID", "GITHUB_TOKEN", "GITHUB_REPO")
               if not os.getenv(k)]
    if missing:
        log.error("Missing required environment variables: %s", ", ".join(missing))
        sys.exit(1)

# ---------------------------------------------------------------------------
# GHL helpers
# ---------------------------------------------------------------------------

def ghl_headers():
    return {
        "Authorization": f"Bearer {GHL_API_KEY}",
        "Version": "2021-07-28",
        "Content-Type": "application/json",
    }


def ghl_get(path, params=None):
    url = f"{GHL_BASE}{path}"
    resp = requests.get(url, headers=ghl_headers(), params=params, timeout=15)
    if not resp.ok:
        log.error("GHL request failed: %s %s → %s %s", "GET", url, resp.status_code, resp.text[:300])
        resp.raise_for_status()
    return resp.json()


def get_pipeline_and_stage_ids():
    """Return (pipeline_id, stage_id) by matching on name."""
    data = ghl_get("/opportunities/pipelines", {"locationId": GHL_LOCATION_ID})
    for pipeline in data.get("pipelines", []):
        if pipeline.get("name") == PIPELINE_NAME:
            for stage in pipeline.get("stages", []):
                if stage.get("name") == STAGE_NAME:
                    log.info("Found pipeline '%s' (id: %s)", PIPELINE_NAME, pipeline["id"])
                    log.info("Found stage   '%s' (id: %s)", STAGE_NAME, stage["id"])
                    return pipeline["id"], stage["id"]
            log.error("Pipeline '%s' found but stage '%s' not found. Stages available: %s",
                      PIPELINE_NAME, STAGE_NAME,
                      [s["name"] for s in pipeline.get("stages", [])])
            sys.exit(1)

    log.error("Pipeline '%s' not found. Pipelines available: %s",
              PIPELINE_NAME, [p["name"] for p in data.get("pipelines", [])])
    sys.exit(1)


def get_opportunities(pipeline_id, stage_id):
    """Fetch all opportunities at the target stage using cursor-based pagination."""
    all_opps = []
    params = {
        "location_id": GHL_LOCATION_ID,
        "pipeline_id": pipeline_id,
        "pipeline_stage_id": stage_id,
        "limit": 100,
    }

    while True:
        data = ghl_get("/opportunities/search", params)
        batch = data.get("opportunities", [])
        all_opps.extend(batch)

        meta = data.get("meta", {})
        total = meta.get("total", 0)

        log.debug("Fetched %d / %d opportunities so far", len(all_opps), total)

        if len(all_opps) >= total or len(batch) < 100:
            break

        # Cursor-based pagination
        params["startAfter"]   = meta.get("startAfter")
        params["startAfterId"] = meta.get("startAfterId")

    log.info("Fetched %d opportunit%s at '%s'",
             len(all_opps), "y" if len(all_opps) == 1 else "ies", STAGE_NAME)
    return all_opps

# ---------------------------------------------------------------------------
# GitHub helpers
# ---------------------------------------------------------------------------

def github_headers():
    return {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def github_get(path, params=None):
    url = f"{GITHUB_BASE}{path}"
    resp = requests.get(url, headers=github_headers(), params=params, timeout=15)
    if not resp.ok:
        log.error("GitHub GET failed: %s → %s %s", url, resp.status_code, resp.text[:300])
        resp.raise_for_status()
    return resp.json()


def github_post(path, payload):
    url = f"{GITHUB_BASE}{path}"
    resp = requests.post(url, headers=github_headers(), json=payload, timeout=15)
    if not resp.ok:
        log.error("GitHub POST failed: %s → %s %s", url, resp.status_code, resp.text[:300])
        resp.raise_for_status()
    return resp.json()


def ensure_labels():
    """Create any missing labels in the repo."""
    for label in REQUIRED_LABELS:
        name = label["name"]
        check = requests.get(
            f"{GITHUB_BASE}/repos/{GITHUB_REPO}/labels/{quote(name)}",
            headers=github_headers(),
            timeout=15,
        )
        if check.status_code == 404:
            github_post(f"/repos/{GITHUB_REPO}/labels", label)
            log.info("Created label: %s", name)
        elif check.ok:
            log.debug("Label already exists: %s", name)
        else:
            log.warning("Could not verify label '%s': %s", name, check.status_code)


def issue_exists_for_opportunity(opp_id, already_processed):
    """
    Two-layer deduplication:
    1. In-memory set for the current run (avoids hammering GitHub search API)
    2. GitHub search for cross-run deduplication
    """
    if opp_id in already_processed:
        return True

    # GitHub search API has a 30 req/min rate limit — add a small sleep to be safe
    time.sleep(1)

    query = f'repo:{GITHUB_REPO} is:issue in:body "ghl_opportunity_id: {opp_id}"'
    data = github_get("/search/issues", {"q": query})
    return data.get("total_count", 0) > 0


def build_issue_body(opp):
    opp_id       = opp.get("id", "")
    contact      = opp.get("contact", {})
    contact_name = contact.get("name", "Unknown")
    email        = contact.get("email", "")
    company      = contact.get("companyName", "")
    value        = opp.get("monetaryValue") or 0
    deal_value   = f"£{value:,.0f}"

    # Best-effort: pull first non-empty custom field string value
    scope_text = ""
    for cf in opp.get("customFields", []):
        val = cf.get("fieldValueString", "")
        if val:
            scope_text = val
            break

    # Direct link to the GHL opportunity in the pipeline view
    ghl_link = (
        f"https://app.gohighlevel.com/v2/location/{GHL_LOCATION_ID}"
        f"/pipeline?opportunityId={opp_id}"
    )

    scope_section = f"\n**Project Scope:**\n{scope_text}\n" if scope_text else ""

    return f"""## New Client: {opp.get('name', '')}

| Field | Value |
|-------|-------|
| Contact | {contact_name} |
| Email | {email or '—'} |
| Company | {company or '—'} |
| Deal Value | {deal_value} |
| Stage | Payment 1 Received |
| GHL Opportunity | [View in GoHighLevel]({ghl_link}) |
{scope_section}
---

### Onboarding Checklist

- [ ] Send welcome / onboarding email
- [ ] Create project folder in Notion
- [ ] Schedule discovery / kickoff call
- [ ] Set up Linear project and initial tasks
- [ ] Confirm scope, assumptions, and acceptance criteria in writing
- [ ] Collect required access / credentials

---

<!-- ghl_opportunity_id: {opp_id} -->
"""


def create_issue(opp, dry_run=False):
    opp_id     = opp.get("id", "")
    name       = opp.get("name", "Unknown")
    value      = opp.get("monetaryValue") or 0
    deal_value = f"£{value:,.0f}"

    title = f"[{name}] - {deal_value} - {opp_id}"
    body  = build_issue_body(opp)

    if dry_run:
        log.info("DRY RUN — would create issue: %s", title)
        return None

    issue = github_post(
        f"/repos/{GITHUB_REPO}/issues",
        {
            "title":  title,
            "body":   body,
            "labels": [l["name"] for l in REQUIRED_LABELS],
        },
    )
    log.info("Created issue #%d: %s  →  %s", issue["number"], title, issue["html_url"])
    return issue

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(dry_run=False):
    validate_env()

    log.info("=" * 60)
    log.info("GHL → GitHub Bridge  %s", "[DRY RUN]" if dry_run else "[LIVE]")
    log.info("Pipeline : %s", PIPELINE_NAME)
    log.info("Stage    : %s", STAGE_NAME)
    log.info("Repo     : %s", GITHUB_REPO)
    log.info("=" * 60)

    pipeline_id, stage_id = get_pipeline_and_stage_ids()
    opportunities = get_opportunities(pipeline_id, stage_id)

    if not opportunities:
        log.info("No opportunities found at this stage — nothing to do.")
        return

    if not dry_run:
        ensure_labels()

    already_processed = set()
    created  = 0
    skipped  = 0
    errors   = 0

    for opp in opportunities:
        opp_id = opp.get("id", "")
        name   = opp.get("name", "Unknown")

        try:
            if issue_exists_for_opportunity(opp_id, already_processed):
                log.info("SKIP  — issue already exists for '%s' (%s)", name, opp_id)
                skipped += 1
            else:
                create_issue(opp, dry_run=dry_run)
                already_processed.add(opp_id)
                created += 1
        except Exception as exc:
            log.error("ERROR processing '%s' (%s): %s", name, opp_id, exc)
            errors += 1

    log.info("-" * 60)
    log.info("Done.  Created: %d  |  Skipped: %d  |  Errors: %d", created, skipped, errors)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--setup" in args:
        validate_env()
        ensure_labels()
        log.info("Label setup complete.")
        sys.exit(0)

    run(dry_run="--dry-run" in args)
