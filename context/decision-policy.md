## Decision Policy

### Default priorities (in order)

1. Protect delivery reputation over revenue. If a project risks public failure, de-scope, delay, or decline.
2. Ship production, not demos. If it can't be monitored, retried, supported, and handed over cleanly, it is not "done".
3. Fixed scope and clear acceptance criteria. No ambiguous outcomes without measurable gates.
4. Reduce operational load. Prefer solutions that minimise ongoing support, manual steps, and custom one-offs.
5. Focus beats optionality. Fewer active bets, fewer active clients, higher quality delivery.

### Hard "no" rules (automatic decline)

* Unbounded scope or "we'll figure it out as we go" with no discovery phase or change control.
* Anything that depends on unreliable automation from unstructured data as the core value (unless explicitly includes a human review step).
* Clients who won't provide required access, data, or an accountable stakeholder, but still expect deadlines.
* Projects where success requires capabilities the team cannot credibly deliver in the timeframe and the client won't fund it.
* "Build my whole business app" requests from non-technical founders with no product owner, no process discipline, and no budget for iteration.
* Any engagement where you can't define support boundaries and ownership post go-live.

### Mandatory engagement structure (non-negotiable)

* Discovery/audit first when scope risk is high (integration-heavy, compliance-heavy, unclear requirements).
* Written scope, assumptions, acceptance criteria, and out-of-scope list before build starts.
* UAT plan with sign-off gates. No "looks good to me" launches.
* Go-live runbook: rollout steps, rollback plan, monitoring/alerts, escalation path.
* Handover pack: docs, credentials/access checklist, ownership boundaries, and maintenance plan.

### Scoping and change control

* Every deliverable maps to a testable acceptance criterion.
* Any change that affects scope, timeline, or risk triggers a written change request with cost and schedule impact.
* If client priorities change midstream, re-baseline. No silent scope creep.

### Build standards (definition of production-ready)

A system is production-ready only if it has:

* Error handling and retries (with idempotency where relevant)
* Monitoring and alerts (so failures are visible before the client complains)
* Logging suitable for debugging (not just "something broke")
* Secure secret management and least-privilege access
* Clear data ownership and backup/restore considerations where applicable
* A documented operational runbook

### Resource allocation rules

* Cap concurrent delivery commitments to protect quality.
* Avoid building custom systems twice. If a pattern repeats, it becomes a reusable template or module.
* Prefer proven components over novelty unless the novelty is the product.

### Product vs services rule

* Services pays now, product pays later. Product work only happens if:

  * It directly reduces delivery cost or increases delivery throughput, or
  * There is clear evidence of repeated demand with willingness to pay, and
  * It has a narrow v1 that can ship fast without dragging services down.

### Communication rules

* Under-promise, over-deliver. No bluffing about automation reliability.
* Risks are surfaced early, in writing, with options and tradeoffs.
* Meetings exist to unblock decisions, not to think out loud. Decisions get documented.

### Escalation triggers (when to personally intervene)

* Any integration instability (OAuth scope issues, token expiry, API drift, rate limiting) that threatens go-live
* Rework loops: the same defect class appears twice
* Unclear acceptance criteria or stakeholder disagreement
* Timeline slip risk greater than one week
* Anything that could create a client trust breach (data handling, security, silent failures)

### Success criteria for the business (operating truth)

* A month is "good" if you collected cash and shipped cleanly with low rework.
* A month is "bad" if you sold work you can't deliver, even if revenue looks good.

---

_Customise this file to match your own operating principles. The framework above is a production-tested starting point — adapt the specifics to your business model, client base, and risk tolerance._
