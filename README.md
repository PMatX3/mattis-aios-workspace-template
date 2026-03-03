# AIOS Workspace Template

**An AI Operating System for running your business with Claude Code.**

AIOS is a structured workspace that gives Claude Code persistent context about you, your business, and your goals — so every session starts informed, not from zero. It's designed for founders, consultants, and operators who want an AI that functions as a genuine business partner, not a generic chat tool.

---

## What This Is

Most AI interactions start with re-explaining everything. AIOS solves this by building a context layer Claude reads at the start of every session. Once set up:

- Claude knows your business, role, and current strategy
- You never re-explain who you are or what you're doing
- Structured commands handle common workflows (planning, executing, priming)
- Worktrees let you run parallel Claude sessions (delivery, commercial, research) without conflicts
- GitHub issue templates enable autonomous Claude agents to work tickets without hand-holding

---

## Quick Start

```bash
# 1. Clone this template
git clone https://github.com/YOUR_USERNAME/mattis-aios-workspace-template my-workspace
cd my-workspace

# 2. Run setup (creates worktrees + installs shell aliases)
bash scripts/setup.sh
source ~/.zshrc

# 3. Fill in your context files
# Edit these 4 files with your business details:
#   context/business-info.md
#   context/personal-info.md
#   context/strategy.md
#   context/current-data.md
# OR: run the ContextOS module to have Claude interview you (see module-installs/context-os/)

# 4. Launch Claude
cs        # launches Claude and runs /prime automatically
```

After step 4, Claude will read your context files and confirm it understands your business.

---

## Folder Structure

```
.
├── CLAUDE.md              # Master context file — always loaded, keep current
├── .claude/
│   ├── commands/          # /prime, /create-plan, /implement
│   └── skills/            # generate-uat, skill-creator, mcp-integration
├── context/               # Who you are, your business, strategy, metrics
│   ├── business-info.md
│   ├── personal-info.md
│   ├── strategy.md
│   ├── current-data.md
│   ├── decision-policy.md
│   └── import/            # Drop docs here for Claude to ingest
├── plans/                 # Dated implementation plans
├── outputs/               # Deliverables and registers
├── artifacts/             # Project-specific outputs
├── reference/
│   ├── scorecard-metrics.md
│   ├── shell-aliases.md
│   └── templates/         # 6 delivery templates (SOW, UAT, runbook, etc.)
├── module-installs/
│   └── context-os/        # Guided context builder module
├── scripts/
│   ├── setup.sh           # One-time workspace setup
│   └── wt.sh              # Worktree helper
└── .github/
    └── ISSUE_TEMPLATE/
        └── agent-task.md  # Template for agent-ready GitHub issues
```

---

## Commands

Run these inside a Claude Code session (after `cs` or `claude`):

| Command | What it does |
|---|---|
| `/prime` | Loads your context and confirms Claude understands your business |
| `/create-plan [request]` | Creates a detailed implementation plan in `plans/` |
| `/implement [plan-path]` | Executes a plan created by `/create-plan` |

---

## Shell Aliases

After running `setup.sh`, you get:

| Alias | Description |
|---|---|
| `cs` | Launch Claude (safe mode — prompts for permission) and run `/prime` |
| `cr` | Launch Claude (auto-approve) and run `/prime` |
| `wt` | `cd` to workspace root |
| `wtd` | `cd` to delivery worktree |
| `wtc` | `cd` to commercial worktree |
| `wtr` | `cd` to research worktree |

---

## Parallel Worktrees

The workspace creates three isolated branches so you can run parallel Claude sessions without conflicts:

| Branch | Use for |
|---|---|
| `main` | Planning, strategy, workspace maintenance |
| `delivery` | Client work, UAT plans, runbooks, handover packs |
| `commercial` | Proposals, content, outbound, pricing |
| `research` | Analysis, strategy thinking, background research |

Open each branch in a separate terminal → run `cs` → Claude sessions work independently.

---

## Customise It

The context files are where your business lives. Fill them in:

1. **`context/business-info.md`** — What your business does, who it serves, key products/services
2. **`context/personal-info.md`** — Your role, responsibilities, how the workspace helps you
3. **`context/strategy.md`** — Current priorities, what success looks like, key decisions
4. **`context/current-data.md`** — Key metrics, current state, data sources

Then update `CLAUDE.md` to remove any generic text and reflect your actual business.

> **Tip:** Use the ContextOS module (`module-installs/context-os/`) to have Claude interview you and build these files automatically.

---

## Agent-Ready GitHub Issues

This workspace includes a convention for running Claude Code agents autonomously on GitHub issues.

### How it works

1. Write an issue using the **Agent Task** template (`.github/ISSUE_TEMPLATE/agent-task.md`)
2. Add the `agent-ready` label
3. In a worktree terminal: `claude` → paste the issue URL → agent reads and executes
4. Agent opens a PR → adds `human-review` label
5. You review and merge

### Labels

| Label | Meaning |
|---|---|
| `agent-ready` | Fully specified; agent can pick it up |
| `agent-in-progress` | Agent is working it |
| `needs-spec` | Needs more detail before an agent can work it |
| `human-review` | Work done; needs human sign-off |

An agent-ready issue must contain: context, precise task, testable acceptance criteria, file paths, out-of-scope boundaries, and verification steps.

---

## Delivery Templates

Six production-tested templates in `reference/templates/`:

| Template | Use for |
|---|---|
| `audit-checklist.md` | 7-day structured audit of an existing system |
| `sow-scope-acceptance.md` | Statement of Work with acceptance criteria |
| `uat-plan.md` | UAT plan with test cases and sign-off |
| `go-live-runbook.md` | Go-live sequence, rollback plan, monitoring |
| `handover-pack.md` | Ownership transfer documentation |
| `change-request.md` | Scope/timeline/price change control |

---

## Weekly Operating Rhythm

Every Monday (~90 min):

1. `outputs/project-register.md` — update project status, risks, next milestone
2. `reference/scorecard-metrics.md` — fill this week's scorecard row
3. Check WIP count against your limit
4. Publish one piece of content for your primary acquisition channel
5. Send targeted outreach to ICP
6. Unblock your team

---

## Module Installers

`module-installs/` contains plug-and-play modules that extend the workspace:

| Module | What it does |
|---|---|
| `context-os/` | Guided interview to build all 4 context files from scratch (30–45 min) |

To install: open the module's `INSTALL.md` and follow the instructions (or tell Claude to run it).

---

## License

MIT — use, fork, and customise freely.
