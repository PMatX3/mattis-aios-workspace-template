#!/usr/bin/env bash
# wt.sh — Worktree helper
#
# Usage:
#   ./scripts/wt.sh list              List all active worktrees
#   ./scripts/wt.sh new <name>        Create a new worktree + branch
#   ./scripts/wt.sh open <name>       Print the path (use with: cd $(./scripts/wt.sh open <name>))
#   ./scripts/wt.sh remove <name>     Remove a worktree and delete its branch

ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
WT_DIR="$ROOT/.worktrees"

cmd="${1}"
name="${2}"

case "$cmd" in
  list)
    git -C "$ROOT" worktree list
    ;;

  new)
    if [[ -z "$name" ]]; then
      echo "Usage: wt.sh new <name>"
      exit 1
    fi
    branch="${name}"
    path="$WT_DIR/$name"
    if git -C "$ROOT" show-ref --verify --quiet "refs/heads/$branch"; then
      echo "Branch '$branch' already exists. Adding worktree..."
      git -C "$ROOT" worktree add "$path" "$branch"
    else
      git -C "$ROOT" worktree add -b "$branch" "$path"
    fi
    echo ""
    echo "Worktree ready: $path"
    echo "Open in a new terminal and run: claude"
    ;;

  open)
    if [[ -z "$name" ]]; then
      echo "Usage: cd \$(./scripts/wt.sh open <name>)"
      exit 1
    fi
    echo "$WT_DIR/$name"
    ;;

  remove)
    if [[ -z "$name" ]]; then
      echo "Usage: wt.sh remove <name>"
      exit 1
    fi
    path="$WT_DIR/$name"
    git -C "$ROOT" worktree remove "$path" --force
    git -C "$ROOT" branch -d "$name" 2>/dev/null && echo "Branch '$name' deleted." || echo "Branch '$name' kept (has unpushed commits or couldn't delete)."
    ;;

  *)
    echo "wt.sh — Worktree helper"
    echo ""
    echo "Commands:"
    echo "  list             List all active worktrees"
    echo "  new <name>       Create a new worktree + branch"
    echo "  open <name>      Print path (use: cd \$(./scripts/wt.sh open <name>))"
    echo "  remove <name>    Remove worktree and delete branch"
    echo ""
    echo "Standard worktrees:"
    echo "  delivery    — client delivery work (UAT plans, runbooks, handover packs)"
    echo "  commercial  — proposals, content, outbound, pricing"
    echo "  research    — analysis, background research, strategy thinking"
    ;;
esac
