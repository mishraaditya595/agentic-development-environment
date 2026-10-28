"""Regression tests for explicit work state, workspace gating and sensor proofs."""
import json
from concurrent.futures import ThreadPoolExecutor
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

    def test_status_does_not_create_missing_journal(self):
        from harness.session import events
        state = self.root / ".agentic-dev/state"
        self.assertFalse(state.exists())
        self.assertEqual(summary(self.root)["completed_count"], 0)
        self.assertEqual(events(self.root), [])
        self.assertFalse(state.exists())
        state.mkdir()
        self.assertEqual(summary(self.root)["completed_count"], 0)
        self.assertFalse((state / "sessions.jsonl").exists())

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

    def test_simultaneous_session_starts_are_serialized(self):
        def start(_):
            try:
                apply(self.root, "start", title="Concurrent")
                return "started"
            except ValueError:
                return "already active"
        with ThreadPoolExecutor(max_workers=2) as executor:
            statuses = list(executor.map(start, range(2)))
        self.assertEqual(sorted(statuses), ["already active", "started"])
        self.assertEqual(summary(self.root)["active"]["title"], "Concurrent")

    def test_truncated_journal_recovers_on_next_write(self):
        from harness.session import events
        apply(self.root, "start", title="First")
        journal = self.root / ".agentic-dev/state/sessions.jsonl"
        with journal.open("ab") as stream:
            stream.write(b'{"kind":"checkpoint","step":"broken')
        self.assertEqual(len(events(self.root)), 1)
        self.assertEqual(summary(self.root)["active"]["title"], "First")
        apply(self.root, "checkpoint", step="Recovered")
        self.assertEqual(len(events(self.root)), 2)
        self.assertNotIn(b"broken", journal.read_bytes())

    def test_invalid_complete_journal_line_is_not_silently_dropped(self):
        apply(self.root, "start", title="First")
        journal = self.root / ".agentic-dev/state/sessions.jsonl"
        with journal.open("ab") as stream:
            stream.write(b'invalid json\n')
        with self.assertRaises(ValueError):
            summary(self.root)
        with self.assertRaises(ValueError):
            apply(self.root, "checkpoint", step="No data loss")

    def test_journal_symlinked_state_directory_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / ".agentic-dev/state").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaises(OSError):
                apply(self.root, "start", title="Forbidden")
            self.assertFalse((Path(outside) / "sessions.jsonl").exists())

    def test_reserved_workspace_members_rejected(self):
        for member in (".git", ".agentic-dev"):
            (self.root / member).mkdir(exist_ok=True)
            save(self.root / ".agentic-dev/workspace.json", {"schema_version":1,
                "repositories":[{"name":"reserved","path":member}]})
            with self.assertRaises(ValueError):
                inspect(self.root)

    def test_unknown_sensor_property_rejected(self):
        folder = self.root / "fixtures"
        folder.mkdir()
        (folder / "clean").write_text("safe")
        (folder / "broken").write_text("bad")
        save(self.root / ".agentic-dev/sensors.json", {"schema_version":1,"sensors":[{
            "id":"invalid", "argv":[sys.executable, "{path}"],
            "clean":"fixtures/clean","violation":"fixtures/broken","timeout":5}]})
        with self.assertRaisesRegex(ValueError, "Unsupported sensor"):
            registry(self.root)

    def test_sensor_rejects_untrusted_paths(self):
        save(self.root / ".agentic-dev/sensors.json", {"schema_version":1,"sensors":[{
            "id":"escape", "argv":[sys.executable,"{path}"],
            "clean":"../outside", "violation":"../outside"}]})
        with self.assertRaises(ValueError):
            registry(self.root)


if __name__ == "__main__":
    unittest.main()
