"""Small deterministic multi-repository verification runner.

No clone, merge, branch mutation, or cross-repository writes.
"""
from __future__ import annotations
import json
from pathlib import Path
from harness.core import gather_checks, doctor


def members(root: Path):
    manifest = root / ".agentic-dev/workspace.json"
    if manifest.is_symlink() or not manifest.is_file():
        raise ValueError("Missing regular .agentic-dev/workspace.json")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("repositories"), list):
        raise ValueError("Invalid workspace manifest schema")
    seen = set()
    resolved = []
    for member in data["repositories"]:
        if not isinstance(member, dict) or not isinstance(member.get("name"), str) or not isinstance(member.get("path"), str):
            raise ValueError("Every member requires name and path")
        name, rel = member["name"].strip(), Path(member["path"])
        if (not name or name in seen or rel.is_absolute() or len(rel.parts) != 1
                or rel.parts[0] in (".", "..", ".git", ".agentic-dev")):
            raise ValueError("Duplicate member or invalid relative path")
        path = root / rel
        if path.is_symlink() or not path.is_dir() or path.parent != root:
            raise ValueError("Workspace member must be an existing, direct, non-symlink child directory")
        seen.add(name)
        resolved.append((name, path))
    if not resolved:
        raise ValueError("Workspace manifest must declare at least one repository")
    return resolved


def inspect(root: Path, check: str | None = None):
    items = []
    for name, path in members(root):
        if check is None:
            result = doctor(path)
            status = "configured" if not result["issues"] else "incomplete"
            items.append({"name": name, "path": path.name, "status": status, "doctor": result})
        else:
            try:
                outcome = gather_checks(path, [check])
                status = outcome[0]["status"]
            except (ValueError, OSError, json.JSONDecodeError) as exc:
                status = "blocked"
                outcome = [{"name": check, "status": status, "detail": str(exc)}]
            items.append({"name": name, "path": path.name, "status": status, "results": outcome})
    return {"schema_version": 1, "members": items,
            "verdict": "pass" if items and all(i["status"] == "pass" for i in items) else "incomplete"}
