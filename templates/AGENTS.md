# Project Agent Instructions

This repository uses a project-local Agentic Development Environment (ADE) installation.

## Discover ADE resources

- Selected skills are installed under .agents/skills/ and/or .claude/skills/ by the bootstrap script.
- Shared workflow definitions: .agentic-dev/workflows/
- Shared engineering policies: .agentic-dev/rules/
- Output templates: .agentic-dev/templates/

Use native skill discovery for ordinary developer requests. For complete feature delivery, use the feature-delivery skill where installed. Refer to the applicable workflows, rules and templates when executing tasks.

## Project-specific context

Document your actual architecture, build/test commands, code-generation instructions and release constraints here. Do not invent commands.

## Safety and verification

Preserve user changes and follow the repository's stricter existing policies. Report real check outcomes. Creating a pull request is not merging it; merging, deploying and production data changes require explicit human authorization.

<!-- ADE ROUTING START v1 -->
## ADE skill selection

This repository uses the Agentic Development Environment. For each coding task,
consult `.agentic-dev/skill-map.json` and choose the relevant **installed**
primary skill. Supporting skills are optional; do not invoke absent skills.
Read its SKILL.md and follow relevant project rules. Descriptions are guidance,
not a guarantee that a model will select the correct skill automatically.

Before claiming completion, run the configured ADE checks where available;
missing, failed, or blocked checks are never passing evidence. Merging,
deploying, force pushing and changing production data require explicit
human authorization.
<!-- ADE ROUTING END -->
