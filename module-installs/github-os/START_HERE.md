# GitHub-OS — Start Here

Welcome! This module connects your GitHub account to your AIOS workspace so your AI always knows what's shipping — commits, PRs, and which repos are active.

**Setup time:** 10-15 minutes
**Technical level:** Beginner-friendly — no coding required

---

## Before you start, you'll need:

- [ ] An AIOS workspace set up on your computer (from the AAA Hub template)
- [ ] Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [ ] A GitHub account with repos you want to track

If you don't have the AIOS workspace set up yet, grab the template first:
👉 https://github.com/PMatX3/mattis-aios-workspace-template

---

## How to install (3 steps)

### Step 1 — Unzip this file

You've already done this if you're reading it! You should see a folder called `github-os` containing:
- `START_HERE.md` ← you're reading this
- `README.md` — overview
- `INSTALL.md` — full step-by-step guide
- `scripts/collect_github.py` — the connector script

### Step 2 — Drop the folder into your workspace

Move the `github-os` folder into the `module-installs/` folder inside your AIOS workspace.

It should look like this when you're done:
```
your-workspace/
└── module-installs/
    └── github-os/        ← this folder goes here
        ├── START_HERE.md
        ├── INSTALL.md
        ├── README.md
        └── scripts/
```

### Step 3 — Run the installer

Open your workspace in Claude Code and type:

```
/install module-installs/github-os
```

Claude will walk you through the rest — getting your GitHub token, setting your org/username, testing the connection, and setting everything up.

---

## What happens after install?

Every morning your workspace will automatically pull:
- Commits pushed today across all active repos
- Open pull requests waiting for review
- PRs merged today

Your AI sees this data every time you start a session. You can ask things like:
- *"How many commits did we push this week?"*
- *"Which repos are most active right now?"*
- *"Do we have any PRs waiting for review?"*

---

## Need help?

Post in the AAA Hub community and tag Patrick — happy to help you get it running.
