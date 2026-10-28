---
name: plan-implementer
description: >
  Implement an already agreed software plan or scoped task, maintaining traceability to acceptance criteria and producing verified test evidence. Use when asked to execute a plan, milestone, or task list; do not use for plan-only requests or independent code review.
license: Apache-2.0
---

# Plan Implementer

Execute the authorized plan systematically without silently changing its scope or claiming unrun checks.

## Procedure

1. Locate the specific plan and target repository instructions; verify the branch, worktree, starting state, and any pre-existing user changes.
2. Extract task dependencies and acceptance criteria. Check that the plan still matches current code; note material drift rather than forcing outdated instructions.
3. Implement tasks in dependency order, taking the smallest changes needed to satisfy behavior. Preserve user edits and existing architecture.
4. Add or update meaningful tests covering success, failure, state transitions, and regressions. Do not hide absent data with invented defaults.
5. Run the actual repository checks available in the environment. Capture command, outcome and relevant failure detail; distinguish unavailable tooling from code failures.
6. Update affected documentation, examples, migrations, and integration notes. Inspect the final diff for unrelated changes and secrets.
7. Report each acceptance criterion as verified, implemented but not verified, blocked, or not implemented. Hand off for independent review when appropriate.

## Scope changes and failures

If a new requirement or structural obstacle makes the approved plan unsafe or impossible, stop that affected work and explain the impact and a revision. Continue independent safe tasks when possible. Do not reclassify a failed test as passing. Do not erase uncommitted changes or force through merges.

## Authorization

Commits, remote pushes and PR creation require the relevant workflow authorization. Merging, production deployment, irreversible migration, branch deletion and force push require explicit human authorization; never infer approval from "finish the task".
