#!/bin/sh
# Thin compatibility entry point: one authoritative Python parser validates all skills.
set -eu
root=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
exec python3 "$root/scripts/skill_validation.py" --skills-dir "$root/skills"