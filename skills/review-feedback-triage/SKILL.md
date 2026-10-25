---
name: review-feedback-triage
description: Evaluates code-review comments and audit feedback against the actual repository before implementing, accepting, clarifying, or pushing back on each item.
license: Apache-2.0
---

# Review Feedback Triage

Read all feedback first. Translate each item into a technical requirement, inspect the affected code and repository constraints, then decide what evidence supports action.

## Classification

Use: confirmed defect, valid improvement, clarification needed, context-dependent recommendation, unsupported claim, or out of scope. Resolve unclear items before partially implementing a multi-item request.

## Execution

Prioritize security, correctness, compatibility, and data integrity. Check actual usage before accepting speculative “professionalization” work. Implement one item at a time, add a regression check when behavior changes, and verify the result. Push back with concrete code, tests, or compatibility evidence when a suggestion is wrong.

See [feedback classification](references/feedback-classification.md).
