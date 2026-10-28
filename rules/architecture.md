# Architecture and compatibility

- Observe existing module boundaries, dependency direction, public interfaces and stored data formats before redesign.
- Prefer extending established patterns to creating parallel infrastructures.
- For schema or protocol changes, examine old/new client compatibility, backfill safety, idempotency, rollback and partial upgrades.
- Define ownership and interface contracts before parallelizing agent work.
- Treat migration ordering, transactionality, retries and user-data preservation as correctness issues, not mere style.
- Record trade-offs only to the level needed for the change's risk; avoid design documents for trivial edits.
