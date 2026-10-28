# Optional ADE lifecycle hooks

ADE's normal bootstrap installs skills, routing instructions, and a check runner. **It does not automatically enable hooks.** Project hooks can execute commands, so installing them is a separate explicit decision.

## Supported integrations

- Claude Code project hook configuration in `.claude/settings.json`.
- Codex project hook configuration in `.codex/hooks.json` (project must be trusted).
- OpenCode continues to use ADE's portable Agent Skills and manually invoked checks. A native OpenCode adapter is not claimed supported here.

Reference documentation: [Claude Code hooks](https://code.claude.com/docs/en/hooks), [Codex hooks](https://learn.chatgpt.com/docs/hooks), [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-advanced).

## Install explicitly

From an ADE checkout, after you have installed the normal bundle in your target project:

```sh
python3 scripts/install-hooks.py --target /path/to/repo --agents claude,codex --dry-run
python3 scripts/install-hooks.py --target /path/to/repo --agents claude,codex
```

The command refuses to overwrite existing settings, even when they contain a compatible custom hook. Manually merge configurations if there is a conflict. It copies `ade-hook.py` and its module into the installed bin and creates separate runtime hook JSON files only when absent. No automatic edits to `.gitignore` or approval configuration.

## What happens in a coding session

**UserPromptSubmit:** adds a short reminder to consult `.agentic-dev/skill-map.json` and use only skills present in `.agentic-dev/config.json`. This provides context; it does not classify or force a skill activation.

**Stop:** if Git shows working-tree changes, runs the configured `fast` check with at most a 45-second execution limit. If it fails, asks the coding agent to continue fixing the problem, but only for one continuation. The second stop does not block again. If the test is unconfigured, Git is unavailable, or execution times out, it reports that verification is unconfirmed rather than implying it passed. If there are no working-tree changes it skips; committed work still needs full CI and review.

Enable a real fast check first in `.agentic-dev/harness.json`. Do not use a shell command or destructive command there; the harness runs user-configured argument arrays directly.

## Security boundaries

- Native hooks are advisory—not a substitute for branch protection, required CI or human merge approval.
- A repository-installed script can be modified by code with write permission, so a hook is not an immutable policy boundary.
- Existing configuration files are never overwritten; conflicted installation aborts before writing anything.
- The stop hook avoids printing command output into the prompt to reduce accidental secret propagation. It reports status and limited reason only.
- Repeated stop failures result in a warning, not an infinite correction loop.
- Actual behavior depends on the installed version of the coding agent. Validate with a throwaway project and review hook permissions before enabling in production repositories.
