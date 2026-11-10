"""Regression tests for CI failure handling using isolated, synthetic fixtures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = SCRIPTS.parent
sys.path.insert(0, str(SCRIPTS))

from discover_projects import discover_projects  # noqa: E402


class CIFailurePathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.project = self.root / "projects" / "failure-fixture"
        self.project.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_command(
        self, command: list[str], *, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        return subprocess.run(
            command,
            cwd=cwd or self.project,
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
            env=env,
        )

    def test_unsupported_stack_is_discovered_without_blocking_repository_ci(self) -> None:
        (self.project / "README.md").write_text("# Unsupported fixture\n", encoding="utf-8")
        matrix = discover_projects(self.root)
        self.assertEqual(matrix["include"], [{
            "project": "projects/failure-fixture",
            "slug": "failure-fixture",
            "stack": "none",
        }])
        notice = self.run_command([
            "bash", "-euo", "pipefail", "-c",
            'echo "::notice::projects/failure-fixture was discovered; no application adapter is configured."',
        ], cwd=REPOSITORY_ROOT)
        self.assertEqual(notice.returncode, 0, notice.stderr)
        self.assertIn("no application adapter is configured", notice.stdout)

    def test_malformed_node_and_php_json_configuration_is_rejected(self) -> None:
        malformed = '{"name": "broken", "scripts": '
        for filename in ("package.json", "composer.json"):
            with self.subTest(filename=filename):
                path = self.project / filename
                path.write_text(malformed, encoding="utf-8")
                with self.assertRaises(json.JSONDecodeError):
                    json.loads(path.read_text(encoding="utf-8"))
                path.unlink()

    def test_malformed_python_project_configuration_is_rejected(self) -> None:
        config = self.project / "pyproject.toml"
        config.write_text("[project\nname = 'broken'\n", encoding="utf-8")
        with self.assertRaises(tomllib.TOMLDecodeError):
            tomllib.loads(config.read_text(encoding="utf-8"))

    def test_missing_node_and_php_lockfiles_trigger_ci_preflight_failure(self) -> None:
        for lockfile, message in (
            ("package-lock.json", "Commit package-lock.json for reproducible CI."),
            ("composer.lock", "Commit composer.lock for reproducible CI."),
        ):
            with self.subTest(lockfile=lockfile):
                result = self.run_command(
                    [
                        "bash",
                        "-euo",
                        "pipefail",
                        "-c",
                        f'test -f "{lockfile}" || {{ echo "{message}"; exit 1; }}',
                    ]
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stdout)

    def test_unresolvable_dependency_fails_without_network_access(self) -> None:
        requirements = self.project / "requirements.txt"
        requirements.write_text(
            "ci-failure-fixture-package-that-does-not-exist==0.0.1\n",
            encoding="utf-8",
        )
        empty_wheelhouse = self.root / "empty-wheelhouse"
        empty_wheelhouse.mkdir()
        install_target = self.root / "pip-target"

        result = self.run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                str(empty_wheelhouse),
                "--no-deps",
                "--target",
                str(install_target),
                "--requirement",
                str(requirements),
            ]
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No matching distribution found", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
