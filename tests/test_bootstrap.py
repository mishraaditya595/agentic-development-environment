"""Offline regression tests for installation and conflict handling (Python 3.9+)."""
import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/bootstrap.py"
spec = importlib.util.spec_from_file_location("bootstrap", SCRIPT)
bootstrap = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bootstrap)


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
            self.assertTrue((t / "AGENTS.md").read_text().startswith("DO NOT MERGE\n"))
            self.assertIn("ADE ROUTING START", (t / "AGENTS.md").read_text())
            self.assertEqual((t / "CLAUDE.md").read_text(), "Our project instructions\n")
            self.assertIn("MANAGED AGENTS.md", result.stdout)
            self.assertIn("PRESERVE CLAUDE.md", result.stdout)

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

    def test_regular_file_parent_aborts_before_writes(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            (t / ".agents").write_text("keep")
            result = run(t, "--agents", "codex")
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("CONFLICT", result.stderr)
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertEqual((t / ".agents").read_text(), "keep")
            # An interrupted attempt must not poison the next installation.
            (t / ".agents").unlink()
            self.assertEqual(run(t, "--agents", "codex").returncode, 0)

    def test_rejects_symlink_parent(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as other:
            t = Path(p)
            (t / ".agents").symlink_to(Path(other), target_is_directory=True)
            result = run(t, "--agents", "codex")
            self.assertEqual(result.returncode, 2)
            self.assertFalse((Path(other) / "skills").exists())
            self.assertFalse((t / ".agentic-dev").exists())

    def test_rejects_symlink_destination_file(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as other:
            t = Path(p)
            outside = Path(other) / "outside"
            outside.write_text("safe")
            dest = t / ".agents/skills/plan-creator/SKILL.md"
            dest.parent.mkdir(parents=True)
            dest.symlink_to(outside)
            result = run(t, "--preset", "minimal")
            self.assertEqual(result.returncode, 2)
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertEqual(outside.read_text(), "safe")

    def test_rejects_dangling_agents_instructions(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            (t / "AGENTS.md").symlink_to(t / "missing.md")
            result = run(t)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertTrue((t / "AGENTS.md").is_symlink())

    def test_adds_agents_and_skills_without_removing_old_selection(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--agents", "codex", "--preset", "minimal").returncode, 0)
            second = run(t, "--agents", "codex,claude", "--preset", "minimal")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertIn("UPDATE .agentic-dev/config.json", second.stdout)
            self.assertTrue((t / ".claude/skills/plan-creator/SKILL.md").is_file())
            third = run(t, "--agents", "codex", "--skills", "test-engineer")
            self.assertEqual(third.returncode, 0, third.stderr)
            config = json.loads((t / ".agentic-dev/config.json").read_text())
            self.assertEqual(config["agents"], ["claude", "codex"])
            self.assertIn("test-engineer", config["skills"])
            self.assertIn("plan-creator", config["skills"])
            self.assertTrue((t / ".claude/skills/test-engineer/SKILL.md").is_file())
            self.assertEqual(run(t, "--agents", "codex", "--preset", "minimal").returncode, 0)

    def test_modified_managed_file_blocks_additive_expansion(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            mod = t / ".agents/skills/plan-creator/SKILL.md"
            mod.write_text("modified")
            old = (t / ".agentic-dev/config.json").read_bytes()
            result = run(t, "--agents", "codex,claude", "--preset", "minimal")
            self.assertEqual(result.returncode, 2)
            self.assertEqual(old, (t / ".agentic-dev/config.json").read_bytes())
            self.assertFalse((t / ".claude").exists())

    def test_modified_inventory_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            config = t / ".agentic-dev/config.json"
            config.write_text(config.read_text() + "\n")
            result = run(t, "--agents", "codex,claude", "--preset", "minimal")
            self.assertEqual(result.returncode, 2)
            self.assertIn("CONFLICT", result.stderr)
            self.assertFalse((t / ".claude").exists())

    def test_rolls_back_when_write_fails_halfway(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            actual = bootstrap._write_new
            counter = [0]

            def failing(*args, **kwargs):
                counter[0] += 1
                if counter[0] == 4:
                    raise OSError("simulated disk full")
                return actual(*args, **kwargs)

            with mock.patch.object(bootstrap, "_write_new", side_effect=failing), contextlib.redirect_stderr(io.StringIO()) as errors, contextlib.redirect_stdout(io.StringIO()):
                result = bootstrap.main(["--target", str(t), "--preset", "minimal"])
            self.assertEqual(result, 1)
            self.assertIn("INSTALL FAILED", errors.getvalue())
            self.assertFalse((t / ".agentic-dev").exists())
            self.assertFalse((t / ".agents").exists())
            self.assertFalse((t / "AGENTS.md").exists())

    def test_failed_config_replace_rolls_back_new_files(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            config = t / ".agentic-dev/config.json"
            old = config.read_bytes()
            with mock.patch.object(bootstrap.os, "replace", side_effect=OSError("simulated replace failure")), contextlib.redirect_stderr(io.StringIO()) as errors, contextlib.redirect_stdout(io.StringIO()):
                result = bootstrap.main(["--target", str(t), "--agents", "codex,claude", "--preset", "minimal"])
            self.assertEqual(result, 1)
            self.assertIn("INSTALL FAILED", errors.getvalue())
            self.assertEqual(config.read_bytes(), old)
            self.assertFalse((t / ".claude").exists())
            self.assertFalse(list((t / ".agentic-dev").glob(".config-*.tmp")))

    def test_symlink_inserted_after_preflight_is_not_followed(self):
        with tempfile.TemporaryDirectory() as p, tempfile.TemporaryDirectory() as other:
            t = Path(p)
            outside = Path(other) / "important.txt"
            outside.write_text("untouched")
            actual = bootstrap._write_new
            injected = [False]
            injected_path = [None]

            def raced(root_fd, target, path, content, created_files, created_dirs):
                if not injected[0]:
                    injected[0] = True
                    injected_path[0] = path
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.symlink_to(outside)
                return actual(root_fd, target, path, content, created_files, created_dirs)

            with mock.patch.object(bootstrap, "_write_new", side_effect=raced), contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                result = bootstrap.main(["--target", str(t), "--preset", "minimal"])
            self.assertEqual(result, 1)
            self.assertEqual(outside.read_text(), "untouched")
            self.assertTrue(injected_path[0].is_symlink())  # attacker-owned link is preserved
            self.assertFalse((t / ".agents").exists())

    def test_modified_routing_block_fails_before_writes(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            path = t / "AGENTS.md"
            path.write_text(path.read_text().replace("ADE ROUTING END", "ADE ROUTING END") + "")
            # Change only the managed content, leaving the markers intact.
            path.write_text(path.read_text().replace("primary skill", "different skill"))
            old = path.read_bytes()
            result = run(t, "--agents", "claude", "--preset", "minimal")
            self.assertEqual(result.returncode, 2)
            self.assertIn("CONFLICT", result.stderr)
            self.assertEqual(path.read_bytes(), old)
            self.assertFalse((t / ".claude").exists())

    def test_existing_agents_routing_is_idempotent(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            (t / "AGENTS.md").write_text("PROJECT RULE\n")
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            updated = (t / "AGENTS.md").read_text()
            self.assertEqual(updated.count("ADE ROUTING START"), 1)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            self.assertEqual((t / "AGENTS.md").read_text(), updated)

    def test_existing_agents_routing_restored_if_inventory_update_fails(self):
        with tempfile.TemporaryDirectory() as p:
            t = Path(p)
            self.assertEqual(run(t, "--preset", "minimal").returncode, 0)
            instructions = t / "AGENTS.md"
            # Simulate an older local project that has instructions but no ADE section.
            instructions.write_text("ORIGINAL PROJECT RULE\\n")
            before = instructions.read_bytes()
            old_config = (t / ".agentic-dev/config.json").read_bytes()
            original_replace = bootstrap.os.replace
            calls = [0]

            def fail_second_replace(*args, **kwargs):
                calls[0] += 1
                if calls[0] == 2:
                    raise OSError("injected inventory replace error")
                return original_replace(*args, **kwargs)

            with mock.patch.object(bootstrap.os, "replace", side_effect=fail_second_replace), contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                result = bootstrap.main(["--target", str(t), "--agents", "codex,claude", "--preset", "minimal"])
            self.assertEqual(result, 1)
            self.assertEqual(instructions.read_bytes(), before)
            self.assertEqual((t / ".agentic-dev/config.json").read_bytes(), old_config)
            self.assertFalse((t / ".claude").exists())

    def test_unknown_skill_is_invalid(self):
        with tempfile.TemporaryDirectory() as p:
            result = run(Path(p), "--skills", "made-up-skill")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("invalid --skills", result.stderr)


if __name__ == "__main__":
    unittest.main()