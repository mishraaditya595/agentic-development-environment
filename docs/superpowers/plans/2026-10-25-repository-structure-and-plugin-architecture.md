# Repository Structure and Plugin Architecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the repository so published skills live under one manageable namespace, remain discoverable/installable through skills.sh, and can later be adapted into plugins for Claude Code, Codex, and other agent runtimes without duplicating the core behavior.

**Architecture:** Treat each skill as a self-contained package under `skills/<skill-name>/`, with `SKILL.md` as the portable source of truth and references/evals beside it. Treat runtime integrations as thin adapters under `plugins/<runtime>/<plugin-name>/`; adapters may add commands, hooks, agents, manifests, or runtime-specific instructions, but must not become the canonical implementation of a skill. Shared schemas, conventions, and validation live in `docs/` and `scripts/` rather than at repository root.

**Tech Stack:** Markdown skill format, YAML frontmatter, GitHub repository layout, `npx skills` CLI, optional runtime-specific JSON/Markdown manifests, shell-based validation.

## Global Constraints

- Keep every published skill independently usable through `skills.sh`.
- Preserve each skill’s stable `name`, `description`, and `license` frontmatter.
- Do not make a skill depend on private workspace files or local-only configuration.
- Keep review-only behavior read-only unless a user explicitly requests a separate fix mode.
- Do not add a runtime plugin until its runtime contract and registration path are documented.
- Preserve Apache-2.0 licensing and do not commit credentials or generated runtime state.
- Do not require a package manager or build system solely to validate Markdown skills.

---

### Task 1: Define the repository package layout

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `skills/README.md`
- Modify: `plugins/README.md`
- Create: `docs/architecture/repository-layout.md`

**Interfaces:**
- Produces the authoritative directory contract used by future contributors.

- [ ] **Step 1: Document the target tree**

Adopt this layout:

```text
skills/
  evidence-based-code-review/
    SKILL.md
    references/
    evals/
    README.md
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
  architecture/
  authoring/
research_notes/
reports/
```

Explain that `skills/` is the publishable catalog, `plugins/` contains runtime adapters, and `research_notes/`/`reports/` are not installable packages.

- [ ] **Step 2: Update contributor guidance**

Replace the current root-level `<skill-directory>` rule with `skills/<skill-name>/`. State that a skill package must contain `SKILL.md`, may contain `references/`, `scripts/`, `assets/`, and `evals/`, and must not import files from outside its own package.

- [ ] **Step 3: Update README install examples**

Change local installation to:

```bash
npx skills add ./ --skill evidence-based-code-review
```

Keep the published form:

```bash
npx skills add <owner>/<repository> --skill evidence-based-code-review
```

Add a “Catalog” section showing that future skills are added below `skills/` rather than as new root directories.

- [ ] **Step 4: Record the publishing rationale**

Document that skills.sh discovers valid `SKILL.md` files in repository folders, so nested packages allow one repository/pack while avoiding root-level clutter. Verify with `npx skills add ./ --list` and the selected skill install command.

- [ ] **Step 5: Review references**

Check every path in `AGENTS.md`, `README.md`, and `skills/README.md`; there must be no remaining instruction that expects `code-review/` at repository root.

### Task 2: Move the existing skill into the catalog namespace

**Files:**
- Move: `code-review/` → `skills/evidence-based-code-review/`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `skills/README.md`

**Interfaces:**
- Produces the first canonical package at `skills/evidence-based-code-review/`.
- Preserves the public skill identifier `evidence-based-code-review`.

- [ ] **Step 1: Move without changing skill content**

Move `SKILL.md`, `references/`, and `evals/` together. Do not rename the frontmatter `name` field or alter relative references during the move.

- [ ] **Step 2: Add package-local README**

Create `skills/evidence-based-code-review/README.md` with purpose, compatibility, install command, package contents, and a note that `SKILL.md` is the runtime entrypoint.

- [ ] **Step 3: Update all repository references**

Change root documentation and contributor instructions to point to `skills/evidence-based-code-review/`. Keep research material outside the package unless it is needed at runtime.

- [ ] **Step 4: Verify package isolation**

Read the moved `SKILL.md` and confirm every referenced file resolves within `skills/evidence-based-code-review/`.

### Task 3: Add lightweight skill validation

**Files:**
- Create: `scripts/validate-skills.sh`
- Create: `docs/authoring/skill-package.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Command: `./scripts/validate-skills.sh`
- Validates every `skills/*/SKILL.md` without requiring a package manifest.

- [ ] **Step 1: Define validation rules**

Validate that each package has `SKILL.md`, frontmatter delimiters, non-empty `name`, `description`, and `license`, and that relative Markdown links point to existing files.

- [ ] **Step 2: Implement the shell validator**

Use portable shell plus standard macOS tools already available in the repository environment. Exit non-zero with the package and failed rule; do not modify files.

- [ ] **Step 3: Document authoring rules**

Explain package boundaries, frontmatter stability, trigger descriptions, reference loading, eval placement, and how to run the validator and skills CLI listing.

- [ ] **Step 4: Verify failure and success paths**

Run the validator against the valid repository, then temporarily test a copy with missing frontmatter and confirm it fails. Remove the temporary fixture afterward.

### Task 4: Establish the cross-runtime plugin contract

**Files:**
- Create: `docs/architecture/plugin-contract.md`
- Modify: `plugins/README.md`
- Create: `plugins/README.template.md`

**Interfaces:**
- Defines the adapter contract for Claude Code, Codex, and future runtimes.

- [ ] **Step 1: Separate portable skills from adapters**

Document that `SKILL.md` owns workflow, safety rules, and evidence standards. A plugin owns only runtime registration, invocation UX, permissions, hooks, and any translation needed for that runtime.

- [ ] **Step 2: Define adapter metadata**

Require each plugin to document: runtime name/version range, install path, registration file, supported skills, required permissions, side effects, configuration, and verification command.

- [ ] **Step 3: Define capability mapping**

Use a table mapping portable concepts to runtime features:

```text
portable skill → Claude Code skill/command/agent/hook
portable skill → Codex skill/instruction/command integration
portable skill → other runtime’s native extension point
```

State that adapters may point to or package a skill, but must not fork its instructions without recording the divergence.

- [ ] **Step 4: Define versioning and compatibility**

Version portable skill behavior independently from runtime adapters. Record runtime compatibility in adapter metadata and use a compatibility matrix in each plugin README.

### Task 5: Scaffold runtime-specific plugin directories without implementing plugins

**Files:**
- Modify: `plugins/README.md`
- Create: `plugins/claude-code/README.md`
- Create: `plugins/codex/README.md`
- Create: `plugins/other/README.md`

**Interfaces:**
- Produces documented extension points, not empty fake plugins.

- [ ] **Step 1: Document Claude Code placement**

Describe where a future Claude Code plugin’s `.claude-plugin/plugin.json`, commands, agents, hooks, and plugin README belong. Require an explicit registration example before adding a real plugin.

- [ ] **Step 2: Document Codex placement**

Describe Codex-specific adapters as a separate namespace, with skills remaining portable and runtime-specific commands/configuration kept inside `plugins/codex/<plugin-name>/`.

- [ ] **Step 3: Document other runtimes**

Use `plugins/other/<runtime-name>/<plugin-name>/` rather than creating new root directories. Require a runtime contract before accepting a new adapter.

- [ ] **Step 4: Add a no-duplication rule**

State that a plugin cannot copy the full skill instructions as its source of truth; it must reference the canonical package or explain a deliberate runtime limitation.

### Task 6: Final publishing and regression verification

**Files:**
- Modify: `README.md`
- Modify: `skills/README.md`
- Modify: `plugins/README.md`
- Modify: `docs/architecture/repository-layout.md`

- [ ] **Step 1: Verify the package list**

Run:

```bash
./scripts/validate-skills.sh
npx skills add ./ --list
```

Expected: the validator passes and `evidence-based-code-review` is discoverable.

- [ ] **Step 2: Verify local install**

Run the documented local install command into a temporary destination or disposable test project and confirm the installed package contains `SKILL.md`, `references/`, and `evals/`.

- [ ] **Step 3: Verify documentation links**

Read all changed Markdown files and confirm examples use `skills/evidence-based-code-review/`, no root-level future-skill convention remains, and plugin documentation does not claim an unimplemented registration path.

- [ ] **Step 4: Check the final diff**

Run `git status --short` and `git diff --check`; inspect the complete diff for unrelated changes, broken relative paths, or accidental generated/private files.
