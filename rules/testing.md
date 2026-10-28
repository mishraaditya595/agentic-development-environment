# Testing and evidence rules

- Derive tests from observable acceptance criteria, including error and boundary cases.
- Prefer meaningful assertions over smoke tests that merely execute a path.
- Select unit, integration, contract or UI tests based on the risk and implementation boundary.
- Verify retries, state transitions, persisted state and null/absent values where relevant.
- Run the repository's actual supported commands; do not invent a default test command.
- Report command, scope, pass/fail/blocked result, failures and known coverage limits.
- A missing SDK, unavailable secret or external outage is an environmental blocker, not a passing test or automatically a code defect.
- Do not delete or weaken a failing test to get a green result without a justified behavior change.
