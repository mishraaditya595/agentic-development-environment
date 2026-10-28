# Design review: Test Double Han coding skills

Source reviewed: [testdouble/han — han-coding/skills](https://github.com/testdouble/han/tree/main/han-coding/skills) (October 2026). Han is a reference for design choices, **not** an ADE runtime dependency or copied content. All ADE skill wording and implementation remain original and Apache-2.0 licensed.

## Principles adopted

| Han example | Concept | ADE adaptation |
| --- | --- | --- |
| [Skill catalog](https://github.com/testdouble/han/tree/main/han-coding/skills) | Positive and negative use cases clarify adjacent task boundaries | [Skill-routing guide](../authoring/skill-routing.md) and package-local negative-trigger evals |
| [Code overview](https://github.com/testdouble/han/blob/main/han-coding/skills/code-overview/SKILL.md) | Explain observed purpose and execution flow, distinguish observation from inferred intent | repo-onboarding separates code evidence, documentation and inference |
| [Automated test planning](https://github.com/testdouble/han/blob/main/han-coding/skills/automated-test-planning/SKILL.md) | Validate realistic behavior via public seams, not brittle private details | test-engineer and rules/testing.md enforce risk-based behavior tests |
| [Finding filters](https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/finding-filters.md) | Independently challenge findings against reachable paths and counter-evidence | evidence-based-code-review references/finding-challenge.md |
| [Output verification](https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/output-verification.md) | Check internal consistency and readability before presenting results | PR review workflow and review-report template final checks |
| [Refactor](https://github.com/testdouble/han/blob/main/han-coding/skills/refactor/SKILL.md) | Small behavior-preserving edits with a baseline and post-change checks | workflows/refactoring.md, including explicit testless-project limitation |
| [Architectural analysis](https://github.com/testdouble/han/blob/main/han-coding/skills/architectural-analysis/SKILL.md) | Scale depth of investigation to change size and risk | feature-delivery and review scale proportionally; specialist agents are optional |
| [Manual test planning](https://github.com/testdouble/han/blob/main/han-coding/skills/manual-test-planning/SKILL.md) | Manual acceptance checks are different from automated test evidence | Verification matrices distinguish automated, manual and blocked checks |

## Intentional ADE differences

- Every package is **independently usable** via standard SKILL.md; no Han plugins, Claude-only directives or mandatory sibling skills.
- No mandatory multi-agent swarm or ceremony for small edits. Scale investigation to risk and available tooling.
- No forced user approval for every design step; only consequential ambiguity or protected side effects require it.
- Native skill activation is model-dependent. Skills, workflows and routing docs cannot guarantee enforcement; CI and permissions must protect merges and releases.
- Never copy Han instructions, scripts, templates, framework-specific variables or helper logic into ADE.

## Evaluation

Use each package's positive, negative and difficult scenario prompts in a real installed runtime. Record skill actually loaded, results, misses, false activations, permissions and evidence behavior. Merely including a test prompt is not proof of successful activation.

Potential later scope: API-contract design and a dedicated architecture health skill, but only if routing evals show there is demand without unacceptable overlap.
