"""
Lead Engine Pipeline — Full Run

Orchestrates the complete pipeline:
1. Load leads from CSV
2. Enrich each lead with AI research
3. Generate personalised outreach drafts
4. Push everything to Airtable

Usage:
    python scripts/lead-engine/run_pipeline.py --csv path/to/leads.csv
    python scripts/lead-engine/run_pipeline.py --test  # Sample data
    python scripts/lead-engine/run_pipeline.py --csv leads.csv --airtable

The voice qualifier runs separately via webhook_server.py + Vapi.
"""

import json
import sys
import argparse
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_env

from enrich_lead import enrich_lead, load_csv_leads, get_sample_leads, push_to_airtable
from generate_outreach import generate_outreach, push_outreach_to_airtable

try:
    import anthropic
except ImportError:
    print("Install anthropic SDK: pip install anthropic")
    sys.exit(1)


def send_telegram_summary(stats: dict):
    """Send pipeline run summary to Telegram."""
    import urllib.request

    try:
        bot_token = get_env("TELEGRAM_BOT_TOKEN", required=False)
        chat_id = get_env("TELEGRAM_CHAT_ID", required=False)
        if not bot_token or not chat_id:
            return

        msg = f"""*Lead Engine Pipeline Complete*

Leads processed: {stats['total']}
Hot (7+): {stats['hot']}
Warm (4-6): {stats['warm']}
Skip (<4): {stats['skip']}
Errors: {stats['errors']}
Outreach drafted: {stats['outreach_generated']}

Run time: {stats['duration_seconds']:.0f}s"""

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Telegram notification error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Run the full Lead Engine pipeline")
    parser.add_argument("--csv", help="Path to lead source CSV export")
    parser.add_argument("--test", action="store_true", help="Run with sample data")
    parser.add_argument("--airtable", action="store_true", help="Push results to Airtable")
    parser.add_argument("--output-dir", default="artifacts/lead-engine", help="Output directory for results")
    parser.add_argument("--min-score", type=int, default=4, help="Minimum ICP score for outreach (default: 4)")
    parser.add_argument("--delay", type=float, default=2.0, help="Delay between API calls (default: 2.0)")
    args = parser.parse_args()

    if not args.csv and not args.test:
        parser.print_help()
        print("\nProvide --csv with a CSV export or --test for sample data.")
        sys.exit(1)

    start_time = time.time()

    # Setup
    api_key = get_env("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Step 1: Load leads
    print("=" * 60)
    print("STEP 1: Loading leads")
    print("=" * 60)

    if args.test:
        leads = get_sample_leads()
    else:
        leads = load_csv_leads(args.csv)

    print(f"Loaded {len(leads)} leads.\n")

    # Step 2: Enrich leads
    print("=" * 60)
    print("STEP 2: AI Research + Enrichment")
    print("=" * 60)

    enriched_results = []
    for i, lead in enumerate(leads):
        name = lead.get("name", "Unknown")
        print(f"[{i+1}/{len(leads)}] Enriching: {name}...")

        try:
            enriched = enrich_lead(client, lead)
            enriched_results.append(enriched)

            if "error" not in enriched:
                score = enriched.get("icp_fit_score", 0)
                tier = enriched.get("lead_tier", "unknown")
                print(f"  Score: {score}/10 ({tier})")
            else:
                print(f"  ERROR: {enriched['error']}")
        except Exception as e:
            print(f"  FAILED: {e}")
            enriched_results.append({"error": str(e), "original_lead": lead})

        if i < len(leads) - 1:
            time.sleep(args.delay)

    # Save enrichment results
    enriched_path = output_dir / f"enriched-{timestamp}.json"
    enriched_path.write_text(json.dumps(enriched_results, indent=2, ensure_ascii=False))
    print(f"\nEnrichment results saved to {enriched_path}")

    # Step 3: Generate outreach for qualified leads
    print(f"\n{'=' * 60}")
    print("STEP 3: Outreach Draft Generation")
    print("=" * 60)

    qualified = [
        r for r in enriched_results
        if r.get("icp_fit_score", 0) >= args.min_score and "error" not in r
    ]
    print(f"Generating outreach for {len(qualified)} leads (score >= {args.min_score}).\n")

    outreach_results = []
    for i, lead in enumerate(qualified):
        name = lead.get("original_lead", {}).get("name", "Unknown")
        print(f"[{i+1}/{len(qualified)}] Drafting outreach for: {name}...")

        try:
            outreach = generate_outreach(client, lead)
            outreach_results.append(outreach)

            if "error" not in outreach:
                style = outreach.get("follow_up_style", "unknown")
                cr_len = len(outreach.get("connection_request", ""))
                print(f"  Style: {style} | CR: {cr_len} chars")
            else:
                print(f"  ERROR: {outreach['error']}")
        except Exception as e:
            print(f"  FAILED: {e}")
            outreach_results.append({"error": str(e), "lead_name": name})

        if i < len(qualified) - 1:
            time.sleep(args.delay)

    # Save outreach results
    outreach_path = output_dir / f"outreach-{timestamp}.json"
    outreach_path.write_text(json.dumps(outreach_results, indent=2, ensure_ascii=False))
    print(f"\nOutreach drafts saved to {outreach_path}")

    # Step 4: Push to Airtable if requested
    if args.airtable:
        print(f"\n{'=' * 60}")
        print("STEP 4: Pushing to Airtable")
        print("=" * 60)
        push_to_airtable(enriched_results)
        push_outreach_to_airtable(outreach_results)

    # Summary
    duration = time.time() - start_time
    hot = sum(1 for r in enriched_results if r.get("lead_tier") == "hot")
    warm = sum(1 for r in enriched_results if r.get("lead_tier") == "warm")
    skip = sum(1 for r in enriched_results if r.get("lead_tier") == "skip")
    errors = sum(1 for r in enriched_results if "error" in r)
    outreach_ok = sum(1 for r in outreach_results if "error" not in r)

    stats = {
        "total": len(leads),
        "hot": hot,
        "warm": warm,
        "skip": skip,
        "errors": errors,
        "outreach_generated": outreach_ok,
        "duration_seconds": duration,
    }

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")
    print(f"Total leads:       {stats['total']}")
    print(f"Hot (7+):          {stats['hot']}")
    print(f"Warm (4-6):        {stats['warm']}")
    print(f"Skip (<4):         {stats['skip']}")
    print(f"Errors:            {stats['errors']}")
    print(f"Outreach drafted:  {stats['outreach_generated']}")
    print(f"Duration:          {stats['duration_seconds']:.0f}s")
    print(f"\nOutputs:")
    print(f"  Enrichment: {enriched_path}")
    print(f"  Outreach:   {outreach_path}")

    # Print outreach drafts for review
    print(f"\n{'=' * 60}")
    print("OUTREACH DRAFTS FOR REVIEW")
    print(f"{'=' * 60}")
    for r in outreach_results:
        if "error" in r:
            continue
        print(f"\n--- {r.get('lead_name', 'Unknown')} ({r.get('lead_company', '')}) | ICP: {r.get('icp_score', '?')}/10 ---")
        print(f"CONNECTION REQUEST:")
        print(f"  {r.get('connection_request', '')}")
        print(f"FOLLOW-UP ({r.get('follow_up_style', '')}):")
        print(f"  {r.get('follow_up_message', '')}")

    # Send Telegram summary
    send_telegram_summary(stats)

    return stats


if __name__ == "__main__":
    main()
