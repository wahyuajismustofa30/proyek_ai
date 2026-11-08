"""Tests for monorepo project and stack discovery."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discover_projects import discover_projects  # noqa: E402


class DiscoverProjectsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def make_project(self, name: str, *manifests: str) -> Path:
        project = self.root / "projects" / name
        project.mkdir(parents=True)
        for manifest in manifests:
            (project / manifest).write_text("{}", encoding="utf-8")
        return project

    def test_discovers_each_supported_stack_in_a_multi_stack_project(self) -> None:
        self.make_project("web-api", "package.json", "pyproject.toml", "composer.json")
        self.assertEqual(
            discover_projects(self.root)["include"],
            [
                {"project": "projects/web-api", "slug": "web-api", "stack": "node"},
                {"project": "projects/web-api", "slug": "web-api", "stack": "python"},
                {"project": "projects/web-api", "slug": "web-api", "stack": "php"},
            ],
        )

    def test_reports_project_without_supported_manifest(self) -> None:
        self.make_project("design-system", "README.md")
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects/design-system", "slug": "design-system", "stack": "none"}],
        )

    def test_rejects_hidden_project_directory_instead_of_silently_ignoring_it(self) -> None:
        self.make_project(".internal", "package.json")
        with self.assertRaisesRegex(ValueError, "Invalid project directory name"):
            discover_projects(self.root)

    def test_rejects_uppercase_spaces_and_special_characters(self) -> None:
        for name in ("MyProject", "my project", "my_project", "project..backup", "équipe"):
            with self.subTest(name=name):
                self.make_project(name)
                with self.assertRaisesRegex(ValueError, "Invalid project directory name"):
                    discover_projects(self.root)
                (self.root / "projects" / name).rmdir()

    def test_rejects_symlink_entries(self) -> None:
        target = self.root / "real-project"
        target.mkdir()
        link = self.root / "projects" / "linked-project"
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is not supported in this environment")
        with self.assertRaisesRegex(ValueError, "Symlink entries are not allowed"):
            discover_projects(self.root)

    def test_returns_a_sentinel_for_an_empty_projects_directory(self) -> None:
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects", "slug": "__no_projects__", "stack": "none"}],
        )


if __name__ == "__main__":
    unittest.main()
