"""Optional, lightweight Claude/Codex lifecycle hook adapter.

It emits structured context or a bounded stop continuation request. It is not a
security sandbox and does not guarantee model skill activation.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess

from harness.core import config_for, run_one

MAX_REASON = 500


def hook_context(root: Path):
    path = root / ".agentic-dev/skill-map.json"
    if not path.is_file() or path.is_symlink():
        return "ADE routing map not installed; use normal project instructions."
    try:
        routes = json.loads(path.read_text(encoding="utf-8")).get("routes", [])
    except (OSError, ValueError, AttributeError):
        return "ADE routing map invalid; do not assume skills are available."
    try:
        config = json.loads((root / ".agentic-dev/config.json").read_text(encoding="utf-8"))
        installed = set(config.get("skills", []))
    except (OSError, ValueError, AttributeError, TypeError):
        installed = set()
    names = sorted({x.get("primary") for x in routes if isinstance(x, dict)
                    and isinstance(x.get("primary"), str) and x.get("primary") in installed})
    return ("ADE skill routing: consult .agentic-dev/skill-map.json and choose an "
            "installed primary skill matching the user request. Known primary names: " +
            ", ".join(names[:20]) + ". Never merge or deploy without explicit authorization.")


def changed(root: Path):
    try:
        proc = subprocess.run(["git", "status", "--porcelain", "--untracked-files=normal"],
                              cwd=root, capture_output=True, text=True, errors="replace", timeout=5)
        if proc.returncode != 0:
            return None
        return bool(proc.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        return None


def _context(event, message):
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}}


def process(root: Path, event: str, payload: dict):
    if event == "prompt":
        message = hook_context(root)
        return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                       "additionalContext": message}}
    if event != "stop":
        raise ValueError("Unsupported hook event")
    if payload.get("stop_hook_active"):
        return _context("Stop", "ADE stop hook already requested continuation; do not claim unverified checks passed.")
    dirty = changed(root)
    if dirty is False:
        return _context("Stop", "ADE stop hook skipped: no local Git working-tree changes. This is not an independent verification verdict.")
    if dirty is None:
        return _context("Stop", "ADE stop hook could not establish Git change state; verification remains unconfirmed.")
    try:
        config = config_for(root)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return _context("Stop", f"ADE fast check unavailable: {type(exc).__name__}. Do not claim tests passed.")
    item = config["checks"].get("fast")
    if not item:
        return _context("Stop", "ADE fast check not configured; do not claim verification.")
    # Keep interactive stop hooks bounded independently of the configured
    # project check timeout. No subprocess continuation after timeouts.
    check = run_one(root, "fast", {**item, "timeout_seconds": min(45, item.get("timeout_seconds",120))})
    if check["status"] == "pass":
        return _context("Stop", "ADE fast check passed. Full checks, requirements and independent review remain separate.")
    if check["status"] == "fail":
        return {"decision": "block", "reason": "ADE fast check failed (exit code " +
                str(check["exit_code"]) + "). Inspect and correct the project test output, then reverify."}
    return _context("Stop", "ADE fast check blocked or timed out; stop was not prevented. Report verification as blocked.")
