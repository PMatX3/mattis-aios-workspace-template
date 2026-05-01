"""
Webhook Server — AIOS Lead Engine

Handles Vapi tool calls for the voice qualifier:
- bookDiscoveryCall: Books a call via CRM calendar API (e.g. GHL, HubSpot)
- logQualification: Updates Airtable + sends Telegram notification

Usage:
    python scripts/lead-engine/webhook_server.py          # Start on port 3100
    python scripts/lead-engine/webhook_server.py --port 8080

Expose via ngrok for Vapi:
    ngrok http 3100
    Then set the ngrok URL as serverUrl in the Vapi agent config.
"""

import json
import sys
import argparse
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_env


def send_telegram(message: str):
    """Send a notification via Telegram."""
    try:
        bot_token = get_env("TELEGRAM_BOT_TOKEN", required=False)
        chat_id = get_env("TELEGRAM_CHAT_ID", required=False)
        if not bot_token or not chat_id:
            print("Telegram not configured, skipping notification")
            return

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = json.dumps({
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }).encode()

        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=10)
        print(f"Telegram notification sent")
    except Exception as e:
        print(f"Telegram error: {e}")


def book_crm_appointment(caller_name: str, company_name: str, preferred_day: str = None, context: str = ""):
    """Book a discovery call via CRM calendar API. Replace GHL with your CRM if needed."""
    try:
        api_key = get_env("GHL_API_KEY")
        location_id = get_env("GHL_LOCATION_ID")
        calendar_id = get_env("GHL_CALENDAR_ID", required=False) or ""

        if not calendar_id:
            print("CRM calendar ID not set. Logging booking request for manual follow-up.")
            return {
                "success": False,
                "message": f"Booking request logged. We'll reach out to {caller_name} at {company_name} to schedule.",
                "manual_follow_up": True,
            }

        # Create contact in CRM if not exists (example uses GHL — adapt for your CRM)
        contact_url = f"https://services.leadconnectorhq.com/contacts/"
        contact_data = json.dumps({
            "locationId": location_id,
            "name": caller_name,
            "companyName": company_name,
            "tags": ["lead-engine", "voice-qualified"],
            "source": "Lead Engine",
        }).encode()

        contact_req = urllib.request.Request(
            contact_url,
            data=contact_data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Version": "2021-07-28",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(contact_req, timeout=15) as resp:
                contact_result = json.loads(resp.read())
                contact_id = contact_result.get("contact", {}).get("id", "")
                print(f"CRM contact created/found: {contact_id}")
        except Exception as e:
            print(f"CRM contact creation error (may already exist): {e}")
            contact_id = ""

        return {
            "success": True,
            "message": f"I've noted down your details. We'll send you a calendar link for a 15-minute call. What's the best email to send that to?",
            "contact_id": contact_id,
        }

    except Exception as e:
        print(f"CRM booking error: {e}")
        return {
            "success": False,
            "message": "I'll have the team reach out directly to schedule. What's the best way to contact you?",
            "error": str(e),
        }


def log_qualification(caller_name: str, qualified: bool, reason: str, business_type: str = "", delivery_needs: str = ""):
    """Log qualification result and send notification."""
    status = "Qualified" if qualified else "Not Qualified"
    emoji = "+" if qualified else "-"

    msg = f"""*Lead Engine: New {status} Lead*

{emoji} *{caller_name}*
Business: {business_type or 'Unknown'}
{f'Delivery needs: {delivery_needs}' if delivery_needs else ''}
Reason: {reason}"""

    if qualified:
        msg += "\n\nAction: Book discovery call"

    send_telegram(msg)

    try:
        from pyairtable import Api
        api_key = get_env("AIRTABLE_API_KEY", required=False)
        base_id = get_env("AIRTABLE_BASE_ID", required=False)
        if api_key and base_id:
            api = Api(api_key)
            table = api.table(base_id, "Lead Engine")
            table.batch_upsert(
                [
                    {
                        "fields": {
                            "Name": caller_name,
                            "Status": status,
                            "Qualification Reason": reason,
                            "Business Type": business_type,
                            "Delivery Needs": delivery_needs,
                        }
                    }
                ],
                key_fields=["Name"],
                typecast=True,
            )
            print(f"Airtable updated: {caller_name} -> {status}")
    except ImportError:
        print("pyairtable not installed, skipping Airtable update")
    except Exception as e:
        print(f"Airtable update error: {e}")

    return {"logged": True, "status": status}


class VapiWebhookHandler(BaseHTTPRequestHandler):
    """Handles incoming webhook requests from Vapi."""

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        message_type = payload.get("message", {}).get("type", "")

        if message_type == "function-call":
            function_call = payload.get("message", {}).get("functionCall", {})
            fn_name = function_call.get("name", "")
            fn_params = function_call.get("parameters", {})

            print(f"\nVapi function call: {fn_name}")
            print(f"Parameters: {json.dumps(fn_params, indent=2)}")

            if fn_name == "bookDiscoveryCall":
                result = book_crm_appointment(
                    caller_name=fn_params.get("callerName", ""),
                    company_name=fn_params.get("companyName", ""),
                    preferred_day=fn_params.get("preferredDay", ""),
                    context=fn_params.get("context", ""),
                )
            elif fn_name == "logQualification":
                result = log_qualification(
                    caller_name=fn_params.get("callerName", ""),
                    qualified=fn_params.get("qualified", False),
                    reason=fn_params.get("reason", ""),
                    business_type=fn_params.get("businessType", ""),
                    delivery_needs=fn_params.get("deliveryNeeds", ""),
                )
            else:
                result = {"error": f"Unknown function: {fn_name}"}

            response = {"result": json.dumps(result)}
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            return

        if message_type == "end-of-call-report":
            report = payload.get("message", {})
            transcript = report.get("transcript", "")
            duration = report.get("duration", 0)
            ended_reason = report.get("endedReason", "")

            print(f"\nCall ended: duration={duration}s, reason={ended_reason}")

            summary_msg = f"""*Lead Engine: Call Complete*
Duration: {duration}s
Ended: {ended_reason}
Transcript length: {len(transcript)} chars"""
            send_telegram(summary_msg)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"received": true}')
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"received": true}')

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="Vapi webhook server for Lead Engine")
    parser.add_argument("--port", type=int, default=3100, help="Port to listen on (default: 3100)")
    args = parser.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), VapiWebhookHandler)
    print(f"Lead Engine webhook server running on port {args.port}")
    print(f"Expose with: ngrok http {args.port}")
    print("Waiting for Vapi calls...\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()


if __name__ == "__main__":
    main()
