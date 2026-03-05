# Calendly-OS — Calendly Data Connector

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

Connect your Calendly account to your AIOS workspace. Pull scheduled call data into a local database — automatically, every morning.

**What you'll have when this is done:**
- Daily call booking snapshots in your local database
- Call counts per day so your AI can track acquisition trends
- Individual event records (name, type, time, location)

**Setup time:** 10-15 minutes
**Cost:** Free (uses Calendly's built-in Personal Access Token API)
**Requires:** Python 3.10+, an AIOS workspace (DataOS recommended)

---

## What data does it collect?

| Metric | Where it comes from | How often |
|---|---|---|
| Calls booked per day | Calendly Scheduled Events | Daily |
| Individual event details | Calendly Scheduled Events | Daily |
| Event type (name) | Calendly Scheduled Events | Daily |

---

## Quick start

Run `/install module-installs/calendly-os` in Claude Code and follow the guided setup.

Or jump straight to [INSTALL.md](INSTALL.md) for step-by-step instructions.
