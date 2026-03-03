# Shell Aliases for Claude Code

## Setup (new machine or collaborator)

Run the setup script once after cloning. It creates worktrees and installs all aliases automatically:

```bash
bash scripts/setup.sh
source ~/.zshrc
```

The script detects where the repo lives and writes the correct paths — no manual editing needed.

## Manual setup

If you prefer to add aliases yourself, add these to your `~/.zshrc` (or `~/.bashrc`), replacing the path with wherever you cloned the repo:

```bash
alias cs='claude "/prime"'
alias cr='claude --dangerously-skip-permissions "/prime"'
WS="/path/to/your-workspace"
alias wt='cd "$WS"'
alias wtd='cd "$WS/.worktrees/delivery"'
alias wtc='cd "$WS/.worktrees/commercial"'
alias wtr='cd "$WS/.worktrees/research"'
```

Then reload: `source ~/.zshrc`

## The Aliases

### `cs` — Claude Safe

```bash
alias cs='claude "/prime"'
```

Launches Claude Code and immediately runs `/prime` to load workspace context. Claude will ask for permission before executing commands, reading sensitive files, or making changes.

**Use when:** Starting a new session where you want to review and approve each action.

### `cr` — Claude Run

```bash
alias cr='claude --dangerously-skip-permissions "/prime"'
```

Launches Claude Code with permission prompts disabled, then runs `/prime`. Claude can execute commands and make changes without asking for approval.

**Use when:** You trust the task, want faster iteration, or are doing routine work where constant approvals slow you down.

## Why Both?

- **`cs`** gives you oversight — good for unfamiliar tasks, sensitive operations, or when you want to learn what Claude is doing
- **`cr`** gives you speed — good for familiar workflows where you trust Claude to operate autonomously

Both run `/prime` automatically so Claude starts every session fully oriented to your workspace, goals, and context.

---

## Worktree Navigation

```bash
alias wt='cd /path/to/your-workspace'
alias wtd='cd /path/to/your-workspace/.worktrees/delivery'
alias wtc='cd /path/to/your-workspace/.worktrees/commercial'
alias wtr='cd /path/to/your-workspace/.worktrees/research'
```

| Alias | Branch | Use for |
|-------|--------|---------|
| `wt` | `main` | Workspace root |
| `wtd` | `delivery` | Client delivery artifacts (UAT plans, runbooks, handover packs) |
| `wtc` | `commercial` | Proposals, content, outbound, pricing |
| `wtr` | `research` | Analysis, strategy thinking, background research |

### Typical parallel session workflow

1. In your current terminal — do main/planning work, use `cs` or `cr` as normal
2. Open a new terminal tab → `wtd && cs` to start a Claude session on the delivery branch
3. Open another tab → `wtc && cs` for commercial work

Each session operates on its own branch. No file conflicts between parallel Claude instances.

### Ad-hoc worktrees

```bash
./scripts/wt.sh new <name>        # create a branch + worktree
./scripts/wt.sh list              # see all active worktrees
./scripts/wt.sh remove <name>     # clean up when done
```
