# UAT Plan Template

**Project:** [Name]
**Client / Partner:** [Name]
**UAT Window:** [Start date] – [End date]
**UAT Lead (Delivery):** [YOUR_NAME]
**UAT Lead (Client):** [Name, role]
**Version:** 1.0

---

## Purpose

This plan defines what will be tested, how it will be tested, who signs off, and what "pass" means. UAT is the final gate before go-live. Nothing goes live without a signed UAT sign-off.

---

## UAT Environment

| Item | Details |
|---|---|
| Environment URL / endpoint | [URL or access method] |
| Credentials / access method | [How testers log in or trigger the system] |
| Test data available | [Yes / No — describe if yes] |
| Reset / teardown process | [How to clear test state between runs] |

---

## Test Cases

_Each acceptance criterion from the SOW maps to at least one test case here._

### Module / Feature: [e.g. Voice Agent — Inbound Call Handling]

| TC# | Test Case | Steps | Expected Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| TC-01 | Happy path — call answered and routed correctly | 1. Call test number 2. Say "[phrase]" | Agent responds within 2s, routes to correct flow | | |
| TC-02 | Unrecognised input — graceful fallback | 1. Call test number 2. Say random phrase | Agent acknowledges, offers transfer or retry | | |
| TC-03 | API failure — retry behaviour | 1. Simulate API timeout 2. Trigger call | Agent retries 3x; logs failure; does not crash | | |
| TC-04 | Edge case — [describe] | [Steps] | [Expected result] | | |

### Module / Feature: [e.g. Error Handling & Monitoring]

| TC# | Test Case | Steps | Expected Result | Pass/Fail | Notes |
|---|---|---|---|---|---|
| TC-05 | Alert fires on failure | 1. Trigger production failure 2. Wait 5 min | Alert received in Slack / email | | |
| TC-06 | Retry with backoff | 1. Introduce transient API error | System retries with 1s / 2s / 4s backoff, then logs | | |

### Module / Feature: [Add more as needed]

---

## Defect Handling

| Severity | Definition | SLA for Fix | Example |
|---|---|---|---|
| **P1 — Blocker** | System unusable; core flow broken; data loss | Fix before sign-off | Call agent crashes on first call |
| **P2 — Critical** | Core flow degraded; workaround possible | Fix before sign-off | Incorrect routing in 1 of 5 scenarios |
| **P3 — Minor** | Non-core; cosmetic; edge case | Fix or accept risk in writing | Log message formatting |

**Process:**
1. Defect found → logged with steps to reproduce, severity, and screenshot/log
2. Assigned to delivery team
3. Fix verified by UAT lead before re-testing
4. P1 / P2 defects must be resolved before sign-off. No exceptions.

---

## UAT Schedule

| Day | Activity | Owner |
|---|---|---|
| Day 1 | Environment confirmed; test data ready; TC-01 to TC-05 executed | Delivery team |
| Day 2 | Client executes assigned test cases; defects logged | Client |
| Day 3 | Defect fixes deployed; re-test of failed cases | Delivery team |
| Day 4 | Final pass on all test cases; sign-off decision | Both |

---

## Exit Criteria

UAT is complete and sign-off can proceed when:

- [ ] All P1 and P2 defects resolved and re-tested
- [ ] All test cases have a Pass or Accepted-Risk result
- [ ] Runbook reviewed and confirmed accurate
- [ ] Client UAT lead confirms in writing

---

## UAT Sign-Off

By signing off, the client confirms:
- The system meets the acceptance criteria defined in the SOW
- Outstanding items are documented and accepted as-is or addressed in a change request
- The project may proceed to go-live

| Party | Name | Date | Signature |
|---|---|---|---|
| [YOUR_COMPANY] | [YOUR_NAME] | | |
| Client / Partner | | | |

---

## Outstanding Items at Sign-Off (if any)

| Item | Severity | Resolution Plan | Owner |
|---|---|---|---|
| [Any known issue accepted at sign-off] | P3 | [What happens to it] | |

---

_Template version: 2026-03-03_
_Next: `reference/templates/go-live-runbook.md`_
