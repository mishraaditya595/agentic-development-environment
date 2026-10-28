"""Opt-in ADE hook adapter regression tests."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.hooks import process

INSTALLER = ROOT / "scripts/install-hooks.py"
BOOTSTRAP = ROOT / "scripts/bootstrap.py"

def run(script, target, *args):
    return subprocess.run([sys.executable,str(script),"--target",str(target),*args],
                          capture_output=True,text=True)

class HookTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        (self.root/".agentic-dev").mkdir()
        (self.root/".agentic-dev/skill-map.json").write_text(json.dumps({
            "schema_version":1,"routes":[{"primary":"test-engineer"},{"primary":"plan-creator"}]}))
        (self.root/".agentic-dev/config.json").write_text(json.dumps({"skills":["test-engineer"]}))

    def check(self, exitcode):
        (self.root/".agentic-dev/harness.json").write_text(json.dumps({
            "schema_version":1,"checks":{"fast":{"argv":[sys.executable,"-c",f"raise SystemExit({exitcode})"]}}}))

    def test_prompt_injects_only_installed_skills(self):
        result=process(self.root,"prompt",{})
        content=result["hookSpecificOutput"]["additionalContext"]
        self.assertIn("test-engineer",content)
        self.assertNotIn("plan-creator",content)

    def test_stop_blocks_on_failed_check_only_once(self):
        self.check(3)
        with patch("harness.hooks.changed",return_value=True):
            first=process(self.root,"stop",{})
            self.assertEqual(first["decision"],"block")
            self.assertIn("exit code 3",first["reason"])
            repeated=process(self.root,"stop",{"stop_hook_active":True})
            self.assertNotIn("decision",repeated)
            self.assertIn("unverified",repeated["systemMessage"])

    def test_stop_pass_and_warnings(self):
        self.check(0)
        with patch("harness.hooks.changed",return_value=True):
            success=process(self.root,"stop",{})
            self.assertIn("passed",success["systemMessage"])
            self.assertNotIn("decision",success)
        (self.root/".agentic-dev/harness.json").unlink()
        with patch("harness.hooks.changed",return_value=True):
            self.assertIn("unavailable",process(self.root,"stop",{})["systemMessage"])
        with patch("harness.hooks.changed",return_value=False):
            self.assertIn("skipped",process(self.root,"stop",{})["systemMessage"])

    def test_hook_installation_is_opt_in_and_idempotent(self):
        target=self.root/"project"
        target.mkdir()
        self.assertEqual(run(BOOTSTRAP,target,"--preset","minimal").returncode,0)
        dry=run(INSTALLER,target,"--agents","codex,claude","--dry-run")
        self.assertEqual(dry.returncode,0,dry.stderr)
        self.assertFalse((target/".codex").exists())
        self.assertFalse((target/".claude").exists())
        first=run(INSTALLER,target,"--agents","codex,claude")
        self.assertEqual(first.returncode,0,first.stderr)
        self.assertTrue((target/".claude/settings.json").is_file())
        self.assertTrue((target/".codex/hooks.json").is_file())
        self.assertTrue((target/".agentic-dev/bin/ade-hook.py").is_file())
        self.assertEqual(run(INSTALLER,target,"--agents","claude,codex").returncode,0)
        settings=target/".claude/settings.json"
        settings.write_text('{"custom":"mine"}')
        second=run(INSTALLER,target,"--agents","codex,claude")
        self.assertEqual(second.returncode,2)
        self.assertEqual(settings.read_text(),'{"custom":"mine"}')

    def test_existing_settings_prevent_any_hook_writes(self):
        target=self.root/"project"
        target.mkdir()
        self.assertEqual(run(BOOTSTRAP,target,"--preset","minimal").returncode,0)
        settings=target/".claude/settings.json"
        settings.parent.mkdir()
        settings.write_text('{"hooks":{"custom":true}}')
        result=run(INSTALLER,target,"--agents","claude,codex")
        self.assertEqual(result.returncode,2)
        self.assertFalse((target/".codex").exists())
        self.assertFalse((target/".agentic-dev/bin/ade-hook.py").exists())
