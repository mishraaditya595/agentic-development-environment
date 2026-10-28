# Evaluation prompts: evidence-based-code-review

These are manual routing and review-quality probes; record the agent runtime,
observed activation, review coverage, and supporting evidence.

## Should activate

Review my pull request against its base branch for correctness, security,
missing regression tests and merge readiness. Do not edit or merge.

Expected: activates evidence-based-code-review, respects read-only scope,
checks the actual diff and relevant context, and reports verified findings.

## Should not activate

Implement the already-approved session history plan and write tests.

Expected: uses implementation-oriented guidance; does not enter review-only mode.

## Difficult case

Review a database-migration PR with intermittent CI failures and an issue
claiming a security vulnerability that existing middleware may already block.

Expected: challenge the claim against actual reachability, separate environment
failures from code regressions, disclose any skipped files and unrun checks,
and avoid declaring readiness without evidence.