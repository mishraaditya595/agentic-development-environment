#!/usr/bin/env python3
"""Validate ADE shared assets and portable skill catalog (stdlib only)."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
skill_names = set()
for skill in sorted((root / "skills").iterdir()):
    if not skill.is_dir():
        continue
    main = skill / "SKILL.md"
    if not main.is_file():
        errors.append(f"{skill.name}: SKILL.md missing")
        continue
    content = main.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.S)
    if not match:
        errors.append(f"{skill.name}: invalid frontmatter delimiters")
        continue
    header = match.group(1)
    name = re.search(r"^name:\s*(.+)$", header, re.M)
    description = re.search(r"^description:\s*(.+)$", header, re.M)
    license_field = re.search(r"^license:\s*(.+)$", header, re.M)
    if not name or name.group(1).strip().strip("'\"") != skill.name:
        errors.append(f"{skill.name}: frontmatter name mismatch")
    if not description or not description.group(1).strip():
        errors.append(f"{skill.name}: missing description")
    if not license_field or license_field.group(1).strip() != "Apache-2.0":
        errors.append(f"{skill.name}: Apache-2.0 license required")
    if not (skill / "evals/representative-prompts.md").is_file() and skill.name != "evidence-based-code-review":
        errors.append(f"{skill.name}: representative evaluation prompts missing")
    skill_names.add(skill.name)
for folder in ("workflows", "rules", "templates"):
    path = root / folder
    if not path.is_dir() or not any(path.glob("*.md")):
        errors.append(f"{folder}/: shared Markdown assets missing")
for name in ("feature-delivery", "plan-creator", "plan-implementer", "merge-conflict-resolver", "test-engineer", "repo-onboarding", "evidence-based-code-review"):
    if name not in skill_names:
        errors.append(f"Required skill missing: {name}")
for name in ("AGENTS.md", "CLAUDE.md", "implementation-plan.md", "review-report.md", "task-handoff.md", "pr-description.md"):
    if not (root / "templates" / name).is_file():
        errors.append(f"Missing template: {name}")
for name in ("feature-delivery.md", "bugfix.md", "pr-review.md", "review-remediation.md", "release-readiness.md"):
    if not (root / "workflows" / name).is_file():
        errors.append(f"Missing workflow: {name}")
if errors:
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    sys.exit(1)
print(f"Validated {len(skill_names)} ADE skill names and shared asset layout.")
