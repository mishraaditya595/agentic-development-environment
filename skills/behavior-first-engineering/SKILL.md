---
name: behavior-first-engineering
description: Implements features, bug fixes, and behavior changes by defining observable behavior first, creating the strongest practical regression check, then making the smallest complete change.
license: Apache-2.0
---

# Behavior-First Engineering

Define what must be observable before writing implementation code. Prefer a failing automated check, but adapt honestly when the repository is legacy, testless, generated, configuration-only, migration-heavy, or UI-only.

## Cycle

1. Identify the behavior, boundary cases, and existing contract.
2. Write the smallest check that should fail before the change, when practical.
3. Run it and confirm the failure is meaningful rather than a setup error.
4. Implement only enough to satisfy the behavior.
5. Run the focused check, then the relevant broader suite.
6. Refactor only while behavior remains green.
7. Use `proof-before-done` principles before reporting completion.

For exceptions, name the replacement evidence: a migration dry run, typecheck, snapshot, browser flow, command transcript, or explicit manual protocol. Never use “too simple” as an unexamined reason to skip verification.

See [test design](references/test-design.md) and [legacy/testless guidance](references/legacy-and-testless-code.md).
