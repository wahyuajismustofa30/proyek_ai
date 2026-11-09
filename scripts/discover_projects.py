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

    Hidden files at the projects root are ignored. Hidden directories at that
    level are rejected to prevent silently hiding a project from CI. Nested
    directories (including hidden tool/configuration directories) belong to
    their parent project and are not independently discovered.
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
                continue

            validate_project_directory_name(project_dir.name)
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
        with args.github_output.open("a", encoding="utf-8") as output:
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
