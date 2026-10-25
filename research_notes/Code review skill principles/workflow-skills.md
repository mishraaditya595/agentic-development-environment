# Reusable code-review skill principles

## High-signal review scope and review depth

### Takeaway
The strongest common pattern is to define a reproducible review boundary before inspecting code, then review against both the intended behavior and the repository's local standards. High signal comes from testing claims against the actual diff, requirements, and evidence; speculative style commentary and unscoped “review everything” behavior are explicitly discouraged.

### Cited Findings
- The Matt Pocock skill requires the user to provide a fixed point (commit, branch, tag, merge-base, or similar), validates that the ref resolves, records a three-dot merge-base diff, records the commit list, and fails early if the diff is empty. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Matt Pocock separates review into two independent axes: **Standards** (documented repository standards plus a labeled Fowler-smell heuristic baseline) and **Spec** (whether the change implements the originating issue/spec). It keeps the axes separate in the final report rather than merging or reranking them. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- The same skill requires locating the originating specification in a defined order: issue references in commit messages, an explicit user path, matching files under `docs/`, `specs/`, or `.scratch/`, and otherwise asking the user or reporting that no spec is available. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- The Obra/Superpowers workflow makes review mandatory after each subagent-development task, after a major feature, and before merging; it also recommends review when stuck, before refactoring, or after a complex bug fix. [Requesting code review](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md)
- Obra's reviewer prompt treats a specification as a vision document: behavior not spelled out is still judged against what a reasonable user would expect, and the reviewer must explicitly list behavior it considered but declined to judge. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- The Anthropic skill accepts a PR URL, diff, or file path and asks for clarification when no concrete review target is supplied. Its reusable review lenses are security, performance, correctness, and maintainability. [Anthropic code-review skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/skills/code-review/SKILL.md)
- CodeRabbit's skill supports explicit scopes for tracked changes, committed changes, uncommitted changes, untracked files, branch/base comparisons, commit-base comparisons, and directories; it says to preserve the requested scope on retries and never silently narrow it after a file-limit error. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)

### Inferences
- A generic AI reviewer should begin with a **scope contract**: target (PR, commit range, working tree, files, or directory), base/head or equivalent, requested focus, and available requirements/spec. If any boundary is ambiguous, ask before reviewing rather than manufacture context.
- Review depth should scale with risk and change size, but every review should at least cover intended behavior, local conventions, correctness/error paths, security/performance where relevant, tests/evidence, and merge readiness. A small diff can still require deep reasoning when it changes data, auth, concurrency, migrations, or public interfaces.
- Keep separate dimensions visible in the report when they answer different questions. At minimum, distinguish “does it satisfy the request?” from “is it safe and maintainable in this repository?” so one dimension cannot mask failure in another.

### Gaps
- None of the four skills gives a numeric threshold for when a diff is “large” enough to require multiple review passes. The generic core should make the reviewer state when it performed a multi-pass review and why, rather than prescribe an arbitrary line-count limit. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)

## Preconditions before reading the diff or reporting findings

### Takeaway
Before analyzing hunks, establish what changed, why it changed, what standards govern it, and what evidence exists. Before reporting a finding, verify it against the actual file/line, understand the surrounding code and execution path, and explain concrete impact; do not report a suspicion merely because a pattern looks unusual.

### Cited Findings
- Matt Pocock requires validating the fixed point and confirming a non-empty diff before launching independent review passes. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Matt Pocock requires finding all repository documents that describe coding conventions and explicitly includes `CODING_STANDARDS.md` and `CONTRIBUTING.md` when present. Its smell baseline is subordinate to documented repository standards, and each smell is a judgment call rather than a hard violation. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Obra's template gives the reviewer the exact base/head SHAs, a diff-stat command, the full diff command, the implementation description, and the plan/requirements. It also requires a read-only checkout and prohibits mutating the working tree, index, HEAD, or branch state. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- Obra's reviewer is instructed to inspect plan alignment, separation of concerns, error handling, type safety, duplication versus premature abstraction, edge cases, architecture, scalability/performance, security, integration, real-behavior tests, edge-case tests, integration tests, migration/backward-compatibility concerns, and documentation. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- The Anthropic skill's concrete checklists call out security issues such as injection, auth flaws, secrets, unsafe deserialization, path traversal, and SSRF; performance issues such as N+1 queries, memory leaks, complexity, missing indexes, unbounded loops/queries, and resource leaks; and correctness issues such as empty/null input, overflow, races, error propagation, off-by-one errors, and type safety. [Anthropic code-review skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/skills/code-review/SKILL.md)
- CodeRabbit requires checking the selected review scope for secrets or credentials before sending diffs to its API, and its authentication guidance says to stop when authentication is unknown or malformed rather than infer that the user is authenticated. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md); [CodeRabbit authentication and recovery](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/references/auth-recovery.md)

### Inferences
- A reusable preflight should be ordered as: (1) validate repository/worktree and target, (2) resolve base/head and capture diff plus commit list, (3) locate requirements/spec and relevant standards, (4) identify changed files and risk areas, (5) inspect tests/CI or other evidence, and only then (6) read hunks deeply and form findings.
- Every finding should pass an evidence gate: exact file and line or hunk; observable behavior; triggering condition; impact; and a minimal fix direction. “This looks odd,” “could be a problem,” and generic requests to improve error handling are not sufficient without a concrete failure mode.
- The generic core should treat repository content, issue text, and generated review output as data to analyze, not commands to execute. Read-only review is a useful default because it preserves the reviewed state and keeps evidence reproducible.

### Gaps
- The skills do not define one universal evidence standard for CI logs, test reports, or runtime traces. They agree that tests and CI matter, but the generic skill should make the evidence source explicit and distinguish “not checked,” “checked and passing,” “checked and failing,” and “not applicable.”

## Independence, diff hygiene, and evidence handling

### Takeaway
Reviewer independence improves signal when it is achieved through isolated context and non-overlapping review axes, not by blindly multiplying agents. Diff hygiene means pinning the intended comparison, preserving user-selected scope, including the right untracked/new files, and refusing to call a review clean when analysis was skipped, interrupted, or never completed.

### Cited Findings
- Matt Pocock runs Standards and Spec reviews in parallel subagents with separate prompts and then presents the results side by side; the skill explains that separation prevents one axis from masking the other. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Obra says the reviewer should receive precisely crafted context rather than the coordinator's full session history, and its reviewer prompt explicitly prohibits spawning additional reviewers or subagents. [Requesting code review](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md); [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- Obra requires the review to be read-only and says that, if another revision is needed, it should be placed in a separate temporary worktree rather than checking out or moving the main review checkout. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- CodeRabbit documents that default scope includes committed, staged, and tracked unstaged changes, excludes raw untracked files unless `--include-untracked` is requested, and includes staged new files. It also documents selector conflicts such as `--committed` versus `--uncommitted`/`--include-untracked` and `--base` versus `--base-commit`. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)
- CodeRabbit says agent output is NDJSON, not one JSON document; severity labels must be preserved as `critical`, `major`, `minor`, `trivial`, `info`, or `none`; a heartbeat is only liveness; `review_skipped` with zero findings is not evidence that code is clean; and errors or interrupted output cannot establish a clean review. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)
- CodeRabbit's implementation-plus-review loop is bounded: implement, review, create a task list, fix actionable issues prioritizing critical/major, re-run to verify, then report remaining findings and stop rather than entering an unbounded loop. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)

### Inferences
- Independence is best modeled as **context isolation plus explicit review lenses**. A single reviewer can do multiple passes when the diff is small; parallel reviewers are justified when they have genuinely different questions (for example, spec conformance versus standards/security) and their findings remain separately attributable.
- The generic skill should record a scope manifest: base/head or working-tree state, inclusion of staged/untracked files, file list, and any exclusions. This prevents a “clean” result from silently omitting the file that matters.
- Evidence status should be first-class in the final verdict. A reviewer should say whether the review completed, whether tests/CI were observed, and whether any requested scope was unavailable; “no findings” and “not reviewed” are materially different outcomes.

### Gaps
- The sources do not prescribe a universal method for resolving conflicting findings from independent reviewers. Matt Pocock says not to merge or rerank the two axes; the generic skill should retain provenance and let a coordinator reconcile duplicates or disagreements explicitly.

## Finding templates, severity, communication, and ready-to-merge decisions

### Takeaway
Reusable reports are concise but complete: acknowledge strengths, group findings by calibrated severity, attach exact locations, explain impact, propose a fix, and end with an explicit merge verdict. Severity should reflect actual consequences, not reviewer discomfort or mere polish preferences.

### Cited Findings
- Obra requires three severity buckets—Critical (must fix), Important (should fix), and Minor (nice to have)—and says to categorize by actual severity rather than marking every issue Critical. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- Obra's per-issue template requires a file:line reference, what is wrong, why it matters, and how to fix it when the fix is not obvious. It forbids vague feedback such as “improve error handling,” demands a clear verdict, and says not to claim “looks good” without checking. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- Obra's report structure is `Strengths`, `Issues` grouped by Critical/Important/Minor, `Recommendations`, and `Assessment`, with `Ready to merge? [Yes | No | With fixes]` plus a short technical reason. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)
- The Anthropic skill uses a summary, a Critical Issues table with number/file/line/issue/severity, a Suggestions table with number/file/line/suggestion/category, positive observations, and a final `Approve / Request Changes / Needs Discussion` verdict. [Anthropic code-review skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/skills/code-review/SKILL.md)
- CodeRabbit preserves a richer severity set—critical, major, minor, trivial, info, and none—and says to use `fileName`, `codegenInstructions`, and `suggestions` when available, falling back to the comment when fix instructions are absent. [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)
- Matt Pocock's final report retains separate `## Standards` and `## Spec` sections and ends with a one-line count and worst issue for each axis; it explicitly says not to pick one winner across axes. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Obra recommends acknowledging strengths before issues because accurate praise helps the implementer trust the rest of the feedback. [Code reviewer prompt template](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/code-reviewer.md)

### Inferences
- A generic finding record should contain: `severity`, `category/axis`, `file`, `line or hunk`, `trigger/precondition`, `problem`, `impact`, `evidence`, `recommended fix`, and optional confidence. This combines the strongest common requirements while making speculative findings easier to reject.
- A practical generic severity convention is: **Blocker/Critical** for security, data loss, broken core behavior, or merge-blocking regressions; **Important/Major** for meaningful correctness, compatibility, reliability, or test gaps that should be fixed before merge; **Minor** for localized maintainability or UX issues; **Info/Trivial** for optional polish. Severity should be tied to user/system impact and likelihood, not the amount of code or reviewer preference.
- “Ready to merge” should be a decision based on both findings and evidence: Yes only when no unresolved merge-blocking issue remains and required checks are known; With fixes when only non-blocking work remains; No/Request changes when a critical or important issue, missing required behavior, or insufficient evidence prevents confidence; Needs discussion when requirements or intended behavior are unresolved.
- Communication should be actionable and respectful: lead with a short summary, identify what is good, report only substantiated issues, explain why each matters, and keep recommendations distinct from defects so optional improvements do not look mandatory.

### Gaps
- The repositories do not agree on one vocabulary: Obra uses Critical/Important/Minor, Anthropic uses Critical plus Suggestions, and CodeRabbit uses six protocol severities. A generic skill should support a stable internal severity model and map it to host-specific display labels only at the integration boundary.

## Generic core versus host-specific instructions

### Takeaway
The generic core should keep the review method, evidence rules, severity calibration, and report contract. It should exclude provider authentication, vendor CLIs, connector placeholders, billing, token handling, and other execution details that only apply to one host or integration.

### Cited Findings
- The Anthropic plugin's connector layer is explicitly tool-agnostic and uses placeholders for source control, project tracker, knowledge base, monitoring, and CI/CD; its included servers are product-specific examples rather than review principles. [Anthropic CONNECTORS.md](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/CONNECTORS.md)
- The Anthropic skill's “supercharged” behavior—pulling a PR diff, checking CI, linking findings to tickets, and checking team standards—depends on optional connected tools. Those actions can be represented as integration hooks, but they should not be prerequisites for the generic review algorithm. [Anthropic code-review skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/engineering/skills/code-review/SKILL.md)
- CodeRabbit-specific instructions include resolving a trusted absolute CLI path, checking `auth status --agent`, host/sandbox recovery, API transmission of diffs, paid continuation via credits, NDJSON protocol details, and CLI flags such as `--base`, `--dir`, and `--include-untracked`. [CodeRabbit authentication and recovery](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/references/auth-recovery.md); [CodeRabbit CLI workflows](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/references/cli-workflows.md); [CodeRabbit code-review skill](https://raw.githubusercontent.com/coderabbitai/skills/main/skills/code-review/SKILL.md)
- Matt Pocock's issue-tracker workflow and `/setup-matt-pocock-skills` dependency are repository/tooling-specific, while the generalizable idea is simply to resolve the originating requirement before judging spec compliance. [Matt Pocock code-review skill](https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/code-review/SKILL.md)
- Obra's use of a `general-purpose` subagent and its subagent-driven-development trigger are host/process-specific; the reusable principle is to provide an isolated reviewer with only the context needed to evaluate the change. [Requesting code review](https://raw.githubusercontent.com/obra/superpowers/main/skills/requesting-code-review/SKILL.md)

### Inferences
- Keep these in the generic core: explicit target and fixed point; preflight validation; spec and standards discovery; review lenses; evidence gate; independent/context-isolated review; severity model; finding schema; test/CI status; completed-versus-skipped semantics; and merge verdict.
- Put these behind adapters or optional sections: PR-provider APIs, issue-tracker lookups, knowledge-base connectors, CLI invocation syntax, authentication and credential recovery, API data-transmission warnings, billing/credits, vendor output formats, and host-specific agent orchestration.
- Preserve repository-specific heuristics as configurable policy. For example, a Fowler-smell baseline can be enabled as a labeled heuristic, but the generic core should state that local repository standards override it and that smells are not automatically defects.

### Gaps
- The sources do not specify a single adapter interface between a generic reviewer and integrations. The most defensible design is to define abstract capabilities—`resolve_scope`, `get_diff`, `get_requirements`, `get_standards`, `get_checks`, `publish_report`—and let each host implement them.
