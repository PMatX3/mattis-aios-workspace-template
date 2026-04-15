# Check Drift — Compare Code Changes Against Acceptance Criteria

> Detects when code has drifted from the agreed requirements or acceptance criteria.
> Run after commits, before PRs, or during delivery reviews.

## Purpose

Code drift is the silent killer of delivery projects. The build starts aligned with the spec, then gradually diverges as developers make decisions that weren't in the requirements. By the time UAT arrives, the gap between "what was agreed" and "what was built" is too wide to fix cheaply.

This command catches drift early by comparing recent code changes against the acceptance criteria or requirements document.

## Usage

```
/check-drift [repo-path] [requirements-path]
```

- `repo-path`: Path to the git repository (default: current directory)
- `requirements-path`: Path to the requirements, UAT checklist, or acceptance criteria document

## How It Works

### Step 1: Gather the Baseline

Read the requirements or acceptance criteria document. This is the source of truth. Extract every testable requirement into a numbered list.

If no requirements path is provided, look for these files in order:
1. `requirements.md` or `REQUIREMENTS.md` in the repo root
2. `docs/requirements.md`
3. `docs/acceptance-criteria.md`
4. Any UAT checklist in the repo
5. The most recent plan file in `plans/` that mentions this project

If nothing is found, tell the user: "No requirements document found. Point me to your spec, UAT checklist, or acceptance criteria."

### Step 2: Get Recent Changes

Run `git log --oneline -20` to see recent commits. Then run `git diff HEAD~10..HEAD --stat` to see which files changed and the scope of changes.

For each significantly changed file, read the diff: `git diff HEAD~10..HEAD -- <file>`

If the user specifies a PR branch, use `git diff main...<branch>` instead.

### Step 3: Map Changes to Requirements

For each code change, determine:

1. **Which requirement does this change serve?** Map the change back to a specific requirement number.
2. **Is this change aligned?** Does it implement what the requirement asks for, correctly?
3. **Is this change unrelated?** Code that doesn't map to any requirement is potential scope creep.
4. **Is this change contradicting?** Code that does the opposite of what a requirement specifies is a defect.

### Step 4: Produce the Drift Report

Output a structured report:

```
# Drift Report
**Repo:** [path]
**Requirements:** [doc path]
**Commits reviewed:** [range]
**Date:** [today]

## Alignment Summary

| Status | Count |
|--------|-------|
| Aligned | X |
| Drifted | X |
| New scope (not in requirements) | X |
| Requirements not yet addressed | X |

## Aligned Changes
[List changes that correctly implement requirements, with requirement number]

## Drift Detected
[For each drifted change:]
- **File:** [path]
- **Change:** [what was changed]
- **Requirement:** [what it should have done]
- **Drift:** [how it differs]
- **Severity:** Critical / Warning / Minor
- **Recommendation:** [fix suggestion]

## New Scope (Potential Scope Creep)
[Changes that don't map to any requirement]
- **File:** [path]
- **Change:** [what was added]
- **Assessment:** Intentional enhancement / Scope creep / Technical debt fix / Refactoring
- **Action needed:** Add to requirements / Remove / Discuss with stakeholder

## Requirements Not Yet Addressed
[Requirements from the spec that have no corresponding code changes]

## Landmines Detected
[Code patterns that look suspicious: hardcoded values, commented-out code, 
TODO/FIXME/HACK comments, workarounds that bypass the normal flow, 
error handling that silently swallows failures]
```

### Step 5: Recommend Actions

Based on the drift report, recommend:
- Which drifted changes need immediate attention
- Whether a stakeholder conversation is needed before proceeding
- Whether the requirements document needs updating to reflect intentional changes
- Whether a change request should be raised for new scope

## Notes

- Run this before creating a PR, not after merging
- The report is advisory. Not every "new scope" item is bad. Sometimes the developer made a good call that the spec didn't anticipate. The point is to make it visible.
- If drift is found, update the requirements document after the discussion. The requirements should always reflect what was actually agreed, not what was originally written.
- Save drift reports to `artifacts/{project}/drift-report-{date}.md` for audit trail
- This command pairs with `/reverse-engineer` for projects that have code but no requirements
