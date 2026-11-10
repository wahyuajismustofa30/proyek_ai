"""Regression tests for adaptive project checks."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run_project_checks as checks  # noqa: E402


class AdaptiveProjectChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write_json(self, name, value):
        (self.project / name).write_text(json.dumps(value), encoding="utf-8")

    def test_node_without_scripts_is_notice_not_failure(self):
        self.write_json("package.json", {"name": "plain-site"})
        with patch.object(checks, "run") as run, patch.object(checks, "report") as report:
            checks.node(self.project)
        run.assert_not_called()
        report.assert_called_once()
        self.assertEqual(report.call_args.args[0], "NOTICE")

    def test_node_runs_available_scripts_without_requiring_test(self):
        self.write_json("package.json", {"scripts": {"lint": "eslint .", "build": "vite build"}})
        (self.project / "package-lock.json").write_text("{}", encoding="utf-8")
        with patch.object(checks, "run") as run, patch.object(checks, "report") as report:
            checks.node(self.project)
        self.assertEqual(run.call_args_list[0].args[0][:2], ["npm", "ci"])
        self.assertEqual(run.call_args_list[1].args[0], ["npm", "run", "lint"])
        self.assertEqual(run.call_args_list[2].args[0], ["npm", "run", "build"])
        self.assertTrue(any(call.args[0] == "NOTICE" for call in report.call_args_list))

    def test_invalid_node_manifest_fails(self):
        (self.project / "package.json").write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid package.json"):
            checks.node(self.project)

    def test_python_without_tests_is_notice(self):
        (self.project / "pyproject.toml").write_text("[project]\nname='sample'\n", encoding="utf-8")
        with patch.object(checks, "run") as run, patch.object(checks, "report") as report:
            checks.python_project(self.project)
        run.assert_not_called()
        self.assertEqual(report.call_args.args[0], "NOTICE")

    def test_python_runs_when_test_file_exists(self):
        tests = self.project / "tests"
        tests.mkdir()
        (tests / "test_sample.py").write_text("def test_ok(): pass\n", encoding="utf-8")
        with patch.object(checks, "run") as run, patch.object(checks, "report"):
            checks.python_project(self.project)
        self.assertTrue(any(call.args[0][-2:] == ["pytest", "-q"] for call in run.call_args_list))

    def test_invalid_pyproject_fails(self):
        (self.project / "pyproject.toml").write_text("[project\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid pyproject.toml"):
            checks.python_project(self.project)

    def test_php_without_test_script_is_notice(self):
        self.write_json("composer.json", {"name": "sample/package"})
        with patch.object(checks, "run") as run, patch.object(checks, "report") as report:
            checks.php_project(self.project)
        self.assertEqual(run.call_args.args[0][:2], ["composer", "validate"])
        self.assertEqual(report.call_args.args[0], "NOTICE")

    def test_php_runs_configured_test_script(self):
        self.write_json("composer.json", {"scripts": {"test": "phpunit"}})
        (self.project / "composer.lock").write_text("{}", encoding="utf-8")
        with patch.object(checks, "run") as run, patch.object(checks, "report"):
            checks.php_project(self.project)
        self.assertTrue(any(call.args[0][:2] == ["composer", "run-script"] for call in run.call_args_list))

    def test_invalid_composer_manifest_fails(self):
        (self.project / "composer.json").write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Invalid composer.json"):
            checks.php_project(self.project)


if __name__ == "__main__":
    unittest.main()
