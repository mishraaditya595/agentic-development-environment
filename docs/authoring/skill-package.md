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

## Originality and enhancement

Outside repositories may inform a skill, but the package must use original
names, wording, examples, and decision rules. Add a package-local note when
another project materially influenced the design. Enhance imported ideas with
repository-aware exceptions, explicit evidence states, bounded failure
handling, and this app's authorization rules. Do not make users approve a
design or side effect when the request is already clear and low risk.

## Validation

From the repository root, run:

```sh
./scripts/validate-skills.sh
```

The shell entrypoint delegates to `scripts/skill_validation.py`, the single Python 3.9+ stdlib validator also imported by `validate-ade.py`. It checks required frontmatter, canonical names/licenses, local Markdown links and evaluation prompts for **every** skill, without special-case exceptions. It exits nonzero when a rule fails. When available, also inspect the catalog with:

```sh
npx skills add ./ --list
```

## Cross-agent routing and package boundaries

See [skill routing](skill-routing.md) for descriptions, positive/non-trigger evals, and the distinction between native discovery and deterministic enforcement. New standalone skills must contain their own necessary references; do not depend on shared workflows/, rules/ or templates/ in the root checkout.

For changes involving installer or shared documents, also run:

    python3 scripts/validate-ade.py
    python3 -m unittest discover -s tests -v

The bootstrap requires Python 3.9+ with POSIX secure directory-descriptor support. It checks all destination conflicts before writing, refuses symlinks, and attempts to remove new files and empty directories if a write fails.
