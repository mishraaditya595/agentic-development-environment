#!/usr/bin/env python3
"""Opt-in, create-only Claude/Codex hook configuration installer.

Safe default is NOT to install native hooks. Run this only after reviewing the
project hook commands and the installed ADE check configuration.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bootstrap


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, help="Existing ADE project root")
    parser.add_argument("--agents", default="claude,codex", help="claude,codex")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.target).absolute()
    names = sorted(set(bootstrap.names(args.agents)))
    if not root.is_dir() or root.is_symlink() or not names or not set(names) <= {"claude","codex"}:
        parser.error("Need existing non-symlink target and supported --agents claude,codex")
    if not (root / ".agentic-dev/bin/ade-harness.py").is_file():
        parser.error("Install ADE bundle with scripts/bootstrap.py before enabling hooks")
    assets = {
        root / ".agentic-dev/bin/ade-hook.py": (ROOT / "scripts/ade-hook.py").read_bytes(),
        root / ".agentic-dev/bin/harness/hooks.py": (ROOT / "harness/hooks.py").read_bytes(),
    }
    for agent in names:
        if agent == "claude":
            assets[root / ".claude/settings.json"] = (ROOT / "harness/adapters/claude-hooks.json").read_bytes()
        if agent == "codex":
            assets[root / ".codex/hooks.json"] = (ROOT / "harness/adapters/codex-hooks.json").read_bytes()
    try:
        create, same, conflicts, _, _ = bootstrap.preflight(root, assets, [], None)
    except (OSError, ValueError) as exc:
        print("Preflight failed: " + str(exc), file=sys.stderr)
        return 2
    if conflicts:
        for path in conflicts:
            print("CONFLICT " + str(path.relative_to(root)), file=sys.stderr)
        print("Existing settings were not replaced. Review/merge hooks manually.", file=sys.stderr)
        return 2
    for path in create:
        print(("WOULD CREATE " if args.dry_run else "CREATE ") + str(path.relative_to(root)))
    print(f"{len(create)} new, {len(same)} identical")
    if args.dry_run:
        return 0
    root_fd = None
    made_files, made_dirs = [], []
    try:
        if (not hasattr(os, "O_DIRECTORY") or not hasattr(os, "O_NOFOLLOW")
                or not {os.open, os.mkdir, os.unlink, os.rmdir} <= os.supports_dir_fd):
            raise OSError("Secure hook installation requires POSIX directory-descriptor support")
        root_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for path in create:
            bootstrap._write_new(root_fd, root, path, assets[path], made_files, made_dirs)
    except OSError as exc:
        failures = bootstrap._rollback(root_fd, root, made_files, made_dirs, []) if root_fd is not None else []
        print("Hook installation failed: " + str(exc), file=sys.stderr)
        if failures:
            print("Rollback incomplete: " + "; ".join(failures), file=sys.stderr)
        return 1
    finally:
        if root_fd is not None:
            os.close(root_fd)
    print("Hook configs created. Review them and restart/trust the selected coding agent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
