"""Tests for static website CI smoke validation."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_static_site import check_static_site  # noqa: E402


class CheckStaticSiteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_serves_root_index_html_over_http(self) -> None:
        (self.project / "index.html").write_text(
            "<!doctype html><html><title>Static fixture</title></html>",
            encoding="utf-8",
        )
        check_static_site(self.project)


    def test_serves_alternate_root_entrypoint_over_http(self) -> None:
        (self.project / "home.html").write_text(
            "<!doctype html><html><title>Alternate</title></html>",
            encoding="utf-8",
        )
        check_static_site(self.project, "home.html")

    def test_rejects_entrypoint_path_traversal(self) -> None:
        with self.assertRaisesRegex(ValueError, "must stay inside"):
            check_static_site(self.project, "../outside.html")

    def test_rejects_project_without_root_index_html(self) -> None:
        with self.assertRaisesRegex(ValueError, "entrypoint is missing or is not a regular file"):
            check_static_site(self.project)

    def test_rejects_index_html_directory(self) -> None:
        (self.project / "index.html").mkdir()
        with self.assertRaisesRegex(ValueError, "entrypoint is missing or is not a regular file"):
            check_static_site(self.project)


if __name__ == "__main__":
    unittest.main()
