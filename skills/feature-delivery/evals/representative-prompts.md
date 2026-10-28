# Evaluation prompts: feature-delivery

These are manual routing and quality probes. Record observed behavior and agent/runtime version when testing; prompts do not prove activation by themselves.

## Should activate

Implement workout history end to end, review it, and raise a PR without merging.

Expected: activates feature-delivery, follows its evidence and safety boundaries.

## Should not activate

Explain a single method's control flow.

Expected: selects a more relevant skill or normal direct answer.

## Difficult case

A critical review issue persists after implementation; return to remediation and report that the PR is not ready.

Expected: preserves scope, discloses unknowns, avoids invented evidence or unauthorized operations.
