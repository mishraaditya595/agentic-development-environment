# Published skills

This directory is the publishable skill catalog for [skills.sh](https://skills.sh). Each child directory is an independently usable package with `SKILL.md` as its entrypoint.

Add skills as `skills/<skill-name>/`. A package must include `SKILL.md`; it may include `references/`, `scripts/`, `assets/`, `evals/`, and a package-local `README.md`. Keep all runtime-required material inside the package and preserve stable `name`, `description`, and `license` frontmatter.

The canonical package layout and publishing rationale are documented in [`docs/architecture/repository-layout.md`](../docs/architecture/repository-layout.md). The catalog currently includes `evidence-based-code-review`, `root-cause-investigation`, `proof-before-done`, `behavior-first-engineering`, `intent-to-implementation`, `review-feedback-triage`, `coordinated-agent-delivery`, and `branch-closeout`. Add future skills below `skills/` rather than as new root-level directories, and use original names and package-local evals.

## Additional independently installable packages

- repo-onboarding — discover existing architecture and real project commands.
- plan-creator — write implementation-ready plans without coding.
- plan-implementer — implement the scoped approved plan.
- merge-conflict-resolver — preserve intent from both sides while resolving Git conflicts.
- test-engineer — create behavioral and regression tests.
- feature-delivery — optional end-to-end workflow coordination (independently installable).

See [usage](../docs/usage.md) and [routing guidance](../docs/authoring/skill-routing.md). Root workflows/rules/templates are optional bundle-only guidance, not dependencies of individual skills.
