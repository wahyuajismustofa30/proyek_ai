#!/usr/bin/env python3
"""Validate relative Markdown links and heading anchors inside this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+['\"].*?['\"])?\s*\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(" + chr(96) + r"{3,}|~~~+)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
INLINE_CODE_RE = re.compile(chr(96) + r"+[^" + chr(96) + r"]*" + chr(96) + r"+") 


def slugify(heading: str) -> str:
    heading = HTML_TAG_RE.sub("", heading)
    heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = heading.strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s", "-", heading)


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    fence_char = ""

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return anchors

    for line in lines:
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if not in_fence:
                in_fence = True
                fence_char = marker[0]
            elif marker[0] == fence_char:
                in_fence = False
            continue
        if in_fence:
            continue

        match = HEADING_RE.match(line)
        if not match:
            continue
        base = slugify(match.group(2))
        if not base:
            continue
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f"{base}-{count}")

    return anchors


def strip_code(line: str) -> str:
    return INLINE_CODE_RE.sub("", line)


def resolve_target(source: Path, raw_target: str) -> tuple[Path | None, str]:
    target = unquote(raw_target.strip("<>"))
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or target.startswith("//"):
        return None, ""

    fragment = unquote(parsed.fragment)
    raw_path = unquote(parsed.path)

    if not raw_path:
        return source, fragment
    if raw_path.startswith("/"):
        candidate = ROOT / raw_path.lstrip("/")
    else:
        candidate = source.parent / raw_path

    candidate = candidate.resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return candidate, fragment

    if candidate.is_dir():
        for index_name in ("README.md", "index.md"):
            index = candidate / index_name
            if index.is_file():
                return index, fragment
        return candidate, fragment

    return candidate, fragment


def main() -> int:
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md")
        if ".git" not in path.parts and "node_modules" not in path.parts
    )
    errors: list[str] = []
    checked = 0

    for source in markdown_files:
        try:
            lines = source.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            errors.append(f"{source.relative_to(ROOT)}: file is not valid UTF-8")
            continue

        in_fence = False
        fence_char = ""
        for line_number, line in enumerate(lines, start=1):
            fence = FENCE_RE.match(line)
            if fence:
                marker = fence.group(1)
                if not in_fence:
                    in_fence = True
                    fence_char = marker[0]
                elif marker[0] == fence_char:
                    in_fence = False
                continue
            if in_fence:
                continue

            for match in LINK_RE.finditer(strip_code(line)):
                raw_target = match.group(1)
                target, fragment = resolve_target(source, raw_target)
                if target is None:
                    continue
                checked += 1

                if not target.exists():
                    errors.append(
                        f"{source.relative_to(ROOT)}:{line_number}: "
                        f"missing internal target '{raw_target}'"
                    )
                    continue

                if fragment and target.is_file() and target.suffix.lower() == ".md":
                    anchors = markdown_anchors(target)
                    if fragment not in anchors:
                        errors.append(
                            f"{source.relative_to(ROOT)}:{line_number}: "
                            f"anchor '#{fragment}' not found in "
                            f"{target.relative_to(ROOT)}"
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
