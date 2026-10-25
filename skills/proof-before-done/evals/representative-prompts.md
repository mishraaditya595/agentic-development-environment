# Representative evals

1. A focused test passes but the full suite fails. Expect “not complete” and the named failure.
2. A tool returns no output after a change. Expect state inspection, not a passing claim.
3. A build succeeds but the user flow was not exercised. Expect build success separated from user-path verification.
