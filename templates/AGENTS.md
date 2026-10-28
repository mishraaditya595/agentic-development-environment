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
