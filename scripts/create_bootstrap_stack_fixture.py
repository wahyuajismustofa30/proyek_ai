"""Create a real bootstrap-generated fixture for each supported application stack."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = REPOSITORY_ROOT / "scripts" / "bootstrap_project.py"

FIXTURES: dict[str, dict[str, str]] = {
    "node": {
        "name": "Bootstrap Node.js E2E",
        "files": {
            "package.json": json.dumps(
                {
                    "name": "bootstrap-nodejs-e2e",
                    "version": "0.1.0",
                    "private": True,
                    "type": "module",
                    "scripts": {"test": "node --test"},
                },
                indent=2,
            ) + "\n",
            "src/math.js": "export function add(a, b) { return a + b; }\n",
            "test/math.test.js": (
                'import test from "node:test";\n'
                'import assert from "node:assert/strict";\n'
                'import { add } from "../src/math.js";\n\n'
                'test("adds two numbers", () => { assert.equal(add(2, 3), 5); });\n'
            ),
        },
    },
    "python": {
        "name": "Bootstrap Python E2E",
        "files": {
            "pyproject.toml": (
                "[build-system]\n"
                'requires = ["setuptools>=68"]\n'
                'build-backend = "setuptools.build_meta"\n\n'
                "[project]\n"
                'name = "bootstrap-python-e2e"\n'
                'version = "0.1.0"\n'
                'requires-python = ">=3.10"\n\n'
                "[tool.setuptools.packages.find]\n"
                'where = ["src"]\n\n'
                "[tool.pytest.ini_options]\n"
                'testpaths = ["tests"]\n'
            ),
            "requirements-test.txt": "pytest==8.4.2\n",
            "src/bootstrap_python_e2e/__init__.py": (
                "def add(a: int, b: int) -> int:\n"
                "    return a + b\n"
            ),
            "tests/test_app.py": (
                "from bootstrap_python_e2e import add\n\n"
                "def test_adds_two_numbers() -> None:\n"
                "    assert add(2, 3) == 5\n"
            ),
        },
    },
    "php": {
        "name": "Bootstrap PHP E2E",
        "files": {
            "composer.json": json.dumps(
                {
                    "name": "bootstrap/php-e2e",
                    "description": "Temporary PHP bootstrap end-to-end fixture",
                    "type": "project",
                    "license": "MIT",
                    "require": {},
                    "scripts": {"test": "php tests/run.php"},
                },
                indent=2,
            ) + "\n",
            "tests/run.php": (
                "<?php\n"
                "declare(strict_types=1);\n\n"
                "function add(int $a, int $b): int { return $a + $b; }\n"
                "if (add(2, 3) !== 5) {\n"
                '    fwrite(STDERR, "Addition test failed\\n");\n'
                "    exit(1);\n"
                "}\n"
                'echo "PHP bootstrap test passed\\n";\n'
            ),
        },
    },
}


def create_fixture(stack: str, output_root: Path) -> Path:
    """Run the actual bootstrap CLI, then add a minimal runnable app for stack."""
    fixture = FIXTURES[stack]
    completed = subprocess.run(
        [
            sys.executable,
            str(BOOTSTRAP),
            "--name",
            fixture["name"],
            "--output",
            str(output_root),
        ],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr or completed.stdout)

    slug = project_slug(fixture["name"])
    project = output_root.resolve() / slug
    for relative, content in fixture["files"].items():
        target = project / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return project


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack", choices=sorted(FIXTURES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    project = create_fixture(args.stack, args.output)
    print(f"BOOTSTRAP_PROJECT={project}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
