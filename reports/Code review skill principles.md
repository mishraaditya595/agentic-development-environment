# Code-review skill principles: implementation report

## Executive decision

Across the fifteen reference repositories covered by the research notes, the strongest common design is **an evidence-first generic review core with conditional rule packs and host adapters**. The local skill already has the right conservative spine: exact scope, repository discovery, selective lenses, precise findings, separate unknowns, and an explicit verdict. Extend that spine; do not turn the skill into a universal technology checklist.

### Incorporate into the generic core

1. **A reproducible scope contract.** Record the target, base/head or working-tree state, requested focus, included staged/untracked files, exclusions, and whether the diff is empty or unavailable. Preserve the requested scope on retries; never silently narrow it.
2. **Separate spec conformance from repository standards.** Report “does it implement the request?” separately from “is it safe and maintainable here?” Repository rules override generic smell heuristics.
3. **A lightweight threat/risk model before detailed lenses.** Identify changed entry points, assets, actors/tenants, trust boundaries, privileged operations, external systems, feature gates, and blast radius; trace the highest-impact abuse paths.
4. **Conditional lens routing.** Keep an always-on baseline—scope, correctness, security/privacy, compatibility, failure/concurrency, tests, maintainability, performance, and verification—then activate backend, frontend, API, database, accessibility, supply-chain, or operations checks from changed files, symbols, contracts, and behavior.
5. **Changed-file coverage accounting.** Report total, reviewed, skipped, and coverage rate, with a reason for every skip. A clean result must not conceal incomplete review.
6. **An evidence gate for every finding.** Require exact location, triggering scenario, reachable source/control, violated invariant or missing protection, concrete impact, evidence, and smallest credible remedy. Convert incomplete security or performance claims into “needs verification” items.
7. **Orthogonal severity and confidence.** Retain `Critical / Important / Minor`, but add confidence/reachability/evidence status. High impact with incomplete reachability is not a confirmed high-confidence finding.
8. **Behavior-focused test review.** Check whether a test would fail if the change were reverted, covers changed error/boundary paths, asserts contracts rather than implementation details, and uses an outer integration/contract test when needed.
9. **Explicit completion semantics.** Distinguish checked-and-passing, checked-and-failing, not run, not applicable, unable to inspect, and interrupted/skipped. “No findings” is never equivalent to proof of safety.
10. **Bounded independence and fix loops.** Use separate spec/standards or risk passes only when the change warrants it; preserve provenance and reconcile duplicates explicitly. In fix mode, implement → review → verify once or a small bounded number of times.

These principles are supported by the workflow, security, quality, and reporting references from Matt Pocock, Obra/Superpowers, Anthropic, CodeRabbit, Addy Osmani, Gemini CLI, Sentry, Cursor, Alibaba, wshobson, and Dify. The local implementation should preserve its existing read-only default, evidence bar, severity vocabulary, and verdicts.

## Keep as optional adapters or opt-in modes

| Adapter/mode | What belongs there | Activation condition |
| --- | --- | --- |
| **Relational database / SQL** | Parameter binding and identifier allowlists; query cardinality and joins; constraints and data integrity; execution plans; transaction/isolation/lock behavior; migration expand/contract, backfills, interruption and rollback evidence. | SQL, schema, migration, ORM, persistence, or database-facing changes. |
| **PostgreSQL** | JSONB/array operators and indexes, GIN/GiST, `CITEXT`, `TIMESTAMPTZ`, domains/enums, partitioning, PL/pgSQL, extensions, RLS, and PostgreSQL grants. | Confirmed PostgreSQL engine/version and repository convention. |
| **Backend framework** | Tenant predicates, repository boundaries, controller/domain direction, ORM session semantics, hidden I/O, dialect portability, and framework-specific contracts. | Matching framework or backend abstraction is present; do not prescribe Dify/SQLAlchemy paths globally. |
| **Frontend/UI** | Computed accessible names and final semantics, keyboard/focus through async states, forms/overlays, localization/zoom/forced colors/reduced motion, client query/cache/SSR ownership, and component lifetime. | Rendered UI, browser state, navigation, client data, or shared UI primitives change. Accessibility failures remain correctness defects. |
| **API/contract** | Producer-consumer tracing, generated-client readiness, exact DTO/nullability/enum behavior, status/error/pagination/rate-limit compatibility, cache keys/invalidation/retry, and rollout order. | Any public route, schema, serializer, event, generated client, config, or persistence format changes. |
| **Supply-chain/security integrations** | Lockfile integrity, registry scope, dependency confusion, install hooks, action pinning, artifact provenance/SBOM, CI permissions, and untrusted PR execution. | Manifests, lockfiles, package-manager config, build/install scripts, CI, containers, or release tooling change. |
| **Adversarial/modern-threat pack** | Business-logic abuse, replay/races, SSRF redirect/DNS/IP bypasses, prototype pollution, DOM clobbering, WebSocket controls, GraphQL cost, and LLM prompt/indirect injection. | Matching boundary, import, endpoint, protocol, or stateful workflow exists. |
| **Strict quality/deep-audit mode** | Change/file-size heuristics, complexity reduction, dead-code hygiene, mutation testing, fuzzing, load testing, staged artifacts, approval checkpoints, or multi-reviewer orchestration. | Explicit request, high blast radius, large diff, or repository tooling supports it. |
| **Host/provider adapters** | PR/issue/CI connectors, vendor CLIs, authentication and credential recovery, API transmission, billing/credits, NDJSON/vendor output, and publishing comments. | A host integration is actually configured; none should be a prerequisite for local review. |

Do not promote vendor syntax, exact framework defaults, CLI flags, authentication flows, numeric scores, or PostgreSQL mechanisms into the generic core. Portable goals—code/data separation, least privilege, data integrity, compatibility, bounded resource use, atomic/recoverable state, and evidence—belong in the core; mechanisms belong in adapters.

## Concrete implementation plan

The following files/sections should change in a later implementation. This report intentionally does not modify them.

### `skills/evidence-based-code-review/SKILL.md`

- **Operating rules:** add the scope manifest, separate severity from confidence, and define completed/skipped/not-verified semantics.
- **Phase 1 — Establish the scope:** require a validated fixed point or equivalent comparison, a non-empty/available target, explicit staged/untracked handling, and separate `Spec` and `Standards` inputs.
- **Phase 2 — Discover the repository:** collect a changed-file coverage manifest and identify routing signals from paths, imports, symbols, contracts, manifests, and deployment files—not paths alone.
- **Phase 3 — Review applicable lenses:** insert a compact threat/risk summary before lenses and reference a routing matrix for backend, frontend, API, database, accessibility, testing, supply-chain, and operations passes.
- **Phase 4 — Independent review:** define when a second pass is warranted, keep pass provenance, and state whether multi-pass review occurred and why.
- **Report/Verdict:** require coverage, confidence, reachability, evidence status, and unresolved assumptions in addition to the existing finding and verdict contract.

### `skills/evidence-based-code-review/references/review-lenses.md`

- Add a **Lens activation matrix** with behavior and file signals for backend, frontend, API/contract, database/migration, accessibility, testing, performance, supply-chain, and rollout.
- Expand **Failure and concurrency** with transaction boundaries, isolation, lock ordering, conflict detection, retry/idempotency, autocommit, partial success, and recoverable restart points.
- Expand **Tests and verification** with behavior-vs-implementation assertions, regression-test necessity, semantic UI queries, integration/contract boundaries, and optional bounded mutation checks.
- Expand **Performance** with causal workload evidence: N+1, unbounded fetches/retries, pagination, serialized independent work, query-plan/measurement requirements, and render/subscription cost.
- Expand **Architecture/maintainability** with canonical-helper reuse, ownership/dependency direction, thin wrappers, duplicate validation, complexity reduction, dead code, and safe change/file size.
- Expand **UI/accessibility** with final composed semantics, accessible-name computation, focus continuity, forms/overlays, localization, zoom/forced colors, and reduced motion.

### `skills/evidence-based-code-review/references/security-checklist.md`

- Add the dataflow record: asset/impact, actor, source, transformation, sink, protection, reachability, and evidence.
- Add explicit fail-closed, object/tenant authorization, sensitive-data minimization, and full SSRF lifecycle checks.
- Add a **conditional supply-chain pass** for manifests, lockfiles, registries, install hooks, CI actions, provenance, and untrusted execution.
- Add a **conditional adversarial/modern-threat pass** rather than applying protocol-specific checks to every review.
- State that attacker control and reachability must be confirmed before reporting a security defect; otherwise report the exact verification needed.

### `skills/evidence-based-code-review/references/compatibility-checklist.md`

- Add database migration prompts for lock duration, table rewrites, online/concurrent index/constraint builds, long-running backfills, expand/contract sequencing, dual-read/write periods, restart safety, observability, and rollback limits.
- Add schema/data-integrity prompts for primary/unique/foreign/check/not-null constraints, type/precision/time-zone semantics, defaults, orphan/invalid-value checks, and index/constraint compatibility.
- Add API/client/query/cache prompts for generated clients, exact type/nullability/enum behavior, cache invalidation/retry, SSR/dehydration, and URL/storage ownership.

### `skills/evidence-based-code-review/references/report-template.md`

- Add a **Review dimensions** block separating `Spec` and `Standards` conclusions.
- Add **Coverage** fields: total/reviewed/skipped files, exclusions, and coverage rate.
- Add **Confidence/evidence** fields to each finding: confidence, reachability, evidence observed, and evidence still needed.
- Keep the existing `Verification`, `Not verified`, `Questions / decisions needed`, and `Assessment` sections; do not add numeric category scores unless criteria are defined.

### New reference files and evaluation follow-up

- Add `skills/evidence-based-code-review/references/database-checklist.md` for portable SQL/database checks and evidence requirements.
- Add a separate PostgreSQL adapter/reference (for example `skills/evidence-based-code-review/references/adapters/postgresql.md`) and keep engine/version applicability explicit.
- If adapters grow, add parallel `backend`, `frontend`, `api-contract`, `supply-chain`, and `modern-threats` references rather than bloating the core file.
- Update `skills/evidence-based-code-review/evals/` after implementation: strengthen `database-migration`, `api-auth-change`, `dependency-update`, and `frontend-accessibility-change` expected outputs for routing, coverage, confidence, and evidence; add a large/high-blast-radius case if deep mode is introduced.
- Update `README.md` only to document the adapter/reference layout and the new report fields.

## Source links

The source links below preserve the references used in the research notes; local links point to the current implementation that the plan targets.

- [Local skill](../skills/evidence-based-code-review/SKILL.md), [review lenses](../skills/evidence-based-code-review/references/review-lenses.md), [security checklist](../skills/evidence-based-code-review/references/security-checklist.md), [compatibility checklist](../skills/evidence-based-code-review/references/compatibility-checklist.md), [report template](../skills/evidence-based-code-review/references/report-template.md)
- [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- [Obra requesting code review](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md) and [reviewer prompt](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- [Anthropic code-review skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/skills/code-review/SKILL.md) and [connectors](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/CONNECTORS.md)
- [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md), [CLI workflows](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/references/cli-workflows.md), and [auth/recovery](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/references/auth-recovery.md)
- [Addy Osmani code-review and quality](https://raw.githubusercontent.com/addyosmani/agent-skills/main/skills/code-review-and-quality/SKILL.md)
- [Gemini CLI code reviewer](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/.gemini/skills/code-reviewer/SKILL.md)
- [Dify backend review](https://raw.githubusercontent.com/langgenius/dify/main/.agents/skills/backend-code-review/SKILL.md) and [frontend review](https://raw.githubusercontent.com/langgenius/dify/main/.agents/skills/frontend-code-review/SKILL.md)
- [Sentry security review](https://github.com/getsentry/skills/blob/d12f250460ffd961f549dbebf7eeb0cf4afd4c2e/skills/security-review/SKILL.md), [SPEC](https://github.com/getsentry/skills/blob/d12f250460ffd961f549dbebf7eeb0cf4afd4c2e/skills/security-review/SPEC.md), and [security references](https://github.com/getsentry/skills/tree/d12f250460ffd961f549dbebf7eeb0cf4afd4c2e/skills/security-review/references)
- [Cursor thermo-nuclear review](https://github.com/cursor/plugins/blob/99b609a72323b70204eab407c622f436e858e112/thermos/skills/thermo-nuclear-review/SKILL.md) and [code-quality review](https://github.com/cursor/plugins/blob/99b609a72323b70204eab407c622f436e858e112/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md)
- [Alibaba open-code-review](https://github.com/alibaba/open-code-review/blob/375f64cd6f67a48a135da83cfcf59c52669a09cb/skills/open-code-review/SKILL.md) and [delegation workflow](https://github.com/alibaba/open-code-review/blob/375f64cd6f67a48a135da83cfcf59c52669a09cb/skills/open-code-review-delegate/SKILL.md)
- [wshobson pre-shipment reviewer](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/operating-kit/agents/code-review-preshipment.md), [PR reviewer](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/ship-mate/agents/review.md), and [full-review command](https://github.com/wshobson/agents/blob/0874a27b17a22e2b7c2e2bcd725768e0803cad06/plugins/comprehensive-review/commands/full-review.md)
- [GitHub Awesome Copilot SQL review](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md) and [PostgreSQL review](https://github.com/github/awesome-copilot/blob/main/skills/postgresql-code-review/SKILL.md)
