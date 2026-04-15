# Elicit — Work Operating Model Interview

> A structured 45-minute interview that captures how someone actually works, producing agent-ready context files for their AIOS workspace.
>
> Based on Nate B. Jones' Agent Soul framework. Adapted for AIOS workspace output.

## Purpose

Before an AIOS workspace can be useful, the person using it needs to describe their work in enough detail for Claude to act on it. Most people cannot do this from scratch. This interview walks them through it layer by layer, with checkpoint approvals between each layer.

The output replaces or enriches their workspace context files: `personal-info.md`, `decision-policy.md`, and generates new files where needed.

## How It Works

Run this command with the team member present. Claude acts as an interviewer, not an assistant. The interview covers five layers in order. After each layer, Claude summarises what was captured and asks for approval before moving on. Nothing is saved without confirmation.

**Important rules for the interviewer:**
- Ask one question at a time. Wait for the answer.
- Follow up on vague answers. "I handle client comms" is not useful. "Every Monday I check the shared inbox, prioritise by client tier, and respond to anything urgent before 10am" is useful.
- Distinguish between what the person says they do (aspirational) and what they actually do (real). Probe for the real version.
- Capture the implicit knowledge: the things they do automatically that they've never written down.
- Keep each layer to roughly 8-10 minutes. The full interview should take 45 minutes.

## The Interview

### Layer 1: Operating Rhythms (8 mins)

Ask about how their days and weeks actually run. Not the calendar version, the real version.

Questions to cover:
- Walk me through a typical day. What happens first, what happens last?
- Which days feel different from others? (e.g., Monday is planning, Friday is lighter)
- When are you most focused? When do you do shallow work?
- What interrupts you most? How do you handle interruptions?
- What time blocks are sacred vs flexible?
- Are there things you do every day/week that aren't in any calendar or task list?
- What does your energy pattern look like across the week?

**Checkpoint:** Summarise the operating rhythms back. Ask: "Does this match how your week actually runs? What did I miss or get wrong?" Wait for confirmation before proceeding.

### Layer 2: Recurring Decisions (8 mins)

Ask about the judgment calls they make regularly.

Questions to cover:
- What decisions do you make every day or week that nobody else makes?
- For each: what information do you need before you can decide?
- What would make you escalate something vs handle it yourself?
- Are there decisions you make on autopilot that you've never explained to anyone?
- What thresholds or rules of thumb do you use? (e.g., "if the client hasn't responded in 3 days, I chase")
- What decisions have you got wrong in the past, and what did you learn?

**Checkpoint:** Summarise the recurring decisions. Ask for confirmation.

### Layer 3: Dependencies (8 mins)

Ask about what they need from others to do their work.

Questions to cover:
- Who do you depend on to get your work done? What do they provide?
- What happens when those people are slow or unavailable?
- Are there regular handoffs between you and other team members?
- What information do you need that comes from outside the team? (clients, tools, systems)
- Is there a single point of failure in your workflow, something that if it breaks, everything stops?
- What workarounds do you use when dependencies fail?

**Checkpoint:** Summarise dependencies. Ask for confirmation.

### Layer 4: Institutional Knowledge (8 mins)

Ask about what they know that nobody else on the team knows.

Questions to cover:
- What do you know about clients, processes, or systems that isn't written down anywhere?
- If you were off sick for two weeks, what would fall through the cracks?
- Are there things you do that you've never trained anyone else to do?
- What context do you carry in your head that a new person would take months to learn?
- What have you learned from mistakes that shaped how you work now?
- Are there relationships (client contacts, supplier contacts) that only you maintain?

**Checkpoint:** Summarise institutional knowledge. Ask for confirmation.

### Layer 5: Friction (8 mins)

Ask about what wastes their time or causes frustration.

Questions to cover:
- What tasks do you dread or procrastinate on?
- What takes longer than it should? Why?
- What do you do manually that you suspect could be automated?
- What tools or processes frustrate you?
- What information do you regularly have to hunt for?
- If you could eliminate one recurring annoyance from your week, what would it be?
- What do you spend time on that doesn't feel like it adds value?

**Checkpoint:** Summarise friction points. Ask for confirmation.

## Output

After all five layers are confirmed, generate the following files in the team member's AIOS workspace:

### 1. Update `context/personal-info.md`

Enrich the existing personal-info.md with the captured operating rhythms, decision patterns, and institutional knowledge. Do not overwrite what's already there. Add sections for:
- Operating rhythms (daily/weekly patterns)
- Key decisions and judgment calls
- Dependencies and handoffs

### 2. Create or update `context/decision-policy.md`

Add the decision rules, thresholds, and escalation criteria captured in Layer 2. Format as clear, actionable rules that Claude can follow.

### 3. Create `context/friction-log.md`

A prioritised list of friction points from Layer 5, each with:
- Description of the friction
- Estimated time cost per week
- Current workaround (if any)
- Automation candidate: yes/no
- Priority: high/medium/low

### 4. Create `context/knowledge-register.md`

The institutional knowledge from Layer 4, formatted as a reference document:
- What the knowledge is
- Where it currently lives (head, docs, system)
- Who else knows it (if anyone)
- Risk if this person is unavailable
- Transfer action needed

### 5. Generate summary

Print a summary showing:
- Total friction hours identified per week
- Number of automation candidates
- Top 3 institutional knowledge risks
- Recommended first actions for their AIOS workspace

## Notes

- This can be run in a mob session (one person interviewed, team watches) or individually
- Each person's outputs go into their own workspace, not the shared workspace
- The interview can be paused and resumed. If paused, save progress to a temp file and resume from the last completed layer
- Run this AFTER the team member has completed the basic AIOS setup (workspace cloned, context files created, /prime working)
