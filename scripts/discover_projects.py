#!/usr/bin/env python3
"""Discover first-level monorepo projects without prescribing internal layout."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

STACK_MANIFESTS = {
    "node": ("package.json",),
    "python": ("pyproject.toml", "requirements.txt"),
    "php": ("composer.json",),
}
PROJECT_SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")

def validate_project_directory_name(name: str) -> None:
    if name.startswith("."):
        raise ValueError(f"Hidden directories are not allowed directly inside projects/: {name!r}.")
    if not PROJECT_SLUG_RE.fullmatch(name):
        raise ValueError(f"Invalid project directory name {name!r}: use lowercase ASCII letters, digits, and single hyphens.")

def discover_projects(repository_root: Path) -> dict[str, list[dict[str, str]]]:
    """Discover first-level project folders; internal files and directories are unrestricted."""
    projects_root = repository_root / "projects"
    entries: list[dict[str, str]] = []
    if projects_root.is_dir():
        for project_dir in sorted(projects_root.iterdir(), key=lambda item: item.name):
            if project_dir.is_symlink():
                raise ValueError(f"Symlink entries are not allowed in projects/: {project_dir.name!r}")
            if not project_dir.is_dir():
                if project_dir.name != "README.md":
                    raise ValueError(f"Only README.md may be stored directly in projects/: {project_dir.name!r}")
                continue
            validate_project_directory_name(project_dir.name)
            project_path = project_dir.relative_to(repository_root).as_posix()
            detected = [
                stack for stack, manifests in STACK_MANIFESTS.items()
                if any((project_dir / manifest).is_file() for manifest in manifests)
            ]
            if not detected:
                entries.append({"project": project_path, "slug": project_dir.name, "stack": "none"})
            else:
                entries.extend({"project": project_path, "slug": project_dir.name, "stack": stack} for stack in detected)
            html_entries = sorted(
                item.name for item in project_dir.iterdir()
                if item.is_file() and not item.is_symlink() and item.suffix.lower() in {".html", ".htm"}
            )
            if html_entries:
                entrypoint = "index.html" if "index.html" in html_entries else html_entries[0]
                entries.append({
                    "project": project_path,
                    "slug": project_dir.name,
                    "stack": "static",
                    "entrypoint": entrypoint,
                })
    if not entries:
        entries.append({"project": "projects", "slug": "__no_projects__", "stack": "none"})
    return {"include": entries}

def main() -> int:
    parser = argparse.ArgumentParser(description="Discover project folders and supported CI stacks.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--github-output", type=Path)
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
            print("Project discovery output must not be written inside projects/.", file=sys.stderr)
            return 2
        with output_path.open("a", encoding="utf-8") as output:
            output.write(f"matrix={payload}\n")
        count = len({item["slug"] for item in matrix["include"] if item["slug"] != "__no_projects__"})
        print(f"Discovered {count} project(s).")
    else:
        print(payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
