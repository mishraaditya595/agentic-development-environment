# ADE Harness Foundation

This first implementation supplements ADE's independent Agent Skills with a portable repository check runner, task routing metadata and evidence reports. It does **not** replace Codex/Claude/OpenCode or deterministically intercept every prompt.

## Installation

From an ADE checkout, preview and then install:

```sh
python3 scripts/bootstrap.py --target /path/to/project --agents codex,claude,opencode --preset standard --dry-run
python3 scripts/bootstrap.py --target /path/to/project --agents codex,claude,opencode --preset standard
```

The installer copies a filtered `.agentic-dev/skill-map.json` (primary and supporting skills present in the selected preset), an initially empty `.agentic-dev/harness.json`, and `.agentic-dev/bin/ade-harness.py` with its Python module.

Existing AGENTS.md and CLAUDE.md files are still preserved. If the project already has them, add a pointer manually: `For development tasks, consult .agentic-dev/skill-map.json and choose the matching installed primary skill.` The generated AGENTS.md in a new project includes the pointer. Native skill selection is model-dependent.

## Configure verification commands

Review actual project commands, then configure `.agentic-dev/harness.json`:

```json
{"schema_version":1,"checks":{"fast":{"argv":["flutter","analyze"],"timeout_seconds":180},"full":{"argv":["flutter","test"],"timeout_seconds":600}}}
```

Commands are passed directly as argument arrays, without shell evaluation or interpolation. They execute project code, so review them first. An empty registry does **not** mean checks passed. Edited configuration is user-owned and preserved during later additive ADE installs.

## Commands

```sh
python3 .agentic-dev/bin/ade-harness.py --target . doctor
python3 .agentic-dev/bin/ade-harness.py --target . check --check fast
python3 .agentic-dev/bin/ade-harness.py --target . verify --check fast --check full --criterion "Workout filters behave correctly"
python3 .agentic-dev/bin/ade-harness.py --target . --evidence .agentic-dev/evidence/verification-001.json verify
```

Nonzero exits fail; missing commands, timeouts and unconfigured checks are blocked. Reports are JSON. Acceptance criteria supplied via `--criterion` are only recorded—successful commands alone cannot establish that all requested behavior works.

Evidence files are create-only and may contain test output or secrets; review before sharing and exclude local evidence from version control.

An explicit failure probe may be invoked with `prove-failure --check-name full -- python3 -c 'raise SystemExit(1)'`. This checks only that the supplied probe fails, **not** that the configured `full` check detects a planted faulty test.

## Not yet implemented

Managed edits to existing AGENTS.md, runtime-specific lifecycle hooks, CI installation into consumer projects, isolated worktree red/green gate proofs, session restoration, invariant sensors and automatic correction loops, workspace coordination, and scored harness audits. These need dedicated tested additions; do not claim they already work.

Human authorization remains required to merge, deploy, force push or modify production data.
