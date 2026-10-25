# Codex adapters

This namespace is reserved for real Codex runtime adapters. It documents the extension point and does not create a fake adapter, skill, or runtime manifest.

## Placement and separation

Each adapter belongs in `plugins/codex/<plugin-name>/` and may contain:

```text
<plugin-name>/
  README.md
  skills/
  commands/
```

Codex-specific commands, configuration, and invocation glue stay inside the adapter directory. Portable skills remain in `skills/<skill-name>/` and continue to be independently usable through skills.sh; do not move or fork a portable skill into `plugins/codex/`.

An adapter README must identify the Codex runtime/version range, exact install and registration procedure, supported canonical skill paths, permissions, side effects, configuration, verification command, and compatibility matrix. If Codex has no equivalent for a portable capability, document the fallback or limitation.

See the [cross-runtime plugin contract](../../docs/architecture/plugin-contract.md) and [`plugins/README.template.md`](../README.template.md).

## No duplication

Codex adapters may translate a portable skill into Codex-native instructions or commands, but they must not copy the full `SKILL.md`, references, or evals as a second source of truth. Record any deliberate divergence and its maintenance procedure in the adapter README.
