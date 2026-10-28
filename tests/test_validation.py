"""One validator must serve both CLI entry points."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from skill_validation import metadata, links, validate_catalog

spec = importlib.util.spec_from_file_location("validate_ade", ROOT / "scripts/validate-ade.py")
validate_ade = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_ade)


class ValidatorTests(unittest.TestCase):
    def test_accepts_folded_description_and_quote(self):
        content = "---\nname: 'demo'\ndescription: >\n  Explains what this skill does\n  and when to use it\nlicense: Apache-2.0\n---\n"
        self.assertEqual(metadata(content, "demo"), [])

    def test_rejects_name_mismatch_missing_license_and_duplicate_fields(self):
        text = "---\nname: wrong\nname: wrong\ndescription: null\nlicense: MIT\n---\n"
        result = " ".join(metadata(text, "demo"))
        for issue in ("duplicate", "name mismatch", "description", "license"):
            self.assertIn(issue, result)

    def test_link_outside_and_missing_local_are_errors(self):
        with tempfile.TemporaryDirectory() as p:
            folder = Path(p) / "skills/demo"
            folder.mkdir(parents=True)
            (folder / "existing.md").write_text("okay")
            result = links("[yes](existing.md) [missing](missing.md) [outside](../../secret.md) [website](https://example.com)\n```\n[ignored](no.md)\n```", folder)
            self.assertEqual(len(result), 2)

    def test_catalog_requires_evals_for_every_skill(self):
        with tempfile.TemporaryDirectory() as p:
            folder = Path(p) / "evidence-based-code-review"
            folder.mkdir()
            (folder / "SKILL.md").write_text("---\nname: evidence-based-code-review\ndescription: Reviewer\nlicense: Apache-2.0\n---\n")
            issues, names = validate_catalog(Path(p))
            self.assertIn("evidence-based-code-review", names)
            self.assertTrue(any("evaluation prompts" in issue for issue in issues))

    def test_shared_layout_requires_refactoring_workflow(self):
        with tempfile.TemporaryDirectory() as p:
            issues = validate_ade.validate(Path(p))
            self.assertIn("Missing workflow: refactoring.md", issues)


if __name__ == "__main__":
    unittest.main()