---
name: Agent Task
about: A fully-specified task that a Claude Code agent can pick up and execute autonomously
title: '[AGENT] '
labels: agent-ready
assignees: ''
---

<!--
INSTRUCTIONS FOR THE HUMAN WRITING THIS ISSUE:
Fill out every section below. Leave nothing vague. An agent will read this and execute —
it cannot ask you clarifying questions mid-task. If a section is unclear, add more detail
before adding the `agent-ready` label.

An issue is agent-ready when:
- Context explains WHY this exists, not just what to do
- Task is precise and unambiguous
- Acceptance criteria are testable checklists (not "should feel right")
- Files affected are listed with actual paths
- Out of scope is explicit — prevents scope creep
- Verification steps can be run mechanically
-->

## Context

<!-- Why does this issue exist? What's the larger goal it connects to?
What broke, what changed, or what decision led to this being needed?
Be specific — include relevant background the agent needs to understand purpose. -->

## Task

<!-- Precise description of what must be done. Use plain, imperative language.
If there are multiple sub-tasks, list them in order. Do not leave room for interpretation. -->

## Acceptance Criteria

<!-- Testable, binary checklist. Each item should be verifiable by running a command,
reading a file, or observing a specific output. "Looks good" is not acceptable here. -->

- [ ]
- [ ]
- [ ]

## Files Likely Affected

<!-- List file paths the agent should read and/or modify. Use actual paths from the repo. -->

- `path/to/file.ext`

## Out of Scope

<!-- What should the agent explicitly NOT do? This prevents unwanted changes. -->

-

## Verification Steps

<!-- How does the agent (and the human reviewer) confirm the work is complete and correct?
These should be mechanical steps: run this command, check this output, read this file. -->

1.
2.
3.

## Labels

<!-- Add the appropriate label after writing this issue:
- `agent-ready`      — issue is complete and ready for agent pickup
- `needs-spec`       — issue needs more detail before agent can work it
- `agent-in-progress` — agent is actively working this
- `human-review`     — agent work complete, needs human sign-off
-->
