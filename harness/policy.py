"""Project invariant registry and deterministic harness health assessment.

Records *claimed* enforcement separately from checks actually run.
"""
from __future__ import annotations
import json
from pathlib import Path

SEVERITIES = {"critical", "important", "advisory"}


def read_invariants(root: Path):
    path = root / ".agentic-dev/invariants.json"
    if not path.exists():
        return [], ["Invariant registry not configured"]
    if path.is_symlink() or not path.is_file():
        return [], ["Invariant registry is not a regular file"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [], [f"Unreadable invariant registry: {exc}"]
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("rules"), list):
        return [], ["Invalid invariant registry schema"]
    issues = []
    result = []
    ids = set()
    for item in data["rules"]:
        if not isinstance(item, dict):
            issues.append("Invalid invariant entry")
            continue
        key = item.get("id")
        severity = item.get("severity")
        enforced = item.get("enforced_by", "not-enforced")
        if (not isinstance(key, str) or not key or key in ids or
                severity not in SEVERITIES or not isinstance(enforced, str) or not enforced):
            issues.append("Invalid or duplicate invariant: " + str(key))
            continue
        ids.add(key)
        result.append({"id": key, "severity": severity, "enforced_by": enforced,
                       "description": str(item.get("description", ""))})
    return result, issues


def audit(root: Path, config: dict | None):
    rules, errors = read_invariants(root)
    configured = config.get("checks", {}) if isinstance(config, dict) else {}
    findings = list(errors)
    classified = []
    for item in rules:
        source = item["enforced_by"]
        if source.startswith("check:"):
            name = source.removeprefix("check:")
            wired = name in configured
        else:
            wired = False
        # Claims of CI/hook enforcement need actual verification and cannot
        # earn credit merely because the user wrote "CI" in a text file.
        classified.append({**item, "check_configured": wired, "verification_status": "not-run"})
        if item["severity"] == "critical" and not wired:
            findings.append(f"Critical invariant {item['id']} lacks a configured executable check")
    level = "unconfigured"
    if config is not None:
        level = "configured"
        if not findings and configured and any(v["check_configured"] for v in classified):
            level = "instrumented"
    return {"level": level, "invariants": classified, "issues": findings,
            "notice": "Audit checks configuration, not the behavior of code, CI or agent skill activation."}
