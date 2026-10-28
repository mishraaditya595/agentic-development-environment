#!/usr/bin/env python3
"""Single stdlib validator for ADE skill metadata, evals and local links."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

NULL_VALUES = {"", "null", "~"}
REQUIRED = ("name", "description", "license")
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def _value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] in ("'", '"') and value[-1] == value[0]:
        value = value[1:-1].strip()
    return value


def metadata(content: str, name: str) -> list[str]:
    """Validate the supported YAML frontmatter subset, including block scalars."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return [f"{name}: frontmatter must start with ---"]
    try:
        end = lines.index("---", 1)
    except ValueError:
        return [f"{name}: frontmatter must end with ---"]
    values: dict[str, str] = {}
    errors: list[str] = []
    idx = 1
    while idx < end:
        line = lines[idx]
        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if not match:
            idx += 1
            continue
        key, value = match.groups()
        if key in values:
            errors.append(f"{name}: duplicate frontmatter field {key}")
        if value in ("|", "|-", "|+", ">", ">-", ">+"):
            block: list[str] = []
            while idx + 1 < end and (lines[idx + 1].startswith((" ", "\t")) or not lines[idx + 1].strip()):
                idx += 1
                block.append(lines[idx].strip())
            value = " ".join(part for part in block if part)
        values[key] = _value(value)
        idx += 1
    for key in REQUIRED:
        if values.get(key, "").lower() in NULL_VALUES:
            errors.append(f"{name}: frontmatter {key} is empty or missing")
    if values.get("name") and values["name"] != name:
        errors.append(f"{name}: frontmatter name mismatch")
    if values.get("license") and values["license"] != "Apache-2.0":
        errors.append(f"{name}: Apache-2.0 license required")
    return errors


def links(content: str, folder: Path) -> list[str]:
    """Validate relative Markdown file links without following URLs or anchors."""
    errors = []
    fenced = False
    for line in content.splitlines():
        if FENCE_RE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in LINK_RE.finditer(line):
            link = match.group(1).strip().split()[0].strip("<>")
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or link.startswith(("/", "#")):
                continue
            local = unquote(parsed.path)
            if not local:
                continue
            resolved = (folder / local).resolve()
            if not resolved.is_relative_to(folder.resolve()):
                errors.append(f"{folder.name}: Markdown link leaves skill package: {link}")
            elif not resolved.is_file():
                errors.append(f"{folder.name}: Markdown link does not exist: {link}")
    return errors


def validate_catalog(skills_dir: Path) -> tuple[list[str], set[str]]:
    errors: list[str] = []
    skill_names: set[str] = set()
    if not skills_dir.is_dir():
        return [f"skills/ directory does not exist: {skills_dir}"], skill_names
    for folder in sorted(skills_dir.iterdir()):
        if not folder.is_dir():
            continue
        name = folder.name
        main = folder / "SKILL.md"
        if not main.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        skill_names.add(name)
        content = main.read_text(encoding="utf-8")
        errors.extend(metadata(content, name))
        errors.extend(links(content, folder))
        if not (folder / "evals/representative-prompts.md").is_file():
            errors.append(f"{name}: representative evaluation prompts missing")
    if not skill_names:
        errors.append("no skill packages found")
    return errors, skill_names


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    args = parser.parse_args(argv)
    errors, names = validate_catalog(args.skills_dir)
    for error in errors:
        print("FAIL " + error, file=sys.stderr)
    if errors:
        return 1
    print(f"Validated {len(names)} skill package(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())