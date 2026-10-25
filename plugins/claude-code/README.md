# Claude Code adapters

This namespace is reserved for real Claude Code runtime adapters. It documents placement and registration; it is not itself a plugin and does not include a fake manifest or placeholder implementation.

## Placement

Each adapter belongs in `plugins/claude-code/<plugin-name>/` and may contain:

```text
<plugin-name>/
  .claude-plugin/plugin.json
  README.md
  commands/
  agents/
  hooks/
```

- `.claude-plugin/plugin.json` is the adapter's Claude Code manifest and registration metadata.
- `commands/` contains runtime-specific command entry points.
- `agents/` contains runtime-specific agent definitions.
- `hooks/` contains lifecycle hooks, when the adapter needs them.
- `README.md` documents the canonical skills, runtime/version range, install path, registration file, permissions, side effects, configuration, verification, and compatibility matrix.

The portable workflow remains in `skills/<skill-name>/SKILL.md`. Commands, agents, and hooks should invoke or reference that package rather than reproduce it.

## Registration requirement

Before adding a real adapter, its README must include an explicit registration example showing the intended install destination and how `.claude-plugin/plugin.json` registers the adapter with Claude Code. The example must use the actual runtime contract and must not claim that an unimplemented plugin is registered. Verify both registration and a representative invocation with a concrete command or runtime action.

See the [cross-runtime plugin contract](../../docs/architecture/plugin-contract.md) and [`plugins/README.template.md`](../README.template.md) for required metadata.

## No duplication

Do not copy the full `SKILL.md`, references, or evals into a Claude Code adapter. Document any deliberate runtime limitation or translation and its compatibility impact in the adapter README.
