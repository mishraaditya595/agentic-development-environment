#!/usr/bin/env python3
"""Install portable ADE assets safely into a target project (Python 3.9+).

Offline and stdlib-only. Preflight all conflicts, reject symlinks, and remove
files/directories created by this run if writing fails. Existing managed files
are never overwritten; only a verified, canonical config can be updated when
adding agents or skills.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = ROOT / "skills"
sys.path.insert(0, str(ROOT))
from harness.routing import managed_instructions
SHARED = ("workflows", "rules", "templates")
PRESETS = {
    "minimal": ("plan-creator", "plan-implementer", "evidence-based-code-review"),
    "standard": (
        "repo-onboarding", "plan-creator", "plan-implementer",
        "evidence-based-code-review", "merge-conflict-resolver", "test-engineer",
        "feature-delivery", "root-cause-investigation", "proof-before-done",
        "harness-doctor", "harness-verify",
    ),
}
AGENT_DESTINATIONS = {
    "codex": Path(".agents/skills"),
    "opencode": Path(".agents/skills"),
    "claude": Path(".claude/skills"),
}
CONFIG = Path(".agentic-dev/config.json")
LEGACY = json.loads((ROOT / "routing/legacy-v1-blobs.json").read_text())["files"]

def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def content_hash(data):
    return hashlib.sha256(data).hexdigest()



def names(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def catalog() -> list[str]:
    return sorted(p.name for p in SKILL_ROOT.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())


def config_bytes(agents: list[str], skills: list[str], manifest=None) -> bytes:
    config = {
        "schema_version": 1,
        "agents": agents,
        "skills": skills,
        "installation": "local-copy",
        "update_policy": "refuse modified or conflicting destinations",
    }
    if manifest is not None:
        config["schema_version"] = 2
        config["files"] = manifest
    return (json.dumps(config, indent=2) + "\n").encode("utf-8")


def gather(target: Path, agents: list[str], skills: list[str]) -> tuple[dict[Path, bytes], list[str]]:
    """Return desired files and user-owned instruction notes without target writes."""
    out: dict[Path, bytes] = {}
    notes: list[str] = []
    for category in SHARED:
        for source in sorted((ROOT / category).rglob("*")):
            if source.is_file():
                out[target / ".agentic-dev" / category / source.relative_to(ROOT / category)] = source.read_bytes()
    # A stable catalog survives additive skill installs without unsafe file rewrites.
    # Agents must only invoke entries whose primary skill is actually installed.
    out[target / ".agentic-dev/skill-map.json"] = (ROOT / "routing/skill-map.json").read_bytes()
    if not (target / ".agentic-dev/harness.json").exists():
        out[target / ".agentic-dev/harness.json"] = (json.dumps(
        {"schema_version": 1, "checks": {}}, indent=2) + "\n").encode("utf-8")
    out[target / ".agentic-dev/bin/ade-harness.py"] = (ROOT / "scripts/ade-harness.py").read_bytes()
    out[target / ".agentic-dev/bin/harness/core.py"] = (ROOT / "harness/core.py").read_bytes()
    out[target / ".agentic-dev/bin/harness/__init__.py"] = (ROOT / "harness/__init__.py").read_bytes()
    out[target / ".agentic-dev/bin/harness/policy.py"] = (ROOT / "harness/policy.py").read_bytes()
    if not (target / ".agentic-dev/invariants.json").exists():
        out[target / ".agentic-dev/invariants.json"] = (json.dumps({"schema_version":1, "rules":[]}, indent=2) + "\n").encode("utf-8")
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
        if name == "AGENTS.md" and path.is_file() and not path.is_symlink():
            out[path] = managed_instructions(path.read_bytes())
            notes.append("MANAGED AGENTS.md: preserve existing content; add ADE routing block if absent")
        elif path.exists() or path.is_symlink():
            notes.append(f"PRESERVE {name}: existing instructions unchanged")
        else:
            out[path] = (ROOT / "templates" / name).read_bytes()
    out[target / CONFIG] = config_bytes(agents, skills)
    return out, notes


def existing_config(target, agents, skills, available):
    path = target / CONFIG
    if path.is_symlink():
        raise ValueError("config.json is a symlink")
    if not path.exists():
        return agents, skills, None, {}
    raw = path.read_bytes()
    try:
        info = json.loads(raw)
        old_agents, old_skills = info["agents"], info["skills"]
        if (not isinstance(old_agents, list) or not isinstance(old_skills, list)
                or not all(isinstance(x, str) for x in old_agents + old_skills)
                or not old_agents or not old_skills
                or old_agents != sorted(set(old_agents)) or old_skills != sorted(set(old_skills))
                or not set(old_agents) <= set(AGENT_DESTINATIONS)
                or not set(old_skills) <= set(available)):
            raise ValueError("invalid inventory selections")
        version = info.get("schema_version")
        if version == 1 and raw == config_bytes(old_agents, old_skills):
            previous = {}
            for rel, sha in LEGACY.items():
                if (any(rel.startswith(".agentic-dev/" + kind + "/") for kind in SHARED)
                        or any(rel.startswith(str(AGENT_DESTINATIONS[agent]) + "/" + skill + "/")
                               for agent in old_agents for skill in old_skills)):
                    previous[rel] = ("git", sha)
            return sorted(set(agents + old_agents)), sorted(set(skills + old_skills)), raw, previous
        manifest = info.get("files")
        if (version != 2 or not isinstance(manifest, dict) or
                any(not isinstance(k, str) or not isinstance(v, str)
                    or not re.fullmatch(r"[a-f0-9]{64}", v)
                    or k.startswith("/") or ".." in Path(k).parts for k, v in manifest.items())
                or raw != config_bytes(old_agents, old_skills, manifest)):
            raise ValueError("invalid versioned inventory")
        return sorted(set(agents + old_agents)), sorted(set(skills + old_skills)), raw, {
            k: ("sha256", v) for k,v in manifest.items()}
    except (TypeError, KeyError, ValueError) as exc:
        raise ValueError("config.json has been modified or is invalid") from exc


def preflight(target, desired, agents, old_config, previous, no_routing=False):
    creates, same, conflicts, replacements, snapshots = [], [], [], [], {}
    for rel, (algo, signature) in previous.items():
        path = target / rel
        if path.is_symlink() or not path.is_file():
            conflicts.append(path)
            continue
        data = path.read_bytes()
        valid = (git_blob(data) == signature if algo == "git" else content_hash(data) == signature)
        if not valid:
            conflicts.append(path)
    for path, content in sorted(desired.items()):
        cur = path.parent
        invalid = path.is_symlink()
        while cur != target and not invalid:
            invalid = cur.is_symlink() or (cur.exists() and not cur.is_dir())
            cur = cur.parent
        if invalid:
            conflicts.append(path)
            continue
        if not path.exists():
            creates.append(path)
            continue
        if not path.is_file():
            conflicts.append(path)
            continue
        old = path.read_bytes()
        snapshots[path] = old
        if old == content:
            same.append(path)
        elif path == target / CONFIG and old_config == old:
            replacements.append(path)
        elif path == target / "AGENTS.md":
            if no_routing:
                same.append(path)
            else:
                try:
                    if managed_instructions(old) == content:
                        replacements.append(path)
                    else:
                        conflicts.append(path)
                except ValueError:
                    conflicts.append(path)
        elif str(path.relative_to(target)) in previous:
            replacements.append(path)
        else:
            conflicts.append(path)
    return creates, same, sorted(set(conflicts)), replacements, snapshots

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


def _replace_existing(root_fd: int, target: Path, path: Path, content: bytes,
                      old: bytes, created_files: list[tuple[Path, int, int]],
                      created_dirs: list[Path],
                      updated: list[tuple[Path, bytes, bytes]] | None = None) -> None:
    """Atomically replace a preflighted regular file after re-reading its bytes.

    Record successful replacements so a later failure can restore the original.
    """
    parent_fd = _parent_fd(root_fd, target, path, created_dirs, make=False)
    tmp_name = ".ade-" + uuid.uuid4().hex + ".tmp"
    try:
        flags = os.O_RDONLY | os.O_NOFOLLOW
        with os.fdopen(os.open(path.name, flags, dir_fd=parent_fd), "rb") as stream:
            if stream.read() != old:
                raise OSError(f"{path.relative_to(target)} changed during installation")
        fd = os.open(tmp_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=parent_fd)
        identity = os.fstat(fd)
        created_files.append((path.with_name(tmp_name), identity.st_dev, identity.st_ino))
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
        # File was verified with O_NOFOLLOW, and parent is dirfd-pinned.
        os.replace(tmp_name, path.name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        if updated is not None:
            updated.append((path, old, content))
    finally:
        os.close(parent_fd)

def _rollback(root_fd: int, target: Path, files: list[tuple[Path, int, int]],
              dirs: list[Path], updated: list[tuple[Path, bytes, bytes]]) -> list[str]:
    failures = []
    for path, old, new in reversed(updated):
        try:
            _replace_existing(root_fd, target, path, old, new, files, dirs)
        except OSError as exc:
            failures.append(f"Cannot restore {path.relative_to(target)}: {exc}")
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
    parser.add_argument("--no-agents-routing", action="store_true", help="Leave AGENTS.md unchanged")
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
        agents, skills, old_config, previous = existing_config(target, agents, skills, available)
        desired, notes = gather(target, agents, skills)
        if args.no_agents_routing and (target / "AGENTS.md").is_file():
            desired[target / "AGENTS.md"] = (target / "AGENTS.md").read_bytes()
        for relative in (".agentic-dev/harness.json", ".agentic-dev/invariants.json"):
            path = target / relative
            if path.is_file() and not path.is_symlink():
                desired[path] = path.read_bytes()
        manifest = {str(path.relative_to(target)): content_hash(data)
                    for path, data in desired.items()
                    if path != target / CONFIG and path.name not in ("AGENTS.md", "CLAUDE.md")
                    and path not in (target / ".agentic-dev/harness.json",
                                     target / ".agentic-dev/invariants.json")}
        desired[target / CONFIG] = config_bytes(agents, skills, manifest)
        creates, same, conflicts, replacements, snapshots = preflight(
            target, desired, agents, old_config, previous, args.no_agents_routing)
    except ValueError as exc:
        print(f"CONFLICT {exc}\nNo files changed.", file=sys.stderr)
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
    for path in replacements:
        print(f"{'WOULD UPDATE' if args.dry_run else 'UPDATE'} {path.relative_to(target)}")
    print(f"Summary: {len(creates)} new, {len(same)} identical, {len(replacements)} updates, 0 conflicts")
    if args.dry_run:
        return 0
    created_files: list[tuple[Path, int, int]] = []
    created_dirs: list[Path] = []
    root_fd = None
    updated_files: list[tuple[Path, bytes, bytes]] = []
    try:
        # The POSIX dir_fd + O_NOFOLLOW combination protects ancestor paths too.
        # Fail closed on runtimes that cannot supply these operations.
        if (not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW")
                or not {os.open, os.mkdir, os.unlink, os.rmdir} <= os.supports_dir_fd):
            raise OSError("secure installation requires directory-descriptor and O_NOFOLLOW support")
        root_fd = os.open(target, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for path in creates:
            _write_new(root_fd, target, path, desired[path], created_files, created_dirs)
        for path in sorted(replacements, key=lambda item: item == target / CONFIG):
            _replace_existing(root_fd, target, path, desired[path], snapshots[path],
                              created_files, created_dirs, updated_files)
    except OSError as exc:
        failures = _rollback(root_fd, target, created_files, created_dirs, updated_files) if root_fd is not None else []
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