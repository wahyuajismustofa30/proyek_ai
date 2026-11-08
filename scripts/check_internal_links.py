#!/usr/bin/env python3
"""Validate local Markdown links and heading fragments with a Markdown parser."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
PARSER = MarkdownIt("default", {"html": True})


def github_slugify(heading: str) -> str:
    """Create a GitHub-style heading slug from rendered heading text."""
    heading = re.sub("<[^>]+>", "", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w -]", "", heading, flags=re.UNICODE)
    return re.sub(" +" , "-", heading)


def read_markdown(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path}: file is not valid UTF-8") from exc


def markdown_anchors(path: Path) -> set[str]:
    """Collect explicit HTML IDs and GitHub-style Markdown heading anchors."""
    tokens = PARSER.parse(read_markdown(path))
    anchors: set[str] = set()
    counts: dict[str, int] = {}

    for index, token in enumerate(tokens):
        html_tokens = [token, *(token.children or [])]
        for html_token in html_tokens:
            if html_token.type in {"html_block", "html_inline"}:
                anchors.update(re.findall(r"""\bid\s*=\s*["']([^"']+)["']""", html_token.content, re.I))
                anchors.update(re.findall(r"""\bname\s*=\s*["']([^"']+)["']""", html_token.content, re.I))

        if token.type != "heading_open":
            continue
        inline = tokens[index + 1] if index + 1 < len(tokens) else None
        if inline is None or inline.type != "inline":
            heading = ""
        else:
            heading = "".join(
                child.content for child in (inline.children or [])
                if child.type in {"text", "code_inline"}
            )
        base = github_slugify(heading)
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")

    return anchors


def resolve_target(source: Path, raw_target: str) -> tuple[Path | None, str, str | None]:
    """Resolve a Markdown destination; external URLs are intentionally skipped."""
    parsed = urlsplit(raw_target.strip())
    if parsed.scheme or parsed.netloc or raw_target.startswith("//"):
        return None, "", None

    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)
    if not raw_path:
        candidate = source
    elif raw_path.startswith("/"):
        candidate = ROOT / raw_path.lstrip("/")
    else:
        candidate = source.parent / raw_path

    candidate = candidate.resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return candidate, fragment, "target escapes the repository"

    if candidate.is_dir():
        for index_name in ("README.md", "index.md"):
            index = candidate / index_name
            if index.is_file():
                return index, fragment, None
    return candidate, fragment, None


def markdown_destinations(path: Path) -> list[str]:
    """Extract parsed link and image destinations, excluding code examples."""
    tokens = PARSER.parse(read_markdown(path))
    destinations: list[str] = []

    def visit(token) -> None:
        if token.type == "link_open":
            href = token.attrGet("href")
            if href:
                destinations.append(href)
        elif token.type == "image":
            src = token.attrGet("src")
            if src:
                destinations.append(src)
        for child in token.children or []:
            visit(child)

    for token in tokens:
        visit(token)
    return destinations


def main() -> int:
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )
    errors: list[str] = []
    checked = 0

    for source in markdown_files:
        try:
            destinations = markdown_destinations(source)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        for raw_target in destinations:
            target, fragment, resolution_error = resolve_target(source, raw_target)
            if target is None:
                continue
            checked += 1

            if resolution_error:
                errors.append(
                    f"{source.relative_to(ROOT)}: link '{raw_target}' {resolution_error}"
                )
                continue

            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: missing internal target '{raw_target}'"
                )
                continue

            if fragment and target.is_file() and target.suffix.lower() == ".md":
                try:
                    anchors = markdown_anchors(target)
                except ValueError as exc:
                    errors.append(str(exc))
                    continue
                if fragment not in anchors:
                    errors.append(
                        f"{source.relative_to(ROOT)}: anchor '#{fragment}' "
                        f"not found in {target.relative_to(ROOT)}"
                    )

    if errors:
        print("Internal Markdown link validation failed:")
        for error in errors:
            print(f"  - {error}")
        print(f"\n{len(errors)} error(s); checked {checked} internal link(s).")
        return 1

    print(
        f"Internal Markdown links valid: {checked} link(s) "
        f"across {len(markdown_files)} Markdown file(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
