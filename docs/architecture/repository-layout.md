# Repository layout

This document is the authoritative directory contract for the repository.

## Target tree

```text
skills/
  evidence-based-code-review/
    SKILL.md
    references/
    evals/
    README.md
  root-cause-investigation/
  proof-before-done/
  behavior-first-engineering/
  intent-to-implementation/
  review-feedback-triage/
  coordinated-agent-delivery/
  branch-closeout/
plugins/
  claude-code/
    <plugin-name>/
      .claude-plugin/plugin.json
      README.md
      commands/
      agents/
      hooks/
  codex/
    <plugin-name>/
      README.md
      skills/
      commands/
  other/
    <runtime-name>/<plugin-name>/
docs/
  architecture/
  authoring/
research_notes/
reports/
```

## Directory responsibilities

- **`skills/`** is the publishable catalog. Every skill package is independently usable through skills.sh and has `SKILL.md` as its portable source of truth. A package may include `references/`, `scripts/`, `assets/`, `evals/`, and a package-local README, but runtime-required files must stay inside that package.
- **`plugins/`** contains runtime adapters. Adapters may add commands, hooks, agents, manifests, permissions, or runtime-specific instructions, but they must not become the canonical implementation of a skill or duplicate its full instructions.
- **`docs/architecture/`** and **`docs/authoring/`** contain repository-wide contracts and contributor guidance.
- **`research_notes/`** and **`reports/`** are source material and design records. They are not installable or publishable packages.
- **`.opencode/`** is local runtime state, including chat attachments and the existing `.opencode/.gitignore`; it is excluded by the root `.gitignore` and is not publishable skill or plugin content.

## Publishing rationale

skills.sh discovers valid `SKILL.md` files in repository folders. Nesting packages below `skills/` lets one repository publish a manageable catalog while avoiding root-level clutter and preserving independent package boundaries. Before publishing, verify discovery with:

```bash
npx skills add ./ --list
npx skills add ./ --skill evidence-based-code-review
```

The published form uses the same stable skill identifier:

```bash
npx skills add <owner>/<repository> --skill evidence-based-code-review
```
