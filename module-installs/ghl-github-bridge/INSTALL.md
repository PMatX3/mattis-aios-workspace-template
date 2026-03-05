# GHL→GitHub Bridge — AIOS Module Installer

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

<!-- MODULE METADATA
module: ghl-github-bridge
version: v1
status: RELEASED
released: 2026-03-05
requires: [context-os, ghl-os, github-os]
phase: 3
category: Automation
complexity: moderate
api_keys: 4 (GHL_API_KEY, GHL_LOCATION_ID, GITHUB_TOKEN, GITHUB_REPO)
env_config: 2 (GHL_TRIGGER_PIPELINE, GHL_TRIGGER_STAGE)
setup_time: 15-20 minutes
-->

---

## FOR CLAUDE

You are helping a user connect GHL to GitHub so deals automatically become GitHub issues. Follow these rules:

**Behavior:**
- The user must know which pipeline and stage they want to trigger on — ask before proceeding
- Show the list of pipelines and stages from GHL so they can confirm the exact name (names must match exactly)
- Use a dry run first — never create real issues without user confirmation
- Explain deduplication clearly — reassure them that running it multiple times is safe
- Celebrate the first real issue creation

**Pacing:**
- After getting credentials: "Let me run a dry run first — I'll show you what issues would be created without actually creating them."
- After dry run: "That's what it'll create. Ready to run it for real?"
- After first real issue: "Done — check your GitHub repo, you should see the new issue."

**Key things to check:**
- GHL_TRIGGER_PIPELINE and GHL_TRIGGER_STAGE must match GHL pipeline/stage names exactly (case-sensitive)
- Run `--dry-run` first before any live run
- GITHUB_REPO must be in `owner/repo` format (e.g. `acme/delivery-projects`)
- The GitHub token needs `repo` scope (issues write access)

**How to discover pipeline/stage names:**
Run a dry-run first, which will log the available pipelines if the names don't match. Or tell the user to check GHL > Opportunities > Pipeline view.

---

## OVERVIEW

When a deal lands in your payment-received stage in GHL, the next step is always the same: create a project, send a welcome email, schedule the kickoff. The bridge automates the first part of that — creating the GitHub Issue so nothing falls through the cracks.

**What it does:**
1. Polls GHL for opportunities at your chosen pipeline stage
2. For each new opportunity — creates a GitHub Issue with client info + onboarding checklist
3. Deduplicates — safe to run daily or on-demand without creating duplicate issues

**What you need:**
- GHL API key + Location ID (if you've already installed GHL-OS, these are already in your `.env`)
- GitHub Personal Access Token with `repo` scope
- Your delivery repository name (in `owner/repo` format)
- The exact name of your trigger pipeline and stage in GHL

---

## PHASE 1: IDENTIFY YOUR TRIGGER

### Step 1: Decide which pipeline stage triggers issue creation

Think about where in your GHL pipeline you want a GitHub Issue created. Common choices:
- **"Payment Received"** — money in, onboarding starts
- **"Contract Signed"** — signed, about to invoice
- **"Proposal Accepted"** — earlier trigger, includes pre-sale steps in the checklist

[VERIFY] Ask: "Which pipeline and stage do you want to use as the trigger? Go to GHL > Opportunities and look at your pipeline — what are the exact names?"

---

## PHASE 2: GET YOUR CREDENTIALS

### Step 2: Check if GHL credentials are already set

If you've installed GHL-OS, your GHL credentials are already in `.env`. Skip to Step 3.

If not, add them now:
```
GHL_API_KEY=pit-your-token-here
GHL_LOCATION_ID=your-location-id-here
```

See [ghl-os/INSTALL.md](../ghl-os/INSTALL.md) for how to get these.

---

### Step 3: Create a GitHub Personal Access Token

If you've installed GitHub-OS, your GitHub token is already in `.env`. Skip to Step 4.

If not:
1. Go to GitHub > Settings > Developer settings > Personal access tokens
2. Generate a new token (classic)
3. Name it `AIOS Workspace`
4. Tick the `repo` scope (needed to create issues)
5. Copy the token (`ghp_...`)

---

## PHASE 3: CONFIGURE THE BRIDGE

### Step 4: Add all credentials to your .env file

Open your workspace's `.env` file. You need these values:

```
# GHL credentials (skip if already set from GHL-OS)
GHL_API_KEY=pit-your-token-here
GHL_LOCATION_ID=your-location-id-here

# GitHub credentials (skip if already set from GitHub-OS)
GITHUB_TOKEN=ghp-your-token-here
GITHUB_REPO=your-org/your-repo-name

# Bridge trigger config
GHL_TRIGGER_PIPELINE=Your Pipeline Name Here
GHL_TRIGGER_STAGE=Your Stage Name Here
```

> **Important:** `GHL_TRIGGER_PIPELINE` and `GHL_TRIGGER_STAGE` must match your GHL pipeline names exactly — including capitalisation and spacing.

[VERIFY] Save the file. Read back the GITHUB_REPO and trigger values to confirm they're correct.

---

### Step 5: Install the bridge script

Copy the bridge into your scripts directory:

```bash
cp module-installs/ghl-github-bridge/scripts/ghl_github_bridge.py scripts/ghl_github_bridge.py
```

Install the required dependency (if not already installed):

```bash
.venv/bin/pip install requests python-dotenv
```

---

### Step 6: Set up GitHub labels

The bridge creates three labels in your repo to tag onboarding issues. Run the setup command:

```bash
.venv/bin/python scripts/ghl_github_bridge.py --setup
```

Expected:
```
Created label: ghl-linked
Created label: payment-received
Created label: ready-for-onboarding
Label setup complete.
```

If labels already exist, it skips them — safe to run multiple times.

---

## PHASE 4: TEST THE CONNECTION

### Step 7: Run a dry run

Before creating any real issues, do a dry run to preview what it would create:

```bash
.venv/bin/python scripts/ghl_github_bridge.py --dry-run
```

**Expected output (success, deals found):**
```
2026-03-05 09:00:01  INFO      ============================================================
2026-03-05 09:00:01  INFO      GHL → GitHub Bridge  [DRY RUN]
2026-03-05 09:00:01  INFO      Pipeline : Your Pipeline Name
2026-03-05 09:00:01  INFO      Stage    : Your Stage Name
2026-03-05 09:00:03  INFO      Fetched 2 opportunities at 'Your Stage Name'
2026-03-05 09:00:04  INFO      DRY RUN — would create issue: [Client Name] - £5,000 - opp123
2026-03-05 09:00:05  INFO      DRY RUN — would create issue: [Client Name 2] - £3,500 - opp456
2026-03-05 09:00:05  INFO      Done.  Created: 2  |  Skipped: 0  |  Errors: 0
```

**If you see `Pipeline 'X' not found`:**
- The pipeline name doesn't match. The log will show you the available pipeline names — update `GHL_TRIGGER_PIPELINE` in `.env`.

**If opportunities count is 0:**
- No deals are currently at that stage — this is fine. The bridge will create issues when deals move there.

[VERIFY] Confirm the dry run shows the deals you expect (or 0 if the stage is currently empty).

---

### Step 8: Run for real

Once the dry run looks right, run it live:

```bash
.venv/bin/python scripts/ghl_github_bridge.py
```

Check your GitHub repository — you should see new issues with the client details and onboarding checklist.

---

## PHASE 5: AUTOMATE (OPTIONAL)

### Step 9: Schedule the bridge to run daily

The bridge is most useful when it runs automatically — checking for new payment-stage deals each morning.

**If you already have a DataOS cron running**, add the bridge to your collection pipeline:

```bash
# Add to your launchd plist or cron schedule:
.venv/bin/python scripts/ghl_github_bridge.py
```

Or ask Claude: "Set up a daily cron to run the GHL GitHub bridge at 7am"

**Run on-demand anytime:**
```bash
.venv/bin/python scripts/ghl_github_bridge.py
```

---

## DONE

Your GHL pipeline is now connected to your GitHub delivery repo.

**What you've got:**
- Automatic GitHub Issues when deals reach your trigger stage
- Client name, email, deal value, and GHL link in every issue
- Onboarding checklist built into each issue
- Deduplication — safe to run daily

**Next steps:**
- Customise the onboarding checklist in `scripts/ghl_github_bridge.py` → `build_issue_body()`
- Ask Claude to modify the checklist to match your onboarding process
- Set up a daily cron so it runs automatically

---

## TROUBLESHOOTING

| Problem | Fix |
|---|---|
| `Pipeline 'X' not found` | Check GHL_TRIGGER_PIPELINE matches exactly — look at the error log for available pipeline names |
| `Stage 'X' not found` | Check GHL_TRIGGER_STAGE matches exactly — log will show available stages in that pipeline |
| `Missing required environment variables` | Check `.env` has GHL_API_KEY, GHL_LOCATION_ID, GITHUB_TOKEN, GITHUB_REPO |
| Issues not creating (no error) | The stage may be empty — check GHL for deals at that stage |
| Duplicate issues appearing | Deduplication requires the hidden comment to be intact in the issue body — don't edit or remove it |
| GitHub 403 Forbidden | Your GITHUB_TOKEN needs `repo` scope to create issues — regenerate with correct scopes |
| `requests` not found | Run `.venv/bin/pip install requests` |
