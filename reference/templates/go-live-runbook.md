# Go-Live Runbook Template

**Project:** [Name]
**Client / Partner:** [Name]
**Go-Live Date:** [Date]
**Go-Live Lead:** [YOUR_NAME]
**Client Contact on Go-Live Day:** [Name, phone/Slack]
**Version:** 1.0

---

## Purpose

This runbook covers the go-live sequence, rollback plan, monitoring checks, and escalation path. It must be readable by someone unfamiliar with the project. No tribal knowledge allowed.

---

## Pre-Go-Live Checklist

Complete all items before initiating go-live.

### Technical Readiness

- [ ] UAT sign-off received (written confirmation)
- [ ] All P1 and P2 defects resolved
- [ ] Production environment provisioned and verified
- [ ] All API credentials and secrets loaded into production (not dev/test values)
- [ ] OAuth tokens valid and refresh flows tested in production
- [ ] Rate limits confirmed with production API keys
- [ ] Monitoring and alerting configured and tested (alert fired successfully in test)
- [ ] Logging configured: errors, warnings, and key events captured
- [ ] Rollback procedure tested (can we revert if needed?)

### Operational Readiness

- [ ] Runbook reviewed with client stakeholder
- [ ] Support contact and escalation path agreed
- [ ] Client knows how to report an incident
- [ ] Data backup confirmed (if applicable)
- [ ] DNS / endpoint changes prepared (if applicable, deployed only at go-live)

---

## Go-Live Sequence

_Follow in order. Do not skip steps. Mark each complete._

| Step | Action | Owner | Done? |
|---|---|---|---|
| 1 | Confirm go-live window agreed with client | Delivery lead | [ ] |
| 2 | Final backup / snapshot taken (if applicable) | Delivery lead | [ ] |
| 3 | [e.g. Deploy production config / activate workflow] | Delivery lead | [ ] |
| 4 | [e.g. Point DNS / webhook to production endpoint] | Delivery lead | [ ] |
| 5 | [e.g. Run smoke test: trigger one live call/event] | Delivery lead | [ ] |
| 6 | Monitor for 15 minutes: no errors, alerts quiet | Delivery lead | [ ] |
| 7 | Client executes a real transaction or call | Client | [ ] |
| 8 | Confirm result is correct end-to-end | Both | [ ] |
| 9 | Declare go-live successful; notify client in writing | Delivery lead | [ ] |
| 10 | Monitor for first 2 hours; available for escalation | Delivery lead | [ ] |

---

## Rollback Plan

**Trigger for rollback:**
Any P1 issue discovered within the first 2 hours of go-live that cannot be resolved immediately.

**Rollback steps:**

| Step | Action | Owner | Time estimate |
|---|---|---|---|
| 1 | Notify client immediately (call, not Slack) | Delivery lead | 2 min |
| 2 | [e.g. Revert webhook / DNS to previous endpoint] | Delivery lead | 5 min |
| 3 | [e.g. Disable production workflow; re-enable staging] | Delivery lead | 5 min |
| 4 | Confirm old system is operational | Delivery lead + Client | 10 min |
| 5 | Log incident: what failed, when, what was done | Delivery lead | 15 min |
| 6 | Schedule post-mortem and revised go-live date | Delivery lead | [Date TBD] |

**Rollback decision authority:** [YOUR_NAME] (no committee required for P1)

---

## Monitoring & Alerting

| What | Tool / Location | Alert Goes To | Check Frequency |
|---|---|---|---|
| [e.g. API error rate] | [e.g. CloudWatch / n8n error log] | [e.g. Slack #alerts] | Continuous |
| [e.g. Failed calls] | [e.g. VAPI dashboard] | [e.g. Email + Slack] | Continuous |
| [e.g. Token expiry] | [e.g. OAuth monitor] | [e.g. Slack #alerts] | Daily |
| [e.g. Workflow execution] | [e.g. Make/n8n run log] | [e.g. Slack #alerts] | Per run |

**Post go-live monitoring window:**
- First 2 hours: active monitoring, on-call
- First 48 hours: daily check
- First 2 weeks: weekly check (unless incident)

---

## Escalation Path

| Severity | Trigger | Contact | How |
|---|---|---|---|
| P1 | System down / data loss / core flow broken | [YOUR_NAME] | Call: [number] |
| P1 (client-side) | Client notices failure before we do | [Client contact] | Call delivery lead immediately |
| P2 | Degraded function, workaround available | [YOUR_NAME] | Slack or email within 2 hours |
| P3 | Minor issue, no business impact | [YOUR_NAME] | Log; address in next review |

---

## Key Contacts

| Role | Name | Contact |
|---|---|---|
| Delivery lead | [YOUR_NAME] | [email / phone] |
| Client stakeholder | [Name] | [email / phone] |
| [Third-party / API vendor] | [Name] | [Support URL / email] |

---

## Post-Go-Live Notes

_Fill in after go-live:_

- **Go-live time:** [Time]
- **Issues encountered:** [None / describe]
- **Rollback triggered:** [Yes / No]
- **First incident (if any):** [Description]
- **Sign-off confirmed by client:** [Yes / No / Date]

---

_Template version: 2026-03-03_
_Next: `reference/templates/handover-pack.md`_
