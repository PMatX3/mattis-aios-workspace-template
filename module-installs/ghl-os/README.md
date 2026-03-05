# GHL-OS — GoHighLevel Data Connector

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

Connect your GoHighLevel sub-account to your AIOS workspace. Pull pipeline opportunities, new contacts, and appointment data into a local database — automatically, every morning.

**What you'll have when this is done:**
- Live GHL pipeline data in your local database
- Daily snapshots: opportunity counts by stage, new contacts, appointments booked
- Numbers loaded into `key-metrics.md` every morning so your AI always knows your pipeline

**Setup time:** 15-20 minutes
**Cost:** Free (uses GHL's built-in Private Integration API)
**Requires:** Python 3.10+, an AIOS workspace (DataOS recommended)

---

## What data does it collect?

| Metric | Where it comes from | How often |
|---|---|---|
| Open opportunities by pipeline stage | GHL Opportunities | Daily |
| Total pipeline value (£/$ per stage) | GHL Opportunities | Daily |
| New contacts added today | GHL Contacts | Daily |
| Appointments booked today | GHL Calendars | Daily |

---

## Quick start

Run `/install module-installs/ghl-os` in Claude Code and follow the guided setup.

Or jump straight to [INSTALL.md](INSTALL.md) for step-by-step instructions.
