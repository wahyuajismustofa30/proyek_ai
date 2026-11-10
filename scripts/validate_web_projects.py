#!/usr/bin/env python3
"""Validate HTML, CSS syntax, and local asset references in monorepo projects."""

from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

import html5lib
import tinycss2

HTML_EXTENSIONS = {".html", ".htm"}
HTML_FRAGMENT_FILENAMES = {"head-snippet.html"}
CSS_EXTENSIONS = {".css"}
EMPTY_CHECK_EXTENSIONS = HTML_EXTENSIONS | CSS_EXTENSIONS | {".svg"}
ALLOWED_EMPTY_FILENAMES = {".gitkeep", "__init__.py", ".nojekyll"}
EXCLUDED_DIRECTORIES = {
    "node_modules",
    ".venv",
    "venv",
    ".git",
    "__pycache__",
}
ROOT_EXCLUDED_DIRECTORIES = {"vendor", "dist", "build"}
ASSET_ATTRIBUTES = {"src", "href", "poster", "data"}
SRCSET_RE = re.compile(r"(?<![\w-])srcset\s*=\s*(['\"])(.*?)\1", re.IGNORECASE)


def local_target(raw: str, source: Path, project: Path) -> Path | None:
    """Resolve local URLs relative to the source file or website root."""
    value = raw.strip()
    if not value or value.startswith("#") or value.lower().startswith("data:"):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    root = project.resolve()
    candidate = root / path.lstrip("/") if path.startswith("/") else source.parent / path
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        raise ValueError(f"reference escapes project directory: {raw}")
    return candidate


def parse_srcset(value: str) -> list[str]:
    """Parse srcset URLs without splitting commas embedded in data URLs."""
    urls: list[str] = []
    position = 0
    while position < len(value):
        while position < len(value) and (value[position].isspace() or value[position] == ","):
            position += 1
        if position >= len(value):
            break
        start = position
        while position < len(value) and not value[position].isspace():
            position += 1
        url = value[start:position]
        trailing = len(url) - len(url.rstrip(","))
        url = url.rstrip(",")
        if url:
            urls.append(url)
        if trailing:
            continue
        depth = 0
        while position < len(value):
            char = value[position]
            if char == "(":
                depth += 1
            elif char == ")" and depth:
                depth -= 1
            elif char == "," and depth == 0:
                position += 1
                break
            position += 1
    return urls


def css_delimiter_errors(source: str) -> list[str]:
    """Detect unbalanced CSS delimiters without counting those in strings/comments."""
    errors: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[tuple[str, int, int]] = []
    quote: str | None = None
    escaped = False
    comment = False
    line = 1
    column = 0
    index = 0

    while index < len(source):
        char = source[index]
        next_char = source[index + 1] if index + 1 < len(source) else ""

        if char == "\n":
            line += 1
            column = 0
        else:
            column += 1

        if comment:
            if char == "*" and next_char == "/":
                comment = False
                index += 1
                column += 1
        elif quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char == "/" and next_char == "*":
            comment = True
            index += 1
            column += 1
        elif char in {"'", '"'}:
            quote = char
        elif char == "\\":
            # CSS escapes can contain delimiter characters; skip the escaped char.
            if next_char:
                index += 1
                column += 1
        elif char in "([{":
            stack.append((char, line, column))
        elif char in ")]}":
            if not stack or stack[-1][0] != pairs[char]:
                errors.append(f"unmatched closing delimiter {char!r} at line {line}, column {column}")
            else:
                stack.pop()
        index += 1

    if quote:
        errors.append("unterminated string")
    if comment:
        errors.append("unterminated comment")
    for delimiter, start_line, start_column in stack:
        errors.append(
            f"unclosed delimiter {delimiter!r} opened at line {start_line}, column {start_column}"
        )
    return errors


def css_url_values(tokens):
    """Yield URL references from parsed CSS tokens, excluding comments and ordinary strings."""
    for token in tokens:
        token_type = getattr(token, "type", None)
        if token_type == "url":
            yield token.value
            continue
        if token_type == "function":
            if token.lower_name == "url":
                significant = [
                    item for item in token.arguments
                    if item.type not in {"whitespace", "comment"}
                ]
                if len(significant) == 1 and significant[0].type == "string":
                    yield significant[0].value
            yield from css_url_values(token.arguments)
            continue
        if token_type == "at-rule":
            if token.lower_at_keyword == "import":
                significant = [
                    item for item in token.prelude
                    if item.type not in {"whitespace", "comment"}
                ]
                if significant and significant[0].type == "string":
                    yield significant[0].value
            yield from css_url_values(token.prelude)
            if token.content is not None:
                yield from css_url_values(token.content)
            continue
        for attribute in ("content", "prelude", "arguments"):
            nested = getattr(token, attribute, None)
            if nested is not None:
                yield from css_url_values(nested)


def css_rule_errors(rules: list, file: Path) -> list[str]:
    """Validate declarations and recursively inspect nested CSS at-rules."""
    errors: list[str] = []
    block_rules = {"container", "document", "layer", "media", "scope", "supports"}
    declaration_rules = {"font-face", "page", "property", "counter-style"}
    for rule in rules:
        if rule.type == "error":
            errors.append(f"{file}: CSS syntax error: {rule.message}")
        elif rule.type == "qualified-rule":
            declarations = tinycss2.parse_declaration_list(
                rule.content, skip_comments=True, skip_whitespace=True
            )
            for item in declarations:
                if item.type == "error":
                    errors.append(f"{file}: CSS syntax error: {item.message}")
        elif rule.type == "at-rule" and rule.content is not None:
            keyword = rule.lower_at_keyword
            if keyword in block_rules or keyword.endswith("keyframes"):
                nested = tinycss2.parse_rule_list(
                    rule.content, skip_comments=True, skip_whitespace=True
                )
                errors.extend(css_rule_errors(nested, file))
            elif keyword in declaration_rules:
                declarations = tinycss2.parse_declaration_list(
                    rule.content, skip_comments=True, skip_whitespace=True
                )
                for item in declarations:
                    if item.type == "error":
                        errors.append(f"{file}: CSS syntax error: {item.message}")
    return errors


def validate_project(project: Path) -> list[str]:
    errors: list[str] = []
    if not project.is_dir():
        return [f"{project}: project directory does not exist"]

    files: list[Path] = []
    project_root = project.resolve()
    for current_root, directory_names, file_names in os.walk(project_root):
        current_path = Path(current_root)
        root_level = current_path == project_root
        directory_names[:] = sorted(
            name
            for name in directory_names
            if name not in EXCLUDED_DIRECTORIES
            and not (root_level and name in ROOT_EXCLUDED_DIRECTORIES)
            and not (current_path / name).is_symlink()
        )
        files.extend(
            current_path / name
            for name in file_names
            if not (current_path / name).is_symlink()
        )
    files.sort()
    html_files = [p for p in files if p.suffix.lower() in HTML_EXTENSIONS]
    css_files = [p for p in files if p.suffix.lower() in CSS_EXTENSIONS]

    for file in files:
        if file.name in ALLOWED_EMPTY_FILENAMES:
            continue
        if (
            file.suffix.lower() in EMPTY_CHECK_EXTENSIONS
            and file.stat().st_size == 0
        ):
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
        is_fragment = file.name in HTML_FRAGMENT_FILENAMES
        try:
            strict_parser = html5lib.HTMLParser(strict=True)
            if is_fragment:
                strict_parser.parseFragment(document, container="head")
            else:
                strict_parser.parse(document)
        except (html5lib.html5parser.ParseError, ValueError) as exc:
            errors.append(f"{file}: invalid HTML: {exc}")

        # Parse attributes via the HTML parser, not a broad regex.
        from html5lib import HTMLParser
        parser = HTMLParser(strict=False)
        tree = parser.parseFragment(document, container="head") if is_fragment else parser.parse(document)
        for element in tree.iter():
            for attribute, value in element.attrib.items():
                name = attribute.rsplit("}", 1)[-1].lower()
                candidates = parse_srcset(value) if name == "srcset" else ([value] if name in ASSET_ATTRIBUTES else [])
                for raw_url in candidates:
                    try:
                        target = local_target(raw_url, file, project)
                        if target is not None and not target.is_file():
                            errors.append(f"{file}: missing local asset: {raw_url}")
                    except ValueError as exc:
                        errors.append(f"{file}: {exc}")

    for file in css_files:
        try:
            stylesheet = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"{file}: CSS is not valid UTF-8")
            continue
        for message in css_delimiter_errors(stylesheet):
            errors.append(f"{file}: CSS syntax error: {message}")

        rules = tinycss2.parse_stylesheet(stylesheet, skip_comments=True, skip_whitespace=True)
        errors.extend(css_rule_errors(rules, file))
        for raw_url in css_url_values(rules):
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
