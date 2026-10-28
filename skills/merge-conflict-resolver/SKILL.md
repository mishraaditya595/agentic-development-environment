---
name: merge-conflict-resolver
description: >
  Resolve Git merge, rebase, or cherry-pick conflicts by examining both sides and retaining intended behavior, then verify the integration. Use when the developer asks to fix conflicts or complete a conflicted merge. Do not use for ordinary code review or silently discard one side.
license: Apache-2.0
---

# Merge Conflict Resolver

A conflict marker removed is not proof that the integration is correct.

## Procedure

1. Inspect git status, operation in progress, base and target refs, repository instructions and existing uncommitted work. Do not start a merge just to explore.
2. Locate every conflict, including rename/delete, file mode, generated artifacts, dependency lockfiles, migrations, and semantic conflicts without markers.
3. Inspect base, ours, and theirs as well as relevant callers and tests; understand the purpose of each change before deciding a resolution.
4. Choose a resolution that preserves requirements from both sides where compatible. If requirements truly conflict, describe alternatives and seek a decision instead of guessing.
5. Keep edits focused on the conflict; apply necessary integration changes and update tests that express combined behavior.
6. Run syntax checks and relevant tests, search for leftover conflict markers, and inspect the resulting staged/unstaged diff.
7. Report conflicts resolved, rationale per nontrivial choice, checks run, and remaining semantic risks.

## Safety and limits

Do not blindly select ours/theirs, discard unrelated local changes, use force push, abort an operation destructively, or amend published commits without explicit authorization. Do not claim to have completed a rebase or merge when Git still reports conflicts. If tooling is unavailable, give manual resolutions with clear verification gaps. Never merge a PR into a protected branch without explicit human approval.
