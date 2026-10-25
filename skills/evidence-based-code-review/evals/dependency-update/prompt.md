---
tags: [skill-creator, code-review]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Review the current change in this repository. It updates a production dependency and its lockfile. Check compatibility, licensing or supply-chain concerns visible in the repository, runtime behavior, build reproducibility, and test coverage. Do not edit files or install anything. Tell me what evidence is missing and whether the change is ready to merge.
