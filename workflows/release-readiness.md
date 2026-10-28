# Release readiness workflow

**Trigger:** Prepare or assess a release candidate; never automatically deploy.
**Inputs:** target release, changed commits, deployment environment and repository release instructions.

1. Establish candidate revision and its intended behavior, dependency graph, and previously shipped compatibility baseline.
2. Check CI results, reproducible builds, test evidence, generated assets, migrations, permissions, security and secret hygiene.
3. Check configuration differences, feature switches, schema/application rollback compatibility, observability, backup and recovery steps.
4. Identify environmental checks not run, credentials unavailable and high-risk manual verifications.
5. Produce go/no-go assessment, known risks, rollback/forward-fix plan and a clearly attributed human approval gate.

**Boundary:** Never interpret "ready" as permission to deploy, merge, publish packages, migrate production data or delete release branches.
