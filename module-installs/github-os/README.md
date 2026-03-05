# GitHub-OS — GitHub Activity Connector

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

Connect your GitHub organisation (or personal account) to your AIOS workspace. Pull daily code activity into a local database — automatically, every morning.

**What you'll have when this is done:**
- Daily commit and PR snapshots across all your active repos
- Per-repository breakdown so you can see where work is happening
- Delivery throughput data your AI can use to track output trends

**Setup time:** 10-15 minutes
**Cost:** Free (uses GitHub's REST API with a personal access token)
**Requires:** Python 3.10+, an AIOS workspace (DataOS recommended)

---

## What data does it collect?

| Metric | Where it comes from | How often |
|---|---|---|
| Commits today (per repo) | GitHub REST API | Daily |
| Open PRs (per repo) | GitHub REST API | Daily |
| Merged PRs today (per repo) | GitHub REST API | Daily |
| Active repos (updated in last 30 days) | GitHub REST API | Daily |

Works with both **GitHub organisations** and **personal accounts**.

---

## Quick start

Run `/install module-installs/github-os` in Claude Code and follow the guided setup.

Or jump straight to [INSTALL.md](INSTALL.md) for step-by-step instructions.
