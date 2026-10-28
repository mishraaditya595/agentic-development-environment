#!/usr/bin/env python3
"""Validate ADE shared assets and the canonical skill catalog (stdlib only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from skill_validation import validate_catalog

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SKILLS = (
    "feature-delivery", "plan-creator", "plan-implementer", "merge-conflict-resolver",
    "test-engineer", "repo-onboarding", "evidence-based-code-review",
)
REQUIRED_TEMPLATES = (
    "AGENTS.md", "CLAUDE.md", "implementation-plan.md", "review-report.md",
    "task-handoff.md", "pr-description.md",
)
REQUIRED_WORKFLOWS = (
    "feature-delivery.md", "bugfix.md", "pr-review.md", "review-remediation.md",
    "refactoring.md", "release-readiness.md",
)


def validate(root: Path) -> list[str]:
    errors, names = validate_catalog(root / "skills")
    for folder in ("workflows", "rules", "templates"):
        path = root / folder
        if not path.is_dir() or not any(path.glob("*.md")):
            errors.append(f"{folder}/: shared Markdown assets missing")
    for name in REQUIRED_SKILLS:
        if name not in names:
            errors.append(f"Required skill missing: {name}")
    for name in REQUIRED_TEMPLATES:
        if not (root / "templates" / name).is_file():
            errors.append(f"Missing template: {name}")
    for name in REQUIRED_WORKFLOWS:
        if not (root / "workflows" / name).is_file():
            errors.append(f"Missing workflow: {name}")
    try:
        routes = json.loads((root / "routing/skill-map.json").read_text(encoding="utf-8"))
        if routes.get("schema_version") != 1 or not isinstance(routes.get("routes"), list):
            errors.append("Invalid routing catalog")
        else:
            seen = set()
            for route in routes["routes"]:
                if route["id"] in seen:
                    errors.append("Duplicate route: " + route["id"])
                seen.add(route["id"])
                for name in [route["primary"]] + route["supporting"]:
                    if name not in names:
                        errors.append("Route references missing skill: " + name)
                if not route.get("triggers") or not route.get("exclude"):
                    errors.append("Route missing positive/negative examples: " + route["id"])
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append("Routing validation failed: " + str(exc))
    return errors


def main() -> int:
    errors = validate(ROOT)
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if errors:
        return 1
    print("Validated ADE skill catalog and shared asset layout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())