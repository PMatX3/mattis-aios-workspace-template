# Handover Pack Template

**Project:** [Name]
**Client / Partner:** [Name]
**Handover Date:** [Date]
**Handed Over By:** [YOUR_NAME] / [YOUR_COMPANY]
**Received By:** [Name, role]
**Version:** 1.0

---

## Purpose

This pack transfers ownership of the delivered system from the delivery team to the client/partner. After sign-off, the client owns the system. Support obligations are as defined in the SOW.

No handover pack = no clean close. This document is mandatory for every engagement.

---

## 1. System Overview

**What was built:**
[2–3 sentences. What the system does, key flows, what it's integrated with.]

**Architecture summary:**
[Brief description or link to architecture diagram. Platforms used, key services, data flows.]

**Live URLs / endpoints / phone numbers:**
| Item | Value |
|---|---|
| [e.g. Webhook endpoint] | [URL] |
| [e.g. Phone number] | [Number] |
| [e.g. Dashboard URL] | [URL] |

---

## 2. Access & Credentials Checklist

All credentials and access must be transferred. Tick when confirmed by client.

| Item | Location / Tool | Client Has Access? | Notes |
|---|---|---|---|
| [e.g. Platform account] | [Tool] | [ ] | |
| [e.g. API keys] | [Password manager / vault] | [ ] | |
| [e.g. OAuth app credentials] | [Platform] | [ ] | Refresh tokens must be rotated post-handover |
| [e.g. Cloud console access] | [AWS / GCP / Azure IAM] | [ ] | |
| [e.g. Automation platform] | [n8n / Make / Zapier] | [ ] | |
| [e.g. Monitoring dashboard] | [Tool] | [ ] | |
| [e.g. GitHub repo] | GitHub | [ ] | |
| [e.g. Domain / DNS] | [Registrar] | [ ] | |

**Post-handover action:** Client should rotate/change any shared passwords once access is confirmed.

---

## 3. Documentation Inventory

| Document | Location | Description |
|---|---|---|
| This handover pack | [Path / URL] | Ownership transfer record |
| SOW / Scope document | [Path / URL] | What was agreed |
| UAT sign-off | [Path / URL] | Acceptance record |
| Architecture diagram | [Path / URL] | System design |
| Runbook | [Path / URL] | How to operate and debug the system |
| API integration notes | [Path / URL] | Endpoints, auth, rate limits, gotchas |
| [Any other doc] | [Path / URL] | |

---

## 4. Operational Runbook Summary

_Key things the client needs to know to operate the system day-to-day. Full runbook at link above._

**How to restart / reset the system if it breaks:**
[Step-by-step instructions in plain language]

**How to check if the system is working:**
[Where to look, what to expect, what a healthy system looks like]

**What to do if an alert fires:**
[Who to contact, what to check first, what to log]

**Token / credential maintenance:**
[How often credentials expire, how to renew them, who does it]

**Known limitations / gotchas:**
- [e.g. OAuth token expires every 60 days — must be refreshed manually or via scheduled refresh flow]
- [e.g. Rate limit on [API]: 100 calls/minute — do not trigger bulk imports]
- [e.g. System does not handle [edge case] — must be handled manually]

---

## 5. Ownership Boundaries

**What the delivery team is responsible for after handover:**
[e.g. Nothing — this is a clean close. / Warranty period of X days for defects found against acceptance criteria.]

**What the client is responsible for after handover:**
- Day-to-day operation of the system
- Monitoring alert responses
- Credential rotation
- Any changes to scope or integrations
- Costs of third-party platforms (API usage, telephony, hosting)

**Excluded from delivery team responsibility:**
- Changes made by client to the system after handover
- Third-party platform outages or API changes
- Anything outside the accepted scope

---

## 6. Support After Go-Live

| Type | Covered? | Notes |
|---|---|---|
| Warranty defects (per SOW) | [Yes / No / Duration] | Defects against UAT-accepted criteria only |
| New features or changes | No | Requires new SOW / change request |
| General support questions | No | Runbook and documentation are the support |
| Emergency (P1 data loss) | [As agreed] | Contact: [email / phone] |

---

## 7. Handover Sign-Off

By signing below, the client confirms:
- [ ] All credentials and access transferred and verified
- [ ] Documentation received and accessible
- [ ] Runbook reviewed and understood
- [ ] Ownership boundaries agreed
- [ ] No outstanding P1 or P2 defects

| Party | Name | Role | Date | Signature |
|---|---|---|---|---|
| [YOUR_COMPANY] | [YOUR_NAME] | Delivery Lead | | |
| Client / Partner | | | | |

---

_Template version: 2026-03-03_
