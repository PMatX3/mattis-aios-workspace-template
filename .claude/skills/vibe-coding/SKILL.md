---
name: vibe-coding
description: "Vibe Coding toolkit for non-technical builders shipping with AI agents. Six modes: (1) Start Coding - initialize a disciplined coding session with guardrails, (2) Wall Diagnostic - assess gaps across 5 supervisory skills, (3) Rules File Builder - generate a customized rules file, (4) Task Decomposer - break big changes into small safe steps, (5) Security Audit - check for vulnerabilities and missing error handling, (6) Engineer Briefing - create a handoff doc for hiring engineering help. Use when the user says 'start coding', 'write code', 'vibe coding', 'wall diagnostic', 'rules file', 'task decomposer', 'security audit', 'engineer briefing', 'check my project', or wants to help a client who vibe-codes with AI agents."
---

# Vibe Coding Wall

Operational toolkit for builders shipping software with AI coding agents. Based on the five supervisory skills every non-technical builder needs: version control, context management, rules files, blast radius discipline, and production readiness.

## Modes

Select based on what the user or client needs. If unclear, start with the Wall Diagnostic.

| Mode | When to Use | Reference |
|---|---|---|
| **Start Coding** | Beginning a coding session. Sets guardrails, checks for rules file, enforces discipline throughout. | `references/start-coding.md` |
| **Wall Diagnostic** | First engagement, or periodic check-in. Scores the builder across 5 dimensions. | `references/wall-diagnostic.md` |
| **Rules File Builder** | Builder has no rules file, or current one is not working. | `references/rules-file-builder.md` |
| **Task Decomposer** | Before any big change. Breaks it into small safe steps. | `references/task-decomposer.md` |
| **Security Audit** | App has real users, handles data, or is about to launch. | `references/security-audit.md` |
| **Engineer Briefing** | Builder is ready to hire engineering help. | `references/engineer-briefing.md` |

---

## How to Run With Clients

This is a consulting delivery tool. When running with a client:

1. **Start with the Wall Diagnostic** to understand where they are
2. Based on scores, recommend the next mode (usually Rules File Builder or Task Decomposer)
3. If they handle customer data, run the Security Audit before anything else
4. If scores are low across the board and the project is revenue-critical, recommend the Engineer Briefing

### Delivery Flow

```
Wall Diagnostic → identify gaps → deliver relevant mode(s) → follow-up
```

### Positioning

Frame this as an "AI Development Health Check" for clients. The diagnostic gives you a natural opening to offer ongoing advisory (monthly retainer) or a one-off hardening engagement.

---

## Running a Mode

Load the appropriate reference file for the selected mode and follow its complete workflow. Each reference file contains the full role, instructions, output format, and guardrails.

If the user asks for a specific mode by name, go directly to it. If they say "start coding", "write code", or "let's code", default to **Start Coding**. If they say "vibe coding" or "check my project" without specifying, default to the Wall Diagnostic.

---

## Rules

- Only assess based on what the user/client tells you. Do not assume.
- Never recommend "learn to code" as a solution. The framing is supervisory skills, not engineering skills.
- Be honest about risks but never condescending. These builders shipped something real.
- Keep voice-friendly: short sentences, no long bullet lists, plain English.
- If a situation requires a professional engineer immediately (compliance, data breach, payment processing issues), say so directly.
