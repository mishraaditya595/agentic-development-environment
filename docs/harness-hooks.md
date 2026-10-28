# Optional ADE lifecycle hooks

ADE's standard bootstrap **only copies inert hook scripts**. Hooks remain disabled until you explicitly install project settings. Hook execution requires Python 3, a supported shell, and an actual configured `fast` check.

## Claude Code

Use `python3 scripts/install-hooks.py --target /absolute/project --agents claude --local --dry-run`, review the preview, then omit `--dry-run`. The `--local` option creates `.claude/settings.local.json` for your own machine, avoiding team-wide activation. Without `--local`, settings are written to `.claude/settings.json` and **may affect collaborators if committed**. Existing settings are never overwritten; on conflict, the installer prints the exact JSON `hooks` object to merge manually.

Claude commands resolve scripts through `CLAUDE_PROJECT_DIR`, so they work when launched from nested folders or in projects without Git. Each command ends with `|| exit 0` to prevent a missing executable from returning status 2 and blocking prompts or stop events. Shell execution and `CLAUDE_PROJECT_DIR` availability should still be validated in your Claude version.

## Codex

Run `python3 scripts/install-hooks.py --target /absolute/project --agents codex --dry-run` and review the generated `.codex/hooks.json`; then omit `--dry-run`. Its command embeds the absolute hook-script path, which avoids reliance on `git rev-parse` from monorepos and submodules. Moving a repository requires reinstalling or updating that path. Existing settings are never overwritten; the installer prints a merge snippet on conflict.

Codex's official [Hooks documentation](https://learn.chatgpt.com/docs/hooks) describes hooks configuration, and the [configuration reference](https://learn.chatgpt.com/docs/config-file/config-basic) lists `features.hooks`. However **the adapter is not yet validated in a live Codex session**. Do not assume `additionalContext`, stop blocking, or project trust works identically to Claude across versions. Verify in a disposable project before relying on it.

## Behavior and safety

At UserPromptSubmit the hook gives the model (not the user) a brief skill-routing reminder through `hookSpecificOutput.additionalContext`. At Stop it checks Git working-tree changes; if changes exist, it runs the configured fast check for up to 45 seconds. A failed check asks for one bounded continuation; the `stop_hook_active` guard prevents loops. Missing tools, a failed hook script, absent config or a clean tree cannot be interpreted as proof of verification.

The 64 KiB input limit is fail-open; an oversized prompt payload falls back to default routing context. Hook output deliberately excludes raw test logs. These hooks are advisory, not authorization boundaries or alternatives to required CI.

## Existing settings, monorepos, and uninstall

With an existing `.claude/settings.json`, choose `--local` or copy the printed `hooks` block and merge it carefully. In a monorepo, run the installer for the exact ADE project root rather than assuming the Git root. Codex uses that absolute directory; Claude uses its project directory variable.

To disable, remove only the ADE hook entries from the selected `.claude/settings.json`, `.claude/settings.local.json`, or `.codex/hooks.json`. Do not delete other hook entries or ADE-managed scripts, which remain available but inert. Review project-trust prompts and settings after any changes.
