"""
Deploy Vapi Agent — AIOS Lead Engine

Creates or updates the Vapi voice qualification agent using the API.

Usage:
    python scripts/lead-engine/deploy_vapi_agent.py                    # Create agent
    python scripts/lead-engine/deploy_vapi_agent.py --update AGENT_ID  # Update existing
    python scripts/lead-engine/deploy_vapi_agent.py --list             # List agents
    python scripts/lead-engine/deploy_vapi_agent.py --test AGENT_ID    # Test call

Requires: VAPI_API_KEY in .env
"""

import json
import sys
import argparse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import get_env

VAPI_BASE = "https://api.vapi.ai"
CONFIG_PATH = Path(__file__).parent / "vapi_agent_config.json"


def vapi_request(method: str, path: str, data: dict = None) -> dict:
    """Make a request to the Vapi API."""
    api_key = get_env("VAPI_API_KEY")
    url = f"{VAPI_BASE}{path}"

    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method=method,
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"Vapi API error ({e.code}): {error_body}")
        sys.exit(1)


def load_config() -> dict:
    """Load the Vapi agent config and prepare it for API submission."""
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    config.pop("_notes", None)
    return config


def create_agent(server_url: str = None):
    """Create a new Vapi agent."""
    config = load_config()

    if server_url:
        config["serverUrl"] = server_url
        print(f"Server URL set to: {server_url}")

    print(f"Creating Vapi agent: {config['name']}...")
    result = vapi_request("POST", "/assistant", config)

    agent_id = result.get("id", "unknown")
    print(f"\nAgent created successfully!")
    print(f"  Agent ID: {agent_id}")
    print(f"  Name: {result.get('name', '')}")
    print(f"\nSave this agent ID. You'll need it for updates and testing.")
    print(f"\nTo test: python scripts/lead-engine/deploy_vapi_agent.py --test {agent_id}")

    id_path = Path(__file__).parent / ".vapi_agent_id"
    id_path.write_text(agent_id)
    print(f"Agent ID saved to {id_path}")

    return result


def update_agent(agent_id: str, server_url: str = None):
    """Update an existing Vapi agent."""
    config = load_config()

    if server_url:
        config["serverUrl"] = server_url

    print(f"Updating Vapi agent: {agent_id}...")
    result = vapi_request("PATCH", f"/assistant/{agent_id}", config)

    print(f"Agent updated successfully!")
    print(f"  Name: {result.get('name', '')}")
    return result


def list_agents():
    """List all Vapi agents."""
    result = vapi_request("GET", "/assistant")

    if not result:
        print("No agents found.")
        return

    print(f"Found {len(result)} agents:\n")
    for agent in result:
        print(f"  ID: {agent.get('id', 'unknown')}")
        print(f"  Name: {agent.get('name', 'unnamed')}")
        print(f"  Created: {agent.get('createdAt', 'unknown')}")
        print()


def test_call(agent_id: str, phone_number: str = None):
    """Trigger a test call to the Vapi agent."""
    if phone_number:
        data = {
            "assistantId": agent_id,
            "customer": {"number": phone_number},
        }
        print(f"Starting outbound test call to {phone_number}...")
        result = vapi_request("POST", "/call/phone", data)
    else:
        data = {"assistantId": agent_id}
        print("Starting web test call...")
        print("Note: For a full test, use the Vapi dashboard or call the assigned phone number.")
        result = vapi_request("POST", "/call/web", data)

    print(f"\nCall initiated:")
    print(f"  Call ID: {result.get('id', 'unknown')}")
    print(f"  Status: {result.get('status', 'unknown')}")
    return result


def main():
    parser = argparse.ArgumentParser(description="Deploy Vapi voice qualification agent")
    parser.add_argument("--create", action="store_true", help="Create a new agent")
    parser.add_argument("--update", metavar="AGENT_ID", help="Update an existing agent")
    parser.add_argument("--list", action="store_true", help="List all agents")
    parser.add_argument("--test", metavar="AGENT_ID", help="Test call an agent")
    parser.add_argument("--phone", help="Phone number for test call (with country code)")
    parser.add_argument("--server-url", help="Webhook server URL (ngrok URL)")
    args = parser.parse_args()

    if args.list:
        list_agents()
    elif args.create:
        create_agent(server_url=args.server_url)
    elif args.update:
        update_agent(args.update, server_url=args.server_url)
    elif args.test:
        test_call(args.test, phone_number=args.phone)
    else:
        id_path = Path(__file__).parent / ".vapi_agent_id"
        if id_path.exists():
            agent_id = id_path.read_text().strip()
            print(f"Existing agent found: {agent_id}")
            print(f"Use --update {agent_id} to update, or --create for a new one.")
        else:
            print("No agent found. Creating new agent...")
            create_agent(server_url=args.server_url)


if __name__ == "__main__":
    main()
