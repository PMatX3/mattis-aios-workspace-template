# Lead Engine

End-to-end lead generation pipeline: scrape leads, AI research, personalised outreach drafts, voice qualification, and call booking.

## Architecture

```
Lead Source CSV (LinkedIn Sales Nav, Apollo, etc.)
        |
        v
  +-------------+
  | enrich_lead |  Claude API: research company, score ICP fit, find pain signals
  +------+------+
         v
  +------------------+
  | generate_outreach |  Claude API: personalised connection request + follow-up
  +------+------------+
         v
  +------------+
  | Airtable    |  Lead Engine table: enriched data + outreach drafts
  +------+------+
         |
    +----+----+
    v         v
 Manual    Vapi Voice
 Review    Qualifier
    |         |
    v         v
 Send on   Books call
 LinkedIn  via CRM
```

## Quick Start

### Prerequisites

```bash
pip install anthropic pyairtable python-dotenv
```

### Environment Variables

Add to your `.env`:

```
ANTHROPIC_API_KEY=sk-ant-...
VAPI_API_KEY=your-vapi-key
AIRTABLE_API_KEY=your-airtable-key
AIRTABLE_BASE_ID=your-base-id
TELEGRAM_BOT_TOKEN=your-bot-token   # Optional, for run notifications
TELEGRAM_CHAT_ID=your-chat-id       # Optional
GHL_API_KEY=your-ghl-key            # Optional, for auto-booking
GHL_LOCATION_ID=your-ghl-location   # Optional
GHL_CALENDAR_ID=your-calendar-id    # Optional
```

### Run the Pipeline

```bash
# Test with sample data
python scripts/lead-engine/run_pipeline.py --test

# Run with real CSV export
python scripts/lead-engine/run_pipeline.py --csv path/to/export.csv

# Run and push to Airtable
python scripts/lead-engine/run_pipeline.py --csv path/to/export.csv --airtable

# Only enrich (no outreach)
python scripts/lead-engine/enrich_lead.py --csv path/to/export.csv

# Only generate outreach (from enrichment results)
python scripts/lead-engine/generate_outreach.py --enriched artifacts/lead-engine/enriched-*.json
```

### Set Up Voice Qualifier

```bash
# 1. Load knowledge base into Open Brain (or skip if not using RAG)
python scripts/lead-engine/load_rag_docs.py

# 2. Deploy the Vapi agent
python scripts/lead-engine/deploy_vapi_agent.py --create

# 3. Start the webhook server (handles booking + qualification logging)
python scripts/lead-engine/webhook_server.py

# 4. Expose webhook via ngrok
ngrok http 3100

# 5. Update agent with ngrok URL
python scripts/lead-engine/deploy_vapi_agent.py --update AGENT_ID --server-url https://xxxx.ngrok.io
```

## Files

| File | Purpose |
|------|---------|
| `run_pipeline.py` | Full pipeline orchestrator (enrich + outreach + Airtable) |
| `enrich_lead.py` | AI lead research and ICP scoring |
| `generate_outreach.py` | Personalised outreach draft generation |
| `load_rag_docs.py` | Load business docs into Open Brain for voice agent |
| `deploy_vapi_agent.py` | Create/update/test the Vapi qualification agent |
| `webhook_server.py` | Handle Vapi tool calls (CRM booking, Airtable updates, Telegram) |
| `vapi_agent_config.json` | Voice agent configuration (system prompt, tools, guardrails) |

## ICP Scoring (template — tune to your business)

Leads are scored 1-10. Customise the scoring rubric in `enrich_lead.py` to match your ICP.

The default rubric is a placeholder — replace it with criteria specific to your offer, sector, and deal size.

**7+** = Hot, **4-6** = Warm, **<4** = Skip

## Outreach Style (template — tune to your voice)

Customise the system prompt in `generate_outreach.py` to match your voice and outreach patterns:
- Connection request length and style
- Follow-up rotations (overflow question, curiosity question, advice give, etc.)
- Sign-off conventions
- Formatting rules (e.g. no em dashes)

## Customisation Notes

This is a template. Three files contain business-specific content that you must adapt:

1. `enrich_lead.py` — `ICP_SCORING_RUBRIC` and `ENRICHMENT_SYSTEM_PROMPT`
2. `generate_outreach.py` — `OUTREACH_SYSTEM_PROMPT`
3. `vapi_agent_config.json` — voice agent system message
4. `load_rag_docs.py` — `RAG_DOCUMENTS` knowledge base content

Replace the placeholder content with your actual ICP, voice, and business details before running against real leads.
