# Manual routing and quality probes

These are **not** executable model-routing tests. Install ADE in a real test repo for each supported agent, then observe what skill was actually loaded.

| User request | Expected primary skill |
| --- | --- |
| Review this PR for regressions; do not edit | evidence-based-code-review |
| Plan a safe migration, no code yet | plan-creator |
| Implement docs/plans/history.md | plan-implementer |
| Fix this conflicted rebase | merge-conflict-resolver |
| Add tests for interrupted restore | test-engineer |
| Map this unfamiliar repository before changes | repo-onboarding |
| Build a feature and open a PR, never merge | feature-delivery |
| Investigate the intermittent 500 | root-cause-investigation |
| Explain this single function | None required |

Record agent/runtime version, installed paths, prompt, expected selection, **observed loaded skill**, output quality, security/authorization behavior, false matches and missed activations. Test two high-risk cases: a failing test must be reported as a failure, and a conflicting transaction invariant must not be resolved via blind ours/theirs selection.

CI validates files and installer behavior; it cannot assert model routing without an agent-runtime harness.
