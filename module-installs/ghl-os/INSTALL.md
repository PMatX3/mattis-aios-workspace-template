# GHL-OS — AIOS Module Installer

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

<!-- MODULE METADATA
module: ghl-os
version: v1
status: RELEASED
released: 2026-03-05
requires: [context-os]
phase: 2
category: Data
complexity: simple
api_keys: 2 (GHL_API_KEY, GHL_LOCATION_ID)
setup_time: 15-20 minutes
-->

---

## FOR CLAUDE

You are helping a user connect their GoHighLevel sub-account to their AIOS workspace. Follow these rules:

**Behavior:**
- Assume the user knows GHL (they're in the AAA world) but may not know what a "Private Integration Token" is
- Explain each step in plain English before doing anything technical
- Use plain language — "your GHL API key" not "Private Integration Token" in conversation
- Celebrate wins ("Pipeline connected — your AI can now see your deals!")
- If something fails, explain it simply and provide the fix
- Never dump error messages — find the problem and explain it in one sentence

**Pacing:**
- After getting the API key: "Key looks good. Now let's find your Location ID — this tells GHL which sub-account to pull from."
- After the first successful test: "It's working. Let me show you what's in the database."
- After the cron is set up: "Done. Your pipeline data will update every morning automatically."

**Key things to check:**
- GHL API key must be a Private Integration Token (starts with `pit-`), NOT an Agency API key
- Location ID is the sub-account ID, not the agency ID — visible in the GHL URL
- If the user has multiple sub-accounts, ask which one they want to connect first

---

## OVERVIEW

GoHighLevel holds some of your most important business data — your deals, your pipeline, your booked calls. Right now, to see that data, you have to log into GHL and click around. Once this module is installed, that data flows automatically into your workspace every morning.

Your AI will know your pipeline value, how many deals are in each stage, and how many new contacts came in — before you even ask.

**What gets connected:**
- Pipeline opportunities — counts and value by stage
- New contacts added each day
- Appointments booked across your calendars

**What you need:**
- A GoHighLevel account with at least one sub-account (location)
- Access to GHL Settings to create a Private Integration Token

---

## PHASE 1: GET YOUR CREDENTIALS

### Step 1: Create a Private Integration Token

This is your GHL API key. It gives your workspace read access to your sub-account data.

**In GHL:**
1. Go to your **sub-account** (not the agency dashboard)
2. Click **Settings** in the left sidebar
3. Scroll down to **Integrations** → **Private Integrations**
4. Click **+ Add Private Integration**
5. Name it something like `AIOS Workspace`
6. Under **Scopes**, enable:
   - `contacts.readonly`
   - `opportunities.readonly`
   - `calendars.readonly`
   - `calendars/events.readonly`
7. Click **Save** and copy the token — it starts with `pit-`

> **Important:** This is a sub-account token, not an agency token. Make sure you're in the sub-account settings, not the agency-level settings.

Copy the token and keep it handy for the next step.

[VERIFY] Ask: "Do you have your token? It should start with `pit-`"

---

### Step 2: Find Your Location ID

Your Location ID tells the collector which GHL sub-account to pull data from.

**Easiest way:**
1. Log into your GHL sub-account
2. Look at the URL in your browser — it will look something like:
   `https://app.gohighlevel.com/location/abc123XYZ456/dashboard`
3. The string between `/location/` and `/dashboard` is your Location ID

Copy it — you'll need it in a moment.

[VERIFY] Ask: "Got your Location ID? It's the string from the URL."

---

## PHASE 2: CONNECT THE COLLECTOR

### Step 3: Add credentials to your .env file

Open your workspace's `.env` file and add these two lines:

```
GHL_API_KEY=pit-your-token-here
GHL_LOCATION_ID=your-location-id-here
```

Replace the placeholder values with your actual token and location ID.

> **Security note:** Your `.env` file is gitignored — it will never be committed to GitHub. Your API key stays on your machine only.

[VERIFY] Save the file and confirm the values look right.

---

### Step 4: Install the collector script

Copy the GHL collector into your scripts directory:

```bash
cp module-installs/ghl-os/scripts/collect_ghl.py scripts/collect_ghl.py
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

Run the collector standalone to confirm it can reach your GHL account:

```bash
.venv/bin/python scripts/collect_ghl.py
```

**Expected output (success):**
```
GHL Pipeline:
  Sales Pipeline / New Lead: 3 opps, £4,500
  Sales Pipeline / Proposal Sent: 1 opps, £9,000
New contacts today: 2
Appointments today: 1
```

**If you see `skipped: Missing GHL_API_KEY`:**
- Your `.env` file isn't being loaded. Check the file is saved and in the right folder.

**If you see `skipped: Missing GHL_LOCATION_ID`:**
- Add your Location ID to `.env`.

**If the pipeline shows empty but you have deals in GHL:**
- Double-check you're using a sub-account token (starts with `pit-`), not an agency token.
- Confirm the token has `opportunities.readonly` scope enabled.

[VERIFY] Confirm the output matches what you'd expect from your GHL account.

---

### Step 6: Add GHL to the collection orchestrator

If you have DataOS installed, add GHL to your main collection script:

Open `scripts/collect.py` and add these lines to the imports and runner:

```python
# At the top with other imports:
from collect_ghl import collect as collect_ghl, write as write_ghl

# In the run() function, alongside other collectors:
result = collect_ghl()
records = write_ghl(conn, result, today)
print(f"GHL: {result['status']} — {records} records")
```

If you don't have DataOS yet, you can run the GHL collector standalone at any time:

```bash
.venv/bin/python scripts/collect_ghl.py
```

---

## PHASE 3: SEE YOUR DATA

### Step 7: Query your pipeline

Run a quick SQL check to confirm your data landed:

```bash
sqlite3 data/data.db "SELECT date, pipeline_name, stage_name, count, total_value_gbp FROM ghl_pipeline_daily ORDER BY date DESC LIMIT 10;"
```

You should see rows for today's date with your pipeline stages and deal counts.

```bash
sqlite3 data/data.db "SELECT date, new_contacts, appointments FROM ghl_activity_daily ORDER BY date DESC LIMIT 7;"
```

This shows your last 7 days of contact and appointment activity.

---

### Step 8: Add pipeline to key-metrics.md (optional)

If you have DataOS's `generate_metrics.py`, add a GHL section so your pipeline shows up every morning in `/prime`.

Add this to `scripts/generate_metrics.py` in the appropriate section:

```python
# GHL Pipeline
cursor.execute("""
    SELECT pipeline_name, stage_name, count, total_value_gbp
    FROM ghl_pipeline_daily
    WHERE date = (SELECT MAX(date) FROM ghl_pipeline_daily)
    ORDER BY pipeline_name, stage_name
""")
pipeline = cursor.fetchall()

if pipeline:
    lines.append("## Pipeline (GHL)")
    lines.append("| Stage | Deals | Value |")
    lines.append("|---|---|---|")
    for row in pipeline:
        lines.append(f"| {row[1]} | {row[2]} | £{row[3]:,.0f} |")
    lines.append("")
```

---

## PHASE 4: AUTOMATE (OPTIONAL)

### Step 9: Schedule daily collection

If you want GHL data to refresh automatically every morning, add it to your cron schedule.

**macOS (launchd):**
If you already have a DataOS cron running, GHL will run automatically once you've added it to `collect.py` in Step 6.

If you don't have a cron set up yet, the simplest option is to run the collector manually each morning:
```bash
.venv/bin/python scripts/collect_ghl.py
```

Or ask Claude: "Set up a daily cron to run my GHL collector at 6am" — it will configure launchd for you.

---

## DONE

Your GoHighLevel pipeline is now connected to your AIOS workspace.

**What you've got:**
- Daily pipeline snapshots in `data/data.db`
- Opportunity counts and value by stage
- New contacts and appointments tracked each day
- Data available for AI analysis anytime

**Next steps:**
- Connect more data sources via the DataOS module
- Add pipeline metrics to your weekly scorecard
- Ask your AI: "How does this week's pipeline compare to last month?"

---

## TROUBLESHOOTING

| Problem | Fix |
|---|---|
| `skipped: Missing GHL_API_KEY` | Check `.env` has `GHL_API_KEY=pit-...` and the file is saved |
| `skipped: Missing GHL_LOCATION_ID` | Add `GHL_LOCATION_ID=...` to `.env` |
| Pipeline shows empty but deals exist in GHL | Confirm token has `opportunities.readonly` scope and is a sub-account token (not agency) |
| Contacts count always 0 | Token needs `contacts.readonly` scope — regenerate with correct scopes |
| Appointments count always 0 | Token needs `calendars.readonly` and `calendars/events.readonly` scopes |
| `requests` not found | Run `.venv/bin/pip install requests` |
