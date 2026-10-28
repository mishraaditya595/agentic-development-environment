"""ADE harness: explicit commands, truthful evidence and read-only diagnostics.

Python 3.9+, standard library. Never infer commands from arbitrary source strings;
users opt in by writing .agentic-dev/harness.json in the target project.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

CONFIG = Path(".agentic-dev/harness.json")
ROUTES = Path(".agentic-dev/skill-map.json")
VALID_NAMES = frozenset(("fast", "full", "integration", "smoke", "lint", "typecheck"))
ALLOWED_STATUSES = ("pass", "fail", "blocked", "skipped")
MAX_TIMEOUT = 1800

from harness.policy import audit as policy_audit


def report_entry(name: str, status: str, *, command=None, returncode=None, duration_ms=None, detail=""):
    assert status in ALLOWED_STATUSES
    return dict(name=name, status=status, command=command, exit_code=returncode,
                duration_ms=duration_ms, detail=detail)


def config_for(root: Path):
    path = root / CONFIG
    if not path.is_file() or path.is_symlink():
        raise ValueError("No valid .agentic-dev/harness.json; run harness doctor and configure explicit commands")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("Unsupported harness config schema")
    cmds = data.get("checks")
    if not isinstance(cmds, dict):
        raise ValueError("checks must be an object")
    for name, item in cmds.items():
        if name not in VALID_NAMES or not isinstance(item, dict):
            raise ValueError("Unknown check or invalid check object: " + str(name))
        argv = item.get("argv")
        if (not isinstance(argv, list) or not argv or
                not all(isinstance(v, str) and v and "\x00" not in v for v in argv)):
            raise ValueError("Each check must have an argv array of nonempty strings")
        # No shell interpolation; executable path is explicit and arguments remain data.
        timeout = item.get("timeout_seconds", 120)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT:
            raise ValueError(f"{name}: timeout_seconds must be 1..{MAX_TIMEOUT}")
    return data


def run_one(root: Path, name: str, item: dict):
    argv, timeout = item["argv"], item.get("timeout_seconds", 120)
    start = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=root, capture_output=True, text=True, errors="replace",
                              timeout=timeout, shell=False, env={**os.environ, "CI":"true"})
        status = "pass" if proc.returncode == 0 else "fail"
        detail = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()[-6000:]
        return report_entry(name, status, command=argv, returncode=proc.returncode,
                            duration_ms=round((time.monotonic()-start)*1000), detail=detail)
    except subprocess.TimeoutExpired:
        return report_entry(name, "blocked", command=argv,
                            duration_ms=round((time.monotonic()-start)*1000), detail="Timed out; process was terminated")
    except OSError as exc:
        return report_entry(name, "blocked", command=argv,
                            duration_ms=round((time.monotonic()-start)*1000), detail=f"Cannot execute: {exc}")


def selected_names(config: dict, requested: list[str]) -> list[str]:
    names = requested or list(config["checks"])
    if len(names) != len(set(names)):
        raise ValueError("Duplicate check names")
    unknown = set(names) - VALID_NAMES
    if unknown:
        raise ValueError("Unknown checks: " + ", ".join(sorted(unknown)))
    return names


def gather_checks(root: Path, names: list[str]):
    config = config_for(root)
    result = []
    for name in selected_names(config, names):
        item = config["checks"].get(name)
        result.append(run_one(root, name, item) if item else report_entry(
            name, "blocked", detail="Check is not configured; never interpreted as pass"))
    return result


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_evidence(root: Path, report: dict, destination: Path):
    state = root / ".agentic-dev/evidence"
    path = destination if destination.is_absolute() else root / destination
    # Evidence belongs under the reserved directory, not arbitrary project files.
    base = state.resolve()
    if path.is_symlink() or base not in path.resolve().parents:
        raise ValueError("Evidence output must be a new file under .agentic-dev/evidence/")
    if path.exists():
        raise ValueError("Evidence file already exists; refusal to overwrite")
    state.mkdir(parents=True, exist_ok=True)
    payload = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with path.open("xb") as output:
        output.write(payload)
    return str(path.relative_to(root))


def doctor(root: Path):
    checks, notes = {}, []
    try:
        config = config_for(root)
        checks = {name: "configured" for name in config["checks"]}
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        notes.append(str(exc))
    for file in ("AGENTS.md", "CLAUDE.md", ".agentic-dev/skill-map.json"):
        if not (root / file).is_file():
            notes.append(f"Missing: {file}")
    dirs = {name: (root / name).is_dir() for name in (".agents/skills", ".claude/skills", ".agentic-dev/workflows")}
    return {"repository": str(root), "configured_checks": checks,
            "skill_directories": dirs, "issues": notes,
            "note": "Doctor inspects presence only. It does not execute configured checks or certify model routing."}


def proof(root: Path, check: str, argv: list[str]):
    """Run an explicitly supplied *failing* probe against a configured check.

    Caller must provide a safe fixture/test path and must approve executing it.
    No automatic injection or modification of production files.
    """
    configured = config_for(root)["checks"].get(check)
    if not configured:
        raise ValueError("Check is not configured")
    result = run_one(root, "negative-probe", {"argv": argv, "timeout_seconds": configured.get("timeout_seconds", 120)})
    return {"check": check, "probe": result,
            "proven_fails": result["status"] == "fail",
            "note": "Only this explicit probe was tested. Passing does not certify every possible failure path."}


def command(args):
    root = Path(args.target).resolve()
    if not root.is_dir():
        raise ValueError("Target directory does not exist")
    if args.operation == "audit":
        try:
            config = config_for(root)
        except (ValueError, OSError, json.JSONDecodeError):
            config = None
        outcome = policy_audit(root, config)
        status = 0 if not outcome["issues"] and outcome["level"] == "instrumented" else 2
    elif args.operation == "session":
        from harness.session import apply, summary
        outcome = (summary(root) if args.session_action == "status"
                   else apply(root, args.session_action, title=getattr(args, "title", None),
                              plan=getattr(args, "plan", None), step=getattr(args, "step", None),
                              verdict=getattr(args, "verdict", None)))
        status = 0
    elif args.operation == "workspace":
        from harness.workspace import inspect
        outcome = inspect(root, args.check)
        status = 0 if args.check is None or outcome["verdict"] == "pass" else 1
    elif args.operation == "sensor-proof":
        from harness.sensors import prove
        outcome = prove(root, args.sensor)
        status = 0 if outcome["verdict"] == "pass" else 1
    elif args.operation == "doctor":
        outcome = doctor(root)
        status = 0 if not outcome["issues"] else 2
    elif args.operation == "check":
        entries = gather_checks(root, args.check)
        status = 0 if entries and all(v["status"] == "pass" for v in entries) else 1
        outcome = {"schema_version":1, "kind":"check", "timestamp_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
                   "results":entries, "verdict":"pass" if status==0 else "incomplete"}
    elif args.operation == "verify":
        entries = gather_checks(root, args.check or ["fast","full"])
        status = 0 if all(v["status"]=="pass" for v in entries) else 1
        outcome = {"schema_version":1, "kind":"verification", "timestamp_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
                   "acceptance_criteria":args.criterion, "results":entries,
                   "verdict":"verified-checks" if status==0 else "not-verified",
                   "limitations":"Check success alone does not establish acceptance criteria or independent review."}
    elif args.operation == "prove-failure":
        outcome = proof(root, args.check_name, args.probe_argv)
        status = 0 if outcome["proven_fails"] else 1
    else:
        raise ValueError("Unsupported operation")
    if args.evidence:
        outcome["evidence_file"] = write_evidence(root,outcome,Path(args.evidence))
    print(json.dumps(outcome,indent=2))
    return status


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".")
    parser.add_argument("--evidence", help="New path within .agentic-dev/evidence/ (opt-in)")
    sub = parser.add_subparsers(dest="operation", required=True)
    sub.add_parser("doctor")
    sub.add_parser("audit")
    p = sub.add_parser("session", help="Record or read local, append-only work checkpoints")
    nested = p.add_subparsers(dest="session_action", required=True)
    q = nested.add_parser("start")
    q.add_argument("--title", required=True)
    q.add_argument("--plan")
    q = nested.add_parser("checkpoint")
    q.add_argument("--step", required=True)
    q = nested.add_parser("close")
    q.add_argument("--verdict", choices=("verified", "partial", "blocked"), required=True)
    nested.add_parser("status")
    p = sub.add_parser("workspace", help="Inspect member repositories; --check executes member checks")
    p.add_argument("--check", choices=sorted(VALID_NAMES))
    p = sub.add_parser("sensor-proof", help="Run clean and violating fixtures through declared sensors")
    p.add_argument("--sensor")
    for name in ("check","verify"):
        p=sub.add_parser(name)
        p.add_argument("--check",action="append",default=[])
        if name=="verify":
            p.add_argument("--criterion",action="append",default=[],help="Acceptance criterion; not automatically graded")
    p=sub.add_parser("prove-failure")
    p.add_argument("--check-name",choices=sorted(VALID_NAMES),required=True)
    p.add_argument("probe_argv",nargs=argparse.REMAINDER,help="Explicit negative test argv after --")
    args=parser.parse_args(argv)
    if args.operation=="prove-failure" and args.probe_argv and args.probe_argv[0]=="--":
        args.probe_argv=args.probe_argv[1:]
    try:
        return command(args)
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"blocked","error":str(exc)}),file=sys.stderr)
        return 2


if __name__=="__main__":
    raise SystemExit(main())
