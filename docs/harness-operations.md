# Operational harness capabilities

This document describes capabilities in the stacked operations PR, built on the ADE Harness Foundation.

## Session checkpoints

Use a local JSONL journal to persist a task across coding-agent context resets:

    python3 .agentic-dev/bin/ade-harness.py --target . session start --title "Implement history" --plan docs/plans/history.md
    python3 .agentic-dev/bin/ade-harness.py --target . session checkpoint --step "Added persistence regression tests"
    python3 .agentic-dev/bin/ade-harness.py --target . session status
    python3 .agentic-dev/bin/ade-harness.py --target . session close --verdict partial

A session can be closed only with the explicit label verified, partial, or blocked. The CLI does not infer success. No background process automatically tracks work; the coding agent or user must record checkpoints. The journal is local and gitignored under .agentic-dev/state/.

## Workspace verification

For sibling repositories, create a workspace root and the following file at .agentic-dev/workspace.json:

    {
      "schema_version": 1,
      "repositories": [
        {"name": "backend", "path": "backend"},
        {"name": "mobile", "path": "mobile"}
      ]
    }

Each member must be an existing direct child directory. The workspace process does not clone or modify member repositories. Run:

    python3 .agentic-dev/bin/ade-harness.py --target . workspace
    python3 .agentic-dev/bin/ade-harness.py --target . workspace --check fast

The first displays member setup state. The second executes the specifically configured fast check in each member and fails if any member check fails or is blocked. Do not call this cross-repo contract compatibility verification; API review and merge order remain separate.

## Sensor proofs

Create .agentic-dev/sensors.json with a sensor, its executable argv array and two project-relative fixture files:

    {
      "schema_version": 1,
      "sensors": [
        {
          "id": "no-production-fixtures",
          "argv": ["python3", "scripts/check-fixture.py", "{path}"],
          "clean": "tests/fixtures/synthetic.txt",
          "violation": "tests/fixtures/prod-marker.txt",
          "timeout_seconds": 30
        }
      ]
    }

Run:

    python3 .agentic-dev/bin/ade-harness.py --target . sensor-proof --sensor no-production-fixtures

The proof requires the clean fixture to exit zero and the violating fixture to exit nonzero. It never creates or plants the fixture. Both fixtures and the checker must be authored and reviewed by the repository owner. This is proof against known fixtures only; a sensor is not automatically wired into the main check, CI, or Git hooks by this command. Mark invariant enforcement only once those integrations are verified.

## Safety and limitations

Everything is explicit. Commands are argv arrays, not shell interpolation. Repositories are not merged or deployed. Session journals and evidence are excluded from Git by .agentic-dev/.gitignore, not uploaded anywhere. Current journal writes are not a multi-host distributed task store, and workspace checks do not synchronize independent Git branches.


## Journal recovery

Each operation locks the journal before reading and writing. A trailing incomplete JSON record after a crash is ignored during status and truncated before a subsequent successful write; a malformed *complete* record is not discarded automatically. Back up the file and manually repair it before retrying. Only a local POSIX filesystem supporting advisory locks is supported.

If you already have a custom `.agentic-dev/.gitignore`, make sure it excludes `state/` and `evidence/`; ADE does not overwrite it. Existing `sensors.json` configurations are user-owned and preserved.
