# Reverse Engineer — Generate Requirements from an Existing Codebase

> Reads an existing codebase and produces structured requirements, architecture documentation, and a landmine register.
> Use for delivery rescues, onboarding to inherited projects, or any project where code exists but documentation doesn't.

## Purpose

Most delivery rescues start the same way: there's a codebase, it sort of works, nobody documented what it's supposed to do, and the original developer is gone. Before you can fix, extend, or maintain it, you need to understand what it does and why.

This command reads a codebase and produces the documentation that should have existed from the start.

## Usage

```
/reverse-engineer [repo-path]
```

- `repo-path`: Path to the local git repository, or a GitHub URL (will be cloned)
- If no path given, uses the current directory

## How It Works

### Step 1: Reconnaissance

Gather the basics without reading every file:

1. **Read README.md** (if it exists). Note what it claims vs what we'll verify.
2. **Read package.json / requirements.txt / Cargo.toml / go.mod** to identify the tech stack and dependencies.
3. **List the directory structure** (`find . -type f | head -100` or equivalent). Note the architecture pattern (monolith, microservices, monorepo, etc.).
4. **Read .env.example or .env.template** to identify external integrations (APIs, databases, services).
5. **Read any config files** (docker-compose.yml, terraform, CI/CD pipelines).
6. **Run `git log --oneline -30`** to understand recent activity and contributors.
7. **Run `git shortlog -sn`** to identify who built what.

Present the reconnaissance summary to the user and ask: "Does this match your understanding? Anything I'm missing or wrong about?"

### Step 2: Architecture Mapping

Read the key structural files to understand how the system is organised:

1. **Entry points:** main.py, index.ts, app.py, server.js, or equivalent. Trace the startup flow.
2. **Routing/API layer:** Find all API endpoints, routes, or handlers. List them.
3. **Data model:** Find database schemas, migrations, models, or type definitions. Map the entities and relationships.
4. **External integrations:** Find all API calls, webhook handlers, OAuth flows, third-party SDKs. List each integration with: what it connects to, what auth method, what data flows.
5. **Background jobs/crons:** Find scheduled tasks, queue consumers, workers.
6. **Frontend (if applicable):** Identify the UI framework, key pages/components, state management.

Ask clarifying questions where the code is ambiguous. Do not guess. Present each question and wait for the user's answer before proceeding.

### Step 3: Landmine Detection

Scan for code patterns that indicate hidden complexity, fragile workarounds, or decisions that look wrong but might be intentional:

- **Hardcoded values** that should be config (API URLs, credentials, magic numbers)
- **Commented-out code blocks** (why was it disabled? Is it needed?)
- **TODO / FIXME / HACK / WORKAROUND comments** (unresolved technical debt)
- **Empty catch blocks** or error handling that silently swallows failures
- **Overly complex functions** (high cyclomatic complexity, deeply nested logic)
- **Dead code** (functions defined but never called)
- **Inconsistent patterns** (some files use one approach, others use another)
- **Security concerns** (hardcoded secrets, SQL injection vectors, unvalidated inputs)
- **Missing error handling** on external API calls (no retries, no timeouts)
- **Race conditions or concurrency issues** (shared state without locking)

For each landmine found, note:
- What it is
- Where it is (file and line)
- Why it might be there (plausible reason for the original decision)
- Risk if changed (what could break)
- Recommendation: fix now / fix later / leave it / investigate

### Step 4: Requirements Extraction

Based on everything gathered, produce a requirements document written as if the project were being specified from scratch:

```markdown
# Requirements — [Project Name]

**Generated from:** [repo path]
**Date:** [today]
**Status:** Draft (requires stakeholder review)

## Product Overview
[What this system does, who it serves, what problem it solves]

## Tech Stack
[Languages, frameworks, databases, hosting, CI/CD]

## Features
### Feature 1: [Name]
**What it does:** [Description]
**Key behaviours:**
- [Behaviour 1]
- [Behaviour 2]
**Acceptance criteria:**
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]

### Feature 2: [Name]
[Same structure]

## Data Model
[Entities, relationships, key fields]

## External Integrations
| Service | Purpose | Auth Method | Data Flow |
|---------|---------|-------------|-----------|
| [Name]  | [Why]   | [How]       | [What]    |

## API Endpoints
| Method | Path | Purpose | Auth Required |
|--------|------|---------|---------------|
| GET    | /api/... | [What it does] | Yes/No |

## Background Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| [Name] | [Cron] | [What it does] |
```

### Step 5: Architecture Document

Produce a concise architecture document:

```markdown
# Architecture — [Project Name]

## System Overview
[High-level description of how the system is structured]

## Component Diagram
[Describe the major components and how they connect. 
If D2 diagrams are available, suggest creating one.]

## Key Architectural Decisions
| Decision | Rationale | Consequences |
|----------|-----------|--------------|
| [What was decided] | [Why, if known] | [What this means for future work] |

## Deployment
[How it runs: hosting, containers, serverless, etc.]

## Dependencies and Risks
[External dependencies, version risks, deprecated libraries]
```

### Step 6: Produce the Landmine Register

```markdown
# Landmine Register — [Project Name]

| # | File | Line | Type | Description | Risk if Changed | Recommendation |
|---|------|------|------|-------------|-----------------|----------------|
| 1 | [path] | [line] | [type] | [what] | [risk] | [action] |
```

### Step 7: Save and Summarise

Save all outputs to the appropriate location:
- Requirements: `artifacts/{project}/requirements.md` or `plans/`
- Architecture: `artifacts/{project}/architecture.md`
- Landmine register: `artifacts/{project}/landmine-register.md`

Print a summary:
- Total features identified
- Total API endpoints
- Total external integrations
- Total landmines found (by severity)
- Recommended first actions
- Whether this project is ready for `/check-drift` (i.e., are the requirements good enough to drift-check against?)

## Notes

- This command is human-in-the-loop by design. It asks questions and waits for answers. Do not guess when the code is ambiguous.
- The requirements document is a draft. It must be reviewed by someone who knows the business intent. Code tells you what the system does, not what it's supposed to do.
- Run time depends on codebase size. Small repos (< 50 files): 15-20 minutes. Large repos (500+ files): may need multiple sessions focused on different areas.
- For very large repos, start with `/reverse-engineer [path] --scope api` or `--scope frontend` to focus on one layer at a time.
- This command pairs with `/check-drift`: once you have requirements from reverse-engineering, use drift detection to catch future changes that diverge from the spec.
- The landmine register is the most immediately valuable output for delivery rescues. It tells you where NOT to touch without understanding the consequences.
