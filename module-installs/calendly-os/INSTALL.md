# Calendly-OS — AIOS Module Installer

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

<!-- MODULE METADATA
module: calendly-os
version: v1
status: RELEASED
released: 2026-03-05
requires: [context-os]
phase: 2
category: Data
complexity: simple
api_keys: 1 (CALENDLY_API_TOKEN)
setup_time: 10-15 minutes
-->

---

## FOR CLAUDE

You are helping a user connect their Calendly account to their AIOS workspace. Follow these rules:

**Behavior:**
- Calendly is universal — anyone booking calls will know what it is
- Explain each step in plain English before doing anything technical
- Use plain language — "your Calendly API token" not "Personal Access Token" in conversation
- Celebrate wins ("Connected — your AI can now see your call bookings!")
- If something fails, explain it simply and provide the fix in one sentence
- Never dump error messages

**Pacing:**
- After getting the API token: "Got it. Let me test the connection now."
- After the first successful test: "It's working. Here's what it found:"
- After the cron is set up: "Done. Your call data will update every morning automatically."

**Key things to check:**
- Calendly API token is a Personal Access Token (from Settings > Integrations > API & Webhooks)
- NOT an OAuth token — must be the personal token
- If the user has a team/org account, the token still works — it pulls their own events only

---

## OVERVIEW

Calendly is where most AAA members manage their inbound calls. Right now, to see your booking numbers, you have to log into Calendly and click around. Once this module is installed, your call data flows automatically into your workspace every morning.

Your AI will know how many calls you've booked each day — before you even ask.

**What gets connected:**
- Calls booked per day (rolling 14-day window)
- Individual event details: type, time, status, location (Zoom/phone/in-person)

**What you need:**
- A Calendly account (any plan — free works)
- A Personal Access Token from Calendly settings

---

## PHASE 1: GET YOUR CREDENTIALS

### Step 1: Create a Personal Access Token

This is your Calendly API key. It gives your workspace read access to your scheduled events.

**In Calendly:**
1. Click your profile icon (top right)
2. Go to **Profile Settings**
3. Click **Integrations** in the left sidebar
4. Scroll down to **API & Webhooks**
5. Click **Personal Access Tokens**
6. Click **+ Generate New Token**
7. Name it `AIOS Workspace` and click **Create Token**
8. Copy the token — you won't be able to see it again

> **Note:** The token only reads your own events — it doesn't touch your bookings or settings.

[VERIFY] Ask: "Do you have your token? It's the long string you just copied."

---

## PHASE 2: CONNECT THE COLLECTOR

### Step 2: Add your token to the .env file

Open your workspace's `.env` file and add this line:

```
CALENDLY_API_TOKEN=your-token-here
```

Replace `your-token-here` with the token you just copied.

> **Security note:** Your `.env` file is gitignored — it will never be committed to GitHub. Your token stays on your machine only.

[VERIFY] Save the file and confirm the line is there.

---

### Step 3: Install the collector script

Copy the Calendly collector into your scripts directory:

```bash
cp module-installs/calendly-os/scripts/collect_calendly.py scripts/collect_calendly.py
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

### Step 4: Test the connection

Run the collector standalone to confirm it can reach your Calendly account:

```bash
.venv/bin/python scripts/collect_calendly.py
```

**Expected output (success):**
```
Calendly: 8 events in the next/last 7 days
  2026-03-03: 2 call(s)
  2026-03-04: 3 call(s)
  2026-03-06: 3 call(s)
```

**If you see `skipped: Missing CALENDLY_API_TOKEN`:**
- Your `.env` file isn't being loaded. Check the file is saved and in the right folder.

**If you see a 401 Unauthorized error:**
- Your token is incorrect. Re-copy it from Calendly settings.

**If calls count shows 0 but you have bookings:**
- The collector looks at a ±7 day window. If all bookings are older, this is expected. The database will fill up over time.

[VERIFY] Confirm the output shows events you'd expect from your Calendly.

---

### Step 5: Add Calendly to the collection orchestrator

If you have DataOS installed, add Calendly to your main collection script:

Open `scripts/collect.py` and add these lines:

```python
# At the top with other imports:
from collect_calendly import collect as collect_calendly, write as write_calendly

# In the run() function, alongside other collectors:
result = collect_calendly()
records = write_calendly(conn, result, today)
print(f"Calendly: {result['status']} — {records} records")
```

If you don't have DataOS yet, you can run the Calendly collector standalone at any time:

```bash
.venv/bin/python scripts/collect_calendly.py
```

---

## PHASE 3: SEE YOUR DATA

### Step 6: Query your bookings

Run a quick SQL check to confirm your data landed:

```bash
sqlite3 data/data.db "SELECT date, calls_booked FROM calendly_daily ORDER BY date DESC LIMIT 14;"
```

You should see rows for recent dates with your call counts.

```bash
sqlite3 data/data.db "SELECT event_date, name, start_time FROM calendly_events ORDER BY start_time DESC LIMIT 10;"
```

This shows your most recent individual events.

---

### Step 7: Add call bookings to key-metrics.md (optional)

If you have DataOS's `generate_metrics.py`, add a Calendly section so your booking rate shows up every morning in `/prime`.

Add this to `scripts/generate_metrics.py` in the appropriate section:

```python
# Calendly Call Bookings
cursor.execute("""
    SELECT date, calls_booked
    FROM calendly_daily
    WHERE date >= date('now', '-7 days')
    ORDER BY date
""")
calls = cursor.fetchall()

if calls:
    total_calls = sum(r[1] for r in calls)
    lines.append("## Call Bookings (Calendly)")
    lines.append(f"Calls booked last 7 days: **{total_calls}**")
    lines.append("")
    for row in calls:
        lines.append(f"- {row[0]}: {row[1]} call(s)")
    lines.append("")
```

---

## PHASE 4: AUTOMATE (OPTIONAL)

### Step 8: Schedule daily collection

If you want Calendly data to refresh automatically every morning:

**If you already have a DataOS cron running**, Calendly will run automatically once you've added it to `collect.py` in Step 5.

**If you don't have a cron set up yet**, the simplest option is to run the collector manually:
```bash
.venv/bin/python scripts/collect_calendly.py
```

Or ask Claude: "Set up a daily cron to run my Calendly collector at 6am"

---

## DONE

Your Calendly account is now connected to your AIOS workspace.

**What you've got:**
- Daily call booking counts in `data/data.db`
- Individual event records with type and time
- Data available for AI analysis anytime

**Next steps:**
- Ask your AI: "How many discovery calls did I book this week?"
- Compare call bookings with pipeline activity from GHL-OS

---

## TROUBLESHOOTING

| Problem | Fix |
|---|---|
| `skipped: Missing CALENDLY_API_TOKEN` | Check `.env` has `CALENDLY_API_TOKEN=...` and the file is saved |
| 401 Unauthorized | Re-copy the token from Calendly > Settings > Integrations > API & Webhooks |
| 0 events returned but you have bookings | The collector uses a ±7 day window — older events won't appear but future runs will track going forward |
| `requests` not found | Run `.venv/bin/pip install requests` |
