---
tags: [skill-creator, code-review]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Perform a deep review of the current change. It touches a public API, authentication middleware, a database migration, a dependency lockfile, a feature flag, and a frontend flow across many files. Review the exact requested scope, inspect repository rules and the originating spec, route the applicable risk packs, and account for every changed file. Use a second read-only review pass if available. Do not edit, commit, push, or install anything. Report confirmed findings separately from needs-verification items and recommendations, with a merge verdict.
