# `<plugin-name>`

Thin adapter for **`<runtime>`**.

## Canonical skills

- Canonical package: `skills/<skill-name>/` — `<what this adapter exposes>`

## Runtime and compatibility

- Runtime: `<runtime name and supported version range>`
- Adapter version: `<version>`
- Compatibility matrix:

| Adapter | Runtime | Supported skill version | Status |
| --- | --- | --- | --- |
| `<version>` | `<runtime/version range>` | `<skill/version range>` | `<Supported/Experimental>` |

## Installation

- Install path: `<exact destination>`
- Install command/procedure: `<command or steps>`

## Registration and capability mapping

- Registration file: `<path>`
- Entry point: `<command, skill, agent, hook, or other extension point>`
- Portable workflow mapping: `<how SKILL.md is invoked>`
- Permissions/safety mapping: `<runtime controls>`
- Hooks or lifecycle behavior: `<paths or None>`

## Permissions and side effects

- Required permissions: `<filesystem/network/process/credential permissions>`
- Side effects: `<writes, commands, hooks, network calls, or None>`

## Configuration

`<Required and optional settings, defaults, and environment variables. Do not include secrets.>`

## Verification

```bash
<command that verifies registration and a representative invocation>
```

## Divergence and maintenance

This adapter does not duplicate the canonical skill instructions. If the runtime requires a limitation or translation, document it here:

- Divergence: `<None, or exact behavior that differs>`
- Impact: `<compatibility or workflow impact>`
- Update procedure: `<how this adapter stays aligned with skills/<skill-name>/SKILL.md>`
