---
name: scope-check
description: Analyse a client message or email against a Statement of Work (SOW) or contract to determine if the request is in scope, out of scope, or a grey area. Produces a clear verdict with SOW clause references and a ready-to-send professional response. Use when the user pastes a client message and wants to know if it is covered by their SOW, contract, or project agreement. Triggers on phrases like "is this in scope", "check this against the SOW", "scope check", "is this covered", "client is asking for X", or when a client message is shared alongside a SOW or contract file.
---

# Scope Check

Protect margin and manage scope creep by analysing a client request against the signed SOW or contract. Produces a verdict, reasoning with direct SOW quotes, and a draft client response - in one step.

## Inputs

Collect before proceeding:

1. **Client message** - the email, Slack message, or request to analyse. If not provided, ask the user to paste it.
2. **SOW or contract file** - path to the signed agreement. If not provided, search the current directory for files named `sow`, `statement-of-work`, `contract`, or `agreement` (any extension). If multiple found, ask the user which one applies. If none found, ask the user to provide the file path or paste the relevant SOW text.

## Workflow

### Step 1 - Read the SOW

Read the full SOW or contract. Focus on:
- In-scope deliverables (usually "In Scope", "Deliverables", or "Services" section)
- Out-of-scope exclusions
- Change control clause
- Assumptions and constraints that affect scope

### Step 2 - Analyse the request

Compare the client request against the SOW. See `references/scope-analysis.md` for classification patterns and edge cases.

Classify as one of:

- **IN SCOPE** - Clearly covered by a named deliverable or described activity
- **OUT OF SCOPE** - Falls outside SOW deliverables, or explicitly excluded
- **GREY AREA** - The SOW is ambiguous; could reasonably be read either way

### Step 3 - Produce the output

Output three clearly labelled sections:

---

**VERDICT: [IN SCOPE / OUT OF SCOPE / GREY AREA]**

**Reasoning:**
[Reference the specific SOW clause or deliverable. Quote the relevant SOW language directly. If Grey Area, explain both interpretations and what makes it ambiguous.]

**Draft response to client:**
[Professional, direct reply. Tone: clear and commercial, not apologetic. If out of scope or grey area, reference the change control process by name if it exists in the SOW.]

---

## Rules

- Always quote the SOW directly - verdicts without evidence are opinions, not analysis
- Never soften an out-of-scope verdict to avoid conflict; be clear and professional
- Grey Area verdicts must name what is ambiguous and recommend how to resolve it
- Draft responses protect the relationship while protecting the scope
- If no SOW is found and the user cannot provide one, state clearly that you cannot assess scope without the signed agreement
