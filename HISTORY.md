# Workspace History

> Chronological log of all work done in this workspace. Updated every session.
> Most recent entries at the top. Each entry has a date, title, and bullet points.
>
> **How it works:** When you run `/commit` after meaningful work, Claude adds an entry here
> automatically. You don't need to write this file yourself.

---

## 2026-05-01

### Lead Engine Framework Added
- New `scripts/lead-engine/` directory with end-to-end lead generation pipeline (CSV → AI enrichment → personalised outreach → Vapi voice qualification → CRM booking)
- 7 components: orchestrator, enrichment + ICP scoring, outreach drafting, Vapi webhook handler, agent deployment CLI, RAG loader, voice agent config
- ICP rubric, outreach voice, voice agent prompt, and RAG content are placeholders — users customise to their business before running
- New `scripts/config.py` shared env loader

## 2026-03-28

### Template Initialized
- Workspace template created with core structure: context, plans, outputs, reference, scripts, artifacts
- Self-documenting system installed: docs/_index.md, docs/_templates/, HISTORY.md, DESIGN.md
