"""Opt-in sensor proof using clean and deliberately violating fixture files.

No fixture creation or changes to a developer checkout.
"""
from __future__ import annotations
import json
from pathlib import Path
from harness.core import run_one

MAX_TIMEOUT = 1800


def _fixture(root: Path, value):
    if not isinstance(value, str) or not value:
        raise ValueError("Fixture path must be nonempty")
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError("Fixture paths must be project-relative")
    result = root / path
    if (result.is_symlink() or not result.is_file()
            or root.resolve() not in result.resolve().parents):
        raise ValueError("Fixture must be a regular file within the project")
    return str(result)


def registry(root: Path):
    p = root / ".agentic-dev/sensors.json"
    if p.is_symlink() or not p.is_file():
        raise ValueError("Missing .agentic-dev/sensors.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1 or not isinstance(data.get("sensors"), list):
        raise ValueError("Invalid sensor registry")
    out = {}
    for sensor in data["sensors"]:
        if not isinstance(sensor, dict):
            raise ValueError("Invalid sensor")
        unsupported = set(sensor) - {"id", "argv", "clean", "violation", "timeout_seconds"}
        if unsupported:
            raise ValueError("Unsupported sensor keys: " + ", ".join(sorted(unsupported)))
        name, argv = sensor.get("id"), sensor.get("argv")
        if (not isinstance(name, str) or not name or name in out
                or not isinstance(argv, list) or not argv
                or any(not isinstance(arg, str) or not arg or "\x00" in arg for arg in argv)
                or "{path}" not in argv):
            raise ValueError("Invalid sensor id, command or missing {path} token")
        timeout = sensor.get("timeout_seconds", 120)
        if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT:
            raise ValueError("Invalid sensor timeout")
        _fixture(root, sensor.get("clean"))
        _fixture(root, sensor.get("violation"))
        out[name] = sensor
    return out


def prove(root: Path, selected=None):
    definitions = registry(root)
    if selected and selected not in definitions:
        raise ValueError("Unknown sensor: " + selected)
    results = []
    for name in ([selected] if selected else sorted(definitions)):
        item = definitions[name]
        checks = []
        for kind in ("clean", "violation"):
            path = _fixture(root, item[kind])
            argv = [path if v == "{path}" else v for v in item["argv"]]
            result = run_one(root, name + ":" + kind,
                             {"argv": argv, "timeout_seconds": item.get("timeout_seconds", 120)})
            checks.append(result)
        clean, violation = checks
        passed = clean["status"] == "pass" and violation["status"] == "fail"
        results.append({"id": name, "proven": passed, "clean": clean, "violation": violation,
                        "note": "This proves the sensor detects its known fixture only; project wiring must be checked separately."})
    return {"schema_version": 1, "results": results,
            "verdict": "pass" if results and all(x["proven"] for x in results) else "incomplete"}
