# Feature delivery workflow

**Trigger:** A developer asks to deliver a feature or a meaningful milestone, rather than merely to brainstorm it.
**Entry skill:** feature-delivery. Individual skills remain directly invocable.
**Inputs:** requested outcome, repository instructions, current branch, existing plan if provided.
**Outputs:** implementation, tests, review evidence, updated docs where applicable, and PR only if authorized.

| Stage | Responsible capability | Exit gate |
| --- | --- | --- |
| Discover | repo-onboarding (optional) | Relevant architecture, constraints and existing changes are understood |
| Plan | plan-creator (optional) | Tasks, acceptance criteria and risks documented for nontrivial work |
| Implement | plan-implementer (optional) | Scope implemented without discarding unrelated changes |
| Verify | test-engineer + proof-before-done (optional) | Applicable commands actually run; failures/blocks reported |
| Review | evidence-based-code-review (optional) | Blocking findings addressed; self-review labeled if not independent |
| Handoff | branch-closeout (optional) | Diff and evidence summarized; authorized PR prepared |

## Routing and recovery

- Skip heavyweight planning for trivial bounded edits, but never skip checking the requested behavior.
- If a requirement contradicts repository architecture, revise affected tasks before implementing.
- On failing tests, investigate and correct rather than reporting completion. If environmental, report exact blocker and verify what remains possible.
- On blocking review findings, return to implementation and rerun relevant tests before another review.
- On conflicting product requirements, surface the decision and continue independent safe work only.
- Do not merge, deploy, delete, force push or run production migrations without explicit approval.

## Required handoff

Use templates/task-handoff.md where installed. Report status of acceptance criteria, files touched, exact check outcomes, review findings, risks and PR link. The workflow file is guidance, not an auto-executing pipeline; the portable feature-delivery skill provides an independently installable entrypoint.
