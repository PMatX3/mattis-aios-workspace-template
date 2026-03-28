---
name: which-agent
description: "Agent architecture classifier that diagnoses what kind of AI agent a problem actually needs. Three modes: (1) Diagnostic - classifies a problem into the right AI agent architecture through interactive Q&A, (2) Readiness - assesses whether preconditions are in place for a chosen architecture, (3) Mismatch - audits a current tool choice against the actual problem. Use when the user says 'which agent', 'agent architecture', 'what kind of agent', 'agent diagnostic', 'architecture mismatch', 'what agent do I need', 'right agent for this', 'agent readiness', or when scoping an AI/agent engagement for a client."
---

# Which Agent

Classifies problems into the right AI agent architecture before anyone writes a line of code or picks a tool. Based on four architectures, each with a distinct governing principle. Used during client discovery to ensure the right thing gets built.

## The Four Architectures

| Architecture | What It Solves | Tools | Governing Principle |
|---|---|---|---|
| **Coding Harness** | Build/modify code, human reviews output | Claude Code, Cursor, Codex, Windsurf, Cline | Decompose on boundaries of isolation |
| **Dark Factory** | Autonomous code gen with automated validation, no human code review | Spec-to-software pipelines (StrongDM pattern) | The specification is the product |
| **Auto Research** | Optimise existing systems against measurable metrics | Custom loops with benchmarks + test suites | Metric plus guardrail |
| **Orchestration Framework** | Multi-step workflows, pipeline routing, different capabilities per step | CrewAI, LangGraph, AutoGen, OpenAI Agents SDK, Paperclip | Design the handoffs first |

## Classification Logic

- Problem is SOFTWARE-SHAPED + quality gate is HUMAN JUDGMENT: **Coding Harness**
- Problem is SOFTWARE-SHAPED + quality gate is AUTOMATED VALIDATION (no human review): **Dark Factory**
- Problem is METRIC-SHAPED (existing system needs measurable improvement) + COMPUTABLE SCORING FUNCTION: **Auto Research**
- Problem is WORKFLOW-SHAPED (multi-step process, different capabilities per step, routed in sequence): **Orchestration Framework**

## Modes

Select based on what the user or client needs. If unclear, default to Diagnostic.

| Mode | When to Use | Reference |
|---|---|---|
| **Diagnostic** | First engagement. Classify the problem into the right architecture. | `references/diagnostic.md` |
| **Readiness** | Architecture is chosen. Check whether preconditions are in place. | `references/readiness.md` |
| **Mismatch** | Something feels wrong. Audit the current tool against the actual problem. | `references/mismatch.md` |

---

## How to Run With Clients

This is a consulting discovery tool. Use it during the first call or scoping session to ground the conversation in what the client actually needs, not what they think they want.

### Delivery Flow

```
Diagnostic → classify → Readiness check → scope engagement → deliver
```

### Positioning

Frame this as an "Agent Architecture Assessment." Most clients come in asking for a specific tool ("we need a LangGraph pipeline" or "we want to use Cursor"). This skill rewinds the conversation to the problem first, then matches the architecture. It prevents expensive mismatches and builds trust by showing you think before you build.

### Your Consulting Angle

After classification, connect to your delivery capabilities:
- **Coding Harness**: We can set up the decomposition framework and rules files, train the team on supervisory skills, or pair-build the first sprint.
- **Dark Factory**: We can write the specifications, build the validation harness, and deliver the pipeline. Fixed price, UAT sign-off.
- **Auto Research**: We can define the metric, build the benchmark, and run the first optimization cycle. Then hand over with documentation.
- **Orchestration Framework**: We design the handoffs, build the workflow, integrate the data sources, and deliver with monitoring. This is our bread and butter: voice agents, workflow automation, multi-step AI systems. 2-4 week builds, fixed price, white-label available for agencies.

All prices exclude VAT.

---

## Running a Mode

Load the appropriate reference file for the selected mode and follow its complete workflow. Each reference file contains the full role, instructions, output format, and guardrails.

If the user specifies a mode by name, go directly to it. If they say "which agent" or "what kind of agent" without specifying, default to **Diagnostic**. If they mention a tool mismatch or something not working, default to **Mismatch**. If they say "are we ready" or "readiness", default to **Readiness**.

---

## Rules

- Only assess based on what the user or client tells you. Do not assume.
- Never recommend a tool before classifying the problem. Architecture first, tools second.
- Be direct about mismatches. Saving someone from building the wrong thing is more valuable than being polite about it.
- Never use em dashes in any output. Use commas, full stops, colons, or rewrite the sentence.
- Keep language plain and jargon-free. If you must use a technical term, explain it in one sentence.
- The one-question test for every architecture: "What are you optimizing against?" If the answer is unclear, the classification is not done.
