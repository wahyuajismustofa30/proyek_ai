"""Tests for monorepo project and stack discovery."""

from __future__ import annotations

import json
import subprocess
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

    def test_builds_matrix_for_multiple_projects_with_different_stacks(self) -> None:
        """Each independent project folder must produce its own matrix entry."""
        self.make_project("alpha-node", "package.json")
        self.make_project("beta-python", "pyproject.toml")
        self.make_project("gamma-php", "composer.json")

        completed = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve().parents[1] / "discover_projects.py"),
                "--root",
                str(self.root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        matrix = json.loads(completed.stdout)
        self.assertEqual(
            matrix["include"],
            [
                {"project": "projects/alpha-node", "slug": "alpha-node", "stack": "node"},
                {"project": "projects/beta-python", "slug": "beta-python", "stack": "python"},
                {"project": "projects/gamma-php", "slug": "gamma-php", "stack": "php"},
            ],
        )
        self.assertEqual(
            len({item["project"] for item in matrix["include"]}),
            3,
            "The matrix must contain three distinct project directories, not one multi-stack project.",
        )

    def test_reports_project_without_supported_manifest(self) -> None:
        self.make_project("design-system", "README.md")
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects/design-system", "slug": "design-system", "stack": "none"}],
        )

    def test_rejects_hidden_project_directory_with_actionable_message(self) -> None:
        self.make_project(".internal", "package.json")
        with self.assertRaisesRegex(ValueError, "Hidden directories are not allowed directly"):
            discover_projects(self.root)

    def test_allows_hidden_configuration_directories_inside_a_project(self) -> None:
        project = self.make_project("web-app", "package.json")
        hidden_config = project / ".github" / "workflows"
        hidden_config.mkdir(parents=True)
        (hidden_config / "ci.yml").write_text("name: local-template\\n", encoding="utf-8")
        (project / ".gitignore").write_text("node_modules/\\n", encoding="utf-8")

        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects/web-app", "slug": "web-app", "stack": "node"}],
        )

    def test_ignores_root_files_but_rejects_hidden_root_directories(self) -> None:
        (self.root / "projects" / ".gitkeep").write_text("", encoding="utf-8")
        (self.root / "projects" / "notes.txt").write_text("not a project", encoding="utf-8")
        self.assertEqual(
            discover_projects(self.root)["include"],
            [{"project": "projects", "slug": "__no_projects__", "stack": "none"}],
        )

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
