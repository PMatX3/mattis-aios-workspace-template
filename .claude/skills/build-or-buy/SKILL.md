---
name: build-or-buy
description: "Agent deployment decision framework based on the 4:1 Ratio: four engineering problems, one specification problem. Four modes: (1) Diagnostic - interactive assessment scoring codebase readiness, org readiness, and domain complexity to route build vs buy decisions, (2) Readiness - codebase agent-readiness audit across eight pillars with fix plan, (3) Decompose - tear apart a consulting proposal into commodity engineering vs domain expertise, (4) Map - personal 4:1 map for engineers and small team leads. Use when the user says 'build or buy', 'build-or-buy', 'should we build this', 'do we build it ourselves', 'agent readiness', 'codebase readiness', 'proposal decompose', 'consulting proposal', '4:1 ratio', or when evaluating whether to hire consultants for AI/agent deployment."
---

# Build or Buy

Decides whether a business should build AI agent capabilities in-house or buy outside help, and if buying, exactly what to buy. Based on the 4:1 Ratio: five hard problems in agent deployment, four are standard engineering, one genuinely needs domain expertise.

## The 4:1 Ratio

Five hard problems in agent deployment. Four are engineering. One is not.

| # | Problem | Type | Description |
|---|---------|------|-------------|
| 1 | **Context Compression** | ENGINEERING | Long-running agent sessions filling context windows. Published patterns exist. |
| 2 | **Codebase Instrumentation** | ENGINEERING | Pre-commit hooks, documented builds, env vars, dev containers, AGENTS.md. Days not months. |
| 3 | **Linting as Architecture** | ENGINEERING | Lint rules as executable specification agents use to self-correct. Compound returns. |
| 4 | **Multi-Agent Coordination** | ENGINEERING | Orchestrating multiple agents. Do not over-architect before measuring. |
| 5 | **The Specification Problem** | DOMAIN EXPERTISE | Defining what a probabilistic system should do in regulated domains (HIPAA, SOX, insurance, legal). The ONE genuinely hard problem. |

**The insight:** Most consulting firms bundle all five together and charge domain-expertise rates for commodity engineering. The 4:1 Ratio helps clients see what they can own and what they actually need help with.

## Three Scoring Dimensions

| Dimension | High | Medium | Low |
|-----------|------|--------|-----|
| **Codebase Readiness** | New person can clone the repo and ship a fix without asking a human | Some docs, some tests, but gaps exist | Tribal knowledge, no tests, "it works on my machine" |
| **Organizational Readiness** | VP-level AI ownership, constructive security team, data governance, prior tech change experience | Some sponsorship, some governance, but not battle-tested | No clear owner, security says no to everything, no data governance |
| **Domain Complexity** | External, jurisdiction-specific, constantly changing rules with severe consequences | Some regulation, manageable with standard compliance | Internal rules only, low consequence for errors |

## Routing Logic

| Codebase | Org | Domain | Decision |
|----------|-----|--------|----------|
| High | High | Low | BUILD IT YOURSELF |
| High | Low | Any | BUY ORG-LAYER HELP ONLY |
| Low | Any | Any | FIX THE CODEBASE FIRST |
| Any | Any | High | BUY DOMAIN EXPERTISE for the specification layer |
| Medium | Medium | Low | Targeted actions for specific gaps |

## Modes

Select based on what the user or client needs. If unclear, default to Diagnostic.

| Mode | When to Use | Reference |
|---|---|---|
| **Diagnostic** | First engagement. Score readiness, route the decision, map the five problems. | `references/diagnostic.md` |
| **Readiness** | Codebase needs auditing. Eight-pillar agent-readiness assessment with fix plan. | `references/readiness.md` |
| **Decompose** | Client has a consulting proposal. Categorise every deliverable and find the overcharges. | `references/decompose.md` |
| **Map** | Individual engineer or small team lead. Personal 4:1 map for their role and stack. | `references/map.md` |

---

## How to Run With Clients

This is a consulting sales and advisory tool. Use it during discovery, scoping, or when a prospect is evaluating a competing proposal.

### Delivery Flow

```
Diagnostic → route decision → Readiness (if codebase gaps) → scope engagement → deliver
                           → Decompose (if evaluating a proposal) → counter-proposal
                           → Map (if helping an individual) → action plan
```

### Positioning

Frame this as a "Build or Buy Assessment." Most prospects come in either (a) thinking they need to hire a big consulting firm, or (b) thinking they can do everything themselves. This skill grounds the conversation in what is actually hard about their situation and what is not. It builds trust by being honest about what they can own.

### Your Consulting Angle

After assessment, position your consultancy as the engineering layer:

- **Engineering problems (1-4):** "Your team does not have engineers. We are that engineering layer. Fixed price, 2-4 weeks, UAT sign-off, monthly support."
- **Domain expertise (problem 5):** "That is not us. Here is what you need and how to evaluate who provides it."
- **Proposal decomposition:** "This is engineering work being sold at consulting rates. We deliver this at fixed price, not open-ended hourly."
- **Agency partners:** "We white-label. Your client sees your brand. We do the build."

All prices exclude VAT.

---

## Running a Mode

Load the appropriate reference file for the selected mode and follow its complete workflow. Each reference file contains the full role, instructions, output format, and guardrails.

If the user specifies a mode by name, go directly to it. If they say "build or buy" or "should we build this" without specifying, default to **Diagnostic**. If they mention a consulting proposal or SOW, default to **Decompose**. If they say "codebase readiness" or "agent readiness", default to **Readiness**. If they say "4:1 map" or ask about their personal situation, default to **Map**.

---

## Rules

- Only assess based on what the user or client tells you. Do not assume.
- Be honest about what is engineering and what is genuinely hard. The whole point is cutting through bundled consulting.
- Never use em dashes in any output. Use commas, full stops, colons, or rewrite the sentence.
- Keep language plain and jargon-free. If you must use a technical term, explain it in one sentence.
- All prices exclude VAT. State this explicitly in any pricing output.
- When your consultancy can help, say so directly. When it cannot help, say that too.
