#!/usr/bin/env python3
"""Opt-in, create-only ADE hook settings installer."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import shlex
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import bootstrap

def configuration(agent, root):
    script = ('"\u0024{CLAUDE_PROJECT_DIR:-}/.agentic-dev/bin/ade-hook.py"'
              if agent == "claude" else shlex.quote(str(root / ".agentic-dev/bin/ade-hook.py")))
    def hook(event, timeout):
        return [{"hooks":[{"type":"command",
                 "command":"python3 " + script + " " + event + " || exit 0",
                 "timeout":timeout}]}]
    return {"hooks":{"UserPromptSubmit":hook("prompt",10),"Stop":hook("stop",55)}}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target",required=True)
    parser.add_argument("--agents",default="claude")
    parser.add_argument("--local",action="store_true",help="Use personal Claude settings.local.json")
    parser.add_argument("--dry-run",action="store_true")
    args=parser.parse_args(argv)
    root=Path(args.target).absolute()
    agents=sorted(set(bootstrap.names(args.agents)))
    if not root.is_dir() or root.is_symlink() or not agents or not set(agents)<={"claude","codex"}:
        parser.error("Expected existing target and supported agents claude,codex")
    if not (root/".agentic-dev/bin/ade-hook.py").is_file():
        parser.error("Upgrade ADE with scripts/bootstrap.py before installing hooks")
    if args.local and "claude" not in agents:
        parser.error("--local requires claude")
    assets={}
    for agent in agents:
        filename=(".claude/settings.local.json" if args.local else ".claude/settings.json") if agent=="claude" else ".codex/hooks.json"
        assets[root/filename]=(json.dumps(configuration(agent,root),indent=2)+"\n").encode()
    for path,content in assets.items():
        if path.is_symlink() or (path.exists() and (not path.is_file() or path.read_bytes()!=content)):
            print("CONFLICT "+str(path.relative_to(root)),file=sys.stderr)
            print("Merge this hooks object manually:\n"+json.dumps(configuration("claude" if ".claude" in path.parts else "codex",root)["hooks"],indent=2),file=sys.stderr)
            print("No files changed; --local avoids team-wide Claude settings.",file=sys.stderr)
            return 2
    try:
        created,same=bootstrap.install_new_assets(root,assets,dry_run=args.dry_run)
    except (ValueError,OSError) as exc:
        print("Hook setup failed: "+str(exc),file=sys.stderr)
        return 2
    for path in created:
        print(("WOULD CREATE " if args.dry_run else "CREATE ")+str(path.relative_to(root)))
    if not created:
        print("Hooks already installed; no changes.")
    elif not args.dry_run:
        print("Hook settings created. Review and enable them in your coding agent.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
