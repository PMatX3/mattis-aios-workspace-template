# GitHub-OS — AIOS Module Installer

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

<!-- MODULE METADATA
module: github-os
version: v1
status: RELEASED
released: 2026-03-05
requires: [context-os]
phase: 2
category: Data
complexity: simple
api_keys: 2 (GITHUB_TOKEN, GITHUB_ORG)
setup_time: 10-15 minutes
-->

---

## FOR CLAUDE

You are helping a user connect their GitHub account to their AIOS workspace. Follow these rules:

**Behavior:**
- GitHub knowledge varies — some users are comfortable with repos and PRs, others aren't; gauge this from context
- Explain each step in plain English before doing anything technical
- GITHUB_ORG accepts either an organisation name OR a personal username — the script handles both
- Celebrate wins ("Connected — your AI can now see your code activity!")
- Never dump error messages — find the problem and explain it in one sentence

**Pacing:**
- After getting the token: "Got it. Now we need one more thing — your GitHub username or org name."
- After the first successful test: "It's working. Here's what I found:"
- After setup complete: "Done. Your GitHub activity will update every morning."

**Key things to check:**
- Token needs `repo` scope (read access to repos)
- GITHUB_ORG can be a GitHub organisation name OR a personal username — both work
- The script skips repos that haven't been updated in 30 days (normal, reduces API calls)
- Private repos are included if the token has repo scope

---

## OVERVIEW

GitHub holds your delivery output — every commit, every PR, every line of code shipped. Once this module is installed, that activity flows into your workspace daily.

Your AI will know how much code shipped today, which repos are active, and whether PRs are piling up — before you even ask.

**What gets connected:**
- Commits pushed today, per repo
- Open PRs across all active repos
- PRs merged today

**What you need:**
- A GitHub account (free works)
- A Personal Access Token with `repo` read scope
- Your GitHub organisation name or personal username

---

## PHASE 1: GET YOUR CREDENTIALS

### Step 1: Create a Personal Access Token

This is your GitHub API key. It gives your workspace read access to your repositories.

**In GitHub:**
1. Click your profile picture (top right)
2. Go to **Settings**
3. Scroll to the bottom and click **Developer settings**
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token (classic)**
6. Name it `AIOS Workspace`
7. Set expiry to **No expiration** (or 1 year — you'll need to renew it)
8. Under **Select scopes**, tick the `repo` checkbox (this covers all repo read access)
9. Click **Generate token**
10. Copy the token — it starts with `ghp_` and you won't see it again

[VERIFY] Ask: "Do you have your token? It should start with `ghp_`."

---

### Step 2: Note your GitHub username or org name

This tells the collector which account to pull repos from.

- **Personal account:** use your GitHub username (e.g. `johnsmith`)
- **Organisation:** use the org name exactly as it appears in GitHub (e.g. `mattis-consulting-ltd`)

[VERIFY] Ask: "Are we connecting a personal account or an organisation? And what's the exact name?"

---

## PHASE 2: CONNECT THE COLLECTOR

### Step 3: Add credentials to your .env file

Open your workspace's `.env` file and add these two lines:

```
GITHUB_TOKEN=ghp-your-token-here
GITHUB_ORG=your-username-or-org-name
```

Replace the placeholder values with your actual token and account name.

> **Security note:** Your `.env` file is gitignored — it will never be committed to GitHub. Your token stays on your machine only.

[VERIFY] Save the file and confirm both lines are there.

---

### Step 4: Install the collector script

Copy the GitHub collector into your scripts directory:

```bash
cp module-installs/github-os/scripts/collect_github.py scripts/collect_github.py
```

Install the required dependency (if not already installed):

```bash
.venv/bin/pip install requests python-dotenv
```

[VERIFY]
```bash
.venv/bin/python -c "import requests; from dotenv import load_dotenv; print('Dependencies OK')"
```
Expected: `Dependencies OK`

---

### Step 5: Test the connection

Run the collector standalone to confirm it can reach your GitHub account:

```bash
.venv/bin/python scripts/collect_github.py
```

**Expected output (success):**
```
GitHub (mattis-consulting-ltd): 5 active repos
  Commits today: 3
  Open PRs: 2
  Merged today: 1
```

**If you see `skipped: Missing GITHUB_TOKEN`:**
- Your `.env` file isn't being loaded. Check the file is saved and in the right folder.

**If you see a 404 error:**
- Your GITHUB_ORG name might be wrong. The script tries org repos first, then personal — double-check the name.

**If active repos shows 0:**
- All your repos may be older than 30 days without activity — this is normal. The filter keeps API calls efficient. Any repo with a recent push will show up.

[VERIFY] Confirm the repo count and commit numbers match what you'd expect.

---

### Step 6: Add GitHub to the collection orchestrator

If you have DataOS installed, add GitHub to your main collection script:

Open `scripts/collect.py` and add these lines:

```python
# At the top with other imports:
from collect_github import collect as collect_github, write as write_github

# In the run() function, alongside other collectors:
result = collect_github()
records = write_github(conn, result, today)
print(f"GitHub: {result['status']} — {records} records")
```

If you don't have DataOS yet, you can run the GitHub collector standalone at any time:

```bash
.venv/bin/python scripts/collect_github.py
```

---

## PHASE 3: SEE YOUR DATA

### Step 7: Query your activity

Run a quick SQL check to confirm your data landed:

```bash
sqlite3 data/data.db "SELECT date, commits, open_prs, merged_prs, active_repos FROM github_daily ORDER BY date DESC LIMIT 7;"
```

You should see rows for recent dates with your activity numbers.

```bash
sqlite3 data/data.db "SELECT date, repo, commits_today, open_prs FROM github_repos WHERE date = date('now') ORDER BY commits_today DESC;"
```

This shows today's breakdown by repository.

---

### Step 8: Add GitHub activity to key-metrics.md (optional)

If you have DataOS's `generate_metrics.py`, add a GitHub section so delivery throughput shows up every morning in `/prime`.

Add this to `scripts/generate_metrics.py` in the appropriate section:

```python
# GitHub Activity
cursor.execute("""
    SELECT date, commits, open_prs, merged_prs, active_repos
    FROM github_daily
    ORDER BY date DESC
    LIMIT 1
""")
gh = cursor.fetchone()

if gh:
    lines.append("## Code Activity (GitHub)")
    lines.append(f"Commits today: **{gh[1]}** | Open PRs: **{gh[2]}** | Merged today: **{gh[3]}**")
    lines.append(f"Active repos: {gh[4]}")
    lines.append("")
```

---

## PHASE 4: AUTOMATE (OPTIONAL)

### Step 9: Schedule daily collection

If you want GitHub data to refresh automatically every morning:

**If you already have a DataOS cron running**, GitHub will run automatically once you've added it to `collect.py` in Step 6.

**If you don't have a cron set up yet**, run the collector manually:
```bash
.venv/bin/python scripts/collect_github.py
```

Or ask Claude: "Set up a daily cron to run my GitHub collector at 6am"

---

## DONE

Your GitHub activity is now connected to your AIOS workspace.

**What you've got:**
- Daily commit and PR snapshots in `data/data.db`
- Per-repo breakdown of where work is happening
- Data available for AI analysis anytime

**Next steps:**
- Ask your AI: "How many commits did we ship this week?"
- Combine with GHL-OS: correlate delivery throughput with pipeline activity

---

## TROUBLESHOOTING

| Problem | Fix |
|---|---|
| `skipped: Missing GITHUB_TOKEN` | Check `.env` has `GITHUB_TOKEN=ghp-...` and the file is saved |
| 404 Not Found | Check GITHUB_ORG matches your exact GitHub username or org name |
| 0 active repos | All repos may be inactive (no pushes in 30 days) — any active repo will appear next time |
| Token expired | Regenerate your token in GitHub > Settings > Developer settings > Personal access tokens |
| `requests` not found | Run `.venv/bin/pip install requests` |
