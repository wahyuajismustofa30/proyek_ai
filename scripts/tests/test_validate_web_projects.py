"""Tests for project HTML/CSS and asset validation."""

from __future__ import annotations

import tempfile
import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_web_projects import validate_project


class WebValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_valid_html_css_and_local_asset(self) -> None:
        (self.project / "index.html").write_text(
            '<!doctype html><html><head><link rel="stylesheet" href="css/site.css"></head>'
            '<body><img src="assets/logo.svg" alt="Logo"></body></html>',
            encoding="utf-8",
        )
        (self.project / "css").mkdir()
        (self.project / "css" / "site.css").write_text(
            'body { background-image: url("../assets/bg.png"); }', encoding="utf-8"
        )
        (self.project / "assets").mkdir()
        (self.project / "assets" / "logo.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding="utf-8"
        )
        (self.project / "assets" / "bg.png").write_bytes(b"image")
        self.assertEqual(validate_project(self.project), [])

    def test_resolves_root_relative_html_and_css_assets(self) -> None:
        (self.project / "assets").mkdir()
        (self.project / "assets" / "logo.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding="utf-8"
        )
        (self.project / "assets" / "bg.png").write_bytes(b"image")
        (self.project / "index.html").write_text(
            '<!doctype html><html><body><img src="/assets/logo.svg"></body></html>',
            encoding="utf-8",
        )
        (self.project / "css").mkdir()
        (self.project / "css" / "site.css").write_text(
            'body { background: url("/assets/bg.png"); }', encoding="utf-8"
        )
        self.assertEqual(validate_project(self.project), [])

    def test_detects_malformed_declarations_inside_media_and_font_face(self) -> None:
        (self.project / "site.css").write_text(
            "@media screen { .card { color red; } } "
            "@font-face { font-family: Example; src url('font.woff2'); }",
            encoding="utf-8",
        )
        errors = validate_project(self.project)
        self.assertGreaterEqual(sum("CSS syntax error" in error for error in errors), 2)

    def test_parses_srcset_with_data_url_commas(self) -> None:
        (self.project / "assets").mkdir()
        (self.project / "assets" / "image-2x.png").write_bytes(b"image")
        (self.project / "index.html").write_text(
            '<!doctype html><html><body><img srcset="data:image/png;base64,AAAA 1x, '
            'assets/image-2x.png 2x"></body></html>',
            encoding="utf-8",
        )
        self.assertEqual(validate_project(self.project), [])

    def test_reports_missing_srcset_candidate_after_data_url(self) -> None:
        (self.project / "index.html").write_text(
            '<!doctype html><html><body><img srcset="data:image/png;base64,AAAA 1x, '
            'missing-2x.png 2x"></body></html>',
            encoding="utf-8",
        )
        self.assertTrue(any("missing-2x.png" in error for error in validate_project(self.project)))

    def test_reports_missing_html_asset(self) -> None:
        (self.project / "index.html").write_text(
            '<!doctype html><html><body><img src="missing.png" alt="Missing"></body></html>',
            encoding="utf-8",
        )
        self.assertTrue(any("missing local asset" in e for e in validate_project(self.project)))

    def test_reports_missing_css_asset(self) -> None:
        (self.project / "site.css").write_text(
            "body { background: url('missing.png'); }", encoding="utf-8"
        )
        self.assertTrue(any("missing local CSS asset" in e for e in validate_project(self.project)))

    def test_rejects_asset_reference_outside_project(self) -> None:
        (self.project / "index.html").write_text(
            '<!doctype html><html><body><img src="../../outside.png"></body></html>',
            encoding="utf-8",
        )
        self.assertTrue(any("escapes project directory" in e for e in validate_project(self.project)))

    def test_reports_invalid_svg_and_empty_assets(self) -> None:
        (self.project / "broken.svg").write_text("<svg>", encoding="utf-8")
        (self.project / "empty.png").write_bytes(b"")
        errors = validate_project(self.project)
        self.assertTrue(any("invalid SVG/XML asset" in e for e in errors))
        self.assertTrue(any("empty project asset" in e for e in errors))

    def test_reports_malformed_html_and_unclosed_css_block(self) -> None:
        (self.project / "index.html").write_text("<html><p>unclosed", encoding="utf-8")
        (self.project / "site.css").write_text("a { color: red", encoding="utf-8")
        errors = validate_project(self.project)
        self.assertTrue(any("invalid HTML" in e for e in errors))
        self.assertTrue(any("CSS syntax error" in e and "unclosed delimiter" in e for e in errors))

    def test_reports_malformed_css_declaration(self) -> None:
        (self.project / "site.css").write_text("a { color red; }", encoding="utf-8")
        errors = validate_project(self.project)
        self.assertTrue(any("CSS syntax error" in e for e in errors))

    def test_ignores_delimiters_inside_css_strings_and_comments(self) -> None:
        (self.project / "site.css").write_text(
            'a::before { content: "}"; /* } ] ) */ color: red; }',
            encoding="utf-8",
        )
        self.assertEqual(validate_project(self.project), [])


if __name__ == "__main__":
    unittest.main()
