# GHL→GitHub Bridge — Automated Client Onboarding

> A plug-and-play module from the AAA Accelerator.
> Grab this and 15+ more at [aaaaccelerator.com](https://aaaaccelerator.com)

When a deal reaches a specific stage in your GHL pipeline (e.g. "Payment Received"), this bridge automatically creates a GitHub Issue in your delivery repository — complete with client details, deal value, and an onboarding checklist.

No manual copy-paste. No deals falling through the cracks.

**What you'll have when this is done:**
- A GitHub Issue created automatically when payment lands in GHL
- Client name, email, company, and deal value pulled from the opportunity
- A ready-made onboarding checklist in every issue
- Direct link back to the GHL opportunity
- Built-in deduplication — runs safely every day without creating duplicates

**Setup time:** 15-20 minutes
**Cost:** Free (uses GHL Private Integration API + GitHub REST API)
**Requires:** Python 3.10+, GHL sub-account, GitHub repository

---

## How it works

```
GHL Pipeline → "Payment Received" stage
        ↓
   Bridge script runs
        ↓
   Checks GitHub: issue already exists?
        ↓ No
   Creates GitHub Issue with client details + onboarding checklist
```

The bridge uses deduplication — it embeds the GHL opportunity ID in a hidden comment in the issue body. Before creating any issue, it searches GitHub for that ID. Running the bridge multiple times is safe.

---

## What data flows across?

| Field | Source |
|---|---|
| Client name | GHL opportunity name |
| Contact name & email | GHL contact record |
| Company name | GHL contact record |
| Deal value | GHL opportunity value |
| GHL link | Direct link to the opportunity |
| Onboarding checklist | Built into the issue template |

---

## Quick start

Run `/install module-installs/ghl-github-bridge` in Claude Code and follow the guided setup.

Or jump straight to [INSTALL.md](INSTALL.md) for step-by-step instructions.
