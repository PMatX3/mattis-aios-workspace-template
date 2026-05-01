"""
AIOS — Configuration Loader

Reads credentials from .env file in workspace root.
Provides helpers for loading API keys and other env-driven config.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from workspace root (one level up from scripts/)
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = WORKSPACE_ROOT / ".env"

load_dotenv(ENV_PATH)


def get_env(key, required=True):
    """
    Get an environment variable. Returns None if not set.
    Callers handle missing credentials gracefully.
    """
    value = os.getenv(key, "").strip()
    if not value:
        return None
    return value
