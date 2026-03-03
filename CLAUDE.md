# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What This Is

This is an **AIOS (AI Operating System) Workspace** — a structured environment designed for working with Claude Code as a powerful agent assistant across sessions. Start each new Claude Code session with `/prime` to load essential context without bloat.

**This file (CLAUDE.md) is the foundation.** It is automatically loaded at the start of every session. Keep it current — it is the single source of truth for how Claude should understand and operate within this workspace.

---

## The Claude-User Relationship

Claude operates as an **agent assistant** with access to the workspace folders, context files, commands, and outputs. The relationship is:

- **User**: Defines goals, provides context about their role/function, and directs work through commands
- **Claude**: Reads context, understands the user's objectives, executes commands, produces outputs, and maintains workspace consistency

Claude should always orient itself through `/prime` at session start, then act with full awareness of who the user is, what they're trying to achieve, and how this workspace supports that.

---

## Workspace Structure

```
.
├── CLAUDE.md              # This file — core context, always loaded
├── .claude/
│   └── commands/          # Slash commands Claude can execute
│       ├── prime.md       # /prime — session initialization
│       ├── create-plan.md  # /create-plan — create implementation plans
│       └── implement.md   # /implement — execute plans
├── context/               # Background context about you and your business
│   ├── business-info.md   # What the business does, who it serves, key offers
│   ├── personal-info.md   # Your role, responsibilities, how workspace helps
│   ├── strategy.md        # Current priorities, execution plan reference, operating cadence
│   ├── current-data.md    # Weekly scorecard + key metrics
│   ├── decision-policy.md # Guardrails, hard no rules, build standards
│   └── import/            # Drop files here for Claude to ingest (ChatGPT exports, docs)
├── plans/                 # Implementation plans (dated, created by /create-plan)
├── outputs/
│   └── project-register.md  # Active deliveries + pipeline + capacity view
├── reference/
│   ├── scorecard-metrics.md # KPI definitions, formulas, targets, sources
│   ├── shell-aliases.md     # cs / cr shell alias setup
│   └── templates/           # Delivery templates (use for every engagement)
│       ├── audit-checklist.md
│       ├── sow-scope-acceptance.md
│       ├── uat-plan.md
│       ├── go-live-runbook.md
│       ├── handover-pack.md
│       └── change-request.md
├── artifacts/             # Project-specific artifacts (UAT checklists, etc.)
├── module-installs/       # AIOS module installers
└── scripts/               # Automation scripts
```

**Key directories:**

| Directory    | Purpose                                                                             |
| ------------ | ----------------------------------------------------------------------------------- |
| `context/`   | Who you are, business overview, strategy, live scorecard. Read by `/prime`.        |
| `context/import/` | Drop zone for raw docs — Claude reads and incorporates into context files.   |
| `plans/`     | Dated implementation plans. Created by `/create-plan`, executed by `/implement`.   |
| `outputs/`   | Deliverables. Key file: `project-register.md` — update weekly.                    |
| `reference/` | Scorecard definitions, shell setup, and 6 delivery templates.                      |
| `artifacts/` | Project-specific outputs (UAT packs, runbooks for specific clients).               |
| `scripts/`   | Automation tooling.                                                                 |

---

## How to Run the Business Weekly

Every Monday (~90 min):

1. Open `outputs/project-register.md` — update project status, risks, next milestone
2. Open `reference/scorecard-metrics.md` — fill this week's row in the scorecard log
3. Check WIP count against your limit
4. Draft or publish content for your primary acquisition channel
5. Send targeted outreach to ICP
6. Unblock team in your project management tool

---

## Commands

### /prime

**Purpose:** Initialize a new session with full context awareness.

Run this at the start of every session. Claude will:

1. Read CLAUDE.md and context files
2. Summarize understanding of the user, workspace, and goals
3. Confirm readiness to assist

### /create-plan [request]

**Purpose:** Create a detailed implementation plan before making changes.

Use when adding new functionality, commands, scripts, or making structural changes. Produces a thorough plan document in `plans/` that captures context, rationale, and step-by-step tasks.

Example: `/create-plan add a competitor analysis command`

### /implement [plan-path]

**Purpose:** Execute a plan created by /create-plan.

Reads the plan, executes each step in order, validates the work, and updates the plan status.

Example: `/implement plans/2026-01-28-competitor-analysis-command.md`

---

## Running Claude Agents on Issues

This workspace uses a label convention to enable autonomous Claude Code agents to pick up and execute GitHub issues.

### Label Convention

| Label | Meaning |
|---|---|
| `agent-ready` | Issue is fully specified; Claude agent can work it autonomously |
| `agent-in-progress` | Agent is actively working this |
| `needs-spec` | Issue needs more detail before an agent can work it |
| `human-review` | Work done; needs human sign-off |

### Workflow

1. Write issue using the `agent-task` template → add `agent-ready` label
2. In a worktree terminal: `claude` → paste issue URL → agent reads and executes
3. Agent opens PR → adds `human-review` label
4. Human reviews and merges

### What Makes an Issue Agent-Ready

An agent-ready issue must contain:
- **Context** — why this exists, what it connects to
- **Task** — precise description of what must be done
- **Acceptance criteria** — testable, unambiguous checklist
- **Files likely affected** — paths to relevant files
- **Out of scope** — explicit boundaries
- **Verification steps** — how to confirm it's done

Use the `.github/ISSUE_TEMPLATE/agent-task.md` template for every agent issue.

---

## Critical Instruction: Maintain This File

**Whenever Claude makes changes to the workspace, Claude MUST consider whether CLAUDE.md needs updating.**

After any change — adding commands, scripts, workflows, or modifying structure — ask:

1. Does this change add new functionality users need to know about?
2. Does it modify the workspace structure documented above?
3. Should a new command be listed?
4. Does context/ need new files to capture this?

If yes to any, update the relevant sections. This file must always reflect the current state of the workspace so future sessions have accurate context.

**Examples of changes requiring CLAUDE.md updates:**

- Adding a new slash command → add to Commands section
- Creating a new output type → document in Workspace Structure or create a section
- Adding a script → document its purpose and usage
- Changing workflow patterns → update relevant documentation

---

## For Users Downloading This Template

To customize this workspace to your own needs:

1. Run `bash scripts/setup.sh` to create worktrees and install shell aliases
2. Fill in your context documents in `context/` (or run the ContextOS module installer)
3. Update this CLAUDE.md to reflect your business
4. Run `cs` (or `claude "/prime"`) to start your first session

Then use `/create-plan` to plan and `/implement` to execute any structural changes. This ensures everything stays in sync — especially CLAUDE.md, which must always reflect the current state of the workspace.

---

## Session Workflow

1. **Start**: Run `/prime` to load context
2. **Work**: Use commands or direct Claude with tasks
3. **Plan changes**: Use `/create-plan` before significant additions
4. **Execute**: Use `/implement` to execute plans
5. **Maintain**: Claude updates CLAUDE.md and context/ as the workspace evolves

---

## Notes

- Keep context minimal but sufficient — avoid bloat
- Plans live in `plans/` with dated filenames for history
- Outputs are organized by type/purpose in `outputs/`
- Reference materials go in `reference/` for reuse
