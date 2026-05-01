"""
Outreach Draft Generator — AIOS Lead Engine

Takes enriched lead data and generates personalised connection requests
and follow-up messages matching your voice and style.

Usage:
    python scripts/lead-engine/generate_outreach.py --enriched path/to/enriched.json
    python scripts/lead-engine/generate_outreach.py --test  # Run with sample data

Output: Outreach drafts as JSON (stdout) or pushed to Airtable (--airtable flag)
"""

import json
import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_env

try:
    import anthropic
except ImportError:
    print("Install anthropic SDK: pip install anthropic")
    sys.exit(1)


# CUSTOMISE THIS — this prompt defines your outreach voice. Replace with your style.
OUTREACH_SYSTEM_PROMPT = """You are a ghostwriter for [Founder Name], founder of [Your Agency].

Outreach style:
- Connection requests are SHORT (under 300 characters total)
- Always references something specific from the person's profile, post, or company
- Signs off with just "[Founder Name]"
- Tone: direct, warm, peer-to-peer (not salesy, not corporate)
- Never uses em dashes
- Never uses buzzwords like "synergy", "leverage", "revolutionise"

Follow-up patterns (rotate between these 3 styles):
1. OVERFLOW QUESTION: A short question about whether the lead has a delivery gap that matches your offer.
2. CURIOSITY QUESTION: Ask about their tools, process, or how they handle scope. Genuine interest, not qualifying.
3. ADVICE GIVE: Offer free, specific, useful advice with no pitch. Only for newer founders.

Rules:
- Connection request must be under 300 characters
- Follow-up must be under 500 characters
- Never use em dashes
- Never mention pricing
- Never sound automated or templated
- Reference specific details from the enrichment data
- The connection request should NOT pitch. It should give a reason to connect.
- The follow-up should feel like a natural second message, not a sales email

Respond with valid JSON only:
{
    "connection_request": "Hi [Name], ...",
    "follow_up_message": "Hey [Name], ...",
    "follow_up_style": "overflow|curiosity|advice",
    "notes": "Any context about why this approach was chosen"
}
"""


def generate_outreach(client: anthropic.Anthropic, enriched_lead: dict) -> dict:
    """Generate outreach drafts for a single enriched lead."""
    lead = enriched_lead.get("original_lead", {})
    first_name = lead.get("name", "").split()[0] if lead.get("name") else "there"

    context = f"""
Lead details:
- Name: {lead.get('name', 'Unknown')}
- First name: {first_name}
- Company: {lead.get('company', 'Unknown')}
- Title: {lead.get('title', 'Unknown')}
- Location: {lead.get('location', 'Unknown')}
- Headline: {lead.get('headline', 'N/A')}
- About: {lead.get('about', 'N/A')}

AI enrichment:
- Company summary: {enriched_lead.get('company_summary', 'N/A')}
- ICP score: {enriched_lead.get('icp_fit_score', 'N/A')}/10
- ICP reason: {enriched_lead.get('icp_fit_reason', 'N/A')}
- Pain signals: {', '.join(enriched_lead.get('pain_signals', []))}
- Lead tier: {enriched_lead.get('lead_tier', 'N/A')}
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=OUTREACH_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Write a connection request and follow-up for this lead:\n{context}",
            }
        ],
    )

    try:
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3].strip()
        result = json.loads(text)
        result["lead_name"] = lead.get("name", "Unknown")
        result["lead_company"] = lead.get("company", "Unknown")
        result["icp_score"] = enriched_lead.get("icp_fit_score", 0)

        cr_len = len(result.get("connection_request", ""))
        if cr_len > 300:
            result["warning"] = f"Connection request is {cr_len} chars (limit 300)"

        return result
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse outreach response",
            "raw_response": response.content[0].text,
            "lead_name": lead.get("name", "Unknown"),
        }


def get_sample_enriched() -> list[dict]:
    """Sample enriched leads for testing outreach generation."""
    return [
        {
            "company_summary": "Sample Co is a placeholder company used for testing the outreach generator.",
            "icp_fit_score": 9,
            "icp_fit_reason": "Strong placeholder fit. Replace with real enrichment data when integrating with your ICP.",
            "pain_signals": ["Sample signal 1", "Sample signal 2"],
            "personalised_opener": "Hi Alex, sample personalised opener referencing their profile.",
            "lead_tier": "hot",
            "original_lead": {
                "name": "Alex Sample",
                "company": "Sample Co",
                "title": "Founder & CEO",
                "linkedin_url": "https://linkedin.com/in/sample-alex",
                "location": "London, UK",
                "industry": "Sample Industry",
                "headline": "Sample headline describing what they do",
                "about": "Sample about section.",
            },
        },
    ]


def main():
    parser = argparse.ArgumentParser(description="Generate personalised outreach drafts")
    parser.add_argument("--enriched", help="Path to enriched leads JSON file")
    parser.add_argument("--test", action="store_true", help="Run with sample data")
    parser.add_argument("--airtable", action="store_true", help="Update Airtable with drafts")
    parser.add_argument("--output", help="Output JSON file path (default: stdout)")
    parser.add_argument("--min-score", type=int, default=4, help="Minimum ICP score to generate outreach for (default: 4)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between API calls (default: 2.0)")
    args = parser.parse_args()

    if not args.enriched and not args.test:
        parser.print_help()
        print("\nProvide --enriched with enrichment results or --test for sample data.")
        sys.exit(1)

    api_key = get_env("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    if args.test:
        enriched_leads = get_sample_enriched()
        print(f"Running outreach generation on {len(enriched_leads)} sample leads...\n")
    else:
        with open(args.enriched, "r") as f:
            enriched_leads = json.load(f)
        print(f"Loaded {len(enriched_leads)} enriched leads.\n")

    qualified = [
        lead for lead in enriched_leads
        if lead.get("icp_fit_score", 0) >= args.min_score and "error" not in lead
    ]
    skipped = len(enriched_leads) - len(qualified)
    if skipped > 0:
        print(f"Skipping {skipped} leads below ICP score {args.min_score}.\n")

    results = []
    for i, lead in enumerate(qualified):
        name = lead.get("original_lead", {}).get("name", "Unknown")
        print(f"[{i+1}/{len(qualified)}] Generating outreach for: {name}...")

        try:
            outreach = generate_outreach(client, lead)
            results.append(outreach)

            if "error" not in outreach:
                cr = outreach.get("connection_request", "")
                style = outreach.get("follow_up_style", "unknown")
                print(f"  Style: {style} | CR length: {len(cr)} chars")
                if outreach.get("warning"):
                    print(f"  WARNING: {outreach['warning']}")
            else:
                print(f"  ERROR: {outreach['error']}")

        except Exception as e:
            print(f"  FAILED: {e}")
            results.append({"error": str(e), "lead_name": name})

        if i < len(qualified) - 1:
            time.sleep(args.delay)

    output_json = json.dumps(results, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output_json)
        print(f"\nResults saved to {args.output}")
    else:
        print(f"\n{'='*60}")
        print("OUTREACH DRAFTS")
        print(f"{'='*60}")
        for r in results:
            if "error" in r:
                continue
            print(f"\n--- {r.get('lead_name', 'Unknown')} ({r.get('lead_company', '')}) ---")
            print(f"CONNECTION REQUEST ({len(r.get('connection_request', ''))} chars):")
            print(f"  {r.get('connection_request', '')}")
            print(f"\nFOLLOW-UP ({r.get('follow_up_style', 'unknown')}):")
            print(f"  {r.get('follow_up_message', '')}")
            print()

    if args.airtable:
        push_outreach_to_airtable(results)

    return results


def push_outreach_to_airtable(results: list[dict]):
    """Update Airtable Lead Engine records with outreach drafts."""
    try:
        from pyairtable import Api
    except ImportError:
        print("Install pyairtable: pip install pyairtable")
        return

    api_key = get_env("AIRTABLE_API_KEY")
    base_id = get_env("AIRTABLE_BASE_ID")
    table_name = get_env("AIRTABLE_TABLE_NAME") or "Lead Engine"

    api = Api(api_key)
    table = api.table(base_id, table_name)

    records = []
    for r in results:
        if "error" in r:
            continue
        records.append(
            {
                "fields": {
                    "Name": r.get("lead_name", ""),
                    "Connection Request Draft": r.get("connection_request", ""),
                    "Follow-Up Draft": r.get("follow_up_message", ""),
                    "Follow-Up Style": r.get("follow_up_style", ""),
                }
            }
        )

    if records:
        table.batch_upsert(records, key_fields=["Name"], typecast=True)
        print(f"\nUpdated {len(records)} records in Airtable with outreach drafts.")


if __name__ == "__main__":
    main()
