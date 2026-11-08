"""Tests for required AI project template guidance."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import bootstrap_project  # noqa: E402


class TemplateGuidanceTests(unittest.TestCase):
    def test_guidelines_are_linked_and_copied_by_bootstrap(self) -> None:
        template = REPOSITORY_ROOT / "templates" / "ai-project"
        guidelines = template / "docs" / "AI_GUIDELINES.md"
        self.assertTrue(guidelines.is_file())

        expected_link = "[docs/AI_GUIDELINES.md](docs/AI_GUIDELINES.md)"
        for filename in ("README.md", "AGENTS.md"):
            with self.subTest(filename=filename):
                self.assertIn(
                    expected_link,
                    (template / filename).read_text(encoding="utf-8"),
                )

        with tempfile.TemporaryDirectory() as temporary:
            destination = bootstrap_project.bootstrap_project(
                "Guidance Copy Test", Path(temporary), template
            )
            copied = destination / "docs" / "AI_GUIDELINES.md"
            self.assertTrue(copied.is_file())
            self.assertEqual(
                copied.read_text(encoding="utf-8"),
                guidelines.read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
