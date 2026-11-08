#!/usr/bin/env python3
"""Discover first-level monorepo projects and their supported CI stacks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


STACK_MANIFESTS = {
    "node": ("package.json",),
    "python": ("pyproject.toml", "requirements.txt"),
    "php": ("composer.json",),
}


def discover_projects(repository_root: Path) -> dict[str, list[dict[str, str]]]:
    """Return a GitHub Actions matrix with one entry per project and stack."""
    projects_root = repository_root / "projects"
    entries: list[dict[str, str]] = []

    if projects_root.is_dir():
        for project_dir in sorted(projects_root.iterdir(), key=lambda item: item.name):
            if (
                not project_dir.is_dir()
                or project_dir.is_symlink()
                or project_dir.name.startswith(".")
            ):
                continue

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

    matrix = discover_projects(args.root.resolve())
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
