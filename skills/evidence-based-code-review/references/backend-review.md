# Backend and service review adapter

Use this reference when the change affects server handlers, services, domain logic, persistence, workers, jobs, external I/O, authentication, or multi-tenant data.

## Boundaries and ownership

- Keep transport layers responsible for parsing, calling, and serialization; keep business decisions in service or domain owners.
- Keep domain logic independent of request context where the repository’s architecture expects it.
- Keep business-agnostic libraries free of product, tenant, or feature policy.
- Reuse the canonical repository, gateway, validation, error, and authorization boundary instead of bypassing it with a direct client or duplicate helper.

## Data access and writes

- Enforce tenant, account, workspace, or object scope in the authoritative query or service boundary.
- Check explicit transaction boundaries, commit/rollback behavior, isolation, timeout, lock order, conflict detection, and idempotency.
- Keep transactions short enough for the workload and avoid hidden I/O in model properties, serializers, logging, or lazy accessors.
- Check row-count or version results when an update must affect exactly one current record.

## APIs and failures

- Trace producer and consumer contracts, exact types, nullability, enums, errors, pagination, retries, rate limits, and authorization.
- Fail closed on permission or security errors; do not swallow exceptions that leave state uncertain.
- Ensure retries and duplicate delivery cannot create partial or repeated side effects.

## Operations

- Check timeouts, connection pools, queue bounds, background-task lifecycle, cancellation, metrics, logs, and sensitive-data redaction.
- For feature flags or staged rollout, verify safe defaults, disabled-state behavior, old/new client compatibility, and rollback order.
