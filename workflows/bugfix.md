# Bugfix workflow

**Trigger:** Unexpected behavior requiring diagnosis and correction.
**Capabilities:** root-cause-investigation → plan-implementer (when a fix is authorized) → test-engineer → evidence-based-code-review → branch-closeout.

1. Reproduce the problem or establish a measurable proxy. Capture expected versus actual behavior and the relevant environment.
2. Trace from the observed failure to the causal code path; separate confirmed evidence from competing hypotheses.
3. Add a regression test at the narrowest meaningful layer. Prefer a test that fails before the fix.
4. Implement the smallest fix that addresses the root cause without suppressing symptoms or destroying user data.
5. Run regression and nearby checks. Document any environmental barriers to executing tests.
6. Review the actual diff, including compatibility, error paths, retries and documentation changes.
7. Handoff with root cause, fix, evidence and unresolved risks. Prepare a PR only when authorized.

**Recovery:** If the failure cannot be reproduced, do not invent a cause; record diagnostic evidence needed. If the proposed fix changes architecture or schema, invoke feature-delivery style planning and safety checks.
**Safety:** Never test against production data destructively; never auto-merge.
