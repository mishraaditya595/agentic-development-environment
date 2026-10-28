# Engineering rules

- Read the target repository's instructions, architecture and relevant code before making changes; project-specific standards govern implementation details.
- Make the smallest coherent change satisfying the requested behavior. Avoid speculative abstractions, unrelated refactors and unapproved new dependencies.
- Preserve behavior outside the authorized scope; explain intentional breaking changes and verify compatibility.
- Handle errors, missing values, retries, async races and partial failure deliberately. Never silently convert unknown or absent data to a plausible value.
- Distinguish observation, inference and proposal. Do not invent files, APIs, commands or successful outcomes.
- Preserve pre-existing user edits and inspect the final diff for accidental changes.
- Evaluate impacts on callers, persistence, accessibility, performance and security when applicable.
- Never mark an acceptance criterion verified without an executed check or other direct evidence.
