# Review remediation workflow

**Trigger:** The developer explicitly asks to fix reviewer findings.
**Capabilities:** review-feedback-triage → plan-implementer → test-engineer → evidence-based-code-review.

1. Retrieve current review comments and the actual changed code, not only the author's paraphrase.
2. Classify each finding: confirmed defect, misunderstanding, risk, or requires decision. Explain disagreements with evidence.
3. Fix confirmed findings in dependency order; keep changes within review scope unless a risk requires an approved plan change.
4. Add regression tests for behavior-changing fixes. Re-run the relevant checks, recording outcomes and any blockers.
5. Verify each finding against the new diff; report fixed/unverified/declined with reasons.
6. Update the same PR only when authorized. Do not mark a thread resolved without checking its concern.

**Exit:** No unaddressed critical/blocking findings; explicit report of remaining issues. Neither author approval nor a passing local check substitutes for independent review.
