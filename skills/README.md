# Published skills

This directory is the publishable skill catalog for [skills.sh](https://skills.sh). Each child directory is an independently usable package with `SKILL.md` as its entrypoint.

Add skills as `skills/<skill-name>/`. A package must include `SKILL.md`; it may include `references/`, `scripts/`, `assets/`, `evals/`, and a package-local `README.md`. Keep all runtime-required material inside the package and preserve stable `name`, `description`, and `license` frontmatter.

The canonical package layout and publishing rationale are documented in [`docs/architecture/repository-layout.md`](../docs/architecture/repository-layout.md). The first published package is `skills/evidence-based-code-review/`, whose public skill identifier remains `evidence-based-code-review`. Add future skills below `skills/` rather than as new root-level directories.
