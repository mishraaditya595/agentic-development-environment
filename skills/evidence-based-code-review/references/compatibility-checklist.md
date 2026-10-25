# Compatibility and migration checklist

Apply this when the change affects data, schemas, APIs, serialized formats, configuration, queues, caches, plugins, clients, or deployment order.

## Existing data

- Can data written by the previous version still be read?
- Can the new version read old records, optional fields, unknown enum values, older timestamps, and partially written data?
- Are identifiers, ordering, precision, encoding, and time-zone assumptions preserved?

## Migrations

- Is the schema or format version updated through the repository’s normal mechanism?
- Is the upgrade step tested on representative old data?
- Are migrations idempotent, resumable, observable, and safe under interruption?
- Are indexes, constraints, defaults, backfills, and rollback limitations understood?
- For relational or other large persisted stores, check lock duration, table rewrites, online/concurrent index or constraint creation, long-running backfills, dual-read/dual-write sequencing, and a safe restart point after interruption.

## APIs and clients

- Does the server remain compatible with old clients during rollout?
- Does the client tolerate older servers and partial feature rollout?
- Are optional fields safer than changing meaning of existing fields?
- Are status codes, error shapes, pagination, sorting, retries, rate limits, and authentication behavior preserved?
- Are generated clients or schemas regenerated and ready, deprecated operations removed safely, and exact nullability, enum, and DTO/type behavior compatible?

## Queues, caches, and deployment

- Can queued jobs and events produced before the change still be processed?
- Are cache keys, TTLs, invalidation, and serialization compatible?
- Does deployment need a specific order across services, workers, migrations, or clients?
- Is rollback possible after the new schema or format has been written?
- Are feature flags, defaults, environment variables, and disabled-state behavior safe during partial rollout?

## Database-specific evidence when applicable

When SQL or database behavior changes, use engine-appropriate evidence rather than generic assumptions:

- query plans or measurements for performance claims;
- representative data volumes for cardinality, pagination, and index claims;
- explicit transaction boundaries, isolation, commit/rollback, lock ordering, timeout, and deadlock behavior;
- primary/unique/foreign/check/not-null constraints, precision, time-zone semantics, defaults, and orphan/invalid-value checks;
- parameter binding, dynamic identifier allowlists, least privilege, row/object/tenant scope, and sensitive-column selection;
- expand/contract rollout, resumable backfills, and old/new application compatibility.

Keep engine-specific mechanisms such as PostgreSQL operators, index classes, row-level-security syntax, or ORM APIs in separate adapters. Do not treat a vendor feature as automatically better than a simpler repository-compatible design.

If compatibility cannot be proven from the repository, identify the missing contract, fixture, migration test, or deployment evidence.
