#!/usr/bin/env python3
"""Install portable ADE assets safely into a target project (Python 3.9+).

Offline and stdlib-only. Preflight all conflicts, reject symlinks, and remove
files/directories created by this run if writing fails. Existing managed files
are never overwritten; only a verified, canonical config can be updated when
adding agents or skills.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import uuid
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
CONFIG = Path(".agentic-dev/config.json")


def names(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def catalog() -> list[str]:
    return sorted(p.name for p in SKILL_ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def config_bytes(agents: list[str], skills: list[str]) -> bytes:
    config = {
        "schema_version": 1,
        "agents": agents,
        "skills": skills,
        "installation": "local-copy",
        "update_policy": "refuse modified or conflicting destinations",
    }
    return (json.dumps(config, indent=2) + "\n").encode("utf-8")


def gather(target: Path, agents: list[str], skills: list[str]) -> tuple[dict[Path, bytes], list[str]]:
    """Return desired files and user-owned instruction notes without target writes."""
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
    out[target / CONFIG] = config_bytes(agents, skills)
    return out, notes


def existing_config(target: Path, agents: list[str], skills: list[str], available: list[str]) -> tuple[list[str], list[str], bytes | None]:
    """Return cumulative selections only for a byte-identical ADE-managed config."""
    path = target / CONFIG
    if path.is_symlink():
        raise ValueError(".agentic-dev/config.json is a symlink")
    if not path.exists():
        return agents, skills, None
    if not path.is_file():
        raise ValueError(".agentic-dev/config.json is not a regular file")
    raw = path.read_bytes()
    try:
        info = json.loads(raw)
        old_agents = info["agents"]
        old_skills = info["skills"]
        if (not isinstance(old_agents, list) or not isinstance(old_skills, list)
                or not all(isinstance(x, str) for x in old_agents + old_skills)
                or not old_agents or not old_skills
                or old_agents != sorted(set(old_agents)) or old_skills != sorted(set(old_skills))
                or not set(old_agents) <= set(AGENT_DESTINATIONS)
                or not set(old_skills) <= set(available)
                or raw != config_bytes(old_agents, old_skills)):
            raise ValueError("not a canonical ADE selection inventory")
    except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        raise ValueError(".agentic-dev/config.json has been modified or is invalid") from exc
    # Re-runs only add selections; removing installed content needs a reviewed manual change.
    return sorted(set(agents) | set(old_agents)), sorted(set(skills) | set(old_skills)), raw


def preflight(target: Path, desired: dict[Path, bytes], agents: list[str], old_config: bytes | None) -> tuple[list[Path], list[Path], list[Path], bool]:
    create, identical, conflicts = [], [], []
    update_config = False
    # Protected existing instruction files must not be symlinks, including dangling links.
    for name in ("AGENTS.md", "CLAUDE.md"):
        if name == "CLAUDE.md" and "claude" not in agents:
            continue
        if (target / name).is_symlink():
            conflicts.append(target / name)
    if old_config is not None and desired[target / CONFIG] != old_config:
        previous = json.loads(old_config)
        old_assets, _ = gather(target, previous["agents"], previous["skills"])
        for path, content in old_assets.items():
            if path == target / CONFIG or path in (target / "AGENTS.md", target / "CLAUDE.md"):
                continue  # user-owned instructions are deliberately exempt
            if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
                conflicts.append(path)
    for path, content in sorted(desired.items()):
        current = path.parent
        bad_parent = False
        while current != target:
            if current.is_symlink() or (current.exists() and not current.is_dir()):
                bad_parent = True
                break
            current = current.parent
        if bad_parent or path.is_symlink():
            conflicts.append(path)
        elif path.exists():
            if not path.is_file():
                conflicts.append(path)
            elif path == target / CONFIG and old_config is not None:
                # Only the canonical inventory may be updated. New assets are
                # preflighted independently; the config is replaced last.
                if path.read_bytes() != old_config:
                    conflicts.append(path)
                elif content == old_config:
                    identical.append(path)
                else:
                    update_config = True
            elif path.read_bytes() == content:
                identical.append(path)
            else:
                conflicts.append(path)
        else:
            create.append(path)
    return create, identical, sorted(set(conflicts)), update_config


def _parent_fd(root_fd: int, target: Path, path: Path, created_dirs: list[Path], make: bool) -> int:
    """Walk via directory descriptors so swapped parent symlinks cannot redirect writes."""
    fd = os.dup(root_fd)
    try:
        current = target
        for part in path.relative_to(target).parts[:-1]:
            current = current / part
            flags = os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
            try:
                child = os.open(part, flags, dir_fd=fd)
            except FileNotFoundError:
                if not make:
                    raise
                try:
                    os.mkdir(part, dir_fd=fd)
                    created_dirs.append(current)
                except FileExistsError:
                    pass
                child = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def _write_new(root_fd: int, target: Path, path: Path, content: bytes,
               created_files: list[tuple[Path, int, int]], created_dirs: list[Path]) -> None:
    parent_fd = _parent_fd(root_fd, target, path, created_dirs, make=True)
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        fd = os.open(path.name, flags, 0o666, dir_fd=parent_fd)
        identity = os.fstat(fd)
        created_files.append((path, identity.st_dev, identity.st_ino))
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
    finally:
        os.close(parent_fd)


def _update_inventory(root_fd: int, target: Path, content: bytes,
                      old: bytes, created_files: list[tuple[Path, int, int]],
                      created_dirs: list[Path]) -> None:
    """Atomic replace after verifying the existing canonical inventory again."""
    path = target / CONFIG
    parent_fd = _parent_fd(root_fd, target, path, created_dirs, make=False)
    tmp_name = ".config-" + uuid.uuid4().hex + ".tmp"
    try:
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(path.name, flags, dir_fd=parent_fd), "rb") as stream:
            if stream.read() != old:
                raise OSError("config.json changed during installation")
        fd = os.open(tmp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600, dir_fd=parent_fd)
        identity = os.fstat(fd)
        created_files.append((path.with_name(tmp_name), identity.st_dev, identity.st_ino))
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        os.replace(tmp_name, path.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
    finally:
        os.close(parent_fd)


def _rollback(root_fd: int, target: Path, files: list[tuple[Path, int, int]], dirs: list[Path]) -> list[str]:
    failures = []
    for path, device, inode in reversed(files):
        try:
            parent_fd = _parent_fd(root_fd, target, path, [], make=False)
            try:
                found = os.stat(path.name, dir_fd=parent_fd, follow_symlinks=False)
                if stat.S_ISREG(found.st_mode) and (found.st_dev, found.st_ino) == (device, inode):
                    os.unlink(path.name, dir_fd=parent_fd)
            finally:
                os.close(parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            failures.append(f"{path.relative_to(target)}: {exc}")
    for path in reversed(dirs):
        try:
            parent_fd = _parent_fd(root_fd, target, path, [], make=False)
            try:
                os.rmdir(path.name, dir_fd=parent_fd)
            finally:
                os.close(parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            # A non-empty directory could be in use by another process: leave it.
            if path.is_dir() and any(path.iterdir()):
                continue
            failures.append(f"{path.relative_to(target)}: {exc}")
    return failures


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
    try:
        agents, skills, old_config = existing_config(target, agents, skills, available)
        desired, notes = gather(target, agents, skills)
        creates, same, conflicts, update = preflight(target, desired, agents, old_config)
    except ValueError as exc:
        print(f"CONFLICT {CONFIG}: {exc}\nNo files changed.", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"PREFLIGHT FAILED: {exc}\nNo files changed.", file=sys.stderr)
        return 2
    for note in notes:
        print(note)
    for path in conflicts:
        print(f"CONFLICT {path.relative_to(target)}", file=sys.stderr)
    if conflicts:
        print("No files changed. Resolve conflicts manually; existing content is never overwritten.", file=sys.stderr)
        return 2
    for path in creates:
        print(f"{'WOULD CREATE' if args.dry_run else 'CREATE'} {path.relative_to(target)}")
    if update:
        print(f"{'WOULD UPDATE' if args.dry_run else 'UPDATE'} {CONFIG} (additive selections only)")
    print(f"Summary: {len(creates)} new, {len(same)} identical, {int(update)} config update, 0 conflicts")
    if args.dry_run:
        return 0
    created_files: list[tuple[Path, int, int]] = []
    created_dirs: list[Path] = []
    root_fd = None
    try:
        # The POSIX dir_fd + O_NOFOLLOW combination protects ancestor paths too.
        # Fail closed on runtimes that cannot supply these operations.
        if (not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW")
                or not {os.open, os.mkdir, os.unlink, os.rmdir} <= os.supports_dir_fd):
            raise OSError("secure installation requires directory-descriptor and O_NOFOLLOW support")
        root_fd = os.open(target, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for path in creates:
            _write_new(root_fd, target, path, desired[path], created_files, created_dirs)
        if update:
            assert old_config is not None
            _update_inventory(root_fd, target, desired[target / CONFIG], old_config, created_files, created_dirs)
    except OSError as exc:
        failures = _rollback(root_fd, target, created_files, created_dirs) if root_fd is not None else []
        print(f"INSTALL FAILED: {exc}", file=sys.stderr)
        if failures:
            print("Rollback incomplete: " + "; ".join(failures), file=sys.stderr)
        else:
            print("Rolled back files and directories created by this run.", file=sys.stderr)
        return 1
    finally:
        if root_fd is not None:
            os.close(root_fd)
    print("Installed. Restart the coding agent or open a new session for skill discovery.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())