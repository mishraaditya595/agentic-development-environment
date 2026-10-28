# ADE distribution and discovery architecture

Every skill below skills/<name>/ is independently executable from SKILL.md, with package-local supporting files. The shared workflows/, rules/ and templates/ are **optional guidance layers** not required by standalone skill users.

Two supported distribution modes:

| Mode | Mechanism | Shared guidance |
| --- | --- | --- |
| One skill | npx skills add owner/repository --skill name | No |
| Project-local bundle | python3 scripts/bootstrap.py --target PATH | Yes |

The proposed npx agentic-dev CLI is not implemented.

Native skill discovery uses .agents/skills/ for Codex, .claude/skills/ for Claude Code and .agents/skills/ as a compatible OpenCode route. The bootstrap copies files to those paths, deduplicating common destinations. Reopen the agent session after install.

Requests trigger skills through the agent model's semantic matching against skill metadata. Selection is probabilistic; there is no ADE LLM router and no guarantee that a simple request activates a given skill. Existing project instructions may reinforce discovery but do not implement it. A workflow Markdown file does not automatically execute—feature-delivery is a portable SKILL.md entrypoint.

Installer safety: dry-run support, existing instruction preservation, byte-identical idempotency, preflight refusal of conflicts and symlinked destinations, no network or subprocesses, no auto-update or destructive force option. It creates a config inventory, **not** cryptographic provenance. Changes to generated files, updates and removal remain manual until a tested managed manifest is implemented.

Validate with:

    sh scripts/validate-skills.sh
    python3 scripts/validate-ade.py
    python3 -m unittest discover -s tests -v

When the skills CLI is available:

    npx skills add ./ --list

Finally, test real agent activation using tests/skill-routing/README.md; static checks cannot certify runtime model routing. Enforce nonnegotiable merge/deploy controls with branch protection, CI and permissions.
