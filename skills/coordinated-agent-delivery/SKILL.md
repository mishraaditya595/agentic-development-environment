---
name: coordinated-agent-delivery
description: Plans and coordinates multiple agents on genuinely independent software tasks with explicit ownership, dependencies, review gates, and bounded recovery.
license: Apache-2.0
---

# Coordinated Agent Delivery

Use multiple agents only when parallel work reduces time without hiding cross-file coupling. Keep small, tightly coupled, exploratory, or context-heavy work with one agent.

## Coordination contract

1. Decompose by independently reviewable outcome, not by arbitrary file count.
2. Give every task scope, owner, inputs, outputs, files, checks, dependencies, and stop conditions.
3. Assign one owner to shared interfaces and integration points.
4. Dispatch bounded work and track it on the current task board.
5. Verify each result against its contract before integration.
6. Resolve conflicts and run an integration check; do not assume parallel success composes.
7. Stop or re-plan when an agent is blocked, scope expands, or evidence is missing.

See [task boundaries](references/task-boundaries.md) and [review gates](references/review-gates.md).
