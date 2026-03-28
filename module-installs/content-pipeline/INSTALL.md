# Content Pipeline -- AIOS Module Installer

<!-- MODULE METADATA
module: content-pipeline
version: v1
status: RELEASED
requires: [data/ directory, .venv]
phase: 4
category: ContentOS
complexity: medium-complex
api_keys: 0
setup_time: 30-45 minutes
-->

---

## FOR CLAUDE

You are helping a user install Content Pipeline, their content intelligence system. This is a **workshop-driven install**, not just copying files. You are running an interactive Brand & Content Workshop that produces customized strategy documents, then installing the pipeline scripts and commands.

**Behavior:**
- Assume the user is non-technical unless they tell you otherwise
- Explain what you are doing at each step in plain English BEFORE doing it
- Celebrate small wins ("Strategy doc looks great, that is the foundation for everything!")
- If something fails, do not dump error logs. Explain the problem simply and suggest the fix
- Never skip verification steps. If a check fails, stop and help the user fix it
- Use encouraging language throughout. They are building something real

**Pacing:**
- Do NOT rush. Pause after major milestones.
- After Phase 1 (Scripts): "Pipeline scripts are installed. Now the fun part, let us figure out YOUR content strategy."
- After Phase 2 (Workshop): "Your strategy docs are locked in. Now let us wire up the commands."
- After Phase 3 (Commands): "Commands are live. Let us test the whole system end-to-end."
- After Phase 4 (Test): "It works! Here is what you just built and what to do next."

**Workshop approach (Phase 2):**
- This is INTERACTIVE. You are interviewing the user about their business, content, and audience.
- Read their context files first (`context/` folder), especially `context/business-info.md`, `context/personal-info.md`, and `context/strategy.md`. Use what you already know about their business to pre-fill answers.
- Ask questions in batches of 2-3, not rapid-fire 20 questions.
- After each workshop section, SHOW them what you wrote and get approval before moving on.
- If they already have a content strategy, adapt. Do not force them to start from scratch.

**Error handling:**
- If Python version is too old, provide exact upgrade instructions for their OS
- If database init fails, check the data/ directory exists and has write permissions
- Never say "check the logs." Find the problem and explain it

---

## OVERVIEW

Content Pipeline turns your content chaos into a strategic system. Instead of staring at a blank page wondering what to create, you will have a pipeline of ideas that are captured, classified, strategically developed, and scheduled, all powered by AI that understands your brand, audience, and business goals.

**What you get when it is done:**
- A content database that tracks every idea from raw capture to published
- Three slash commands: `/capture` (quick idea capture), `/develop` (full concept development with strategic positioning and packaging), `/schedule` (batch scheduling with date management)
- A 7-day context window that gives Claude awareness of your recent content, meetings, and pipeline state, so every idea it develops is informed and strategic
- Strategy documents that teach Claude your brand positioning, audience segments, content pillars, and offers

**Setup time:** 30-45 minutes (most of that is the Brand & Content Workshop, the actual install is quick)
**Running cost:** Free
**What you need:** A `data/` directory (for the SQLite database) and a Python virtual environment (`.venv`)

---

## PREREQUISITES

Check each prerequisite. Verify it works before proceeding.

### Python 3.10+
```bash
python3 --version
```
If not installed or too old: provide OS-specific install instructions.

### Virtual Environment
```bash
ls .venv/bin/activate 2>/dev/null && echo "venv exists" || echo "no venv"
```
If no venv:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Data Directory
```bash
ls data/ 2>/dev/null && echo "data dir exists" || echo "no data dir"
```
If no data directory:
```bash
mkdir -p data
```

### Context Files (for the workshop)
```bash
ls context/*.md 2>/dev/null | head -5
```
If context files exist, read them before Phase 2 to pre-fill workshop answers. If no context files, the workshop will start from scratch (that is fine).

[VERIFY] All prerequisites show version numbers without errors.
Ask: "Everything checks out. Ready to start building?"

---

## PHASE 1: INSTALL SCRIPTS

### Step 1: Install dependencies

```bash
source .venv/bin/activate
pip install python-dotenv requests
```

[VERIFY]
```bash
python3 -c "from dotenv import load_dotenv; import requests; print('Dependencies OK')"
```

### Step 2: Copy content_db.py

Copy `module-installs/content-pipeline/scripts/content_db.py` to `scripts/content_db.py`.

Then initialize the database:
```bash
source .venv/bin/activate && python3 scripts/content_db.py
```

Expected: "Database initialized at: data/content.db" with 2 tables listed.

[VERIFY]
```bash
python3 scripts/content_db.py --check
```
Should show: content_ideas (0 rows), published_content (0 rows).

### Step 3: Copy writer.py

Copy `module-installs/content-pipeline/scripts/writer.py` to `scripts/writer.py`.

[VERIFY]
```bash
source .venv/bin/activate && python3 scripts/writer.py
```
Expected: "Writer module loaded successfully."

### Step 4: Copy context_aggregator.py

Copy `module-installs/content-pipeline/scripts/context_aggregator.py` to `scripts/context_aggregator.py`.

**Note:** The context aggregator automatically detects any DataOS database in `data/` and pulls richer context (YouTube videos with transcripts, meeting summaries) if available. No configuration needed.

[VERIFY]
```bash
source .venv/bin/activate && python3 scripts/context_aggregator.py
```
Expected: Shows counts for recent content, meetings, and pipeline state.

### Step 5: Copy generate_pipeline.py

Copy `module-installs/content-pipeline/scripts/generate_pipeline.py` to `scripts/generate_pipeline.py`.

```bash
mkdir -p content
source .venv/bin/activate && python3 scripts/generate_pipeline.py
```

[VERIFY]
```bash
cat content/pipeline.md | head -5
```
Expected: Shows "# Content Pipeline" header with today's date.

After Phase 1: "Pipeline scripts are installed: database, writer, context aggregator, and pipeline renderer are all live. Now the fun part, let us figure out YOUR content strategy."

---

## PHASE 2: BRAND & CONTENT WORKSHOP

This is the most important phase. You are running an interactive workshop to produce 3 strategy documents that teach Claude everything about the user's content business.

**Before starting:** Read the user's context files to understand their business:
```bash
ls context/
```
Read `context/business-info.md`, `context/personal-info.md`, and `context/strategy.md` if they exist. Use this knowledge throughout the workshop. Do not ask questions you already know the answer to. Pre-fill what you can from these files.

### Workshop Section 1: Platform & Strategy

Ask the user (adapt based on what you already know from context files):

1. "What is your primary content platform?" (YouTube / LinkedIn / Blog / Podcast / other)
2. "How often do you publish, or want to publish? What is your target cadence?"
3. "What are the 3-5 topic categories (content pillars) you create content about?"
4. "Who are your main competitors or peers in your space? How do you differentiate?"
5. "Any content rules you follow? (e.g., 'never hard-sell', 'always include examples')"
6. "How do you prefer to plan your schedule? Weekly batches, ad-hoc, fixed days?"

**After getting answers:** Write `content/strategy.md` using the `templates/strategy.md` template structure. Fill in everything from the conversation. Show the user the completed doc and ask: "Does this capture your strategy accurately? Anything to change?"

Wait for approval before continuing.

### Workshop Section 2: Brand & Audience

Ask the user:

1. "In one sentence, who are you and what do you do?" (their positioning)
2. "What gives you authority on your topic? What credentials, experience, or results do you have?"
3. "Describe your brand voice: formal or casual? Technical or accessible?"
4. "Let us define your audience segments. Who are the 3-5 distinct types of people you create for?"

For each audience segment, explore:
- Who they are (situation, mindset)
- What they want (desired outcome)
- What they need (what they actually need, often different)
- How to speak to them (language level)

5. "What proof points do you use to build trust? Numbers, results, testimonials?"

**After getting answers:** Write `content/brand-and-audience.md` using the template. Show the user and get approval.

### Workshop Section 3: Offers & Funnels

Ask the user:

1. "What do you sell? Walk me through your offers from free to highest-ticket."
2. "How does someone go from watching/reading your content to becoming a customer? What is the funnel?"
3. "How do you mention your offers in content? Do you pitch directly, or use a softer approach?"
4. "Are there any active campaigns or launches that affect what content you should create right now?"

**After getting answers:** Write `content/offers-and-funnels.md` using the template. Show the user and get approval.

### Workshop Summary

After all sections are complete:

```
Workshop complete! Here is what we built:

content/
  strategy.md           -- Your platform, cadence, pillars, competitive positioning
  brand-and-audience.md -- Your brand positioning and audience segments
  offers-and-funnels.md -- Your offers, funnels, and content-to-revenue mapping
  pipeline.md           -- Auto-generated pipeline view (already live from Phase 1)
```

"These docs are what make your AI smart about YOUR content. Every time you run /develop, Claude reads these to position your content strategically. You can update them anytime as your business evolves."

---

## PHASE 3: COMMANDS

### Step 1: Verify commands exist

The `/capture`, `/develop`, and `/schedule` commands should already be in `.claude/commands/` if the user followed the recommended workspace setup. Check:

```bash
ls .claude/commands/capture.md .claude/commands/develop.md .claude/commands/schedule.md 2>/dev/null
```

If all 3 exist, tell the user: "Your content commands are already installed. Let us verify they are up to date."

If any are missing, copy them from `module-installs/content-pipeline/commands/` (if the commands directory exists in the module) or inform the user they need to create them. The commands are:

- **`/capture`** -- Quick idea capture. Classifies and stores a raw idea as a stub in the pipeline.
- **`/develop`** -- The heavy hitter. Takes a stub and turns it into a full concept with strategic positioning, audience alignment, and platform-specific packaging. Loads the 7-day context window.
- **`/schedule`** -- Batch scheduling. Shows developed ideas ranked by priority, lets you pick what to schedule with dates, and calculates creation deadlines.

### Step 2: Create concepts folder

```bash
mkdir -p content/concepts
```

This is where /develop saves full concept documents.

[VERIFY] Commands and concepts directory:
```bash
ls .claude/commands/capture.md .claude/commands/develop.md .claude/commands/schedule.md && ls -d content/concepts/
```

After Phase 3: "Commands are ready. Let us test the whole system end-to-end."

---

## PHASE 4: TEST THE PIPELINE

### Quick Test: Capture an Idea

Walk the user through capturing their first idea:

"Let us test the pipeline. Give me a content idea, anything you have been thinking about creating."

Use the writer module to capture their idea as a stub:

```python
import sys
sys.path.insert(0, ".")
from scripts.content_db import get_connection
from scripts.writer import write_content_idea

conn = get_connection()
idea_id = write_content_idea(conn, {
    "title": "TEST IDEA TITLE",
    "channel": "TEST CHANNEL",
    "format_type": "post",
    "source_type": "manual",
    "description": "TEST DESCRIPTION"
})
print(f"Captured idea #{idea_id}")
conn.close()
```

Then regenerate the pipeline view:
```bash
source .venv/bin/activate && python3 scripts/generate_pipeline.py
```

Verify:
- The idea was stored in the database
- The pipeline.md was regenerated and shows the new stub

### Clean Up Test Data

After verifying everything works, offer to clean up the test idea:

```python
from scripts.content_db import get_connection
conn = get_connection()
conn.execute("DELETE FROM content_ideas WHERE title LIKE 'TEST%'")
conn.commit()
conn.close()
```

Then regenerate pipeline.md:
```bash
source .venv/bin/activate && python3 scripts/generate_pipeline.py
```

### Update CLAUDE.md

Add the following to the user's CLAUDE.md in an appropriate section (e.g., under Commands or as a new Content Pipeline section):

```markdown
### Content Pipeline

Database: `data/content.db` (content_ideas + published_content tables)
Strategy docs: `content/strategy.md`, `content/brand-and-audience.md`, `content/offers-and-funnels.md`
Pipeline view: `content/pipeline.md` (auto-regenerates)
Concept docs: `content/concepts/` (full developed concepts)

Commands:
- `/capture` -- Quick idea capture and classify
- `/develop` -- Full concept development with strategic positioning
- `/schedule` -- Batch scheduling with date management

Scripts:
- `scripts/content_db.py` -- Database schema and connection
- `scripts/writer.py` -- CRUD functions for content ideas
- `scripts/context_aggregator.py` -- 7-day context window builder
- `scripts/generate_pipeline.py` -- Pipeline markdown renderer
```

### What You Built

Present the final summary:

```
Content Pipeline is live! Here is what is running:

Database:        data/content.db (content_ideas + published_content tables)
Strategy docs:   content/strategy.md, brand-and-audience.md, offers-and-funnels.md
Pipeline view:   content/pipeline.md (auto-regenerates)
Concept docs:    content/concepts/ (full developed concepts)

Commands:
  /capture  -- Quick idea capture and classify
  /develop  -- Full concept development with strategic positioning
  /schedule -- Batch scheduling with date management

Context Window:
  The 7-day aggregator pulls your recent content, meetings, and pipeline
  state every time you run /develop, so Claude is always informed.
```

---

## WHAT IS NEXT

Now that Content Pipeline is running, here are your options:

1. **Start capturing ideas** -- Run `/capture` whenever inspiration strikes. Build up a backlog of stubs.

2. **Develop your best ideas** -- Run `/develop #ID` on your highest-potential stubs. Claude will position them strategically and craft platform-specific packaging.

3. **Schedule a content batch** -- Once you have several developed ideas, run `/schedule` to plan your content calendar and calculate creation deadlines.

4. **Update your strategy** -- Your strategy docs in `content/` are living documents. Update them as your brand, audience, or offers evolve. Claude reads them fresh every time.
