# Skill package authoring

Each published skill is an independent package under `skills/<skill-name>/`.
The package's `SKILL.md` is its portable runtime entrypoint; supporting
`references/`, `scripts/`, `assets/`, and `evals/` may live beside it. A skill
must not import files from outside its own package.

## Stable metadata

`SKILL.md` starts with YAML frontmatter delimited by `---` lines. The
frontmatter must contain non-empty `name`, `description`, and `license` fields.
Keep `name` stable after publication. Make `description` specific enough to
explain the trigger and intended use, and preserve the repository's
Apache-2.0 licensing.

## References and evals

Keep reusable guidance in package-local `references/` files and link to them
with relative Markdown links. Reference links must resolve within the package;
do not rely on private workspace paths or local-only configuration. Put
representative prompts and graders under `evals/` so behavior can be checked
without making the skill depend on a particular runtime.

## Validation

From the repository root, run:

```sh
./scripts/validate-skills.sh
```

The validator checks every `skills/*/SKILL.md` for the required frontmatter
and verifies relative Markdown links point to existing package files. It uses
only portable shell and standard macOS tools and exits nonzero when a rule
fails. When available, also inspect the catalog with:

```sh
npx skills add ./ --list
```
