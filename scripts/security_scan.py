#!/usr/bin/env python3
"""
Repository security scan for known supply-chain / malware indicators.

Exit code 0 = clean, 1 = findings (CI should fail).

Run from repo root:
    python scripts/security_scan.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# Paths that must never exist (committed malware from Mar 2025 / Jun 2026 incidents)
FORBIDDEN_PATHS = [
    # ".vscode/tasks.json",  # removed — the content scan catches the malicious version    
    "public/fonts/fa-solid-400.woff2",
    "temp_auto_push.bat",
    "temp_interactive_push.bat",
]

# Content patterns (file path -> optional; scan all text files if None)
CONTENT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("vscode_folder_open_task", re.compile(r'"runOn"\s*:\s*"folderOpen"', re.I)),
    ("curl_pipe_bash", re.compile(r"curl\s+[^\s|]+\s*\|\s*bash", re.I)),
    ("vercel_malware_host", re.compile(r"260120\.vercel\.app", re.I)),
    ("node_fake_font", re.compile(r"node\s+\./public/fonts/fa-solid-400\.woff2", re.I)),
    ("git_force_push_no_verify", re.compile(r"git\s+push\s+-uf\s+.*--no-verify", re.I)),
    ("obfuscated_js_global", re.compile(r"global\s*\[\s*['\"]!['\"]\s*\]\s*=", re.I)),
    ("allow_automatic_tasks_on", re.compile(r'"task\.allowAutomaticTasks"\s*:\s*true', re.I)),
]

SKIP_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    "Demo ONLY",
    "local_output",
    "logs",
}

TEXT_EXTENSIONS = {
    ".py", ".json", ".md", ".sh", ".bat", ".cmd", ".yml", ".yaml",
    ".txt", ".js", ".ts", ".html", ".css", ".woff2", ".env", ".example",
}


def _should_scan(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    # Small woff2/font files may be disguised JS
    if path.suffix.lower() in {".woff2", ".woff", ".eot", ".ttf"} and path.stat().st_size < 25_000:
        return True
    return False


def _iter_scan_files() -> list[Path]:
    files: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO_ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if _should_scan(path):
            files.append(path)
    return files


def check_forbidden_paths() -> list[str]:
    findings: list[str] = []
    for rel in FORBIDDEN_PATHS:
        p = REPO_ROOT / rel
        if p.exists():
            findings.append(f"FORBIDDEN FILE EXISTS: {rel}")
    return findings


def check_vscode_settings() -> list[str]:
    findings: list[str] = []
    settings = REPO_ROOT / ".vscode" / "settings.json"
    if not settings.exists():
        return findings
    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(f"INVALID JSON: .vscode/settings.json ({exc})")
        return findings
    if data.get("task.allowAutomaticTasks") is True:
        findings.append(
            "UNSAFE: .vscode/settings.json has task.allowAutomaticTasks=true"
        )
    if isinstance(data.get("tasks"), dict) and data["tasks"].get("runOn") == "folderOpen":
        findings.append(
            "UNSAFE: .vscode/settings.json embeds a folderOpen auto-task"
        )
    return findings


def check_fake_woff2() -> list[str]:
    findings: list[str] = []
    fonts = REPO_ROOT / "public" / "fonts"
    if not fonts.is_dir():
        return findings
    for path in fonts.glob("*.woff2"):
        try:
            header = path.read_bytes()[:4]
        except OSError:
            continue
        # Real wOFF / wOF2 magic
        if header not in (b"wOFF", b"wOF2") and path.stat().st_size < 25_000:
            text_preview = path.read_text(encoding="utf-8", errors="ignore")[:200]
            if "global[" in text_preview or "require" in text_preview:
                findings.append(
                    f"FAKE FONT (likely JS malware): {path.relative_to(REPO_ROOT)}"
                )
    return findings


def check_content_patterns(files: list[Path]) -> list[str]:
    findings: list[str] = []
    for path in files:
        rel = str(path.relative_to(REPO_ROOT))
        # Skip this scanner and security notice (document attack patterns)
        if rel in {"scripts/security_scan.py", "docs/guides/SECURITY_NOTICE.md"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pattern in CONTENT_PATTERNS:
            if pattern.search(text):
                findings.append(f"PATTERN [{name}]: {rel}")
    return findings


def main() -> int:
    print("=" * 60)
    print("Security scan:", REPO_ROOT.name)
    print("=" * 60)

    all_findings: list[str] = []
    all_findings.extend(check_forbidden_paths())
    all_findings.extend(check_vscode_settings())
    all_findings.extend(check_fake_woff2())
    all_findings.extend(check_content_patterns(_iter_scan_files()))

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for f in all_findings:
        if f not in seen:
            seen.add(f)
            unique.append(f)

    if unique:
        print("\nFAILED — security findings:\n")
        for i, f in enumerate(unique, 1):
            print(f"  {i}. {f}")
        print(f"\nTotal: {len(unique)} issue(s)")
        return 1

    print("\nPASSED — no known malware indicators found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
