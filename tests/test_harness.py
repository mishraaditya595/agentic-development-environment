import json
import os
import time
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from harness.core import config_for, gather_checks, doctor, proof, write_evidence
from harness.policy import audit

class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".agentic-dev").mkdir()

    def configure(self, checks):
        (self.root / ".agentic-dev/harness.json").write_text(json.dumps({"schema_version":1,"checks":checks}))

    def test_missing_config(self):
        with self.assertRaises(ValueError): config_for(self.root)
        self.assertTrue(doctor(self.root)["issues"])

    def test_missing_check_blocked(self):
        self.configure({})
        self.assertEqual(gather_checks(self.root,["fast"])[0]["status"],"blocked")

    def test_pass_fail(self):
        self.configure({"fast":{"argv":[sys.executable,"-c","print(1)"]},"full":{"argv":[sys.executable,"-c","raise SystemExit(7)"]}})
        outcome = gather_checks(self.root,["fast","full"])
        self.assertEqual([x["status"] for x in outcome],["pass","fail"])
        self.assertEqual(outcome[1]["exit_code"],7)

    def test_no_shell_interpolation(self):
        path=self.root/"unexpected"
        self.configure({"fast":{"argv":[sys.executable,"-c","import sys;print(sys.argv[1])","x;touch "+str(path)]}})
        self.assertEqual(gather_checks(self.root,["fast"])[0]["status"],"pass")
        self.assertFalse(path.exists())

    def test_bad_config_rejected(self):
        for item in ({"argv":"echo test"},{"argv":[]},{"argv":["echo"],"timeout_seconds":0},{"argv":["echo"],"timeout_seconds":True}):
            self.configure({"fast":item})
            with self.assertRaises(ValueError): config_for(self.root)

    def test_negative_probe(self):
        self.configure({"full":{"argv":[sys.executable,"-c","print(1)"]}})
        self.assertTrue(proof(self.root,"full",[sys.executable,"-c","raise SystemExit(1)"])["proven_fails"])
        self.assertFalse(proof(self.root,"full",[sys.executable,"-c","print(1)"])["proven_fails"])

    def test_evidence_new_only(self):
        path=Path(".agentic-dev/evidence/probe.json")
        self.assertEqual(write_evidence(self.root,{"a":1},path),str(path))
        with self.assertRaises(ValueError): write_evidence(self.root,{"a":1},path)
        with self.assertRaises(ValueError): write_evidence(self.root,{"a":1},Path("AGENTS.md"))

    def test_invariants_cannot_claim_enforcement_without_checks(self):
        self.configure({})
        (self.root / ".agentic-dev/invariants.json").write_text(json.dumps({
            "schema_version":1,
            "rules":[{"id":"database-safety","severity":"critical","enforced_by":"check:full"}]
        }))
        result = audit(self.root, config_for(self.root))
        self.assertEqual(result["level"], "configured")
        self.assertTrue(result["issues"])
        self.assertEqual(result["invariants"][0]["verification_status"], "not-run")

    def test_rejects_unknown_check_options(self):
        self.configure({"fast": {"argv": [sys.executable, "-c", "print('hi')"], "shell": True}})
        with self.assertRaises(ValueError):
            config_for(self.root)

    def test_evidence_folder_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / ".agentic-dev/evidence").symlink_to(Path(outside), target_is_directory=True)
            with self.assertRaises(ValueError):
                write_evidence(self.root, {"outcome": "blocked"}, Path(".agentic-dev/evidence/leak.json"))
            self.assertFalse((Path(outside) / "leak.json").exists())

    def test_check_timeout_terminates_child_process_group(self):
        pid_file = self.root / "worker.pid"
        child = ("import os,time;open(" + repr(str(pid_file)) +
                 ",'w').write(str(os.getpid()));time.sleep(30)")
        self.configure({"fast": {"argv": [sys.executable, "-c",
            "import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',sys.argv[1]]);time.sleep(30)", child],
            "timeout_seconds": 1}})
        result = gather_checks(self.root, ["fast"])[0]
        self.assertEqual(result["status"], "blocked")
        if pid_file.exists():
            pid = int(pid_file.read_text())
            # A zombie may briefly exist, but the child must not be live.
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                pass
            else:
                if Path("/proc") .is_dir():
                    status = (Path("/proc") / str(pid) / "stat").read_text()
                    self.assertIn(status.split()[2], ("Z", "X"))

    def test_routing_integrity(self):
        routes=json.loads((ROOT/"routing/skill-map.json").read_text())["routes"]
        self.assertEqual(len(routes),len({r["id"] for r in routes}))
        for route in routes:
            self.assertTrue(route["triggers"])
            self.assertTrue(route["exclude"])
            for name in [route["primary"]]+route["supporting"]:
                self.assertTrue((ROOT/"skills"/name/"SKILL.md").exists(),name)
