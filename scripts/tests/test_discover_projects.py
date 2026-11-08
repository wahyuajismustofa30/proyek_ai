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

    def test_ignores_nested_and_hidden_directories(self) -> None:
        project = self.make_project("outer")
        (project / "nested").mkdir()
        (project / "nested" / "package.json").write_text("{}", encoding="utf-8")
        self.make_project(".internal", "package.json")
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects/outer", "slug": "outer", "stack": "none"}],
        )

    def test_returns_a_sentinel_for_an_empty_projects_directory(self) -> None:
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects", "slug": "__no_projects__", "stack": "none"}],
        )


if __name__ == "__main__":
    unittest.main()
