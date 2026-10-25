# Next-Generation Development Skills Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development` (recommended) or `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the catalog with a cohesive set of original, enhanced development skills inspired by useful workflows in `obra/superpowers`, without preserving the source project’s names, wording, mandatory gates, or runtime assumptions.

**Architecture:** Add independently installable packages below `skills/`, each with a distinctive name, portable `SKILL.md`, package-local references, and representative evals. The skills share a common evidence-first philosophy but remain usable independently. Cross-skill relationships are expressed as optional hand-offs and compatibility notes, not imports from other packages or hidden dependencies.

**Tech Stack:** Markdown skill packages, YAML frontmatter, package-local references/evals, portable shell validation, `npx skills` discovery, and repository documentation.

## Global Constraints

- Preserve Apache-2.0 metadata and repository licensing; do not copy Superpowers text wholesale.
- Use original names, descriptions, examples, and workflow language.
- Treat Superpowers as research input, not as the source of truth.
- Every package must work independently through `skills.sh`.
- Every package must include at least one representative eval and explicit non-goals.
- Skills must follow this app’s autonomy rules: clarify only when ambiguity changes the result, and do not impose unnecessary approval gates on clear bounded work.
- Review-only workflows remain read-only unless the user explicitly requests fixing.
- Subagent guidance must respect the app’s existing task, todo, orchestration, and agent-swarm rules.
- Do not add dependencies or a build system just to validate Markdown packages.
- Run `./scripts/validate-skills.sh` and `npx skills add ./ --list` after catalog changes.

## Proposed Catalog

| Package | Purpose | Main enhancement over the source workflow |
| --- | --- | --- |
| `root-cause-investigation` | Debug bugs, failures, and surprising behavior | Adds evidence checkpoints, boundary tracing, confidence tracking, and an explicit stop condition for architectural problems |
| `proof-before-done` | Verify work before claiming completion | Separates claims, evidence, environmental gaps, and user-visible verification |
| `behavior-first-engineering` | Use tests to drive feature and bug-fix implementation | Adapts test-first practice to legacy and testless repositories instead of enforcing a blind universal ritual |
| `intent-to-implementation` | Clarify ambiguous work and choose a design | Uses lightweight discovery proportional to risk, with alternatives, assumptions, anti-goals, and a concise decision record |
| `review-feedback-triage` | Evaluate and implement code-review feedback | Adds evidence classification, dependency ordering, disagreement handling, and regression verification |
| `coordinated-agent-delivery` | Break work across agents safely | Adds task ownership, dependency boundaries, shared-board discipline, result verification, and bounded recovery |
| `branch-closeout` | Finish implementation safely | Adds repository-specific checks, diff hygiene, authorization-aware next-step choices, and handoff output |

## File Map

Each package will contain:

```text
skills/<package-name>/
  SKILL.md
  README.md
  references/
    workflow-checklist.md
    failure-modes.md
  evals/
    representative-prompts.md
```

Not every package needs both references; the implementer should keep the smallest package that still makes the main skill readable and testable. Existing repository conventions for package-local files take precedence.

---

### Task 1: Establish naming, attribution, and catalog conventions

**Files:**
- Create: `docs/architecture/skill-lineage-and-naming.md`
- Modify: `docs/authoring/skill-package.md`
- Modify: `README.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Produces the naming and adaptation policy used by every new skill package.

- [ ] **Step 1: Define the naming policy**

Document that names must describe the behavior we want users to invoke, not mirror names from the researched repository. Record the proposed names exactly as listed above and state that published names become stable interfaces.

- [ ] **Step 2: Define the adaptation policy**

Document that each skill must add app-native behavior, explicit scope boundaries, evidence requirements, and failure handling. Require a short “informed by, not copied from” note in the package README when outside work materially influenced the design.

- [ ] **Step 3: Define the eval requirement**

Require every new package to include one positive trigger, one non-trigger or boundary case, and one difficult scenario where the enhancement matters.

- [ ] **Step 4: Review documentation references**

Read all changed Markdown files and verify that the catalog describes original packages rather than forks or aliases of Superpowers skills.

### Task 2: Add `root-cause-investigation`

**Files:**
- Create: `skills/root-cause-investigation/SKILL.md`
- Create: `skills/root-cause-investigation/README.md`
- Create: `skills/root-cause-investigation/references/workflow-checklist.md`
- Create: `skills/root-cause-investigation/references/failure-modes.md`
- Create: `skills/root-cause-investigation/evals/representative-prompts.md`

**Interfaces:**
- Trigger: bug, regression, failing test, build failure, integration failure, performance anomaly, or unexpected behavior.
- Produces: a reproducible problem statement, evidence chain, tested hypothesis, minimal fix path, and verification report.

- [ ] **Step 1: Write the failing-behavior evals first**

Include prompts for a reproducible test failure, an intermittent multi-layer failure, and a “quick fix” request where the root cause is not yet established. Define expected behavior: investigate before proposing a fix and label uncertainty.

- [ ] **Step 2: Write the package contract**

Require four stages: establish symptoms, locate the failing boundary, test one hypothesis, and implement/verify the root fix. Add a confidence ledger and a rule that three failed fixes trigger an architecture review rather than a fourth guess.

- [ ] **Step 3: Add focused references**

Cover boundary instrumentation, backward tracing, condition-based waiting, and distinguishing code defects from environment failures.

- [ ] **Step 4: Validate the package**

Run the repository validator and inspect all relative links.

### Task 3: Add `proof-before-done`

**Files:**
- Create: `skills/proof-before-done/SKILL.md`
- Create: `skills/proof-before-done/README.md`
- Create: `skills/proof-before-done/references/evidence-matrix.md`
- Create: `skills/proof-before-done/evals/representative-prompts.md`

**Interfaces:**
- Trigger: before claiming a task is fixed, complete, tested, ready, safe, or mergeable.
- Produces: claim-to-evidence mapping, actual command results, coverage limitations, and remaining risks.

- [ ] **Step 1: Define claim categories**

Cover behavior, regression safety, build/type correctness, user-visible operation, repository compliance, and release readiness. Require the skill to verify only claims relevant to the task.

- [ ] **Step 2: Add gap handling**

Distinguish passed, failed, skipped, unavailable, not applicable, and not verified. Explicitly prohibit treating an unrun check as passing.

- [ ] **Step 3: Add user-path verification**

Require a quick end-to-end action when one is available, not only unit-test output.

- [ ] **Step 4: Add evals for misleading success signals**

Include empty tool output, a passing narrow test with a failing full suite, and a successful build with an unverified user flow.

### Task 4: Add `behavior-first-engineering`

**Files:**
- Create: `skills/behavior-first-engineering/SKILL.md`
- Create: `skills/behavior-first-engineering/README.md`
- Create: `skills/behavior-first-engineering/references/test-design.md`
- Create: `skills/behavior-first-engineering/references/legacy-and-testless-code.md`
- Create: `skills/behavior-first-engineering/evals/representative-prompts.md`

**Interfaces:**
- Trigger: new behavior, bug fix, refactor, or behavior-preserving change where verification can be automated.
- Produces: a behavior-focused test or justified verification substitute, minimal implementation, and regression evidence.

- [ ] **Step 1: Define the normal red/green/refactor loop**

Require a test or executable check that would fail before the change whenever practical, followed by minimal implementation and full relevant-suite verification.

- [ ] **Step 2: Add repository-aware exceptions**

Handle legacy code, missing test infrastructure, generated code, configuration, migrations, UI-only changes, and exploratory spikes. Exceptions must be explicit and must name the replacement evidence.

- [ ] **Step 3: Add test-quality rules**

Prefer real behavior over mock behavior, one contract per test, meaningful failure messages, and edge cases tied to the reported risk.

- [ ] **Step 4: Add evals**

Cover a normal feature, a bug fix in a testless repository, and a request where a test would be inappropriate.

### Task 5: Add `intent-to-implementation`

**Files:**
- Create: `skills/intent-to-implementation/SKILL.md`
- Create: `skills/intent-to-implementation/README.md`
- Create: `skills/intent-to-implementation/references/decision-record.md`
- Create: `skills/intent-to-implementation/evals/representative-prompts.md`

**Interfaces:**
- Trigger: ambiguous feature requests, substantial behavior changes, new components, or work with meaningful product/architecture trade-offs.
- Produces: clarified outcome, goals/non-goals, alternatives, assumptions, selected approach, and implementation-ready design summary.

- [ ] **Step 1: Define proportional discovery**

Use a lightweight path for small changes and a fuller design path for high-risk work. Do not force a design ceremony when the request is already concrete and bounded.

- [ ] **Step 2: Require repository reconnaissance**

Inspect relevant code, conventions, tests, and constraints before asking questions already answered by the repository.

- [ ] **Step 3: Add alternatives and anti-goals**

Require two or three credible approaches when trade-offs exist, identify the recommendation, and record what the implementation must not do.

- [ ] **Step 4: Add evals**

Cover an underspecified feature, an already-specified small change, and a request whose safest response is a bounded spike.

### Task 6: Add `review-feedback-triage`

**Files:**
- Create: `skills/review-feedback-triage/SKILL.md`
- Create: `skills/review-feedback-triage/README.md`
- Create: `skills/review-feedback-triage/references/feedback-classification.md`
- Create: `skills/review-feedback-triage/evals/representative-prompts.md`

**Interfaces:**
- Trigger: code-review comments, PR feedback, audit findings, or requested review changes.
- Produces: classified feedback, verified action list, reasoned pushback where necessary, and per-item regression evidence.

- [ ] **Step 1: Define feedback classes**

Classify items as confirmed defect, valid improvement, clarification needed, context-dependent recommendation, unsupported claim, or out of scope.

- [ ] **Step 2: Define ordering and dependency rules**

Resolve unclear items before partial implementation; prioritize correctness, security, and compatibility; test each change independently.

- [ ] **Step 3: Add YAGNI and disagreement handling**

Require checking actual usage and repository constraints before accepting “professionalize this” requests. Allow technical pushback supported by code or tests.

- [ ] **Step 4: Add evals**

Cover correct feedback, incorrect feedback, unclear multi-item feedback, and feedback that conflicts with compatibility requirements.

### Task 7: Add `coordinated-agent-delivery`

**Files:**
- Create: `skills/coordinated-agent-delivery/SKILL.md`
- Create: `skills/coordinated-agent-delivery/README.md`
- Create: `skills/coordinated-agent-delivery/references/task-boundaries.md`
- Create: `skills/coordinated-agent-delivery/references/review-gates.md`
- Create: `skills/coordinated-agent-delivery/evals/representative-prompts.md`

**Interfaces:**
- Trigger: work with genuinely independent tasks that benefit from multiple agents.
- Produces: decomposed task board, ownership/dependency map, bounded dispatches, verified results, and integrated handoff.

- [ ] **Step 1: Define when not to delegate**

Keep single-agent work for small, coupled, exploratory, or context-heavy tasks. Use parallelism only when the work can be independently reviewed and merged.

- [ ] **Step 2: Define task contracts**

Each task must include scope, files, inputs, outputs, checks, and stop conditions. Shared files and integration points must have one owner.

- [ ] **Step 3: Define review gates**

Require result verification, conflict detection, and a final integration review. Add bounded recovery for failed or incomplete agents.

- [ ] **Step 4: Integrate app-native tooling**

Reference the app’s todo, task, orchestration, and agent-swarm facilities without assuming a particular external framework.

### Task 8: Add `branch-closeout`

**Files:**
- Create: `skills/branch-closeout/SKILL.md`
- Create: `skills/branch-closeout/README.md`
- Create: `skills/branch-closeout/references/closeout-checklist.md`
- Create: `skills/branch-closeout/evals/representative-prompts.md`

**Interfaces:**
- Trigger: implementation is complete or the user asks whether a branch/worktree is ready to close.
- Produces: final verification summary, clean diff assessment, documented open work, and authorization-aware next-step options.

- [ ] **Step 1: Define closeout checks**

Inspect status, diff, relevant tests/builds, documentation, generated files, secrets, and repository-specific completion rules.

- [ ] **Step 2: Separate reporting from side effects**

Describe merge, PR, push, cleanup, or discard options without taking those actions unless explicitly authorized.

- [ ] **Step 3: Add handoff output**

Include changed files, checks actually run, known gaps, assumptions, and the next concrete action.

- [ ] **Step 4: Add evals**

Cover a clean branch, a branch with unrelated changes, a failed check, and a branch where cleanup would be destructive.

### Task 9: Catalog integration and cross-skill verification

**Files:**
- Modify: `README.md`
- Modify: `skills/README.md`
- Modify: `docs/architecture/repository-layout.md`
- Modify: `docs/authoring/skill-package.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Produces the discoverable catalog and documents the optional workflow relationships among the new packages.

- [ ] **Step 1: Add the new packages to the catalog**

Describe each package by its original name and behavior. Do not present any package as an official Superpowers port.

- [ ] **Step 2: Document optional sequencing**

Show an example flow such as `intent-to-implementation` → `behavior-first-engineering` → `proof-before-done`, with `root-cause-investigation` and `review-feedback-triage` applied when signaled by the task.

- [ ] **Step 3: Run repository validation**

Run:

```sh
./scripts/validate-skills.sh
npx skills add ./ --list
```

Expected: all packages pass validation and are discoverable with stable names.

- [ ] **Step 4: Perform a package-isolation audit**

Check every new `SKILL.md` for unresolved links, references to private paths, references to unavailable tools, copied source names, and hidden dependencies on another package.

- [ ] **Step 5: Review the complete diff**

Run `git diff --check` and inspect the full diff for accidental source text reuse, missing license metadata, generated state, unrelated edits, or inconsistent names.

## Self-Review Checklist

- [ ] Every proposed skill has an original name and a clear trigger.
- [ ] Every package adds behavior beyond the researched source workflow.
- [ ] Every package has a positive, boundary, and difficult eval scenario.
- [ ] Legacy/testless repositories and environmental failures are handled explicitly.
- [ ] No package requires another package to be installed.
- [ ] No workflow silently performs external side effects.
- [ ] README and catalog documentation describe the new names consistently.
- [ ] Validation and discovery commands are run before declaring the catalog ready.
