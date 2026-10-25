# Published skills

This directory is the publishable skill catalog for [skills.sh](https://skills.sh). Each child directory is an independently usable package with `SKILL.md` as its entrypoint.

Add skills as `skills/<skill-name>/`. A package must include `SKILL.md`; it may include `references/`, `scripts/`, `assets/`, `evals/`, and a package-local `README.md`. Keep all runtime-required material inside the package and preserve stable `name`, `description`, and `license` frontmatter.

The canonical package layout and publishing rationale are documented in [`docs/architecture/repository-layout.md`](../docs/architecture/repository-layout.md). The catalog currently includes `evidence-based-code-review`, `root-cause-investigation`, `proof-before-done`, `behavior-first-engineering`, `intent-to-implementation`, `review-feedback-triage`, `coordinated-agent-delivery`, and `branch-closeout`. Add future skills below `skills/` rather than as new root-level directories, and use original names and package-local evals.
