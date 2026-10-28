#!/usr/bin/env python3
"""Install portable ADE skills and shared guidance into an existing project.

No network, package manager, or third-party dependencies. All writes are
preflighted; existing changed files and symlinked destinations are refused.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / "skills"
SHARED = ("workflows", "rules", "templates")
PRESETS = {
    "minimal": ("plan-creator", "plan-implementer", "evidence-based-code-review"),
    "standard": (
        "repo-onboarding", "plan-creator", "plan-implementer",
        "evidence-based-code-review", "merge-conflict-resolver", "test-engineer",
        "feature-delivery", "root-cause-investigation", "proof-before-done",
    ),
}
AGENT_DESTINATIONS = {
    "codex": Path(".agents/skills"),
    "opencode": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}


def names(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def catalog() -> list[str]:
    return sorted(p.name for p in SKILL_ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def gather(target: Path, agents: list[str], skills: list[str]) -> tuple[dict[Path, bytes], list[str]]:
    """Return desired files and skipped instructions. No target writes."""
    out: dict[Path, bytes] = {}
    notes: list[str] = []
    for category in SHARED:
        for source in sorted((ROOT / category).rglob("*")):
            if source.is_file():
                out[target / ".agentic-dev" / category / source.relative_to(ROOT / category)] = source.read_bytes()
    for destination in sorted({AGENT_DESTINATIONS[agent] for agent in agents}):
        for skill in skills:
            folder = SKILL_ROOT / skill
            for source in sorted(folder.rglob("*")):
                if source.is_file():
                    out[target / destination / skill / source.relative_to(folder)] = source.read_bytes()
    for name in ("AGENTS.md", "CLAUDE.md"):
        if name == "CLAUDE.md" and "claude" not in agents:
            continue
        path = target / name
        if path.exists() or path.is_symlink():
            notes.append(f"PRESERVE {name}: existing instructions unchanged; manually reference .agentic-dev/ resources if desired")
        else:
            out[path] = (ROOT / "templates" / name).read_bytes()
    config = {
        "schema_version": 1,
        "agents": agents,
        "skills": skills,
        "installation": "local-copy",
        "update_policy": "refuse modified or conflicting destinations",
    }
    out[target / ".agentic-dev/config.json"] = (json.dumps(config, indent=2) + "\n").encode("utf-8")
    return out, notes


def unsafe_path(target: Path, destination: Path) -> bool:
    # Symlinked parent directories can escape the destination checkout.
    current = destination
    while current != target:
        if current.is_symlink():
            return True
        current = current.parent
    return target.is_symlink()


def preflight(target: Path, desired: dict[Path, bytes]) -> tuple[list[Path], list[Path], list[Path]]:
    create, identical, conflicts = [], [], []
    for path, content in sorted(desired.items()):
        if unsafe_path(target, path):
            conflicts.append(path)
        elif path.exists():
            if path.is_file() and path.read_bytes() == content:
                identical.append(path)
            else:
                conflicts.append(path)
        else:
            create.append(path)
    return create, identical, conflicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Existing project directory (default: current directory)")
    parser.add_argument("--agents", default="codex", help="Comma-separated: codex,claude,opencode")
    parser.add_argument("--preset", choices=("minimal", "standard", "complete"), default="standard")
    parser.add_argument("--skills", help="Comma-separated exact canonical skill names (overrides preset)")
    parser.add_argument("--dry-run", action="store_true", help="Display actions without writing any files")
    parser.add_argument("--list", action="store_true", help="Show available skill names and exit")
    args = parser.parse_args(argv)
    if args.list:
        print("\n".join(catalog()))
        return 0

    target = Path(args.target).absolute()
    if not target.is_dir() or target.is_symlink():
        parser.error("--target must be an existing non-symlink directory")
    agents = sorted(set(names(args.agents)))
    invalid = set(agents) - set(AGENT_DESTINATIONS)
    if not agents or invalid:
        parser.error(f"invalid --agents: {', '.join(sorted(invalid)) or '(empty)'}")
    available = catalog()
    skills = sorted(set(names(args.skills))) if args.skills is not None else (
        available if args.preset == "complete" else sorted(PRESETS[args.preset])
    )
    invalid_skills = set(skills) - set(available)
    if not skills or invalid_skills or any(not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", s) for s in skills):
        parser.error(f"invalid --skills: {', '.join(sorted(invalid_skills)) or '(empty or malformed)'}")

    desired, notes = gather(target, agents, skills)
    creates, same, conflicts = preflight(target, desired)
    for note in notes:
        print(note)
    for path in conflicts:
        print(f"CONFLICT {path.relative_to(target)}", file=sys.stderr)
    if conflicts:
        print("No files changed. Resolve conflicts manually; existing content is never overwritten.", file=sys.stderr)
        return 2
    for path in creates:
        print(f"{'WOULD CREATE' if args.dry_run else 'CREATE'} {path.relative_to(target)}")
    print(f"Summary: {len(creates)} new, {len(same)} identical, 0 conflicts")
    if args.dry_run:
        return 0
    for path in creates:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(desired[path])
    print("Installed. Restart the coding agent or open a new session for skill discovery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
