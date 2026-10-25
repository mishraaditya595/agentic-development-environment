# Runtime plugins

This directory contains thin adapters for agent runtimes. Portable workflow, safety rules, and evidence standards belong in `skills/<skill-name>/SKILL.md`; plugins own only runtime registration, invocation UX, permissions, hooks, manifests, and runtime-specific translation.

The complete adapter contract is in [`docs/architecture/plugin-contract.md`](../docs/architecture/plugin-contract.md). Use [`README.template.md`](README.template.md) for each future plugin README. The pages for [Claude Code](claude-code/README.md), [Codex](codex/README.md), and [other runtimes](other/README.md) define namespace-specific placement rules.

## Layout

```text
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
```

Add a plugin only when its runtime contract and registration path are documented. A plugin must not copy the full skill instructions as its source of truth; it should reference the canonical skill package or document a deliberate runtime limitation. Research notes and reports are not plugins.

## Namespace rules

- Put Claude Code adapters in `plugins/claude-code/<plugin-name>/`.
- Put Codex adapters in `plugins/codex/<plugin-name>/`; portable skills remain under `skills/`.
- Put every other runtime under `plugins/other/<runtime-name>/<plugin-name>/`.
- Do not create fake plugins, placeholder manifests, or empty runtime packages. A namespace README documents an extension point; a plugin directory is added only when its implementation and registration path are real and documented.

## No duplication

`skills/<skill-name>/SKILL.md` is the canonical source of workflow, safety rules, and evidence standards. A plugin may add only runtime glue—registration, commands, agents, hooks, permissions, configuration, or translation. It must reference the canonical package rather than copy the full skill instructions, references, or evals. If a runtime limitation requires divergence, record the exact limitation and its impact in the plugin README using [`README.template.md`](README.template.md).

## Required plugin README

Every plugin must document its runtime and version range, install path, registration file, supported skills, required permissions, side effects, configuration, verification command, and compatibility matrix. Record any deliberate divergence from the canonical skill instructions. Do not commit credentials or generated runtime state.
