# Git and pull-request rules

- Inspect git status, current branch, base and any user changes before editing or conflict resolution.
- Work on a feature branch for substantial changes; do not commit directly to a protected branch.
- Keep commits focused and messages descriptive; do not add unrelated files or generated artifacts.
- Never discard unrelated local edits; avoid reset --hard, clean -fd, force pushes, rebase of shared branches or branch deletion without explicit approval.
- Creating a PR requires user/workflow authorization. Put summary, actual verification, limitations and risks in the description.
- Reviewing a PR does not imply permission to post comments, edit code, approve, merge or enable auto-merge.
- Merging and protected-branch updates always require explicit human authorization. Do not infer it from "finish", "complete" or "ready".
