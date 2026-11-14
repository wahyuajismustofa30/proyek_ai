#!/usr/bin/env python3
"""Run only the checks configured or discoverable for one project."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "vendor", "dist", "build", "__pycache__"}


def report(level: str, message: str) -> None:
    print(f"{level}: {message}")
    if level == "NOTICE":
        print(f"::notice::{message}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as stream:
            stream.write(f"- **{level}** — {message}\n")


def run(command: list[str], cwd: Path) -> None:
    print("+ " + " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, check=True)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Invalid {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object.")
    return value


def node(project: Path) -> None:
    manifest = load_json(project / "package.json")
    scripts = manifest.get("scripts", {})
    if not isinstance(scripts, dict):
        raise ValueError("package.json scripts must be a JSON object.")
    selected = [name for name in ("lint", "test", "build") if scripts.get(name)]
    if not selected:
        report("NOTICE", f"{project}: no npm lint, test, or build script is configured; application checks skipped.")
        return
    if (project / "package-lock.json").is_file():
        run(["npm", "ci", "--no-audit", "--no-fund"], project)
    else:
        report("NOTICE", f"{project}: package-lock.json is absent; npm install is not reproducible.")
        run(["npm", "install", "--no-package-lock", "--no-audit", "--no-fund"], project)
    for name in selected:
        run(["npm", "run", name], project)
        report("PASS", f"{project}: npm {name} completed.")
    if "test" not in selected:
        report("NOTICE", f"{project}: no npm test script is configured; automated application tests were not run.")


def python_project(project: Path) -> None:
    pyproject = project / "pyproject.toml"
    if pyproject.is_file():
        try:
            tomllib.loads(pyproject.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
            raise ValueError(f"Invalid pyproject.toml: {exc}") from exc
    test_files = []
    for root, dirs, files in os.walk(project):
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        test_files.extend(
            Path(root) / name
            for name in files
            if (name.startswith("test_") and name.endswith(".py")) or name.endswith("_test.py")
        )
    if not test_files:
        report("NOTICE", f"{project}: no Python test files found; application tests were not run.")
        return
    for requirements in ("requirements.txt", "requirements-test.txt", "requirements-dev.txt"):
        path = project / requirements
        if path.is_file():
            run([sys.executable, "-m", "pip", "install", "-r", requirements], project)
    if pyproject.is_file():
        config = tomllib.loads(pyproject.read_text(encoding="utf-8"))
        if "build-system" in config:
            run([sys.executable, "-m", "pip", "install", "-e", "."], project)
    run([sys.executable, "-m", "pip", "install", "pytest==8.4.2"], project)
    run([sys.executable, "-m", "pytest", "-q"], project)
    report("PASS", f"{project}: Python tests completed.")


def php_project(project: Path) -> None:
    manifest = load_json(project / "composer.json")
    scripts = manifest.get("scripts", {})
    if not isinstance(scripts, dict):
        raise ValueError("composer.json scripts must be a JSON object.")
    validate_command = ["composer", "validate", "--no-check-publish"]
    if not (project / "composer.lock").is_file():
        validate_command.append("--no-check-lock")
    run(validate_command, project)
    report("PASS", f"{project}: Composer manifest validation completed.")
    if scripts.get("test"):
        if (project / "composer.lock").is_file():
            run(["composer", "install", "--no-interaction", "--prefer-dist"], project)
        else:
            report("NOTICE", f"{project}: composer.lock is absent; dependency resolution may not be reproducible.")
            run(["composer", "install", "--no-interaction", "--prefer-dist"], project)
        run(["composer", "run-script", "test", "--no-interaction"], project)
        report("PASS", f"{project}: Composer test script completed.")
    else:
        report("NOTICE", f"{project}: no Composer test script is configured; application tests were not run.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stack", choices=("node", "python", "php"))
    parser.add_argument("project", type=Path)
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir():
        print(f"Project directory does not exist: {project}", file=sys.stderr)
        return 2
    try:
        {"node": node, "python": python_project, "php": php_project}[args.stack](project)
    except (ValueError, subprocess.CalledProcessError, OSError) as exc:
        print(f"FAIL: {project}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
