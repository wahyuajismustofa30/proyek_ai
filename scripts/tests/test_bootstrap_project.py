"""Tests for the AI project bootstrap utility."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bootstrap_project as bootstrap  # noqa: E402


class BootstrapProjectTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.template = self.root / "template"
        self.template.mkdir()
        (self.template / "README.md").write_text(
            "# [NAMA PROYEK]\nSlug: {{PROJECT_SLUG}}\n", encoding="utf-8"
        )
        (self.template / "docs").mkdir()
        (self.template / "docs" / "PROJECT_BRIEF.md").write_text(
            "Project: {{PROJECT_NAME}}\n", encoding="utf-8"
        )
        self.output = self.root / "projects"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_slug_normalizes_name(self) -> None:
        self.assertEqual(bootstrap.project_slug("DEKEKU Website Baru"), "dekeku-website-baru")

    def test_copies_template_and_replaces_placeholders(self) -> None:
        result = bootstrap.bootstrap_project(
            "DEKEKU Website", self.output, self.template
        )
        self.assertEqual(result.name, "dekeku-website")
        self.assertEqual(
            (result / "README.md").read_text(encoding="utf-8"),
            "# DEKEKU Website\nSlug: dekeku-website\n",
        )
        self.assertEqual(
            (result / "docs" / "PROJECT_BRIEF.md").read_text(encoding="utf-8"),
            "Project: DEKEKU Website\n",
        )

    def test_json_metadata_escapes_quotes_backslashes_and_unicode(self) -> None:
        (self.template / ".project-meta.json").write_text(
            '{"project_name": "{{PROJECT_NAME}}"}\n', encoding="utf-8"
        )
        name = 'Foo "Bar" \\ Baz café 東京'
        result = bootstrap.bootstrap_project(name, self.output, self.template)
        metadata = json.loads(
            (result / ".project-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["project_name"], name)

    def test_cli_bootstrap_escapes_json_metadata(self) -> None:
        name = 'Uji "Kutip" \\ Backslash café 東京'
        output = self.root / "cli-output"
        result = subprocess.run(
            [
                sys.executable,
                str(Path(bootstrap.__file__).resolve()),
                "--name",
                name,
                "--output",
                str(output),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        metadata_path = (
            output / bootstrap.project_slug(name) / ".project-meta.json"
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        self.assertEqual(metadata["project_name"], name)

    def test_refuses_to_overwrite_existing_directory(self) -> None:
        destination = self.output / "my-project"
        destination.mkdir(parents=True)
        marker = destination / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            bootstrap.bootstrap_project("My Project", self.output, self.template)
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_rejects_empty_or_invalid_names(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap.project_slug("../")
        with self.assertRaises(ValueError):
            bootstrap.bootstrap_project("  ", self.output, self.template)

    def test_dry_run_does_not_create_output(self) -> None:
        result = bootstrap.bootstrap_project(
            "Preview Project", self.output, self.template, dry_run=True
        )
        self.assertEqual(result.name, "preview-project")
        self.assertFalse(self.output.exists())

    def test_real_template_contains_monorepo_metadata_and_no_nested_ci(self) -> None:
        result = bootstrap.bootstrap_project(
            "DEKEKU Landing Page", self.output, bootstrap.DEFAULT_TEMPLATE
        )
        metadata = json.loads(
            (result / ".project-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["project_name"], "DEKEKU Landing Page")
        self.assertEqual(metadata["project_slug"], "dekeku-landing-page")
        self.assertEqual(metadata["ci"]["orchestrator"], "repository-root")
        self.assertFalse((result / ".github" / "workflows" / "ci.yml").exists())
        self.assertFalse((result / ".github" / "dependabot.yml").exists())


    def test_cli_rejects_control_characters_and_long_names_without_creating_output(self) -> None:
        invalid_names = ("Baris\nDua", "A\tB", "X" * 300)
        for index, name in enumerate(invalid_names):
            with self.subTest(name=repr(name)):
                output = self.root / f"rejected-{index}"
                result = subprocess.run(
                    [
                        sys.executable,
                        str(Path(bootstrap.__file__).resolve()),
                        "--name",
                        name,
                        "--output",
                        str(output),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 1)
                self.assertFalse(output.exists())
                self.assertIn("ERROR: ", result.stderr)
                self.assertLess(len(result.stderr), 100)
                self.assertNotIn(str(output), result.stderr)

    def test_rejects_slug_longer_than_63_characters(self) -> None:
        with self.assertRaisesRegex(ValueError, "Slug proyek maksimal 63 karakter"):
            bootstrap.project_slug("A" * 64)


    def test_rolls_back_partial_destination_when_template_copy_fails(self) -> None:
        destination = self.output / "interrupted-copy"

        def fail_after_partial_copy(source: Path, target: Path, **kwargs: object) -> None:
            target = Path(target)
            target.mkdir(parents=True)
            (target / "partial.txt").write_text("partial", encoding="utf-8")
            raise OSError("simulated copy failure")

        with patch.object(bootstrap.shutil, "copytree", side_effect=fail_after_partial_copy):
            with self.assertRaisesRegex(OSError, "simulated copy failure"):
                bootstrap.bootstrap_project("Interrupted Copy", self.output, self.template)

        self.assertFalse(destination.exists(), "A failed bootstrap must not leave a partial project.")



if __name__ == "__main__":
    unittest.main()
