# Cross-runtime plugin contract

This contract defines how runtime adapters in `plugins/` relate to portable skill packages in `skills/`. It applies to Claude Code, Codex, and future runtimes.

## Portable skill versus runtime adapter

The canonical implementation is always the package at `skills/<skill-name>/`. Its `SKILL.md` owns:

- the workflow and decision procedure;
- safety rules, scope, and user-consent requirements;
- evidence, quality, and completion standards; and
- references, scripts, assets, and evals needed by the portable workflow.

A runtime adapter at `plugins/<runtime>/<plugin-name>/` owns only the integration boundary:

- runtime registration and manifest files;
- invocation UX such as commands, agents, or instructions;
- runtime permissions and configuration;
- hooks and lifecycle behavior; and
- translation required to express the portable skill through that runtime.

An adapter may point to or package a canonical skill, but it must not become a second source of truth. Runtime-specific behavior belongs in the adapter only when the runtime requires it.

## Required adapter documentation

Every plugin directory must contain a `README.md` using [`plugins/README.template.md`](../../plugins/README.template.md) as its starting point. The README must state:

| Field | Required content |
| --- | --- |
| Runtime | Runtime name and supported version range, for example `Claude Code >= 1.x < 2.x`. |
| Install path | Exact destination and installation command or procedure. |
| Registration | Registration file and entry point, such as `.claude-plugin/plugin.json` or a Codex configuration entry. |
| Supported skills | Canonical package paths and stable skill names supported by the adapter. |
| Permissions | Filesystem, network, process, credential, or other permissions required. |
| Side effects | Commands, hooks, writes, network calls, or other effects caused by installation or invocation. |
| Configuration | Required and optional settings, defaults, and environment variables. Never commit secrets. |
| Verification | A concrete command or runtime action that proves registration and invocation work. |
| Compatibility | A matrix pairing adapter versions with supported skill versions and runtime versions. |

If a runtime limitation requires diverging from `SKILL.md`, document the exact divergence, affected behavior, and compatibility impact in the plugin README. Do not silently rewrite the workflow.

## Capability mapping

Adapters map the same portable skill concepts to each runtime's native extension points:

| Portable concept | Claude Code adapter | Codex adapter | Other runtime adapter |
| --- | --- | --- | --- |
| Skill workflow | Claude Code skill, command, or agent instructions | Codex skill or instruction integration | The runtime's native skill/instruction extension point |
| Invocation | Command, agent entry point, or documented skill invocation | Skill invocation or runtime command integration | Native command, action, or invocation mechanism |
| Permissions and safety boundary | Plugin manifest, permissions, and hooks | Runtime configuration and command restrictions | Native permission and policy mechanism |
| Lifecycle behavior | Hooks under `hooks/` when required | Runtime-supported hooks or configuration | The runtime's documented lifecycle extension point |
| Portable references/evals | Reference the canonical package; do not duplicate them | Reference the canonical package; do not duplicate them | Reference the canonical package; do not duplicate them |

The adapter README must identify the actual files implementing each mapping. If a capability has no equivalent, say so and describe the fallback.

## Versioning and compatibility

Version portable skill behavior independently from runtime adapters. A change to workflow, safety rules, evidence standards, or package interfaces requires a skill-version note; a change to registration, hooks, commands, or runtime configuration requires an adapter-version note.

Each plugin README must include a compatibility matrix, for example:

| Adapter | Runtime | Supported skill | Status |
| --- | --- | --- | --- |
| `1.0.x` | Claude Code `1.x` | `evidence-based-code-review` `1.x` | Supported |

Use explicit ranges and record breaking changes. An adapter must fail clearly or document degraded behavior when its runtime or supported skill version is outside the stated range. Verification commands should test both registration and a representative invocation.

## No-duplication rule

A plugin must not copy the full contents of a skill's `SKILL.md`, references, or evals as its source of truth. It must reference `skills/<skill-name>/` and add only the runtime glue required for registration and invocation. If packaging constraints require generated or copied content, document its source, generation/update procedure, and divergence check in the adapter README; generated runtime state and credentials must not be committed.

Do not create a plugin until this contract and the runtime's registration path are documented. Do not add a new top-level runtime directory: use `plugins/claude-code/`, `plugins/codex/`, or `plugins/other/<runtime-name>/`.
