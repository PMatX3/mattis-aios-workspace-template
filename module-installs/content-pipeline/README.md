# Content Pipeline Module

A content intelligence system that turns scattered ideas into a strategic pipeline. Capture, develop, and schedule content with AI that understands your brand, audience, and business goals.

## What It Does

Content Pipeline gives you a structured workflow for content creation:

1. **Capture** -- Drop raw ideas into your pipeline with `/capture`. Each idea gets classified by channel, format, content pillar, and audience segment.

2. **Develop** -- Turn stubs into full concepts with `/develop`. Claude reads your strategy docs and a 7-day context window (recent content, meetings, pipeline state) to position each idea strategically. Outputs include audience alignment, funnel positioning, offer alignment, and platform-specific packaging.

3. **Schedule** -- Plan your content calendar with `/schedule`. Pick developed ideas, assign publish dates, and the system calculates creation deadlines based on your format turnaround times.

Everything is stored in a SQLite database (`data/content.db`) and rendered as a browsable markdown pipeline (`content/pipeline.md`).

## What Gets Installed

**Scripts** (copied to `scripts/`):
- `content_db.py` -- Database schema, connection helpers, initialization
- `writer.py` -- CRUD functions for content ideas (capture, develop, update status)
- `context_aggregator.py` -- Builds the 7-day context window from your database(s)
- `generate_pipeline.py` -- Renders the pipeline as browsable markdown

**Strategy Docs** (created during workshop in `content/`):
- `strategy.md` -- Platform, cadence, content pillars, competitive positioning
- `brand-and-audience.md` -- Brand voice, positioning, audience segments
- `offers-and-funnels.md` -- Offer ladder, content-to-revenue funnel, CTA strategy

**Directories:**
- `content/` -- Strategy docs and pipeline view
- `content/concepts/` -- Full concept documents from `/develop`

**Commands** (expected in `.claude/commands/`):
- `capture.md` -- Quick idea capture
- `develop.md` -- Full concept development
- `schedule.md` -- Batch scheduling

## Prerequisites

- Python 3.10+
- A virtual environment (`.venv`)
- A `data/` directory

## Estimated Setup Time

**30-45 minutes.** The script installation takes about 5 minutes. The rest is the Brand & Content Workshop, an interactive session where Claude interviews you about your business, content strategy, audience, and offers to produce customized strategy documents. These docs are what make every `/develop` run strategically informed rather than generic.

## How to Install

Run `/install module-installs/content-pipeline` in Claude Code. Claude will walk you through everything step by step.
