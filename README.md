# Agentic Development Environment (ADE)

**Portable, evidence-driven development skills for AI coding agents.** Build features, investigate bugs, review changes and prepare pull requests consistently—while keeping final merge and production deployment under human control.

ADE provides independently installable [Agent Skills](https://agentskills.io) and optional project-local workflows, rules and output templates. It aims to work across Codex, Claude Code and OpenCode without a proprietary AI router. Native skill selection based on descriptions is **model-dependent**, not guaranteed.

## Get started: install one skill

From your existing project:

    npx skills add mishraaditya595/agentic-development-environment --skill evidence-based-code-review

Or install an implementation skill:

    npx skills add mishraaditya595/agentic-development-environment --skill plan-implementer

Every package is self-contained. It does not require installing ADE as a whole. Other publicly indexed skills can be found on [skills.sh](https://skills.sh/); listing is not guaranteed merely by publishing a repository.

## Get started: install full ADE guidance

The project-local installer is **implemented in Python 3.9+** for POSIX filesystem runtimes (Linux/macOS); a proposed npx agentic-dev CLI is **not published or available**.

In an ADE checkout:

    python3 scripts/bootstrap.py --target /path/to/your-project --agents codex,claude,opencode --preset standard --dry-run
    python3 scripts/bootstrap.py --target /path/to/your-project --agents codex,claude,opencode --preset standard

This installs selected skills, workflow/rule/template references and agent instructions where absent. No scripts are executed in the target repo; no network is required during installation. Conflicting files are refused during preflight without changing anything. Write failures trigger rollback of newly created files and a nonzero exit. Existing AGENTS.md / CLAUDE.md are preserved, while symlinked instructions are refused. Re-running with additional `--agents` or `--skills` safely expands untouched installations; the config inventory is updated last. See [detailed installation and usage](docs/usage.md).

## What developers actually do

After installation, open the repository in a supported coding agent and ask naturally:

> Review my current branch against main for regressions and missing tests. Do not edit files.

> Plan an additive database migration with acceptance criteria. No code yet.

> Implement the approved plan, run appropriate tests and report any unverified criteria.

> Implement session history end to end, review it and open a PR for me. Do not merge.

Agents can choose skills through native discovery; explicitly name a skill if auto-selection misses it. Full lifecycle requests use the portable feature-delivery skill. The agent reads applicable rules/workflows/templates if they were installed and included in project instructions. **No Markdown document enforces a merge gate by itself**—use branch protection and required CI.

## Skill catalog

| Skill | Purpose |
| --- | --- |
| [evidence-based-code-review](skills/evidence-based-code-review/) | Read-only, evidence-backed diff/PR review |
| [repo-onboarding](skills/repo-onboarding/) | Map unfamiliar repositories and actual toolchain |
| [plan-creator](skills/plan-creator/) | Produce implementation-ready plans |
| [plan-implementer](skills/plan-implementer/) | Execute approved plans and report evidence |
| [merge-conflict-resolver](skills/merge-conflict-resolver/) | Resolve conflicts while preserving both sides |
| [test-engineer](skills/test-engineer/) | Design/write behavioral and regression tests |
| [feature-delivery](skills/feature-delivery/) | Orchestrate scoped plan → implementation → verification → review → PR handoff |
| [root-cause-investigation](skills/root-cause-investigation/) | Investigate failures and underlying causes |
| [proof-before-done](skills/proof-before-done/) | Confirm claims against actual evidence |
| [behavior-first-engineering](skills/behavior-first-engineering/) | Behavior-driven implementation where useful |
| [intent-to-implementation](skills/intent-to-implementation/) | Resolve meaningful design ambiguity proportionally |
| [review-feedback-triage](skills/review-feedback-triage/) | Verify and prioritize reviewer feedback |
| [coordinated-agent-delivery](skills/coordinated-agent-delivery/) | Coordinate bounded independent parallel work |
| [branch-closeout](skills/branch-closeout/) | Safe completion and handoff checks |

The canonical review skill retains its stable published name (evidence-based-code-review); no duplicate code-reviewer package is introduced.

## Repository layers

| Folder | Responsibility |
| --- | --- |
| skills/ | Independent, publishable Agent Skills packages |
| workflows/ | Feature, bugfix, PR-review, remediation, refactoring, release-readiness process guidance |
| rules/ | Engineering, testing, security, git, architecture, documentation and agent autonomy standards |
| templates/ | Implementation plan, review, PR, handoff and project instructions |
| scripts/ | Offline installer and package validation |
| tests/ | Bootstrap tests and manual skill-routing evaluation probes |
| plugins/ | Reserved for documented native runtime adapters |
| docs/ | Usage, architecture and contributor guidance |
| research_notes/ and reports/ | Historical design research; not installable skills |

Portable skills do **not** depend on root-level ADE resources. The shared folders support the optional project-local bundle.

## Validate changes

With Python 3.9+ installed:

    sh scripts/validate-skills.sh
    python3 scripts/validate-ade.py
    python3 -m unittest discover -s tests -v

When Node and network access are available, also confirm CLI discovery:

    npx skills add ./ --list

The GitHub Actions workflow runs static checks and bootstrap tests on PRs. Real Claude, Codex and OpenCode skill activation must be evaluated separately using [routing probes](tests/skill-routing/README.md).

## Documentation

- [How to install and use ADE](docs/usage.md)
- [Installation/discovery architecture](docs/architecture/installation-design.md)
- [Authoring and trigger descriptions](docs/authoring/skill-routing.md)
- [Repository package contract](docs/architecture/repository-layout.md)
- [Skill package validation](docs/authoring/skill-package.md)
- [Concepts evaluated from Test Double Han](docs/architecture/han-principles.md)
- [Runtime plugin contract](docs/architecture/plugin-contract.md)

## Principles and limitations

Keep reviews read-only unless asked to fix. Make tests and findings evidence-based; report blocked verification as blocked. Never infer PR permission implies permission to merge. Respect existing project instructions and avoid overwriting them during installation. The current bootstrap supports local copy/install and conflict refusal, but no automatic upgrade, uninstall, published CLI or deterministic skill router.

## License

Apache-2.0. See [LICENSE](LICENSE).
