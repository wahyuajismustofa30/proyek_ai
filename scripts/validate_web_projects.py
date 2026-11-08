#!/usr/bin/env python3
"""Validate HTML, CSS syntax, and local asset references in monorepo projects."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

import html5lib
import tinycss2

HTML_EXTENSIONS = {".html", ".htm"}
CSS_EXTENSIONS = {".css"}
ASSET_ATTRIBUTES = {"src", "href", "poster", "data"}
URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
SRCSET_RE = re.compile(r"(?<![\w-])srcset\s*=\s*(['\"])(.*?)\1", re.IGNORECASE)


def local_target(raw: str, source: Path, project: Path) -> Path | None:
    """Resolve a local URL while rejecting paths that escape the project."""
    value = raw.strip()
    if not value or value.startswith("#") or value.startswith("data:"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    candidate = (source.parent / path).resolve()
    root = project.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError(f"reference escapes project directory: {raw}")
    return candidate


def validate_project(project: Path) -> list[str]:
    errors: list[str] = []
    if not project.is_dir():
        return [f"{project}: project directory does not exist"]

    files = sorted(p for p in project.rglob("*") if p.is_file() and not p.is_symlink())
    html_files = [p for p in files if p.suffix.lower() in HTML_EXTENSIONS]
    css_files = [p for p in files if p.suffix.lower() in CSS_EXTENSIONS]

    for file in files:
        if file.name == ".gitkeep":
            continue
        if file.stat().st_size == 0:
            errors.append(f"{file}: empty project asset or source file")
        if file.suffix.lower() == ".svg":
            try:
                ET.parse(file)
            except (ET.ParseError, OSError) as exc:
                errors.append(f"{file}: invalid SVG/XML asset: {exc}")

    for file in html_files:
        try:
            document = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{file}: HTML is not valid UTF-8")
            continue
        try:
            html5lib.HTMLParser(strict=True).parse(document)
        except (html5lib.html5parser.ParseError, ValueError) as exc:
            errors.append(f"{file}: invalid HTML: {exc}")

        for match in SRCSET_RE.finditer(document):
            for candidate in match.group(2).split(","):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                try:
                    target = local_target(url, file, project)
                    if target is not None and not target.is_file():
                        errors.append(f"{file}: missing asset referenced by srcset: {url}")
                except ValueError as exc:
                    errors.append(f"{file}: {exc}")

        # Parse attributes via the HTML parser, not a broad regex.
        from html5lib import HTMLParser
        parser = HTMLParser(strict=False)
        tree = parser.parse(document)
        for element in tree.iter():
            for attribute, value in element.attrib.items():
                if attribute.rsplit("}", 1)[-1].lower() not in ASSET_ATTRIBUTES:
                    continue
                try:
                    target = local_target(value, file, project)
                    if target is not None and not target.is_file():
                        errors.append(f"{file}: missing local asset: {value}")
                except ValueError as exc:
                    errors.append(f"{file}: {exc}")

    for file in css_files:
        try:
            stylesheet = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{file}: CSS is not valid UTF-8")
            continue
        rules = tinycss2.parse_stylesheet(stylesheet, skip_comments=True, skip_whitespace=True)
        for rule in rules:
            if rule.type == "error":
                errors.append(f"{file}: CSS syntax error: {rule.message}")
        for match in URL_RE.finditer(stylesheet):
            raw_url = match.group(2).strip()
            try:
                target = local_target(raw_url, file, project)
                if target is not None and not target.is_file():
                    errors.append(f"{file}: missing local CSS asset: {raw_url}")
            except ValueError as exc:
                errors.append(f"{file}: {exc}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", nargs="*", type=Path, help="Project directories to validate")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    root = args.root.resolve()
    projects = [p.resolve() for p in args.projects] if args.projects else sorted(
        p.resolve() for p in (root / "projects").glob("*") if p.is_dir() and not p.is_symlink()
    )
    all_errors: list[str] = []
    checked = 0
    for project in projects:
        try:
            project.relative_to(root / "projects")
        except ValueError:
            print(f"Refusing to validate path outside projects/: {project}", file=sys.stderr)
            return 2
        checked += 1
        all_errors.extend(validate_project(project))

    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        print(f"Web validation failed: {len(all_errors)} issue(s) across {checked} project(s).")
        return 1
    print(f"Web validation passed for {checked} project(s) (HTML, CSS, and local asset references).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
