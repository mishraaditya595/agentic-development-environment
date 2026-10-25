---
name: intent-to-implementation
description: Turns ambiguous or consequential development requests into an implementation-ready decision by inspecting the repository, clarifying the outcome, comparing approaches, and recording assumptions and non-goals.
license: Apache-2.0
---

# Intent to Implementation

Use proportional discovery. A clear, bounded edit can proceed. A request with product ambiguity, architectural trade-offs, or meaningful risk needs a short decision record before implementation.

## Workflow

1. Inspect the existing code, instructions, tests, and constraints before asking questions.
2. Restate the outcome, users, success measure, goals, non-goals, and anti-goals.
3. Ask only the question whose answer would materially change the result.
4. Compare credible approaches and recommend one with trade-offs.
5. Record assumptions, compatibility constraints, rollout/rollback concerns, and open decisions.
6. Hand implementation a concise scope and verification plan.

Do not create ceremony for a typo, localized edit, or fully specified small change. A spike is allowed when learning is the goal, but label it exploratory and do not silently turn it into production implementation.

See [decision-record guidance](references/decision-record.md).
