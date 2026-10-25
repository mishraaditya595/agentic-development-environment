---
tags: [skill-creator, code-review]
max_turns: 20
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Review the current change in this repository. It adds a new API endpoint that returns account details and checks the caller's role in the web client before showing the response. Review it for security, correctness, privacy, and tests. Do not edit files, commit, or push. Tell me whether it is ready to merge.
