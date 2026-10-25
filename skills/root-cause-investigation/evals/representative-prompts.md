# Representative evals

1. A unit test fails after a recent refactor. Expect reproduction, diff inspection, one hypothesis, and a regression check before a fix.
2. An API-to-worker-to-database failure is intermittent. Expect redacted boundary evidence and explicit uncertainty rather than a guessed retry.
3. The user asks for a quick patch after two failed attempts. Expect an architecture/environment review and no third blind fix.
