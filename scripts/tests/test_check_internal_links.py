"""Unit tests for the Markdown link validator."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_internal_links as validator  # noqa: E402


class MarkdownParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.md"
        self.target = self.root / "target.md"
        self.source.write_text("", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_extracts_inline_reference_and_image_links(self) -> None:
        self.source.write_text(
            "[inline](target.md)\n"
            "[reference][guide]\n"
            "![image](images/logo.png)\n"
            "[guide]: target.md 'Guide'\n",
            encoding="utf-8",
        )
        self.assertEqual(
            validator.markdown_destinations(self.source),
            ["target.md", "target.md", "images/logo.png"],
        )

    def test_ignores_links_inside_fenced_and_inline_code(self) -> None:
        self.source.write_text(
            "`[inline](missing.md)`\n"
            "```md\n[block](missing.md)\n```\n"
            "[real](target.md)\n",
            encoding="utf-8",
        )
        self.assertEqual(validator.markdown_destinations(self.source), ["target.md"])

    def test_parses_parentheses_and_percent_encoded_paths(self) -> None:
        self.source.write_text("[file](folder/a%20b%28c%29.md)\n", encoding="utf-8")
        self.assertEqual(
            validator.markdown_destinations(self.source),
            ["folder/a b(c).md"],
        )

    def test_heading_anchors_handle_duplicates_and_html_ids(self) -> None:
        self.target.write_text(
            "# Getting Started\n"
            "## Getting Started\n"
            "## API & Usage\n"
            '<a id="custom-anchor"></a>\n',
            encoding="utf-8",
        )
        anchors = validator.markdown_anchors(self.target)
        self.assertTrue({"getting-started", "getting-started-1", "api--usage", "custom-anchor"} <= anchors)

    def test_rejects_paths_that_escape_repository(self) -> None:
        outside = self.root.parent / "outside.md"
        with patch.object(validator, "ROOT", self.root):
            target, _, error = validator.resolve_target(self.source, "../outside.md")
        self.assertEqual(target, outside.resolve())
        self.assertEqual(error, "target escapes the repository")

    def test_resolves_directory_readme(self) -> None:
        folder = self.root / "guide"
        folder.mkdir()
        readme = folder / "README.md"
        readme.write_text("# Guide\n", encoding="utf-8")
        with patch.object(validator, "ROOT", self.root):
            target, fragment, error = validator.resolve_target(self.source, "guide/#guide")
        self.assertEqual(target, readme.resolve())
        self.assertEqual(fragment, "guide")
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()
