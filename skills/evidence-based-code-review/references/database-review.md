# Relational database review adapter

Use this reference only when SQL, schemas, migrations, database queries, ORM access, stored procedures, or transaction behavior are in scope. The generic core remains responsible for scope, severity, evidence, and reporting.

## Query safety and authorization

- Prefer parameter binding and safe query APIs. Allowlist dynamic identifiers that cannot be bound.
- Check least privilege, object/row/tenant scope, stored-procedure execution rights, and authoritative authorization.
- Avoid accidental exposure through broad column selection, especially sensitive fields.
- Check joins, predicates, cardinality, null semantics, and duplicate rows rather than masking symptoms with `DISTINCT`.

## Schema and integrity

- Check primary, unique, foreign-key, check, and not-null constraints against the real invariant.
- Review types, precision, time zones, defaults, normalization trade-offs, and invalid/orphaned data.
- Check index usefulness, redundancy, write cost, and engine/version compatibility.

## Query performance

- Require an execution plan, measurement, or repository-supported evidence before claiming a query is slow or fast.
- Look for N+1 calls, unbounded fetches, missing pagination, non-sargable predicates, Cartesian joins, poor selectivity, and over-indexing.
- Use representative data volumes and concurrency where the workload makes them material.

## Transactions and concurrency

- Identify the transaction boundary and explicit commit/rollback behavior.
- Check isolation, lock acquisition order, deadlock handling, timeout behavior, autocommit assumptions, partial success, idempotency, and conflict detection.
- Keep transactions short enough for the workload and observable enough to recover from failure.

## Migrations and rollout

- Prefer expand/contract sequencing when old and new application versions overlap.
- Check table rewrites, lock duration, online or concurrent index/constraint creation, backfill batching, resumability, restart points, observability, and rollback limits.
- Test representative old data and interrupted/repeated migration runs when the repository supports it.

## Engine adapters

PostgreSQL-specific features such as JSONB/array operators, GIN/GiST indexes, RLS syntax, extensions, and PL/pgSQL belong in a PostgreSQL-specific reference. Confirm the engine and supported version before applying vendor guidance.
