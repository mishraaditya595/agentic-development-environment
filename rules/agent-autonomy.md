# Agent autonomy and authorization

This policy is an instruction layer, not a technical sandbox. Enforce critical controls with repository permissions and CI.

| Operation | Default |
| --- | --- |
| Read repository; inspect history; create local plans | Allowed |
| Edit files within explicitly requested task on working branch | Allowed |
| Run existing non-destructive tests and linters | Allowed |
| Create local commits, push branches, open PRs | Only when requested or permitted by a selected workflow |
| Modify remote issues, approvals or review threads | Only when requested |
| Merge, deploy, production migration, force push, branch deletion, irreversible data changes | Requires explicit human authorization |

- Do not reinterpret approval to open a PR as approval to merge it.
- Do not silently expand scope to bypass a blocker.
- Respect repository-specific restrictions that are stricter than these defaults.
- Report unknown permissions instead of guessing or circumventing them.
