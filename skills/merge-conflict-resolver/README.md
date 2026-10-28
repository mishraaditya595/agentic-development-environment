# merge-conflict-resolver

Portable Agent Skills package for the Agentic Development Environment.

**Use when:** Resolve Git merge, rebase, or cherry-pick conflicts by examining both sides and retaining intended behavior, then verify the integration. Use when the developer asks to fix conflicts or complete a conflicted merge. Do not use for ordinary code review or silently discard one side.

Install from the public repository:

    npx skills add mishraaditya595/agentic-development-environment --skill merge-conflict-resolver

The entrypoint is [SKILL.md](SKILL.md). [Evaluation prompts](evals/representative-prompts.md) are examples for manual routing and quality assessments. The package is independently usable without installing the full ADE environment.

License: Apache-2.0.
