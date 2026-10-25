# Review lenses

Apply these questions selectively. A lens that does not apply should be marked **not applicable**, not silently skipped.

## Lens activation

Always establish scope, requirements, repository rules, changed-file coverage, correctness, security triage, compatibility triage, relevant tests, and verification status. Add focused passes when the change signals them:

| Change signal | Conditional lenses |
| --- | --- |
| Public/API/auth/data boundary | Threat model, authorization, injection, data minimization, abuse cases, rate limits |
| Stateful, financial, queued, retried, or concurrent behavior | Invariants, state machine, idempotency, replay, race, atomicity, resource exhaustion |
| Schema/API/config/flag/deployment change | Compatibility, migration, rollout order, old/new readers, rollback, feature-gate leakage |
| Dependency/build/CI/container/release change | Supply chain, permissions, secrets, pinning, registry integrity, provenance, reproducibility |
| Backend, persistence, jobs, or external I/O | Transactions, data access, repository boundaries, operational behavior |
| UI, browser, component, navigation, or localization change | Accessibility, state ownership, query/cache, responsive behavior, UX |
| Large or high-blast-radius change | Independent axis review, strict structural review, and available dynamic/load/fuzz checks |

Path names are hints. Confirm the lens by following callers, consumers, contracts, and runtime behavior. A skipped file or interrupted pass must appear in coverage.

## 1. Requirements and correctness

- Does the implementation satisfy the stated behavior and acceptance criteria?
- Are all callers, consumers, registrations, exports, configuration defaults, and generated artifacts updated?
- Are null, empty, malformed, duplicate, boundary, retry, timeout, and partial-success cases handled?
- Does the change preserve invariants and ordering assumptions?
- Are asynchronous operations awaited, cancellable where needed, and safe after lifecycle changes?
- Are check-then-write sequences, retries, idempotency, and atomicity correct?
- Does error handling preserve useful context without exposing unsafe internal details?
- Does the implementation match the originating specification, issue, plan, or acceptance criteria? Keep spec compliance separate from standards compliance.

## 2. Security, privacy, and authorization

- What untrusted inputs, identities, files, queries, network calls, secrets, or personal data does the change touch?
- Are authentication, authorization, tenant boundaries, and server-side checks enforced at the real trust boundary?
- Are paths, queries, commands, templates, redirects, serialized data, and deep links validated safely?
- Could logs, metrics, traces, analytics, errors, caches, or test fixtures expose secrets or sensitive data?
- Are dependencies, permissions, cryptography, token handling, and deserialization appropriate for the risk?
- Use a lightweight threat model: identify assets, actors, trust boundaries, privileged operations, and the two or three highest-impact abuse paths.
- For a security finding, confirm attacker control, reachability, missing protection, and impact. Framework mitigations and unreachable paths are reasons not to report a pattern-only issue.

Read `security-checklist.md` when this lens applies.

## 3. Data, API, and persistence compatibility

- Can old data, queued work, cached state, or old clients still be read and processed?
- Are schema versions, migration steps, rollback behavior, indexes, and existing identifiers correct?
- Are public APIs, serialized formats, event payloads, command-line interfaces, and configuration keys backward compatible?
- Are changes to defaults, nullability, enums, pagination, sorting, time zones, encoding, and numeric precision safe?
- Does deployment order matter between clients, services, workers, and databases?
- Trace both producers and consumers, including generated clients, event handlers, CLI/configuration users, caches, and feature-flagged paths.

Read `compatibility-checklist.md` when this lens applies.

## 4. Failure handling and concurrency

- What happens on retries, duplicate delivery, cancellation, timeout, process restart, partial failure, or out-of-order events?
- Are shared resources protected from races, deadlocks, leaks, stale writes, and unbounded queues?
- Does failure leave a consistent recoverable state?
- Are transactions, locks, optimistic concurrency, or idempotency used where the surrounding architecture expects them?

## 5. Tests and verification

- Would a meaningful test fail if the change were reverted?
- Are expected values independent from the implementation under test?
- Do tests cover changed branches, invalid input, empty input, errors, retries, boundaries, and compatibility paths?
- Are integration or contract tests needed at an outer boundary?
- Were the relevant project checks actually run, and are their results reported accurately?
- Prefer behavior, contract, integration, and semantic UI assertions over private implementation details, cosmetic selectors, or tests whose mocks remove the behavior under review.
- Request a missing test only when the changed behavior is externally reachable or regression-prone and the test would protect a concrete contract.

## 6. Performance and resource usage

- Is there a named workload where this could become slow, expensive, or memory-heavy?
- Are queries indexed, lists bounded or paginated, and repeated calls batched where appropriate?
- Is heavy work kept out of hot paths, request handlers, render loops, startup, or the main thread?
- Could retries, polling, logging, caching, subscriptions, file handles, or background tasks grow without bounds?
- Is the performance concern evidenced by code structure, measurements, or repository conventions rather than intuition alone?

## 7. Architecture, reuse, and maintainability

- Does the change reuse an existing abstraction, utility, component, adapter, or policy?
- Does it introduce a forwarding wrapper, speculative option, one-implementation interface, duplicate validation, or feature-specific copy?
- Are boundaries, ownership, dependencies, and error contracts consistent with the repository?
- Is policy leaking into a shared layer, or is shared behavior being hard-coded for one tenant or feature?
- Did a refactor preserve validation, observability, tests, and public behavior?
- Does the change remove complexity or merely relocate it? Look for spaghetti branches, thin pass-through wrappers, unnecessary casts or optionality, wrong-layer logic, duplicated canonical helpers, avoidable sequential orchestration, partial updates, dead code, and files or changes too large to review safely.
- Treat file size or line count as a signal for investigation, not proof of a design defect.

## 8. User experience and accessibility

Apply when a user-facing surface changes:

- Are states for loading, empty, success, error, offline, permission denied, and retry understandable?
- Does the UI work with keyboard, screen readers, high contrast, localization, right-to-left text, and increased text size where applicable?
- Are touch targets, focus order, labels, semantic roles, color contrast, and non-color cues adequate?
- Are destructive actions confirmed and reversible where appropriate?
- Does navigation, browser history, back behavior, and deep linking remain coherent?

## 9. Operations and rollout safety

- Is the change observable through appropriate logs, metrics, traces, alerts, and correlation identifiers without leaking data?
- Can it be rolled back, disabled, feature-flagged, or migrated safely?
- Does it alter resource limits, rate limits, costs, deployment order, permissions, or on-call behavior?
- Are generated artifacts, build outputs, CI configuration, and release metadata consistent?
- Are feature gates, defaults, environment variables, ports, scripts, and rollback paths safe for both enabled and disabled states?

## 10. Adversarial and business-logic review

Apply when the change affects auth, workflows, money, quotas, inventory, permissions, public APIs, uploads, webhooks, queues, or concurrent state:

- Can a caller skip a required state transition or replay an operation?
- Can identifiers, prices, quantities, roles, hidden fields, or feature flags be tampered with?
- Are server-side values authoritative where clients can lie?
- Can retries, races, duplicate messages, or partial side effects create an invalid outcome?
- Are limits, time sources, numeric precision, and failure recovery consistent with the business invariant?

## 11. Supply-chain and build-integrity review

Apply when manifests, lockfiles, registries, install scripts, CI workflows, containers, build tooling, or release files change:

- Are dependency versions, lockfiles, checksums, registries, and action/image references pinned and consistent?
- Could dependency confusion, typosquatting, mutable tags, install hooks, or private-registry fallback alter what executes?
- Are CI permissions and secret exposure appropriate for untrusted pull requests?
- Are generated artifacts and release provenance reproducible enough for this repository?

## 12. Modern threat routing

Activate only when indicated by the technology or behavior:

- external URL fetching: SSRF, redirects, DNS rebinding, internal ranges, metadata services, timeouts;
- browser DOM or object merging: XSS, prototype pollution, DOM clobbering;
- WebSockets or streaming: origin/authentication, message validation, rate limits, lifecycle cleanup;
- GraphQL or flexible queries: depth, cost, batching, authorization, and pagination limits;
- LLM or agent integrations: prompt/indirect injection, tool authorization, data exfiltration, and untrusted retrieved content;
- uploads/archives/XML/serialization: path traversal, bombs, unsafe types, content validation, and resource limits.
