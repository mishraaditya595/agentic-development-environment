---
name: plan-creator
description: >
  Write an implementation-ready, repository-grounded software development plan with scoped tasks, dependencies, acceptance criteria, verification and risks. Use when someone asks to plan a feature, architecture change, migration, or milestone without yet implementing it. Do not change production code.
license: Apache-2.0
---

# Plan Creator

Produce an actionable plan, not a generic wish list. Planning is read-only unless the user separately authorizes writing the plan document.

## Procedure

1. Inspect instructions and the relevant code, interfaces, tests, migrations, and existing design before suggesting changes.
2. State the desired observable behavior, scope, non-goals, constraints, and assumptions. Resolve only ambiguities that materially affect the approach.
3. Compare plausible approaches for meaningful trade-offs; choose the simplest compatible design and document why.
4. Break work into independently verifiable tasks, ordered by prerequisite and with precise boundaries. Do not fabricate paths; distinguish existing files from proposed files.
5. For each task, specify expected changes, acceptance criteria, testing (including failure and regression paths), dependencies, and completion evidence.
6. Account for rollout, backward compatibility, migration safety, security, data loss, documentation, and observability when applicable.
7. Finish with a definition of done and unresolved decisions. Mark environmental limitations.

## Plan output

Use a provided project plan template if one exists; otherwise include: objective; current state and evidence; recommended approach; in/out scope; ordered tasks; acceptance criteria; verification matrix; risks and rollback; dependencies; open questions.

## Boundaries

Do not start implementation while fulfilling a plan-only request. Do not require ceremonial approval for clearly authorized low-risk work. Never imply tests or prototypes ran during planning. For small self-contained edits, a short plan is sufficient; for high-risk migrations, be explicit about failure recovery.
