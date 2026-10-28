---
name: harness-verify
description: Validate completion using explicitly configured ADE project checks and verifiable acceptance criteria. Use before claiming a feature, bugfix or branch is finished or PR-ready. Do not merge or deploy.
license: Apache-2.0
---

# Harness Verify

1. Read repository instructions, actual requested behavior and change scope.
2. Run configured checks through the installed ADE harness when available. Missing execution tooling is blocked, not passed.
3. Record actual command results separately from acceptance-criteria evidence and review outcomes.
4. Inspect the diff for scope drift and important invariants. Passing tests alone is not proof all requirements are met.
5. Address authorized failures with bounded corrections; rerun checks and stop rather than repeatedly retrying without progress.
6. Report limitations, human review needed and exact evidence. Never merge, deploy or change production data without authorization.
