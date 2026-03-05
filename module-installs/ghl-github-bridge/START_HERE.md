# GHL→GitHub Bridge — Start Here

Welcome! This module automatically creates a GitHub Issue whenever a deal reaches a specific stage in your GHL pipeline — so you never miss a new client that needs onboarding.

**Setup time:** 15-20 minutes
**Technical level:** Beginner-friendly — no coding required

---

## Before you start, you'll need:

- [ ] An AIOS workspace set up on your computer (from the AAA Hub template)
- [ ] Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [ ] Access to your GoHighLevel sub-account settings
- [ ] A GitHub repository where you manage client delivery work
- [ ] GHL-OS already installed (so your GHL API key is already in `.env`)

If you don't have the AIOS workspace set up yet, grab the template first:
👉 https://github.com/PMatX3/mattis-aios-workspace-template

---

## How to install (3 steps)

### Step 1 — Unzip this file

You've already done this if you're reading it! You should see a folder called `ghl-github-bridge` containing:
- `START_HERE.md` ← you're reading this
- `README.md` — overview
- `INSTALL.md` — full step-by-step guide
- `scripts/ghl_github_bridge.py` — the bridge script

### Step 2 — Drop the folder into your workspace

Move the `ghl-github-bridge` folder into the `module-installs/` folder inside your AIOS workspace.

It should look like this when you're done:
```
your-workspace/
└── module-installs/
    └── ghl-github-bridge/    ← this folder goes here
        ├── START_HERE.md
        ├── INSTALL.md
        ├── README.md
        └── scripts/
```

### Step 3 — Run the installer

Open your workspace in Claude Code and type:

```
/install module-installs/ghl-github-bridge
```

Claude will walk you through the rest — telling it which pipeline stage triggers the issue, which GitHub repo to post to, and testing the connection with a dry run.

---

## What happens after install?

Whenever you run the bridge (manually or on a schedule), it will:
1. Check your GHL pipeline for deals at the trigger stage
2. For each new deal — create a GitHub Issue with client info + onboarding checklist
3. Skip any deals that already have an issue (safe to run repeatedly)

You can ask Claude to run it on demand:
- *"Run the GHL bridge to check for new clients"*
- *"Do a dry run of the bridge to see what it would create"*

---

## Need help?

Post in the AAA Hub community and tag Patrick — happy to help you get it running.
