# PostgreSQL review adapter

Use only after confirming that the repository targets PostgreSQL and the changed behavior depends on PostgreSQL-specific features. Start with `database-review.md`; these are additional engine-specific questions, not universal rules.

## Query and index behavior

- For JSONB or array containment and search patterns, check the operator semantics, suitable GIN/GiST or other index strategy, selectivity, and representative query plans.
- Check expression indexes, partial indexes, partition keys, CTEs, window functions, and function-wrapped predicates against the actual workload and supported PostgreSQL version.
- Avoid treating a PostgreSQL feature as automatically better than a simpler design that matches repository portability and operational needs.

## Types and constraints

- Review `TIMESTAMPTZ` versus timestamp semantics, numeric precision, enums/domains, `CITEXT`, JSONB structure constraints, defaults, generated values, and identifier behavior.
- Check primary, unique, foreign-key, check, and not-null constraints against the business invariant.

## Security and execution

- Check row-level security policies, session settings, role grants, function `SECURITY DEFINER`/invoker behavior, search-path assumptions, and extension privileges.
- Verify that application authorization is not accidentally replaced by a permissive database policy or a client-only check.

## Migrations and operations

- Check lock duration, table rewrites, concurrent index creation, partition changes, trigger behavior, backfill batching, and rollback limitations.
- For PL/pgSQL functions and triggers, inspect firing conditions, recursion, error handling, transaction behavior, and observability.
