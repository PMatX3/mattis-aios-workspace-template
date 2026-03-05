"""
DataOS — GoHighLevel Collector (v2 API)

Tracks pipeline opportunities, new contacts, and appointments from GHL.
Uses the v2 API (services.leadconnectorhq.com) with Private Integration Tokens.

Note: Revenue/invoice data is sourced from Xero, not GHL.

Requires:
    GHL_API_KEY      — Private Integration Token (pit-xxx) from GHL Settings > Private Integrations
    GHL_LOCATION_ID  — Sub-account location ID (visible in GHL URL: /location/{id}/...)

Tables written:
    ghl_pipeline_daily  — Opportunity counts and value by pipeline/stage
    ghl_activity_daily  — Daily contact and appointment counts
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

try:
    import requests
except ImportError:
    raise ImportError("Missing 'requests' — run: pip install requests")

BASE_URL = "https://services.leadconnectorhq.com"


def _get_headers():
    api_key = os.getenv("GHL_API_KEY", "").strip()
    if not api_key:
        return None
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Version": "2021-07-28",
    }


def _safe_get(headers, endpoint, params=None):
    """Safe GET — returns None on HTTP error or application-level auth failure."""
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=headers,
                         params=params or {}, timeout=15)
        r.raise_for_status()
        data = r.json()
        # GHL v2 returns HTTP 200 with statusCode in body for auth errors
        if isinstance(data, dict) and data.get("statusCode") in (401, 403):
            return None
        return data
    except Exception:
        return None


def _get_all_opportunities(headers, location_id):
    """Fetch all open opportunities via pagination, return as list."""
    opportunities = []
    params = {"location_id": location_id, "status": "open", "limit": 100}

    while True:
        data = _safe_get(headers, "opportunities/search", params)
        if not data:
            break
        batch = data.get("opportunities", [])
        opportunities.extend(batch)
        next_url = data.get("meta", {}).get("nextPageUrl")
        if not next_url or not batch:
            break
        # Extract pagination cursors from nextPageUrl for next request
        meta = data.get("meta", {})
        params["startAfter"] = meta.get("startAfter")
        params["startAfterId"] = meta.get("startAfterId")

    return opportunities


def _get_pipeline_summary(headers, location_id):
    """Get opportunity counts and value by pipeline and stage."""
    pipelines_data = _safe_get(headers, "opportunities/pipelines",
                                {"locationId": location_id})
    if not pipelines_data:
        return []

    # Build lookup: (pipeline_id, stage_id) -> (pipeline_name, stage_name)
    stage_lookup = {}
    for pipeline in pipelines_data.get("pipelines", []):
        for stage in pipeline.get("stages", []):
            stage_lookup[(pipeline["id"], stage["id"])] = {
                "pipeline_name": pipeline["name"],
                "stage_name": stage["name"],
            }

    # Fetch all opportunities and group by pipeline/stage
    all_opps = _get_all_opportunities(headers, location_id)
    counts = {}
    for opp in all_opps:
        key = (opp.get("pipelineId"), opp.get("pipelineStageId"))
        if key not in counts:
            counts[key] = {"count": 0, "total_value_gbp": 0.0}
        counts[key]["count"] += 1
        counts[key]["total_value_gbp"] += float(opp.get("monetaryValue") or 0)

    summary = []
    for (pipeline_id, stage_id), vals in counts.items():
        meta = stage_lookup.get((pipeline_id, stage_id), {})
        if not meta:
            continue
        summary.append({
            "pipeline_name": meta["pipeline_name"],
            "stage_name": meta["stage_name"],
            "count": vals["count"],
            "total_value_gbp": vals["total_value_gbp"],
        })

    return summary


def _get_new_contacts_today(headers, location_id):
    """Get count of contacts created today."""
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    data = _safe_get(headers, "contacts/", {
        "locationId": location_id,
        "limit": 100,
        "sortBy": "dateAdded",
        "sortOrder": "desc",
    })
    if not data:
        return 0
    contacts = data.get("contacts", [])
    return sum(1 for c in contacts
               if (c.get("dateAdded") or "")[:10] == today_str)


def _get_appointments_today(headers, location_id):
    """Get count of appointments across all calendars for today."""
    today = datetime.now(timezone.utc)
    start = today.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = today.replace(hour=23, minute=59, second=59, microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")

    calendars_data = _safe_get(headers, "calendars/", {"locationId": location_id})
    if not calendars_data:
        return 0

    total = 0
    for cal in calendars_data.get("calendars", []):
        cal_id = cal.get("id")
        if not cal_id:
            continue
        data = _safe_get(headers, "calendars/events", {
            "locationId": location_id,
            "calendarId": cal_id,
            "startTime": start,
            "endTime": end,
        })
        if data:
            total += len(data.get("events", []))

    return total


def collect():
    """Fetch GHL pipeline, contacts, and appointment data."""
    headers = _get_headers()
    if not headers:
        return {
            "source": "ghl", "status": "skipped",
            "reason": "Missing GHL_API_KEY — get it from GHL > Settings > Private Integrations"
        }

    location_id = os.getenv("GHL_LOCATION_ID", "").strip()
    if not location_id:
        return {
            "source": "ghl", "status": "skipped",
            "reason": "Missing GHL_LOCATION_ID — visible in GHL URL: /location/{id}/..."
        }

    try:
        pipeline_summary = _get_pipeline_summary(headers, location_id)
        new_contacts = _get_new_contacts_today(headers, location_id)
        appointments = _get_appointments_today(headers, location_id)

        return {
            "source": "ghl",
            "status": "success",
            "data": {
                "pipeline": pipeline_summary,
                "new_contacts_today": new_contacts,
                "appointments_today": appointments,
            }
        }

    except Exception as e:
        return {"source": "ghl", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """Write GHL data to database. Returns records written."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ghl_pipeline_daily (
            date TEXT NOT NULL,
            pipeline_name TEXT NOT NULL,
            stage_name TEXT NOT NULL,
            count INTEGER DEFAULT 0,
            total_value_gbp REAL DEFAULT 0,
            collected_at TEXT,
            PRIMARY KEY (date, pipeline_name, stage_name)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS ghl_activity_daily (
            date TEXT NOT NULL PRIMARY KEY,
            new_contacts INTEGER DEFAULT 0,
            appointments INTEGER DEFAULT 0,
            invoices_sent_count INTEGER DEFAULT 0,
            invoices_paid_count INTEGER DEFAULT 0,
            revenue_sent_mtd REAL DEFAULT 0,
            revenue_paid_mtd REAL DEFAULT 0,
            collected_at TEXT
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    data = result["data"]
    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    for stage in data["pipeline"]:
        conn.execute(
            "INSERT OR REPLACE INTO ghl_pipeline_daily "
            "(date, pipeline_name, stage_name, count, total_value_gbp, collected_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (date, stage["pipeline_name"], stage["stage_name"],
             stage["count"], stage["total_value_gbp"], collected_at)
        )
        records += 1

    conn.execute(
        "INSERT OR REPLACE INTO ghl_activity_daily "
        "(date, new_contacts, appointments, collected_at) "
        "VALUES (?, ?, ?, ?)",
        (date, data["new_contacts_today"], data["appointments_today"], collected_at)
    )
    records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        data = result["data"]
        print("GHL Pipeline:")
        for stage in data["pipeline"]:
            print(f"  {stage['pipeline_name']} / {stage['stage_name']}: "
                  f"{stage['count']} opps, £{stage['total_value_gbp']:,.0f}")
        print(f"New contacts today: {data['new_contacts_today']}")
        print(f"Appointments today: {data['appointments_today']}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")
