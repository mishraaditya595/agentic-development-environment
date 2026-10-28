"""Append-only ADE work-session checkpoints (no agents or background workers).

The state file is local user data. It is never an authority to execute commands.
"""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import re

STATE = Path(".agentic-dev/state/sessions.jsonl")
MAX_FIELD = 2048


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > MAX_FIELD or "\x00" in value:
        raise ValueError(f"{label} must be a nonempty text value of at most {MAX_FIELD} characters")
    return value.strip()


def events(root: Path):
    p = root / STATE
    if p.is_symlink():
        raise ValueError("Session state path must not be a symlink")
    if not p.exists():
        return []
    if not p.is_file():
        raise ValueError("Session state is not a file")
    out = []
    for num, line in enumerate(p.read_text(encoding="utf-8").splitlines(), start=1):
        try:
            event = json.loads(line)
            if not isinstance(event, dict) or event.get("kind") not in ("start", "checkpoint", "close"):
                raise ValueError("invalid event")
            out.append(event)
        except ValueError as exc:
            raise ValueError(f"Session journal line {num} is invalid: {exc}") from exc
    return out


def summary(root: Path):
    records = events(root)
    active = None
    history = []
    for item in records:
        if item["kind"] == "start":
            if active is not None:
                raise ValueError("Session journal contains overlapping active sessions")
            active = {"title": item.get("title"), "plan": item.get("plan"),
                      "started_at": item.get("at"), "checkpoints": []}
        elif item["kind"] == "checkpoint":
            if active is None:
                raise ValueError("Checkpoint exists outside an active session")
            active["checkpoints"].append({"step": item.get("step"), "at": item.get("at")})
        else:
            if active is None:
                raise ValueError("Close exists outside an active session")
            history.append({**active, "finished_at": item.get("at"), "verdict": item.get("verdict")})
            active = None
    return {"active": active, "completed_count": len(history), "last_completed": history[-1] if history else None}


def append(root: Path, entry: dict):
    directory = root / STATE.parent
    parent = root / ".agentic-dev"
    if parent.is_symlink() or directory.is_symlink():
        raise ValueError("Session state must not traverse symlinks")
    if not parent.is_dir():
        raise ValueError("Install ADE before creating session state")
    directory.mkdir(exist_ok=True)
    target = root / STATE
    if target.is_symlink():
        raise ValueError("Session file may not be a symlink")
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(target, flags, 0o600)
    try:
        data = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)


def apply(root: Path, action: str, *, title=None, plan=None, step=None, verdict=None):
    state = summary(root)
    event = {"kind": action, "at": dt.datetime.now(dt.timezone.utc).isoformat()}
    if action == "start":
        if state["active"] is not None:
            raise ValueError("An active session already exists; checkpoint or close it first")
        event["title"] = _text(title, "title")
        if plan is not None:
            rel = Path(_text(plan, "plan"))
            if rel.is_absolute() or ".." in rel.parts:
                raise ValueError("plan must be a project-relative path")
            event["plan"] = str(rel)
    elif action == "checkpoint":
        if state["active"] is None:
            raise ValueError("Cannot checkpoint without an active session")
        event["step"] = _text(step, "step")
    elif action == "close":
        if state["active"] is None:
            raise ValueError("Cannot close a session that is not active")
        if verdict not in ("verified", "partial", "blocked"):
            raise ValueError("Close requires explicit verdict: verified, partial, or blocked")
        event["verdict"] = verdict
    else:
        raise ValueError("Unsupported session action")
    append(root, event)
    return summary(root)
