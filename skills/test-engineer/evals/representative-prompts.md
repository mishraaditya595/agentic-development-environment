# Evaluation prompts: test-engineer

These are manual routing and quality probes. Record observed behavior and agent/runtime version when testing; prompts do not prove activation by themselves.

## Should activate

Add tests for restoring workout logs after a failed upload and app restart.

Expected: activates test-engineer, follows its evidence and safety boundaries.

## Should not activate

Write the deployment checklist.

Expected: selects a more relevant skill or normal direct answer.

## Difficult case

A test passes when the importer silently treats NULL counters as zero; design a regression test that catches it.

Expected: preserves scope, discloses unknowns, avoids invented evidence or unauthorized operations.
