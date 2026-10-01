import json
import unittest
from pathlib import Path

from axiom_hive.analyzer import _RULES, analyze_diff
from axiom_hive.report import render_json

ROOT = Path(__file__).resolve().parents[1]


class ContractTests(unittest.TestCase):
    def test_report_matches_declared_schema_shape_and_enums(self):
        schema = json.loads((ROOT / "assets/review-schema.json").read_text(encoding="utf-8"))
        diff = (
            "diff --git a/app.py b/app.py\n--- a/app.py\n+++ b/app.py\n"
            "@@ -0,0 +1,1 @@\n+def collect(items=[]):\n"
        )
        report = json.loads(render_json(analyze_diff(diff, repo="owner/repo", pr=2)))
        self.assertEqual(set(report), set(schema["required"]))
        self.assertEqual(report["schema_version"], schema["properties"]["schema_version"]["const"])
        self.assertIn(report["assessment"], schema["properties"]["assessment"]["enum"])
        metadata_schema = schema["properties"]["metadata"]
        self.assertEqual(set(report["metadata"]), set(metadata_schema["required"]))
        for key, prop in metadata_schema["properties"].items():
            value = report["metadata"][key]
            if "const" in prop:
                self.assertEqual(value, prop["const"])
            elif isinstance(prop["type"], list):
                valid = (isinstance(value, int) and not isinstance(value, bool)) or value is None
                self.assertTrue(valid)
            elif prop["type"] == "integer":
                self.assertIsInstance(value, int)
                self.assertNotIsInstance(value, bool)
            else:
                self.assertIsInstance(value, {"string": str, "boolean": bool}[prop["type"]])
        finding_schema = schema["properties"]["findings"]["items"]
        self.assertTrue(report["findings"])
        for finding in report["findings"]:
            self.assertEqual(set(finding), set(finding_schema["required"]))
            self.assertIn(finding["severity"], finding_schema["properties"]["severity"]["enum"])
            self.assertIn(finding["confidence"], finding_schema["properties"]["confidence"]["enum"])
            self.assertIsInstance(finding["line"], int)

    def test_rule_catalog_distinguishes_implemented_rules(self):
        catalog = json.loads((ROOT / "assets/severity-rubric.json").read_text(encoding="utf-8"))
        declared = {item["id"] for item in catalog["patterns"] if item["implemented_by_cli"]}
        self.assertEqual(declared, set(_RULES))
        self.assertTrue(all(item["implemented_by_cli"] is False for item in catalog["patterns"] if item["id"] not in _RULES))


if __name__ == "__main__":
    unittest.main()
