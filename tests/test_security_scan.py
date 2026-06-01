"""Ensure repository security scan passes (malware / supply-chain indicators)."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_security_scan_passes():
    script = REPO_ROOT / "scripts" / "security_scan.py"
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"security_scan.py failed:\n{result.stdout}\n{result.stderr}"
    )


def test_forbidden_malware_paths_absent():
    forbidden = [
        # ".vscode/tasks.json",  # removed — the content scan catches the malicious version    
        "public/fonts/fa-solid-400.woff2",
        "temp_auto_push.bat",
        "temp_interactive_push.bat",
    ]
    for rel in forbidden:
        assert not (REPO_ROOT / rel).exists(), f"Malware path still present: {rel}"


def test_vscode_automatic_tasks_disabled():
    import json

    settings = REPO_ROOT / ".vscode" / "settings.json"
    if not settings.exists():
        return
    data = json.loads(settings.read_text(encoding="utf-8"))
    assert data.get("task.allowAutomaticTasks") is not True
