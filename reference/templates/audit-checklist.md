# 7-Day Audit — Checklist Template

**Project:** [Name]
**Client / Partner:** [Name]
**Audit Start:** [Date]
**Audit End:** [Date]
**Auditor:** [YOUR_NAME]
**Price:** [YOUR_PRICE]

---

## Purpose

A 7-day structured review of an existing or in-flight AI/automation project. Outputs a written Audit Report with findings, risks, and a recommended scope for Delivery Rescue (if needed).

---

## Required Inputs (collect before starting)

- [ ] Access to existing system / workflow (credentials, API keys, environment details)
- [ ] Existing documentation (PRDs, specs, architecture diagrams, if any)
- [ ] Accountable stakeholder named and available for 2 x 30-min calls
- [ ] Clear statement of what the system is supposed to do
- [ ] Current error logs or failure reports (if available)
- [ ] Details of any integrations (APIs, webhooks, third-party tools)

---

## Day-by-Day Checklist

### Day 1 — Kick-off & Access

- [ ] Kick-off call with client stakeholder (30 min)
- [ ] Access confirmed for all systems
- [ ] Existing docs reviewed
- [ ] Initial understanding documented (what it does, what's broken, what's at risk)

### Day 2–3 — Technical Review

- [ ] Integration points mapped (APIs, auth flows, webhooks, data sources)
- [ ] Error handling reviewed: retries, idempotency, failure modes
- [ ] Auth and secret management reviewed: token expiry, OAuth scopes, credential storage
- [ ] Rate limits and API quotas identified
- [ ] Monitoring/alerting assessed: what fails silently? what's visible?
- [ ] Data flow traced end-to-end at least once

### Day 4 — Operations Review

- [ ] Deployment process reviewed (how does it get to prod? is it documented?)
- [ ] Rollback capability assessed
- [ ] Runbook existence checked (does one exist? is it accurate?)
- [ ] Support and escalation path reviewed (who owns it post go-live?)
- [ ] Logging quality reviewed (enough to debug a failure without the original dev?)

### Day 5 — Risk Assessment

- [ ] Top 5 risks documented with likelihood and impact
- [ ] Known bugs or defect classes identified
- [ ] Scope ambiguities or missing acceptance criteria noted
- [ ] Compliance or data handling concerns flagged (GDPR, access controls, data residency)

### Day 6 — Findings Draft

- [ ] Audit Report drafted (findings, risks, recommendations)
- [ ] Recommended scope for Delivery Rescue defined (if applicable)
- [ ] Effort and price estimate prepared

### Day 7 — Delivery & Close

- [ ] Findings call with client stakeholder (45 min)
- [ ] Audit Report delivered in writing
- [ ] Delivery Rescue proposal presented (if applicable)
- [ ] Next steps agreed and documented

---

## Audit Report Sections

The final deliverable must include:

1. **Summary** — What we reviewed, when, who was involved
2. **System Overview** — What it does, architecture, key integrations
3. **Findings** — Categorised by severity (Critical / High / Medium / Low)
4. **Top Risks** — What could fail in production and why
5. **Gaps** — Missing documentation, monitoring, error handling, acceptance criteria
6. **Recommendation** — Go / No-Go / Conditional. If Delivery Rescue recommended, why and scope summary.
7. **Proposed Next Steps** — Delivery Rescue scope and price (if applicable)

---

## Acceptance Criteria (for the audit itself)

- [ ] All required inputs were received before Day 2
- [ ] Kick-off and findings calls completed
- [ ] Audit Report delivered in writing by Day 7
- [ ] Client acknowledged receipt of report

---

_Template version: 2026-03-03_
_See `reference/templates/sow-scope-acceptance.md` for the next step if Delivery Rescue is agreed._
