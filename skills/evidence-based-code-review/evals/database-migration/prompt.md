---
tags: [skill-creator, code-review]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Review the current change in this repository. It renames a persisted field and updates the latest schema definition, but the diff does not obviously include an upgrade step. Inspect the migration history, readers and writers, tests, and deployment assumptions. Do not edit files. Report compatibility risks and the merge verdict.
