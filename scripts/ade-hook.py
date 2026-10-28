#!/usr/bin/env python3
"""Opt-in ADE lifecycle hook entrypoint; reads one JSON object from stdin."""
from pathlib import Path
import argparse
import json
import sys

HERE = Path(__file__).resolve()
BIN = HERE.parent if (HERE.parent / "harness").is_dir() else HERE.parents[1]
sys.path.insert(0, str(BIN))
from harness.hooks import process


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("event", choices=("prompt","stop"))
    args = parser.parse_args(argv)
    project = HERE.parents[2] if HERE.parent.name == "bin" else Path.cwd()
    try:
        raw = sys.stdin.read(65537)
        if len(raw) > 65536:
            raw = "{}"  # Keep routing even with unexpectedly large payloads.
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            raise ValueError("Hook input must be JSON object")
        result = process(project, args.event, data)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        result = {"hookSpecificOutput":{"hookEventName": "UserPromptSubmit" if args.event == "prompt" else "Stop",
                  "additionalContext": "ADE hook could not evaluate input; verification remains unconfirmed."}}
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
