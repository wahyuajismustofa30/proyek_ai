"""Tests for the AI project bootstrap utility."""

from __future__ import annotations

import sys
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
