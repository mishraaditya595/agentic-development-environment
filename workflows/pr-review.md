# Pull-request review workflow

**Trigger:** A request to inspect an existing PR, branch, commit range or uncommitted diff.
**Default:** strictly read-only.
**Primary skill:** evidence-based-code-review (canonical name; do not invent a second code-reviewer skill).

1. Establish exact base/head and scope; read the request, acceptance criteria and repository instructions.
2. Inspect relevant changed lines with callers, consumers, tests and migration/configuration impact.
3. Run safe applicable checks only where available and permitted; distinguish missing tools from defects.
4. Identify actionable findings with file/line evidence, severity and concrete effects. Distinguish verified defects, risks and questions.
5. Assess spec completeness separately from code quality and security.
6. Use templates/review-report.md where available, with verdict and verification gaps.

**Review modes:** A plain "review" request never edits code or posts remote comments. Review remediation is a separate authorized request. A PR is not declared ready when blockers or unverified critical areas remain. Never merge as part of a review.
