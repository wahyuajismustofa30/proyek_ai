"""End-to-end tests for the project bootstrap workflow."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from discover_projects import discover_projects  # noqa: E402
from validate_web_projects import validate_project  # noqa: E402


class BootstrapEndToEndTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.output = self.root / "projects"

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_cli_bootstrap_produces_a_discoverable_valid_project(self) -> None:
        name = "DEKEKU Bootstrap E2E"
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "bootstrap_project.py"),
                "--name",
                name,
                "--output",
                str(self.output),
            ],
            cwd=REPOSITORY_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Proyek berhasil dibuat:", completed.stdout)

        project = self.output / "dekeku-bootstrap-e2e"
        self.assertTrue(project.is_dir())

        required_files = (
            "AGENTS.md",
            "README.md",
            "SECURITY.md",
            ".env.example",
            ".project-meta.json",
            "docs/PROJECT_BRIEF.md",
            "docs/ARCHITECTURE.md",
            "docs/TASKS.md",
            "docs/DECISIONS.md",
            "docs/CHANGELOG.md",
            "docs/TESTING.md",
            "src/README.md",
            "tests/README.md",
            "assets/README.md",
        )
        for relative in required_files:
            with self.subTest(path=relative):
                self.assertTrue((project / relative).is_file(), relative)

        metadata = json.loads(
            (project / ".project-meta.json").read_text(encoding="utf-8")
        )
        self.assertEqual(metadata["project_name"], name)
        self.assertEqual(metadata["project_slug"], "dekeku-bootstrap-e2e")
        self.assertEqual(metadata["ci"]["orchestrator"], "repository-root")
        self.assertFalse((project / ".github" / "workflows").exists())
        self.assertFalse((project / ".github" / "dependabot.yml").exists())

        discovered = discover_projects(self.root)["include"]
        self.assertEqual(
            discovered,
            [
                {
                    "project": "projects/dekeku-bootstrap-e2e",
                    "slug": "dekeku-bootstrap-e2e",
                    "stack": "none",
                }
            ],
        )

        # Exercise the same web validator used by project-matrix.yml against
        # a small, self-contained application fixture inside the generated project.
        (project / "index.html").write_text(
            '<!doctype html><html lang="id"><head>'
            '<link rel="stylesheet" href="assets/site.css">'
            '</head><body><img src="assets/logo.svg" alt="Logo"></body></html>',
            encoding="utf-8",
        )
        (project / "assets" / "site.css").write_text(
            'body { background-image: url("background.png"); }',
            encoding="utf-8",
        )
        (project / "assets" / "logo.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
            encoding="utf-8",
        )
        (project / "assets" / "background.png").write_bytes(b"test-image")

        self.assertEqual(validate_project(project), [])

        # A broken local reference must fail, proving the integration check
        # is not merely accepting every generated directory.
        (project / "index.html").write_text(
            '<!doctype html><html><body><img src="assets/missing.png" '
            'alt="Missing"></body></html>',
            encoding="utf-8",
        )
        errors = validate_project(project)
        self.assertTrue(
            any("missing local asset" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
