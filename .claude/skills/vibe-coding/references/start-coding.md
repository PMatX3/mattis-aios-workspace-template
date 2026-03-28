# Start Coding Session

Initialize a coding session with vibe coding discipline baked in. This runs automatically when the user says "start coding", "write code", or similar.

## Instructions

### Step 1: Identify the project

Ask: "What project are we working on? Give me the repo path or project name."

If the user already mentioned a project in the conversation, skip this and use that.

### Step 2: Check for a rules file

Look for a rules file in the project directory. Check in order:
- `CLAUDE.md`
- `.cursorrules`
- `.cursor/rules/`
- `AGENTS.md`
- `.windsurfrules`

If found, read it and confirm: "Found your rules file. I'll follow it."

If not found, say: "No rules file found. Want me to generate one? It takes about 2 minutes and saves you hours of repeating yourself to the agent." If they say yes, switch to the Rules File Builder mode (`references/rules-file-builder.md`). If they say no, continue without one.

### Step 3: Set session ground rules

State these clearly and briefly:

"Session rules are set:

1. **Small tasks only.** I'll work in steps that touch 3 files or fewer. If something needs more, I'll propose a plan first.
2. **Commit checkpoints.** After each working change, I'll prompt you to commit. If anything breaks, we roll back to the last commit, not debug for an hour.
3. **Test before moving on.** After each step, I'll tell you how to verify it works before we continue.
4. **Fresh context.** If this session runs long, I'll flag when it's time to start a new one rather than let quality degrade.
5. **No side quests.** I won't refactor, reorganise, or "improve" things you didn't ask for."

### Step 4: Get the first task

Ask: "What are we building or fixing today?"

If the task sounds large (touching more than 5 files, multiple systems, or the user describes it as "redesign", "overhaul", "rebuild"), automatically decompose it using the Task Decomposer approach before starting. Say: "That's a bigger change. Let me break it into safe steps first." Then decompose and present the steps.

If the task is small and focused, proceed directly.

### Step 5: Work with discipline

Throughout the session, enforce these behaviours:

- **Before each change:** State what you're about to do and which files it touches. If more than 3 files, get approval.
- **After each change:** Give a plain-English test instruction. Wait for confirmation before continuing.
- **After each confirmed change:** Prompt to commit: "That's working. Good time to commit: `git add [files] && git commit -m '[message]'`"
- **If something breaks:** Stop immediately. Say "Something broke. Let's roll back: `git checkout .` and try a different approach." Do not attempt to debug forward through compounding errors.
- **Every 30 minutes or ~5 completed steps:** Check in: "We've been going a while. Want to keep going or start a fresh session? Context quality holds up better with fresh starts."

### Step 6: Session wrap-up

When the user signals they're done or the work is complete:

1. Summarise what was built/changed
2. List all files modified
3. Confirm everything is committed
4. If there's a rules file, suggest any new rules based on problems hit during the session: "Based on today, consider adding these to your rules file: [specific rules from real problems encountered]"
