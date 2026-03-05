# Calendly-OS — Start Here

Welcome! This module connects your Calendly account to your AIOS workspace so your AI always knows how many calls you've booked.

**Setup time:** 10-15 minutes
**Technical level:** Beginner-friendly — no coding required

---

## Before you start, you'll need:

- [ ] An AIOS workspace set up on your computer (from the AAA Hub template)
- [ ] Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [ ] A Calendly account (free or paid — both work)

If you don't have the AIOS workspace set up yet, grab the template first:
👉 https://github.com/PMatX3/mattis-aios-workspace-template

---

## How to install (3 steps)

### Step 1 — Unzip this file

You've already done this if you're reading it! You should see a folder called `calendly-os` containing:
- `START_HERE.md` ← you're reading this
- `README.md` — overview
- `INSTALL.md` — full step-by-step guide
- `scripts/collect_calendly.py` — the connector script

### Step 2 — Drop the folder into your workspace

Move the `calendly-os` folder into the `module-installs/` folder inside your AIOS workspace.

It should look like this when you're done:
```
your-workspace/
└── module-installs/
    └── calendly-os/        ← this folder goes here
        ├── START_HERE.md
        ├── INSTALL.md
        ├── README.md
        └── scripts/
```

### Step 3 — Run the installer

Open your workspace in Claude Code and type:

```
/install module-installs/calendly-os
```

Claude will walk you through the rest — getting your Calendly API token, testing the connection, and setting everything up. Just follow along.

---

## What happens after install?

Every morning your workspace will automatically pull:
- How many calls were booked each day
- What type of calls (discovery, audit, strategy, etc.)
- A 14-day rolling window of call activity

Your AI sees this data every time you start a session. You can ask things like:
- *"How many discovery calls did I book this week?"*
- *"Is my booking rate trending up or down?"*
- *"How many calls do I have this week?"*

---

## Need help?

Post in the AAA Hub community and tag Patrick — happy to help you get it running.
