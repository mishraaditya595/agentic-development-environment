"""Regression tests for explicit work state, workspace gating and sensor proofs."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.session import apply, summary
from harness.workspace import inspect
from harness.sensors import prove, registry


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj), encoding="utf-8")


class OperationsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / ".agentic-dev").mkdir()

    def test_session_start_checkpoint_close_and_resume(self):
        start = apply(self.root, "start", title="Implement offline history", plan="docs/plans/history.md")
        self.assertEqual(start["active"]["title"], "Implement offline history")
        with self.assertRaises(ValueError):
            apply(self.root, "start", title="second session")
        progress = apply(self.root, "checkpoint", step="Tests written")
        self.assertEqual(progress["active"]["checkpoints"][-1]["step"], "Tests written")
        done = apply(self.root, "close", verdict="partial")
        self.assertIsNone(done["active"])
        self.assertEqual(done["last_completed"]["verdict"], "partial")
        self.assertEqual(summary(self.root)["completed_count"], 1)
        self.assertIsNotNone(apply(self.root, "start", title="Continue")["active"])

    def test_session_validation_and_no_fake_verdict(self):
        with self.assertRaises(ValueError):
            apply(self.root, "checkpoint", step="No session")
        with self.assertRaises(ValueError):
            apply(self.root, "start", title="Task", plan="../secrets")
        with self.assertRaises(ValueError):
            apply(self.root, "start", title="")
        apply(self.root, "start", title="Task")
        with self.assertRaises(ValueError):
            apply(self.root, "close", verdict="success")
        self.assertIsNotNone(summary(self.root)["active"])

    def test_workspace_checks_all_repos_without_fake_green(self):
        for name, code in (("backend", 0), ("mobile", 1)):
            repo = self.root / name
            repo.mkdir()
            save(repo / ".agentic-dev/harness.json", {"schema_version":1,
                "checks":{"fast":{"argv":[sys.executable, "-c", f"raise SystemExit({code})"]}}})
        save(self.root / ".agentic-dev/workspace.json", {"schema_version":1,
            "repositories":[{"name":"api","path":"backend"},{"name":"app","path":"mobile"}]})
        report = inspect(self.root, "fast")
        self.assertEqual(report["verdict"], "incomplete")
        self.assertEqual([m["status"] for m in report["members"]], ["pass", "fail"])
        (self.root / "mobile/.agentic-dev/harness.json").unlink()
        self.assertEqual(inspect(self.root, "fast")["members"][1]["status"], "blocked")

    def test_workspace_rejects_path_escape_and_duplicates(self):
        for paths in ([{"name":"escape","path":".."}],
                      [{"name":"same","path":"x"},{"name":"same","path":"y"}]):
            for name in ("x", "y"):
                (self.root / name).mkdir(exist_ok=True)
            save(self.root / ".agentic-dev/workspace.json", {"schema_version":1,
                "repositories":paths})
            with self.assertRaises(ValueError):
                inspect(self.root, "fast")

    def test_sensor_fixture_proof(self):
        folder = self.root / "tests/fixtures"
        folder.mkdir(parents=True)
        (folder / "safe.txt").write_text("SYNTHETIC")
        (folder / "bad.txt").write_text("PRODUCTION")
        command = [sys.executable, "-c",
            "from pathlib import Path;import sys;raise SystemExit(1 if 'PRODUCTION' in Path(sys.argv[1]).read_text() else 0)",
            "{path}"]
        registry_file = {"schema_version":1,"sensors":[{
            "id":"no-prod-data", "argv":command,
            "clean":"tests/fixtures/safe.txt", "violation":"tests/fixtures/bad.txt"}]}
        save(self.root / ".agentic-dev/sensors.json", registry_file)
        report = prove(self.root)
        self.assertEqual(report["verdict"], "pass")
        self.assertTrue(report["results"][0]["proven"])
        registry_file["sensors"][0]["argv"]=[sys.executable,"-c","print('always passing')","{path}"]
        save(self.root / ".agentic-dev/sensors.json", registry_file)
        self.assertEqual(prove(self.root)["verdict"], "incomplete")

    def test_sensor_rejects_untrusted_paths(self):
        save(self.root / ".agentic-dev/sensors.json", {"schema_version":1,"sensors":[{
            "id":"escape", "argv":[sys.executable,"{path}"],
            "clean":"../outside", "violation":"../outside"}]})
        with self.assertRaises(ValueError):
            registry(self.root)


if __name__ == "__main__":
    unittest.main()
