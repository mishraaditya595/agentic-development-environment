# Authoring discoverable skills

Most coding agents expose SKILL.md metadata and ask the model to choose relevant skills. This mechanism is probabilistic, not a deterministic keyword or webhook trigger.

## Metadata guidelines

- A stable kebab-case name must equal its package directory.
- The description states **when to use** the skill, common natural-language requests, expected output and **when not to use** it.
- Avoid vague descriptions ("helps with coding") and overlapping names for the same capability.
- Distinguish plan-creator (planning), plan-implementer (scoped execution), feature-delivery (full lifecycle), and evidence-based-code-review (read-only evaluation).
- Keep runtime-required scripts, assets and references within the independent skill package, not in the ADE root. Users of the skills CLI may install just one skill.
- Specify authorization and verification requirements. Never imply a review request authorizes editing, comments, merge or deployment.

## Example

    ---
    name: plan-creator
    description: >
      Write an implementation-ready plan with repository context,
      acceptance criteria and verification. Use for feature or
      migration planning before code changes. Do not use to execute
      an approved plan or to review a PR.
    license: Apache-2.0
    ---

## Routing evaluation

Each new package needs at least a positive trigger, negative trigger (close alternative), and difficult safety/quality case in evals/. In supported agents, record actual skill loading, agent version, installed paths, correctness and unauthorized side effects.

A negative case might say "implement the approved plan" to ensure plan-creator does *not* match. Agent assertions alone ("I used the skill") are not evidence without a tool trace.

## Layering

An existing AGENTS.md or CLAUDE.md can point to ADE policies and routing choices. Such guidance does not execute Markdown workflow files or override tool permissions. The portable feature-delivery skill is the directly invocable entrypoint for multi-stage delivery.

Published names are stable. evidence-based-code-review is the canonical review skill; code-reviewer describes its role and is not a duplicate package.
