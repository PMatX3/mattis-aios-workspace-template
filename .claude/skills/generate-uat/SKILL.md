---
name: generate-uat
description: Generate a production-accurate UAT plan from a GitHub repository by reading the actual codebase, open issues, and recent PRs. Use when the user provides a GitHub repo URL and wants a UAT plan, test cases, or sign-off document for a software project. Triggers on phrases like "generate UAT", "create UAT plan", "write UAT for", "UAT for this repo", or when a GitHub URL is provided alongside a request for testing or sign-off documentation.
---

# Generate UAT

Produce a production-accurate UAT plan by reading the actual codebase — not just requirements docs. The output maps test cases to real endpoints, real data models, real open issues, and real failure modes.

## Workflow

### Step 1: Gather inputs

Required:
- GitHub repo URL (e.g. `https://github.com/org/repo`)

Infer from context if available:
- Project name and client/partner
- Phase scope (what's in / out of scope for this UAT)
- Go-live target date
- UAT lead on client side

### Step 2: Explore the repository

Run these in parallel:

```bash
# List all files
gh api "repos/{owner}/{repo}/git/trees/main" --field recursive=1 --jq '.tree[] | select(.type=="blob") | .path'

# Open issues (full detail)
gh issue list -R {owner}/{repo} --limit 60 --state open --json number,title,body,labels

# Recent merged PRs
gh pr list -R {owner}/{repo} --limit 20 --state merged --json number,title,body,mergedAt,headRefName

# List branches
gh api "repos/{owner}/{repo}/branches" --jq '.[].name'
```

Read these files (fetch via `gh api "repos/{owner}/{repo}/contents/{path}" --jq '.content' | base64 -d`):
- README.md
- Any docs/ or documentation folders
- Main entry point (app.py, main.py, index.js, etc.)
- Route/endpoint files
- Service/integration files
- Config and environment examples (.env.example)
- Existing test files

Focus on understanding:
- End-to-end workflow (what triggers what)
- All external integrations (APIs, webhooks, OAuth, databases)
- Data models (key fields, statuses, relationships)
- Error handling and retry logic
- Feature flags and environment-gated behaviour
- Open issues (especially P0/P1 — these become explicit test cases)
- Recent PRs (recent fixes = recent failure modes = high-priority test cases)

### Step 3: Write the UAT plan

Save to `artifacts/{project-slug}-uat-plan.md`.

Follow the structure in `references/uat-structure.md`.

Key principles:
- **Every test case maps to real code** — use actual endpoint names, real intent keywords, real field names, real status values from the codebase
- **Open P0/P1 issues become named test cases** — reference the issue number
- **Recent bug fixes become test cases** — if it broke before, test it explicitly
- **Feature flags and env vars are pre-UAT prerequisites** — list them all
- **Phase scope is explicit** — out-of-scope items are named to prevent scope creep
- **Accuracy thresholds** — where AI/ML or extraction is involved, define measurable pass criteria
- **Human gates** — identify every point where a human must approve before automation continues

### Step 4: Update the project register

Update `outputs/project-register.md`:
- Set status to `UAT` for the relevant project row
- Update next milestone to reflect UAT kick-off date

---

## Quality Bar

The UAT plan is complete when someone unfamiliar with the codebase could:
1. Set up the test environment from the prerequisites section alone
2. Execute every test case without needing to read the code
3. Make a clear pass/fail decision on each case
4. Know exactly what needs to be fixed before sign-off

If the UAT plan could have been written without reading the codebase, it is not good enough.
