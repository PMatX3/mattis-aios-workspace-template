"""
DataOS — GitHub Collector

Tracks code activity across Mattis Consulting delivery repositories.
Daily snapshots of commits and PR activity — a proxy for delivery throughput.

Requires:
    GITHUB_TOKEN — Personal access token from github.com/settings/tokens
                   Needs: repo (read) scope
    GITHUB_ORG   — Your GitHub organisation name (e.g. Mattis-Consulting-Ltd)

Tables created:
    github_daily — Aggregate commit/PR activity per day across all repos
    github_repos — Per-repo activity snapshots
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

BASE_URL = "https://api.github.com"


def _get_headers():
    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        return None
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def _get_repos(headers, org):
    """Get all repos for the org (max 100)."""
    r = requests.get(
        f"{BASE_URL}/orgs/{org}/repos",
        headers=headers,
        params={"per_page": 100, "type": "all"},
        timeout=15
    )
    if r.status_code == 404:
        # Try user repos if org not found
        r = requests.get(
            f"{BASE_URL}/users/{org}/repos",
            headers=headers,
            params={"per_page": 100, "type": "all"},
            timeout=15
        )
    r.raise_for_status()
    return r.json()


def _get_commits_since(headers, owner, repo, since_iso):
    """Get commit count for a repo since a given datetime."""
    try:
        r = requests.get(
            f"{BASE_URL}/repos/{owner}/{repo}/commits",
            headers=headers,
            params={"since": since_iso, "per_page": 100},
            timeout=15
        )
        if r.status_code in (409, 404):  # empty repo or not found
            return 0
        r.raise_for_status()
        return len(r.json())
    except Exception:
        return 0


def _get_pr_counts(headers, owner, repo, since_iso):
    """Get open/merged PR counts since a given datetime."""
    try:
        # Recently updated open PRs
        r_open = requests.get(
            f"{BASE_URL}/repos/{owner}/{repo}/pulls",
            headers=headers,
            params={"state": "open", "per_page": 100, "sort": "updated", "direction": "desc"},
            timeout=15
        )
        r_open.raise_for_status()
        open_prs = len(r_open.json())

        # Recently merged PRs (closed and merged)
        r_closed = requests.get(
            f"{BASE_URL}/repos/{owner}/{repo}/pulls",
            headers=headers,
            params={"state": "closed", "per_page": 100, "sort": "updated", "direction": "desc"},
            timeout=15
        )
        r_closed.raise_for_status()
        merged = sum(1 for pr in r_closed.json()
                     if pr.get("merged_at") and pr["merged_at"] >= since_iso)
        return open_prs, merged
    except Exception:
        return 0, 0


def collect():
    """Fetch GitHub activity from the Mattis Consulting org."""
    headers = _get_headers()
    if not headers:
        return {
            "source": "github", "status": "skipped",
            "reason": "Missing GITHUB_TOKEN — get it from github.com/settings/tokens (needs repo read scope)"
        }

    org = os.getenv("GITHUB_ORG", "Mattis-Consulting-Ltd").strip()

    try:
        repos = _get_repos(headers, org)

        # Only look at repos updated in the last 30 days
        thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        since_today = datetime.now(timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0
        ).isoformat()

        repo_data = []
        total_commits_today = 0
        total_open_prs = 0
        total_merged_today = 0

        for repo in repos:
            repo_name = repo["name"]
            updated_at = repo.get("updated_at", "")
            if updated_at < thirty_days_ago:
                continue  # Skip inactive repos

            commits_today = _get_commits_since(headers, org, repo_name, since_today)
            open_prs, merged_today = _get_pr_counts(headers, org, repo_name, since_today)

            total_commits_today += commits_today
            total_open_prs += open_prs
            total_merged_today += merged_today

            repo_data.append({
                "repo": repo_name,
                "commits_today": commits_today,
                "open_prs": open_prs,
                "merged_today": merged_today,
                "last_updated": updated_at[:10] if updated_at else "",
                "is_private": repo.get("private", False),
            })

        return {
            "source": "github",
            "status": "success",
            "data": {
                "org": org,
                "date": today,
                "total_commits_today": total_commits_today,
                "total_open_prs": total_open_prs,
                "total_merged_today": total_merged_today,
                "active_repos": len(repo_data),
                "repos": repo_data,
            }
        }

    except Exception as e:
        return {"source": "github", "status": "error", "reason": str(e)}


def write(conn, result, date):
    """Write GitHub activity to database. Returns records written."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS github_daily (
            date TEXT NOT NULL PRIMARY KEY,
            commits INTEGER DEFAULT 0,
            open_prs INTEGER DEFAULT 0,
            merged_prs INTEGER DEFAULT 0,
            active_repos INTEGER DEFAULT 0,
            org TEXT,
            collected_at TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS github_repos (
            date TEXT NOT NULL,
            repo TEXT NOT NULL,
            commits_today INTEGER DEFAULT 0,
            open_prs INTEGER DEFAULT 0,
            merged_today INTEGER DEFAULT 0,
            last_updated TEXT,
            collected_at TEXT,
            PRIMARY KEY (date, repo)
        )
    """)

    if result.get("status") != "success":
        conn.commit()
        return 0

    data = result["data"]
    collected_at = datetime.now(timezone.utc).isoformat()

    # Daily aggregate
    conn.execute(
        "INSERT OR REPLACE INTO github_daily "
        "(date, commits, open_prs, merged_prs, active_repos, org, collected_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (date, data["total_commits_today"], data["total_open_prs"],
         data["total_merged_today"], data["active_repos"], data["org"], collected_at)
    )

    # Per-repo breakdown
    records = 1
    for repo in data["repos"]:
        conn.execute(
            "INSERT OR REPLACE INTO github_repos "
            "(date, repo, commits_today, open_prs, merged_today, last_updated, collected_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (date, repo["repo"], repo["commits_today"], repo["open_prs"],
             repo["merged_today"], repo["last_updated"], collected_at)
        )
        records += 1

    conn.commit()
    return records


if __name__ == "__main__":
    result = collect()
    if result["status"] == "success":
        data = result["data"]
        print(f"GitHub ({data['org']}): {data['active_repos']} active repos")
        print(f"  Commits today: {data['total_commits_today']}")
        print(f"  Open PRs: {data['total_open_prs']}")
        print(f"  Merged today: {data['total_merged_today']}")
    else:
        print(f"{result['status']}: {result.get('reason', '')}")
