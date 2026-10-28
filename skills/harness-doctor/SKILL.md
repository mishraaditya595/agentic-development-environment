---
name: harness-doctor
description: Inspect ADE installation, routing and project verification check configuration. Use when asked to diagnose harness readiness, missing checks or skill discovery. Do not imply that unconfigured checks have passed.
license: Apache-2.0
---

# Harness Doctor

1. Read repository instructions and inspect installed ADE paths.
2. If available run `python3 .agentic-dev/bin/ade-harness.py --target . doctor`.
3. Report detected routing map, configured checks and missing elements. Do not invent project commands.
4. Distinguish configuration health from executed verification and real model skill activation.
5. Read-only: do not modify files, run setup or deploy while diagnosing.
