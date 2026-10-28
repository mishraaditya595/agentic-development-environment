# Evaluation prompts: plan-creator

These are manual routing and quality probes. Record observed behavior and agent/runtime version when testing; prompts do not prove activation by themselves.

## Should activate

Plan offline-first session history with regression tests and a rollout checklist.

Expected: activates plan-creator, follows its evidence and safety boundaries.

## Should not activate

Implement this already-approved task list.

Expected: selects a more relevant skill or normal direct answer.

## Difficult case

Plan an additive database migration where older app versions remain active and restore can be interrupted.

Expected: preserves scope, discloses unknowns, avoids invented evidence or unauthorized operations.
