# Other runtime adapters

Use this namespace for runtimes that do not have a dedicated top-level adapter namespace. This README documents the convention; it is not an adapter and must not be accompanied by a fake runtime manifest.

## Namespace convention

Create adapters at:

```text
plugins/other/<runtime-name>/<plugin-name>/
```

`<runtime-name>` is the stable, lowercase runtime namespace. `<plugin-name>` identifies the adapter. Keep the runtime's manifests, commands, hooks, agents, configuration, and README inside that plugin directory. Do not create a new root-level directory for a runtime.

Before accepting an adapter, document its runtime contract and registration path, including the exact extension point, supported runtime/version range, install path, canonical skills, permissions, side effects, configuration, verification, and compatibility matrix. Use [`plugins/README.template.md`](../README.template.md) as the README starting point.

## No duplication

The canonical workflow remains in `skills/<skill-name>/SKILL.md`. An adapter may add only the target runtime's integration glue and must reference the canonical package rather than copy its full instructions, references, or evals. Explain any deliberate runtime limitation, divergence, and update procedure in the adapter README.

See the [cross-runtime plugin contract](../../docs/architecture/plugin-contract.md) for the shared rules.
