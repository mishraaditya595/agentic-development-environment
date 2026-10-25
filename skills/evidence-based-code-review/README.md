# Evidence-Based Code Review

An independently usable Agent Skill for conservative, repository-aware review of code changes. It focuses on correctness, requirements, security, compatibility, tests, performance, architecture, maintainability, and evidence-backed reporting.

## Compatibility

This package is portable across repositories and agent runtimes. It requires read access to the repository and permission to run the repository's normal local checks; GitHub CLI, subagents, and language-specific tools are optional.

## Install

From this repository:

```bash
npx skills add ./ --skill evidence-based-code-review
```

After publishing:

```bash
npx skills add <owner>/<repository> --skill evidence-based-code-review
```

## Package contents

- `SKILL.md` — portable workflow and runtime entrypoint
- `references/` — detailed review lenses and reporting guidance
- `evals/` — representative evaluation cases and graders

`SKILL.md` is the runtime entrypoint. Keep runtime-required material inside this package and preserve its stable `name`, `description`, and `license` frontmatter.
