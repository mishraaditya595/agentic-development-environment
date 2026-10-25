# Evidence-Based Code Review

An open-source Agent Skill for rigorous, repository-aware code review across languages, frameworks, repositories, and toolchains.

> Establish the scope. Gather the evidence. Report only what the change supports.

It helps an AI reviewer establish the exact review scope, discover repository conventions, run available checks, inspect surrounding code, and report only evidence-backed findings. It is designed for pull requests, branches, commit ranges, uncommitted work, patches, and local folders.

## Why use it

Evidence-Based Code Review helps an AI reviewer:

- **Establish the exact scope** — review pull requests, branches, commit ranges, patches, uncommitted changes, or local folders.
- **Follow the repository** — discover its instructions, conventions, checks, tests, and existing abstractions instead of assuming a stack.
- **Route the right review lenses** — assess correctness, requirements, security, compatibility, data, tests, performance, architecture, maintainability, and UI quality when relevant.
- **Report evidence-backed findings** — separate blockers, recommendations, questions, and unverified areas.
- **Stay safe by default** — review-only mode does not edit, commit, push, merge, comment on remote systems, or publish results.
- **Support explicit fixing** — review-and-fix mode is separate from ordinary review and keeps the change bounded.

## Install

Install from a local checkout:

```bash
npx skills add ./ --skill evidence-based-code-review
```

Install after publishing the repository:

```bash
npx skills add <owner>/<repository> --skill evidence-based-code-review
```

## Quick start

Try prompts like:

```text
Review my uncommitted changes and tell me whether they are ready to merge.
```

```text
Review PR #42 for security, compatibility, and missing tests.
```

```text
Review this commit range against the repository’s own conventions. Do not change files.
```

## Catalog

The canonical package is `skills/evidence-based-code-review/`, with `SKILL.md` as its portable runtime entrypoint. Future skills belong below `skills/` rather than as new root-level directories.

## Repository layout

```text
skills/
  evidence-based-code-review/
    SKILL.md
    references/
    evals/
    README.md
plugins/
  claude-code/<plugin-name>/
  codex/<plugin-name>/
  other/<runtime-name>/<plugin-name>/
docs/
  architecture/
  authoring/
research_notes/
reports/
```

See [`docs/architecture/repository-layout.md`](docs/architecture/repository-layout.md) for the complete directory contract.

Runtime-specific integrations are documented separately in [`docs/architecture/plugin-contract.md`](docs/architecture/plugin-contract.md), with namespace guidance for [Claude Code](plugins/claude-code/README.md), [Codex](plugins/codex/README.md), and [other runtimes](plugins/other/README.md).

## License

Apache-2.0. See [LICENSE](LICENSE).
