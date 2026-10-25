---
name: branch-closeout
description: Closes out completed development work by checking repository state, verification evidence, diff hygiene, open risks, and authorized next-step options without performing external side effects implicitly.
license: Apache-2.0
---

# Branch Closeout

Use when implementation is complete or someone asks whether a branch, worktree, or change is ready to hand off.

## Closeout

1. Inspect status, staged/unstaged/untracked files, diff, and repository instructions.
2. Run the relevant checks and record exact results.
3. Check documentation, generated files, secrets, unrelated edits, and missing regression coverage.
4. Summarize changed files, evidence, gaps, assumptions, and remaining risks.
5. Present authorized next-step options: continue, create a commit, open a PR, merge, keep, or discard. Do not push, publish, merge, or delete without explicit authorization.

A clean diff is not proof of correct behavior. Use `proof-before-done` principles and state what was not verified.

See [the closeout checklist](references/closeout-checklist.md).
