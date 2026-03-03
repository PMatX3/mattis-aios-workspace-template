#!/usr/bin/env bash
# setup.sh — One-time workspace setup
#
# Run this after cloning to:
#   1. Create standard worktrees (delivery, commercial, research)
#   2. Install shell aliases into ~/.zshrc or ~/.bashrc
#
# Usage: bash scripts/setup.sh

set -e

REPO="$(git -C "$(cd "$(dirname "$0")" && pwd)" rev-parse --show-toplevel)"
WT_DIR="$REPO/.worktrees"
MARKER="# AIWorkspace"

echo "Setting up workspace at: $REPO"
echo ""

# ── 1. Worktrees ──────────────────────────────────────────────────────────────

mkdir -p "$WT_DIR"

declare -A WT_DESC=(
  [delivery]="client delivery artifacts (UAT plans, runbooks, handover packs)"
  [commercial]="proposals, content, outbound, pricing"
  [research]="analysis, strategy thinking, background research"
)

for name in delivery commercial research; do
  if ! git -C "$REPO" show-ref --verify --quiet "refs/heads/$name"; then
    git -C "$REPO" branch "$name"
    echo "  [+] branch:   $name"
  else
    echo "  [=] branch:   $name (exists)"
  fi

  if [ ! -d "$WT_DIR/$name" ]; then
    git -C "$REPO" worktree add "$WT_DIR/$name" "$name" --quiet
    echo "  [+] worktree: .worktrees/$name — ${WT_DESC[$name]}"
  else
    echo "  [=] worktree: .worktrees/$name (exists)"
  fi
done

echo ""

# ── 2. Shell aliases ──────────────────────────────────────────────────────────

if [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  SHELL_RC="$HOME/.bashrc"
else
  echo "No ~/.zshrc or ~/.bashrc found. Add aliases manually — see reference/shell-aliases.md"
  exit 0
fi

if grep -q "$MARKER" "$SHELL_RC" 2>/dev/null; then
  echo "Aliases already installed in $SHELL_RC — skipping."
else
  cat >> "$SHELL_RC" << EOF

$MARKER
alias cs='claude "/prime"'
alias cr='claude --dangerously-skip-permissions "/prime"'
WS="$REPO"
alias wt='cd "\$WS"'
alias wtd='cd "\$WS/.worktrees/delivery"'
alias wtc='cd "\$WS/.worktrees/commercial"'
alias wtr='cd "\$WS/.worktrees/research"'
EOF
  echo "  [+] aliases installed in $SHELL_RC"
fi

echo ""
echo "Done. Run:  source $SHELL_RC"
echo ""
echo "Aliases:"
echo "  cs / cr      launch Claude (safe / auto-approve)"
echo "  wt           cd to workspace root"
echo "  wtd          cd to delivery worktree"
echo "  wtc          cd to commercial worktree"
echo "  wtr          cd to research worktree"
