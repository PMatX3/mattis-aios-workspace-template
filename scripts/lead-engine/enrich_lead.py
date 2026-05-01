"""
Lead Enrichment Script — AIOS Lead Engine

Takes lead data (name, company, title, LinkedIn URL) and uses Claude API
to research and score each lead against your ICP.

Usage:
    python scripts/lead-engine/enrich_lead.py --csv path/to/leads.csv
    python scripts/lead-engine/enrich_lead.py --test  # Run with sample data

Output: Enriched leads as JSON (stdout) or pushed to Airtable (--airtable flag)
"""

import json
import sys
import csv
import time
import argparse
from pathlib import Path

# Add parent dir for shared config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_env

try:
    import anthropic
except ImportError:
    print("Install anthropic SDK: pip install anthropic")
    sys.exit(1)


# CUSTOMISE THIS — replace with your actual ICP scoring criteria
ICP_SCORING_RUBRIC = """
Score each lead 1-10 based on these criteria (add points):
+3: [Primary ICP signal — e.g. "founder of a target-sector business"]
+2: [Secondary signal — e.g. "company size matches sweet spot"]
+2: [Buying intent signal — e.g. "active in relevant communities"]
+1: [Geographic preference — e.g. "based in target markets"]
+1: [Engagement signal — e.g. "posts about relevant topics"]
-2: [Disqualifier — e.g. "wrong-shape role"]
-2: [Disqualifier — e.g. "no clear fit signal"]
-1: [Soft disqualifier — e.g. "early-career, no buying authority"]

Score 7+: Hot lead (prioritise outreach)
Score 4-6: Warm lead (worth connecting)
Score below 4: Skip
"""

# CUSTOMISE THIS — replace [Your Agency] and the positioning sentence
ENRICHMENT_SYSTEM_PROMPT = f"""You are a lead research assistant for [Your Agency], a [one-line positioning of your business].

Your job is to analyse a lead's profile data and produce a structured enrichment report.

{ICP_SCORING_RUBRIC}

You MUST respond with valid JSON only. No markdown, no explanation, just the JSON object.

JSON schema:
{{
    "company_summary": "What this company does in 1-2 sentences",
    "icp_fit_score": 8,
    "icp_fit_reason": "One sentence explaining why they match or don't match the ICP",
    "pain_signals": ["Signal 1", "Signal 2"],
    "personalised_opener": "Hi [FirstName], [one specific observation about their profile or company].",
    "lead_tier": "hot|warm|skip"
}}

Rules:
- Be specific. Reference actual details from their profile, not generic observations.
- The personalised_opener must reference something specific to THIS person.
- Never use em dashes in any output. Use commas, colons, or full stops instead.
- Keep the opener under 200 characters.
- pain_signals should identify real delivery gaps, not generic business challenges.
"""


def enrich_lead(client: anthropic.Anthropic, lead: dict) -> dict:
    """Enrich a single lead with AI research."""
    lead_context = f"""
Name: {lead.get('name', 'Unknown')}
Company: {lead.get('company', 'Unknown')}
Title: {lead.get('title', 'Unknown')}
LinkedIn URL: {lead.get('linkedin_url', 'N/A')}
Location: {lead.get('location', 'Unknown')}
Industry: {lead.get('industry', 'Unknown')}
Headline: {lead.get('headline', 'N/A')}
About: {lead.get('about', 'N/A')}
"""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=ENRICHMENT_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Research and score this lead:\n{lead_context}",
            }
        ],
    )

    try:
        text = response.content[0].text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3].strip()
        result = json.loads(text)
        result["original_lead"] = lead
        return result
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse enrichment response",
            "raw_response": response.content[0].text,
            "original_lead": lead,
        }


def load_csv_leads(csv_path: str) -> list[dict]:
    """Load leads from a CSV export (LinkedIn Sales Nav, Apollo, etc.)."""
    leads = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lead = {
                "name": row.get("First Name", "") + " " + row.get("Last Name", ""),
                "company": row.get("Company", row.get("Company Name", "")),
                "title": row.get("Title", row.get("Job Title", "")),
                "linkedin_url": row.get(
                    "LinkedIn URL", row.get("Profile URL", row.get("Url", ""))
                ),
                "location": row.get("Location", row.get("Geography", "")),
                "industry": row.get("Industry", ""),
                "headline": row.get("Headline", ""),
                "about": row.get("Summary", row.get("About", "")),
            }
            lead["name"] = lead["name"].strip()
            if lead["name"]:
                leads.append(lead)
    return leads


def get_sample_leads() -> list[dict]:
    """Sample leads for testing the enrichment pipeline."""
    return [
        {
            "name": "Alex Sample",
            "company": "Sample Co",
            "title": "Founder & CEO",
            "linkedin_url": "https://linkedin.com/in/sample-alex",
            "location": "London, UK",
            "industry": "Sample Industry",
            "headline": "Sample headline describing what they do",
            "about": "Sample about section. Replace with realistic test data that matches your ICP.",
        },
        {
            "name": "Sam Example",
            "company": "Example Ltd",
            "title": "Operations Manager",
            "linkedin_url": "https://linkedin.com/in/sample-example",
            "location": "Manchester, UK",
            "industry": "Sample Industry",
            "headline": "Sample headline for a non-ICP-fit lead",
            "about": "Sample about for testing the disqualifier path of your scoring rubric.",
        },
    ]


def main():
    parser = argparse.ArgumentParser(description="Enrich leads with AI research")
    parser.add_argument("--csv", help="Path to lead source CSV export")
    parser.add_argument("--test", action="store_true", help="Run with sample data")
    parser.add_argument("--airtable", action="store_true", help="Push results to Airtable")
    parser.add_argument("--output", help="Output JSON file path (default: stdout)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between API calls in seconds (default: 2.0)")
    args = parser.parse_args()

    if not args.csv and not args.test:
        parser.print_help()
        print("\nProvide --csv with a CSV export or --test for sample data.")
        sys.exit(1)

    api_key = get_env("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    if args.test:
        leads = get_sample_leads()
        print(f"Running enrichment on {len(leads)} sample leads...\n")
    else:
        leads = load_csv_leads(args.csv)
        print(f"Loaded {len(leads)} leads from CSV.\n")

    results = []
    for i, lead in enumerate(leads):
        print(f"[{i+1}/{len(leads)}] Enriching: {lead['name']} at {lead['company']}...")
        try:
            enriched = enrich_lead(client, lead)
            results.append(enriched)

            if "error" not in enriched:
                score = enriched.get("icp_fit_score", 0)
                tier = enriched.get("lead_tier", "unknown")
                print(f"  Score: {score}/10 ({tier}) - {enriched.get('icp_fit_reason', '')}")
            else:
                print(f"  ERROR: {enriched['error']}")

        except Exception as e:
            print(f"  FAILED: {e}")
            results.append({"error": str(e), "original_lead": lead})

        if i < len(leads) - 1:
            time.sleep(args.delay)

    output_json = json.dumps(results, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(output_json)
        print(f"\nResults saved to {args.output}")
    else:
        print(f"\n{'='*60}")
        print("ENRICHMENT RESULTS")
        print(f"{'='*60}")
        print(output_json)

    hot = sum(1 for r in results if r.get("lead_tier") == "hot")
    warm = sum(1 for r in results if r.get("lead_tier") == "warm")
    skip = sum(1 for r in results if r.get("lead_tier") == "skip")
    errors = sum(1 for r in results if "error" in r)
    print(f"\nSummary: {hot} hot, {warm} warm, {skip} skip, {errors} errors out of {len(results)} leads")

    if args.airtable:
        push_to_airtable(results)

    return results


def push_to_airtable(results: list[dict]):
    """Push enriched leads to Airtable Lead Engine table."""
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
        lead = r.get("original_lead", {})
        records.append(
            {
                "fields": {
                    "Name": lead.get("name", ""),
                    "Company": lead.get("company", ""),
                    "Title": lead.get("title", ""),
                    "LinkedIn URL": lead.get("linkedin_url", ""),
                    "Location": lead.get("location", ""),
                    "ICP Score": r.get("icp_fit_score", 0),
                    "ICP Reason": r.get("icp_fit_reason", ""),
                    "Company Summary": r.get("company_summary", ""),
                    "Pain Signals": ", ".join(r.get("pain_signals", [])),
                    "Personalised Opener": r.get("personalised_opener", ""),
                    "Lead Tier": r.get("lead_tier", ""),
                    "Status": "New",
                }
            }
        )

    if records:
        table.batch_upsert(records, key_fields=["LinkedIn URL"], typecast=True)
        print(f"\nPushed {len(records)} enriched leads to Airtable '{table_name}' table.")
    else:
        print("\nNo valid records to push to Airtable.")


if __name__ == "__main__":
    main()
