"""Offline installer smoke tests. Requires Python 3 only."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/bootstrap.py"


def run(target, *args):
    return subprocess.run([sys.executable, str(SCRIPT), "--target", str(target), *args], capture_output=True, text=True)


class BootstrapTests(unittest.TestCase):
    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            result = run(t, "--dry-run", "--agents", "codex,claude")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertFalse((t / "AGENTS.md").exists())

    def test_installs_for_multiple_agents_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            args = ("--agents", "codex,claude,opencode", "--preset", "minimal")
            first = run(t, *args)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((t / ".agents/skills/plan-creator/SKILL.md").exists())
            self.assertTrue((t / ".claude/skills/plan-creator/SKILL.md").exists())
            self.assertTrue((t / "AGENTS.md").exists())
            self.assertTrue((t / "CLAUDE.md").exists())
            self.assertTrue((t / ".agentic-dev/workflows/bugfix.md").exists())
            second = run(t, *args)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("0 new", second.stdout)

    def test_preserves_existing_instructions(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            (t / "AGENTS.md").write_text("DO NOT MERGE\n")
            (t / "CLAUDE.md").write_text("Our project instructions\n")
            result = run(t, "--agents", "claude")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((t / "AGENTS.md").read_text(), "DO NOT MERGE\n")
            self.assertEqual((t / "CLAUDE.md").read_text(), "Our project instructions\n")
            self.assertIn("PRESERVE", result.stdout)

    def test_conflicts_abort_all_writes(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            conflict = t / ".agents/skills/plan-creator/SKILL.md"
            conflict.parent.mkdir(parents=True)
            conflict.write_text("custom skill")
            result = run(t, "--agents", "codex")
            self.assertEqual(result.returncode, 2)
            self.assertIn("CONFLICT", result.stderr)
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertEqual(conflict.read_text(), "custom skill")

    def test_rejects_symlink_destination(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as other:
            t = Path(p)
            (t / ".agents").symlink_to(Path(other), target_is_directory=True)
            result = run(t, "--agents", "codex")
            self.assertEqual(result.returncode, 2)
            self.assertFalse((Path(other) / "skills").exists())

    def test_unknown_skill_is_invalid(self):
        with tempfile.TemporaryDirectory() as p:
            result = run(Path(p), "--skills", "made-up-skill")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid --skills", result.stderr)


if __name__ == "__main__":
    unittest.main()
