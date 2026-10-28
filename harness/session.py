"""Append-only ADE work-session checkpoints (no agents or background workers).

The state file is local user data. It is never an authority to execute commands.
"""
from __future__ import annotations

import datetime as dt
import json
import fcntl
from contextlib import contextmanager
import os
from pathlib import Path
import re

STATE = Path(".agentic-dev/state/sessions.jsonl")
MAX_FIELD = 2048


def _text(value, label):
    if not isinstance(value, str) or not value.strip() or len(value) > MAX_FIELD or "\x00" in value:
        raise ValueError(f"{label} must be a nonempty text value of at most {MAX_FIELD} characters")
    return value.strip()


@contextmanager
def journal(root, exclusive=False):
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd_root = os.open(root, flags)
    parent = directory = handle = None
    try:
        parent = os.open(".agentic-dev", flags, dir_fd=fd_root)
        if exclusive:
            try:
                os.mkdir("state", 0o700, dir_fd=parent)
            except FileExistsError:
                pass
        try:
            directory = os.open("state", flags, dir_fd=parent)
        except FileNotFoundError:
            if exclusive:
                raise
            yield None
            return
        try:
            handle = os.open("sessions.jsonl",
                             (os.O_RDWR | os.O_CREAT if exclusive else os.O_RDONLY) | os.O_NOFOLLOW,
                             0o600, dir_fd=directory)
        except FileNotFoundError:
            if exclusive:
                raise
            yield None
            return
        fcntl.flock(handle, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
        yield handle
    finally:
        if handle is not None:
            fcntl.flock(handle, fcntl.LOCK_UN)
            os.close(handle)
        if directory is not None:
            os.close(directory)
        if parent is not None:
            os.close(parent)
        os.close(fd_root)


def read_locked(handle):
    os.lseek(handle, 0, os.SEEK_SET)
    with os.fdopen(os.dup(handle), "rb") as stream:
        content = stream.read()
    pos = content.rfind(b"\n") + 1
    records = []
    for num, line in enumerate(content[:pos].splitlines(), 1):
        try:
            item = json.loads(line)
            if not isinstance(item, dict) or item.get("kind") not in ("start", "checkpoint", "close"):
                raise ValueError("invalid event")
            records.append(item)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError(f"Session journal line {num} is invalid: {exc}") from exc
    return records, pos, len(content)


def events(root: Path):
    with journal(root) as handle:
        if handle is None:
            return []
        records, _, _ = read_locked(handle)
        return records


def _summarize(records):
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


def summary(root: Path):
    return _summarize(events(root))


def append_locked(handle, entry, committed, total):
    if total > committed:
        os.ftruncate(handle, committed)
    os.lseek(handle, 0, os.SEEK_END)
    encoded = (json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    while encoded:
        written = os.write(handle, encoded)
        if written == 0:
            raise OSError("Journal append failed")
        encoded = encoded[written:]
    os.fsync(handle)


def apply(root: Path, action: str, *, title=None, plan=None, step=None, verdict=None):
    with journal(root, exclusive=True) as handle:
        records, committed, total = read_locked(handle)
        state = _summarize(records)
        return _apply_locked(handle, records, committed, total, state, action,
                             title=title, plan=plan, step=step, verdict=verdict)


def _apply_locked(handle, records, committed, total, state, action, *, title, plan, step, verdict):
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
    append_locked(handle, event, committed, total)
    return _summarize(records + [event])
