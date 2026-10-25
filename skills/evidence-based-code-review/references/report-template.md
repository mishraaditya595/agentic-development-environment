# Code review report template

Use this exact order. Omit empty issue severity sections, but keep the other headings when they add useful context.

```markdown
# Code Review

## Summary

One or two sentences describing what changed and the most important conclusion.

## Scope

- Review target:
- Base or comparison point:
- Scope manifest: staged / unstaged / committed / untracked inclusion:
- Requirements used:
- Files or areas inspected:
- Files skipped and reasons:

## Verification

| Check | Result | Notes |
| --- | --- | --- |
| Repository lint/static analysis | pass/fail/not run | command and reason |
| Type check/build | pass/fail/not run | command and reason |
| Relevant tests | pass/fail/not run | scope and result |
| Migration/contract checks | pass/fail/not applicable | evidence |

Coverage: `reviewed / total` files (`coverage%` when meaningful)

Review axes:

- Spec compliance: pass / findings / not verified
- Standards and risk: pass / findings / not verified
- Independent pass: completed / unavailable / not needed

## Strengths

- Concrete positive observation with a file and line when useful.

## Findings

Each finding should include: severity, category/axis, precise location, triggering scenario, violated contract or invariant, evidence, concrete impact, smallest credible fix, confidence, and any evidence still needed.

### Critical

- `path/to/file:line` — **security**: what is wrong, concrete impact, evidence, and the smallest credible fix.

### Important

- `path/to/file:line` — **bug**: what is wrong, concrete impact, evidence, and the smallest credible fix.

### Minor

- `path/to/file:line` — **test**: localized issue and practical improvement.

## Recommendations

Non-blocking improvements or technical debt that are outside the changed behavior.

## Not verified

Checks or environments not available, with the reason and the evidence needed.

Do not describe a skipped or interrupted review as clean.

## Questions / decisions needed

Requirements or product decisions that prevent a confident verdict.

## Assessment

Ready to merge: Yes / With minor follow-ups / No / Needs discussion / Unable to assess

Reasoning: one concise paragraph tied to the findings and verification results.
```

## Finding quality bar

Every finding should have a precise location, a category, a concrete failure mode, an impact, and a credible remedy. Do not report a suspicion as a vulnerability or recommend an abstraction that you have not inspected. If the issue depends on an unanswered requirement, put it under Questions / decisions needed instead.
