# GHL-OS — Start Here

Welcome! This module connects your GoHighLevel account to your AIOS workspace so your AI always knows your pipeline, contacts, and booked calls.

**Setup time:** 15-20 minutes
**Technical level:** Beginner-friendly — no coding required

---

## Before you start, you'll need:

- [ ] An AIOS workspace set up on your computer (from the AAA Hub template)
- [ ] Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [ ] Access to your GoHighLevel sub-account settings

If you don't have the AIOS workspace set up yet, grab the template first:
👉 https://github.com/PMatX3/mattis-aios-workspace-template

---

## How to install (3 steps)

### Step 1 — Unzip this file

You've already done this if you're reading it! You should see a folder called `ghl-os` containing:
- `START_HERE.md` ← you're reading this
- `README.md` — overview
- `INSTALL.md` — full step-by-step guide
- `scripts/collect_ghl.py` — the connector script

### Step 2 — Drop the folder into your workspace

Move the `ghl-os` folder into the `module-installs/` folder inside your AIOS workspace.

It should look like this when you're done:
```
your-workspace/
└── module-installs/
    └── ghl-os/        ← this folder goes here
        ├── START_HERE.md
        ├── INSTALL.md
        ├── README.md
        └── scripts/
```

### Step 3 — Run the installer

Open your workspace in Claude Code and type:

```
/install module-installs/ghl-os
```

Claude will walk you through the rest — getting your GHL API key, finding your Location ID, testing the connection, and setting everything up. Just follow along.

---

## What happens after install?

Every morning your workspace will automatically pull:
- Your open pipeline opportunities by stage (and the £/$ value of each)
- How many new contacts were added
- How many appointments were booked

Your AI sees this data every time you start a session. You can ask things like:
- *"How does my pipeline look this week?"*
- *"How many leads came in yesterday?"*
- *"Which stage has the most stuck deals?"*

---

## Need help?

Post in the AAA Hub community and tag Patrick — happy to help you get it running.
