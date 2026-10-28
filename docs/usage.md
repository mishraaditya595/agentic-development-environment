# Using ADE in another repository

Choose **individual skills** or the **project-local bundle**. You do not need both.

## Option A: Individual skills via skills CLI

From the target repository:

    npx skills add mishraaditya595/agentic-development-environment --skill evidence-based-code-review

    npx skills add mishraaditya595/agentic-development-environment --skill plan-creator

This path installs individually self-contained packages and does not install ADE root-level workflows, rules or templates. See [skills.sh](https://skills.sh/) for the skills CLI and supported agents.

After installing, open a new coding-agent session and ask naturally: "Review my branch against main for bugs; do not edit or merge." The agent may select evidence-based-code-review. Skill selection is **model-dependent and not guaranteed**; ask explicitly for the skill when important.

## Option B: Full project-local guidance from ADE checkout

There is **no published npx agentic-dev CLI** yet. The working bundle installer is a Python 3.9+ script requiring no third-party packages, external commands or network access while running. Secure filesystem writes currently require POSIX `dir_fd`, `O_DIRECTORY` and `O_NOFOLLOW` support (Linux/macOS). Unsupported runtimes fail closed.

First clone or download the reviewed ADE release into a separate directory:

    git clone https://github.com/mishraaditya595/agentic-development-environment.git
    cd agentic-development-environment

Preview the operation:

    python3 scripts/bootstrap.py --target /path/to/my-project --agents codex,claude,opencode --preset standard --dry-run

Install by re-running without --dry-run. Prefer a pinned release or commit for reproducibility, and do not pipe unknown shell installers straight from the internet.

### Supported flags

- --list: show the exact skill catalog in this checkout.
- --agents codex,claude,opencode: selected coding agents (default codex).
- --preset minimal: plan-creator, plan-implementer, evidence-based-code-review.
- --preset standard: adds repo-onboarding, merge-conflict-resolver, test-engineer, feature-delivery, root-cause-investigation, proof-before-done.
- --preset complete: all skill packages.
- --skills plan-creator,test-engineer: explicit set overriding the preset.
- --target PATH: existing project root.
- --dry-run: preview without writes.

### Generated paths

| Path | Purpose |
| --- | --- |
| .agents/skills/<name>/ | Codex and compatible OpenCode skill discovery |
| .claude/skills/<name>/ | Claude Code skill discovery |
| .agentic-dev/workflows/ | Shared stage ordering and failure recovery |
| .agentic-dev/rules/ | Reference engineering policies |
| .agentic-dev/templates/ | Plan, PR, review and handoff document structures |
| .agentic-dev/config.json | Canonical additive selection inventory, **not** a version-lock file |
| AGENTS.md | Project instructions if no existing file |
| CLAUDE.md | Claude instructions if no existing file; imports AGENTS.md |

**Existing AGENTS.md and CLAUDE.md are preserved, never overwritten.** If either already exists, manually link appropriate .agentic-dev guidance into your existing instructions. Existing Claude files may need an @AGENTS.md import. Existing generated files are reused if byte-identical. Non-directory parent paths, modified managed files, symlinks (including dangling instructions), and invalid inventory files cause a preflight conflict before writing. Exclusive file creation with directory descriptors closes destination and parent symlink races. Write failures trigger best-effort rollback of files and empty directories created by the current run; original files are not deleted.

### Adding agents and skills after installation

Run the same bootstrap script again using the **same pinned ADE checkout**:

    python3 scripts/bootstrap.py --target /path/to/my-project --agents codex --preset minimal
    python3 scripts/bootstrap.py --target /path/to/my-project --agents codex,claude --preset minimal
    python3 scripts/bootstrap.py --target /path/to/my-project --agents codex,claude --skills test-engineer --dry-run
    python3 scripts/bootstrap.py --target /path/to/my-project --agents codex,claude --skills test-engineer

The new selections are **additive**: previously installed agents and skills remain selected even when omitted on a later invocation. Only an unmodified, canonical `.agentic-dev/config.json` and an otherwise untouched set of installed managed files may be expanded. New files are created exclusively; the inventory update is atomic and happens last. Project instruction files remain user-owned. Edited, missing or outdated managed assets cause a conflict—review differences instead of deleting `config.json` to bypass protection. Removing selections and upgrading managed *content* remain manual, reviewed operations.

The installer is copy-only and idempotent. It does not implement automatic package updates, uninstallation, a published CLI, a cryptographic lockfile or Windows-specific secure writes. Exit codes: 0 success, 2 preflight conflict, 1 installation/rollback failure. Incomplete rollback is reported explicitly. Do not run multiple installers against the same target concurrently; other processes can still race the inventory update.

For OpenCode, use the .agents/skills compatible discovery path and verify with your installed runtime. Unknown agents require a tested adapter; Markdown placed in arbitrary directories is not automatically loaded.

## Daily use

- "Plan session history with acceptance criteria, and do not implement yet." → plan-creator
- "Implement the approved plan in docs/plans/history.md, run checks, report gaps." → plan-implementer
- "Fix these merge conflicts preserving both sides and test the result." → merge-conflict-resolver
- "Review PR #42 for regressions and missing tests; read-only." → evidence-based-code-review
- "Build the settings screen end to end, add tests, review, prepare a PR, do not merge." → feature-delivery

Shared workflows and rules guide an agent only if it reads them; the feature-delivery SKILL.md is independently usable when installed alone. Native routing can miss skills: use explicit naming as fallback.

Critical gates (required tests, protected branches) belong in actual CI and permissions. An agent cannot declare a blocked check passed. A PR request is not permission to merge or deploy.

## Troubleshooting

If a skill is not discovered, inspect the generated path and SKILL.md frontmatter, restart the agent, and check runtime permissions. If a wrong skill is selected, explicitly name the intended one and record the misroute in routing evaluations. For install conflicts, review existing files manually; the bootstrap never overwrites them. If existing instructions ignore ADE, add references to .agentic-dev/ and confirm the runtime reads them.

Individual installations made through the skills CLI may contribute to skills.sh discovery. Local Python copies do not necessarily affect that directory's ranking.
