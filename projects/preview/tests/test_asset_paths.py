"""Validate local asset references used by the standalone Preview website."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IconMarkupParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data_icons = set()

    def handle_starttag(self, tag, attrs):
        value = dict(attrs).get("data-icon")
        if value:
            self.data_icons.add(value)


class LocalIconAssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.main = (ROOT / "js/main.js").read_text(encoding="utf-8")
        cls.data = (ROOT / "js/data.js").read_text(encoding="utf-8")
        cls.parser = IconMarkupParser()
        cls.parser.feed(cls.html)

    def test_monochrome_mask_url_resolves_from_stylesheet_directory(self):
        match = re.search(
            r"style=\"--icon:url\('([^']+)'\)\"",
            self.main,
        )
        self.assertIsNotNone(match, "Dynamic monochrome icon URL is missing")
        reference = match.group(1)
        self.assertNotIn("/css/assets/", reference)
        resolved = (ROOT / "css" / reference).resolve()
        self.assertTrue(
            resolved.is_relative_to(ROOT.resolve()),
            f"Icon URL escapes the Preview root: {reference}",
        )
        self.assertEqual(
            resolved.relative_to(ROOT.resolve()).as_posix(),
            "assets/icons/monochrome/${name}.svg",
        )

    def test_all_referenced_icon_files_exist(self):
        registry = re.search(
            r"const navigationIcons = new Set\(\[([^]]+)\\]\\)",
            self.main,
        )
        self.assertIsNotNone(registry, "Navigation icon registry was not found")
        monochrome_names = set(re.findall(r"'([a-z0-9-]+)'", registry.group(1)))

        data_names = set(re.findall(r"icon:\\s*'([a-z0-9-]+)'", self.data))
        for detail_icons in re.findall(r"detailIcons:\s*\[([^\]]+)\]", self.data):
            data_names.update(re.findall(r"'([a-z0-9-]+)'", detail_icons))
        data_names.update(re.findall(r"\['[^']+',\s*'([a-z0-9-]+)'\]", self.data))
        data_names.update(self.parser.data_icons)

        missing = []
        for name in sorted(data_names | monochrome_names):
            variant = "monochrome" if name in monochrome_names else "color"
            asset = ROOT / "assets/icons" / variant / f"{name}.svg"
            if not asset.is_file():
                missing.append(f"{variant}/{name}.svg")
        self.assertEqual(missing, [], f"Missing referenced SVG assets: {missing}")

    def test_color_icon_template_resolves_from_preview_root(self):
        match = re.search(r"src=\"assets/icons/color/\$\{name\}\.svg\"", self.main)
        self.assertIsNotNone(match, "Dynamic color icon asset template is missing")
        color_dir = ROOT / "assets/icons/color"
        self.assertTrue(color_dir.is_dir())
        self.assertGreater(
            len(list(color_dir.glob("*.svg"))),
            0,
            "Color icon directory contains no SVG assets",
        )

    def test_css_local_url_references_exist(self):
        for css_path in (ROOT / "css").glob("*.css"):
            css = css_path.read_text(encoding="utf-8")
            for reference in re.findall(r"url\((?:['\"])?([^'\")]+)", css):
                if reference.startswith(("data:", "http:", "https:", "#", "//")):
                    continue
                local_path = (css_path.parent / reference).resolve()
                self.assertTrue(
                    local_path.is_file(),
                    f"{css_path.relative_to(ROOT)} references missing asset {reference}",
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
