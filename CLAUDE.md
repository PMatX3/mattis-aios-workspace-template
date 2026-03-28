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
├── HISTORY.md             # Workspace changelog — updated every session by /commit
├── DESIGN.md              # Design system — colours, fonts, video, docs (fill in your brand)
├── .claude/
│   ├── commands/          # Slash commands Claude can execute
│   │   ├── prime.md       # /prime — session initialization
│   │   ├── create-plan.md # /create-plan — create implementation plans
│   │   ├── implement.md   # /implement — execute plans
│   │   ├── commit.md      # /commit — save work, update docs, update changelog
│   │   ├── install.md     # /install — install AIOS modules
│   │   ├── brainstorm.md  # /brainstorm — find automation opportunities
│   │   ├── explore.md     # /explore — shape ideas interactively
│   │   ├── share.md       # /share — package systems for sharing
│   │   ├── task-audit.md  # /task-audit — map tasks, score automation potential
│   │   ├── capture.md     # /capture — quick content idea capture
│   │   ├── develop.md     # /develop — develop content concept
│   │   └── schedule.md    # /schedule — schedule content calendar
│   └── skills/            # Modular skill packs
│       ├── generate-uat/      # UAT plans from GitHub repos
│       ├── intent-check/      # AI delegation safety framework
│       ├── scope-check/       # Client request vs SOW analysis
│       ├── skill-creator/     # Create or update skills
│       ├── mcp-integration/   # Model Context Protocol setup
│       ├── writing-style/     # Anti-AI-slop writing enforcement
│       ├── vibe-coding/       # Non-technical builder toolkit
│       ├── build-or-buy/      # Agent deployment decision framework
│       └── which-agent/       # Agent architecture classifier
├── docs/                  # Self-documenting workspace
│   ├── _index.md          # Documentation routing index (scanned by /prime and /commit)
│   └── _templates/        # Templates for system and integration docs
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
├── shares/                # Packaged systems for sharing (created by /share)
├── module-installs/       # AIOS module installers
│   ├── context-os/        # Guided context builder (interview-based)
│   ├── content-pipeline/  # Content capture, develop, schedule workflow
│   ├── github-os/         # GitHub activity collection
│   ├── ghl-os/            # GoHighLevel pipeline sync
│   ├── ghl-github-bridge/ # GHL-GitHub two-way sync
│   ├── calendly-os/       # Calendly booking collection
│   └── seo-kit/           # SEO audit skill
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
| `shares/`    | Packaged systems for sharing. Created by `/share`, ready to hand off.              |
| `docs/`      | Auto-maintained technical docs. `_index.md` is the routing index.                  |
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

Reads the plan, executes each step in order, validates the work, updates documentation, and updates the plan status.

Example: `/implement plans/2026-01-28-competitor-analysis-command.md`

### /commit [optional message]

**Purpose:** Save work, update documentation, and keep the changelog current.

Run at the end of every session or after completing meaningful work. Claude will:

1. Stage and commit changed files with a structured commit message
2. Check if any technical docs in `docs/` need creating or updating
3. Add an entry to `HISTORY.md`
4. Offer to push to GitHub

### /install [module-path]

**Purpose:** Install an AIOS module from `module-installs/`.

Reads the module's `INSTALL.md` and executes all installation steps automatically.

Example: `/install module-installs/content-pipeline`

### /brainstorm [optional topic]

**Purpose:** Scan your workspace and find what to build or automate next.

Reads your tasks, processes, and current setup to find manual work that could be automated. Ranks opportunities by impact and feasibility. Run without arguments to scan everything, or with a topic to focus on a specific area.

### /explore [idea]

**Purpose:** Shape an idea into a clear, scoped concept through structured Q&A.

Takes an idea and walks through 5 stages interactively: Discovery, Research, Shape, Scope, Output. Produces a feature exploration doc in `plans/` ready to hand off to `/implement`.

**The cycle:** `/brainstorm` > `/explore` > `/create-plan` > `/implement` > repeat

### /share [system or feature]

**Purpose:** Package a system or feature from your workspace for sharing.

Deep-dives the code first to fully understand it, then produces a self-contained, beginner-friendly package with a Claude-guided installer (INSTALL.md + README.md + scripts). Outputs to `shares/`.

### /task-audit

**Purpose:** Map every recurring task across the business and score automation potential.

Runs a structured interview across 9 business areas, scores each task (Fully Automatable, Partially Automatable, Not Yet, Human-Only), and prioritises by impact x ease. Outputs to `context/task-audit.md`.

### /capture [idea]

**Purpose:** Quick content idea capture with classification.

Stores idea as a stub in the content database with channel, format, pillar, and funnel position. Checks for duplicates. Use `/develop` to flesh out a captured idea.

Example: `/capture Why agencies fail at production readiness`

### /develop [#ID or raw idea]

**Purpose:** Develop a content idea into a fully strategized concept.

Loads strategy docs + 7-day context window (recent content, meetings, pipeline state). Interactive: presents strategic positioning, then packaging, with confirmation at each stage.

Example: `/develop #5`

### /schedule [review]

**Purpose:** Interactive content scheduling session.

Shows developed ideas ranked by priority, current schedule gaps, and channel balance. Assigns dates and updates the pipeline. Use `/schedule review` to review existing schedule.

---

## Skills

Skills are modular capability packs that extend what Claude can do. They activate automatically when relevant.

| Skill | What it does |
|---|---|
| `generate-uat` | Generate production-accurate UAT plans from GitHub repos |
| `intent-check` | Catch delegation failures before they happen (4 modes) |
| `scope-check` | Analyse client requests against your SOW/contract |
| `skill-creator` | Create or update AgentSkills with scripts and references |
| `mcp-integration` | Configure Model Context Protocol servers |
| `writing-style` | Anti-AI-slop enforcement for all prose output |
| `vibe-coding` | Toolkit for non-technical builders shipping with AI (6 modes) |
| `build-or-buy` | Agent deployment decision framework using the 4:1 Ratio |
| `which-agent` | Classify what kind of AI agent a problem actually needs |

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

1. Write issue using the `agent-task` template > add `agent-ready` label
2. In a worktree terminal: `claude` > paste issue URL > agent reads and executes
3. Agent opens PR > adds `human-review` label
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

---

## For Users Downloading This Template

To customize this workspace to your own needs:

1. Run `bash scripts/setup.sh` to create worktrees and install shell aliases
2. Fill in your context documents in `context/` (or run `/install module-installs/context-os`)
3. Fill in `DESIGN.md` with your brand colours, fonts, and voice
4. Update this CLAUDE.md to reflect your business
5. Run `cs` (or `claude "/prime"`) to start your first session

Then use `/create-plan` to plan and `/implement` to execute any structural changes. This ensures everything stays in sync — especially CLAUDE.md, which must always reflect the current state of the workspace.

---

## Session Workflow

1. **Start**: Run `/prime` to load context (reads HISTORY.md + docs/_index.md)
2. **Work**: Use commands or direct Claude with tasks
3. **Ideate**: Use `/brainstorm` > `/explore` to find and shape opportunities
4. **Plan changes**: Use `/create-plan` before significant additions
5. **Execute**: Use `/implement` to execute plans
6. **Save**: Run `/commit` — stages, commits, updates docs and changelog
7. **Audit**: Use `/task-audit` to map tasks and track automation progress
8. **Share**: Use `/share` to package systems for team, clients, or community
9. **Maintain**: Claude updates CLAUDE.md and context/ as the workspace evolves

---

## Notes

- Keep context minimal but sufficient — avoid bloat
- Plans live in `plans/` with dated filenames for history
- Outputs are organized by type/purpose in `outputs/`
- Reference materials go in `reference/` for reuse
- `HISTORY.md` tracks all meaningful work across sessions
- `docs/_index.md` routes Claude to the right documentation for each system
