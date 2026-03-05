"""
DataOS — Calendly Collector

Fetches scheduled events (discovery calls, audit calls, etc.) from Calendly.
Takes daily snapshots of calls booked — a key acquisition signal.

Requires:
    CALENDLY_API_TOKEN — Personal access token from Calendly settings
                         (Settings > Integrations > API & Webhooks > Personal Access Token)

Tables created:
    calendly_events — One row per scheduled event per collection date
"""

import os
import sqlite3
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

try:
    import requests
except ImportError:
    raise ImportError("Missing 'requests' — run: pip install requests")

BASE_URL = "https://api.calendly.com"


def _get_headers():
    token = os.getenv("CALENDLY_API_TOKEN", "").strip()
    if not token:
        return None
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _get_user_uri(headers):
    """Get the current user's URI — needed to filter events."""
    r = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()["resource"]["uri"]


def collect():
    """Fetch scheduled events from Calendly API."""
    headers = _get_headers()
    if not headers:
        return {
            "source": "calendly", "status": "skipped",
            "reason": "Missing CALENDLY_API_TOKEN — get it from Calendly > Settings > Integrations > API & Webhooks"
        }

    try:
        user_uri = _get_user_uri(headers)

        # Collect events active today and recently (last 7 days)
        now = datetime.now(timezone.utc)
        seven_days_ago = (now - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
        seven_days_ahead = (now + timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

        events = []
        page_token = None

        while True:
            params = {
                "user": user_uri,
                "status": "active",
                "count": 100,
                "min_start_time": seven_days_ago,
                "max_start_time": seven_days_ahead,
            }
            if page_token:
                params["page_token"] = page_token

            r = requests.get(f"{BASE_URL}/scheduled_events", headers=headers,
                             params=params, timeout=15)
            r.raise_for_status()
            data = r.json()

            for event in data.get("collection", []):
                events.append({
                    "uri": event.get("uri", ""),
                    "name": event.get("name", ""),
                    "status": event.get("status", ""),
                    "start_time": event.get("start_time", ""),
                    "end_time": event.get("end_time", ""),
                    "location_type": (event.get("location") or {}).get("type", ""),
                    "created_at": event.get("created_at", ""),
                    "updated_at": event.get("updated_at", ""),
                })

            next_page = data.get("pagination", {}).get("next_page_token")
            if not next_page:
                break
            page_token = next_page

        # Aggregate: calls booked per day (from start_time)
        daily_counts = {}
        for e in events:
            if e["start_time"]:
                day = e["start_time"][:10]
                daily_counts[day] = daily_counts.get(day, 0) + 1

        return {
            "source": "calendly",
            "status": "success",
            "data": {
                "events": events,
                "daily_counts": daily_counts,
                "total_events": len(events),
            }
        }

    except Exception as e:
        return {"source": "calendly", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """Write Calendly data to database. Returns records written."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS calendly_daily (
            date TEXT NOT NULL PRIMARY KEY,
            calls_booked INTEGER DEFAULT 0,
            collected_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS calendly_events (
            uri TEXT NOT NULL,
            event_date TEXT NOT NULL,
            name TEXT,
            status TEXT,
            start_time TEXT,
            end_time TEXT,
            location_type TEXT,
            created_at TEXT,
            collected_on TEXT,
            PRIMARY KEY (uri)
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    data = result["data"]
    collected_at = datetime.now(timezone.utc).isoformat()
    records = 0

    # Write daily call counts
    for day, count in data["daily_counts"].items():
        conn.execute(
            "INSERT OR REPLACE INTO calendly_daily (date, calls_booked, collected_at) "
            "VALUES (?, ?, ?)",
            (day, count, collected_at)
        )
        records += 1

    # Write individual events
    for event in data["events"]:
        event_date = event["start_time"][:10] if event["start_time"] else date
        conn.execute(
            "INSERT OR REPLACE INTO calendly_events "
            "(uri, event_date, name, status, start_time, end_time, location_type, created_at, collected_on) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (event["uri"], event_date, event["name"], event["status"],
             event["start_time"], event["end_time"], event["location_type"],
             event["created_at"], collected_at)
        )

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        data = result["data"]
        print(f"Calendly: {data['total_events']} events in the next/last 7 days")
        for day, count in sorted(data["daily_counts"].items()):
            print(f"  {day}: {count} call(s)")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")
