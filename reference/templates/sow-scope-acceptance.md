# Statement of Work — Scope & Acceptance Criteria Template

**Project:** [Name]
**Client / Partner:** [Name]
**Date:** [Date]
**Version:** 1.0
**Author:** [YOUR_NAME] / [YOUR_COMPANY]

---

## 1. Engagement Overview

**What this engagement delivers:**
[One paragraph. What problem are we solving? What is the system or workflow? What does "done" look like at a high level?]

**Start date:** [Date]
**Target UAT sign-off date:** [Date]
**Target go-live date:** [Date]
**Price:** [YOUR_CURRENCY][Amount]
**Payment terms:** [e.g. 60% on start, 40% on UAT sign-off]

---

## 2. In Scope

_Everything listed here is included in the fixed price. Be explicit._

| # | Deliverable | Description |
|---|---|---|
| 1 | [e.g. Voice agent build] | [What it does, what integrations it uses, what platforms] |
| 2 | [e.g. Monitoring & alerts] | [What is monitored, what triggers an alert, where alerts go] |
| 3 | [e.g. UAT support] | [Number of UAT cycles, what we test, who signs off] |
| 4 | [e.g. Runbook] | [What the runbook covers, format] |
| 5 | [e.g. Handover pack] | [What's included in handover] |

---

## 3. Out of Scope

_Anything not listed above is out of scope. Document the most likely misunderstandings explicitly._

- [e.g. Ongoing support or maintenance after go-live handover]
- [e.g. Changes to integrations not listed above]
- [e.g. Training sessions beyond the handover call]
- [e.g. Data migration]
- [e.g. Any work requiring access or credentials not provided]

---

## 4. Acceptance Criteria

_Every deliverable must have a measurable, testable acceptance criterion. "Looks good" is not an acceptance criterion._

| Deliverable | Acceptance Criterion | Test Method |
|---|---|---|
| [e.g. Voice agent] | [e.g. Completes 10 test calls end-to-end with < 2s latency and correct routing in all defined scenarios] | UAT test cases (see UAT plan) |
| [e.g. Error handling] | [e.g. All API failures retry 3x with exponential backoff; failed calls logged with full context] | Failure injection test |
| [e.g. Monitoring] | [e.g. Alert fires within 5 minutes of production failure and delivers to defined Slack channel] | Alert trigger test |
| [e.g. Runbook] | [e.g. A team member unfamiliar with the system can follow the runbook to diagnose and resolve a P1 incident] | Runbook review |
| [e.g. Handover] | [e.g. Client confirms all credentials received and handover pack signed off] | Sign-off form |

---

## 5. Assumptions

_Things we are assuming to be true. If any assumption is wrong, scope or price may change._

- [ ] [e.g. Client provides all API credentials and access within 2 business days of start]
- [ ] [e.g. Client has an accountable stakeholder available for UAT within the agreed window]
- [ ] [e.g. Third-party APIs behave as documented and within defined rate limits]
- [ ] [e.g. No significant changes to third-party platforms during delivery]

---

## 6. Dependencies

_External things we need in order to deliver._

| Dependency | Owner | Required By |
|---|---|---|
| [e.g. API credentials] | Client | [Date] |
| [e.g. Test environment access] | Client | [Date] |
| [e.g. Stakeholder availability for UAT] | Client | [Date] |

---

## 7. Change Control

Any request that changes scope, timeline, or price triggers a formal change request:

1. Change is documented in writing (use `reference/templates/change-request.md`)
2. Impact on cost, timeline, and risk is assessed and communicated
3. Client signs off in writing before work begins
4. No silent scope creep. If it's not in this document, it's a change.

---

## 8. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [e.g. Token expiry mid-delivery] | Medium | High | OAuth refresh flow built as default; token monitoring in runbook |
| [e.g. API changes mid-build] | Low | High | Version-pin where possible; change control if API change required |

---

## 9. Sign-Off

By proceeding past this point, both parties confirm agreement to the scope, acceptance criteria, and out-of-scope list above.

| Party | Name | Date |
|---|---|---|
| [YOUR_COMPANY] | [YOUR_NAME] | |
| Client / Partner | | |

---

_Template version: 2026-03-03_
_Next: `reference/templates/uat-plan.md`_
