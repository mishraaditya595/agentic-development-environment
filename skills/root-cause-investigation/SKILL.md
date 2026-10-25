---
name: root-cause-investigation
description: Investigates bugs, regressions, failing tests, build failures, integration issues, performance anomalies, and surprising behavior before proposing a fix. Use evidence checkpoints and stop guessing when the root cause is not established.
license: Apache-2.0
---

# Root-Cause Investigation

Use this skill whenever behavior is wrong or unexpectedly different. Do not begin with a fix. Begin with an evidence trail.

## Workflow

1. State the symptom, impact, exact reproduction, and what is not yet known.
2. Read the complete error, stack trace, logs, diff, and relevant repository instructions.
3. Reproduce the issue or record why reproduction is unavailable.
4. Map component boundaries and trace the bad value backward to its earliest proven source.
5. Compare the failing path with a working example and list concrete differences.
6. Write one falsifiable hypothesis with supporting evidence and one minimal test.
7. Add or identify a regression check before changing production behavior when practical.
8. Make one focused change, rerun the check, and record the result.
9. If three focused hypotheses fail, stop and assess whether the architecture or environment is the actual problem.

## Evidence rules

Separate observed facts, inferences, hypotheses, and unresolved questions. Instrument boundaries only with safe, redacted diagnostics. Never expose secrets or treat a keyword match as proof of causality.

## Output

Report reproduction, root cause, evidence chain, fix scope, checks run, remaining gaps, and confidence. Environmental failures are separate from code findings.

## Boundaries

This skill does not authorize destructive changes, production actions, or broad refactors. A spike may be exploratory, but keeping spike code requires a separate decision.

See [the workflow checklist](references/workflow-checklist.md) and [failure modes](references/failure-modes.md).
