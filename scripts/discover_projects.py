#!/usr/bin/env python3
"""Discover first-level monorepo projects and their supported CI stacks."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


STACK_MANIFESTS = {
    "node": ("package.json",),
    "python": ("pyproject.toml", "requirements.txt"),
    "php": ("composer.json",),
    "static": ("index.html",),
}
PROJECT_SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

GENERATED_DIRECTORIES = {
    "node_modules", "vendor", ".venv", "venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", ".tox", ".nox", ".cache", "htmlcov",
}
GENERATED_ROOT_DIRECTORIES = {"dist", "build", "coverage", "artifacts"}
GENERATED_FILE_NAMES = {".coverage", ".DS_Store", "Thumbs.db", "npm-debug.log", "yarn-error.log"}
GENERATED_FILE_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".temp"}


def validate_project_contents(project_dir: Path) -> None:
    """Reject common dependency, cache, build, and temporary artifacts."""
    for path in project_dir.rglob("*"):
        relative = path.relative_to(project_dir)
        if path.is_dir():
            if path.name in GENERATED_DIRECTORIES or (
                len(relative.parts) == 1 and path.name in GENERATED_ROOT_DIRECTORIES
            ):
                raise ValueError(
                    f"Generated/dependency directory is not allowed in project "
                    f"{project_dir.name!r}: {relative.as_posix()}. "
                    "Use external temporary storage or keep generated output untracked."
                )
        elif path.is_file():
            if path.name in GENERATED_FILE_NAMES or path.suffix.lower() in GENERATED_FILE_SUFFIXES:
                raise ValueError(
                    f"Generated/temporary file is not allowed in project "
                    f"{project_dir.name!r}: {relative.as_posix()}."
                )


def validate_project_directory_name(name: str) -> None:
    """Reject names that could be hidden, ambiguous, or bypass project discovery."""
    if name.startswith("."):
        raise ValueError(
            f"Hidden directories are not allowed directly inside projects/: {name!r}. "
            "Hidden configuration directories are allowed inside a project folder."
        )
    if not PROJECT_SLUG_RE.fullmatch(name):
        raise ValueError(
            f"Invalid project directory name {name!r}: use lowercase ASCII letters "
            "and digits separated by single hyphens (for example, 'my-project')."
        )


def discover_projects(repository_root: Path) -> dict[str, list[dict[str, str]]]:
    """Discover only visible, valid first-level project directories under projects/.

    Only README.md is permitted as a file at the projects root. Hidden directories
    at that level are rejected to prevent silently hiding a project from CI. Nested
    directories (including hidden tool/configuration directories) belong to their
    parent project and are not independently discovered.
    """
    projects_root = repository_root / "projects"
    entries: list[dict[str, str]] = []

    if projects_root.is_dir():
        for project_dir in sorted(projects_root.iterdir(), key=lambda item: item.name):
            if project_dir.is_symlink():
                raise ValueError(
                    f"Symlink entries are not allowed in projects/: {project_dir.name!r}"
                )
            if not project_dir.is_dir():
                if project_dir.name != "README.md":
                    raise ValueError(
                        f"Only README.md may be stored directly in projects/: {project_dir.name!r}"
                    )
                continue

            validate_project_directory_name(project_dir.name)
            validate_project_contents(project_dir)
            project_path = project_dir.relative_to(repository_root).as_posix()
            detected = [
                stack
                for stack, manifests in STACK_MANIFESTS.items()
                if any((project_dir / manifest).is_file() for manifest in manifests)
            ]

            if not detected:
                entries.append(
                    {"project": project_path, "slug": project_dir.name, "stack": "none"}
                )
            else:
                for stack in detected:
                    entries.append(
                        {"project": project_path, "slug": project_dir.name, "stack": stack}
                    )

    # GitHub Actions cannot expand an empty matrix; this sentinel keeps the job valid.
    if not entries:
        entries.append(
            {"project": "projects", "slug": "__no_projects__", "stack": "none"}
        )

    return {"include": entries}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Discover project folders and supported CI stacks."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Monorepo root (defaults to the parent of scripts/).",
    )
    parser.add_argument(
        "--github-output",
        type=Path,
        help="Append the matrix output to a GitHub Actions output file.",
    )
    args = parser.parse_args()

    try:
        matrix = discover_projects(args.root.resolve())
    except ValueError as error:
        print(f"Project discovery failed: {error}", file=sys.stderr)
        return 2

    payload = json.dumps(matrix, ensure_ascii=False, separators=(",", ":"))

    if args.github_output:
        output_path = args.github_output.expanduser().resolve()
        projects_root = (args.root.resolve() / "projects").resolve()
        if output_path == projects_root or projects_root in output_path.parents:
            print(
                "Project discovery output must not be written inside projects/.",
                file=sys.stderr,
            )
            return 2
        with output_path.open("a", encoding="utf-8") as output:
            output.write(f"matrix={payload}\n")
        count = len(
            {item["slug"] for item in matrix["include"] if item["slug"] != "__no_projects__"}
        )
        print(f"Discovered {count} project(s).")
    else:
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
