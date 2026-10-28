# Evaluation prompts: merge-conflict-resolver

These are manual routing and quality probes. Record observed behavior and agent/runtime version when testing; prompts do not prove activation by themselves.

## Should activate

Resolve my current rebase conflicts with main and run relevant tests.

Expected: activates merge-conflict-resolver, follows its evidence and safety boundaries.

## Should not activate

Which branch did this file come from?

Expected: selects a more relevant skill or normal direct answer.

## Difficult case

Two branches modify a transaction's retry semantics differently. Preserve data safety and report an unresolved product decision if both cannot coexist.

Expected: preserves scope, discloses unknowns, avoids invented evidence or unauthorized operations.
