---
name: proof-before-done
description: Verifies claims that work is fixed, complete, tested, safe, ready, or mergeable by mapping each claim to actual evidence and clearly reporting gaps.
license: Apache-2.0
---

# Proof Before Done

Before claiming completion, list the claims the user will rely on and gather the narrowest credible evidence for each.

## Method

1. Identify relevant claims: behavior, regression safety, build/type correctness, user-visible operation, repository compliance, and release readiness.
2. Find the repository's real checks and the fastest meaningful user-path check.
3. Run checks and inspect output; do not infer success from intent, silence, or a dispatch receipt.
4. Label each claim `passed`, `failed`, `skipped`, `unavailable`, `not applicable`, or `not verified`.
5. Report coverage, failures, environmental limits, assumptions, and next actions.

Run the full relevant suite when affordable, even if a focused test passes. Never call work clean when required evidence was skipped.

See [the evidence matrix](references/evidence-matrix.md).
