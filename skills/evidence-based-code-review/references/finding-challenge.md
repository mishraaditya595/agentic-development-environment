# Independent finding challenge

Before reporting a high-impact defect, challenge your own interpretation using the target repository's actual evidence. This is a filtering pass, not a search for more speculative findings.

For each proposed blocking or high-severity finding:

1. Identify the exact claimed failure, prerequisite state and route by which the changed code can be reached.
2. Check whether surrounding guards, callers, validation, transactions, configuration, tests or prior behavior invalidate the claim.
3. Seek concrete counter-evidence, with file/line or direct execution evidence, rather than accepting an assertion such as "this should work".
4. If a claim is contradicted by direct evidence, remove or correct it and record why internally. If evidence is missing, classify as unverified risk/question, not confirmed defect.
5. Apply the same evidence standard to security claims without dismissing a credible reachable risk merely because reproduction requires restricted access.
6. Verify the final written report has no duplicated or mutually inconsistent recommendations and that its verdict matches its findings and test status.

When no independent reviewer/agent is available, perform a separate self-challenge and label it as such. Do not claim an independent pass occurred when it did not.
