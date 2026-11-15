"""Tests for the curated project-index generator."""
from __future__ import annotations
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from update_project_index import check_project_index, load_catalog, render_project_index, write_project_index  # noqa: E402


class UpdateProjectIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects/category/nested-app").mkdir(parents=True)
        (self.root / "projects/toolbox").mkdir()
        (self.root / "docs").mkdir()
        self.catalog = {
            "schema_version": 1,
            "projects": [{"name": "Nested App", "path": "projects/category/nested-app", "category": "Integration", "description": "A nested application."}],
            "tooling": [{"name": "Toolbox", "path": "projects/toolbox", "description": "Developer utilities."}],
            "categories": [{"name": "Category", "path": "projects/category", "description": "A grouping folder."}]
        }
        self.catalog_path = self.root / "docs/project-catalog.json"
        self.save_catalog()

    def save_catalog(self):
        self.catalog_path.write_text(json.dumps(self.catalog), encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_nested_project_and_separate_tooling_and_category(self):
        rendered = render_project_index(self.root)
        self.assertIn("projects/category/nested-app/", rendered)
        self.assertIn("Toolbox", rendered)
        self.assertIn("Kategori dan wadah", rendered)
        self.assertNotIn("| Category | Integration |", rendered)

    def test_optional_readme_and_index_check(self):
        project = self.root / "projects/category/nested-app"
        (project / "README.md").write_text("# Nested App", encoding="utf-8")
        write_project_index(self.root)
        self.assertTrue(check_project_index(self.root))
        self.catalog["projects"][0]["description"] = "Updated description."
        self.save_catalog()
        self.assertFalse(check_project_index(self.root))
        write_project_index(self.root)
        self.assertTrue(check_project_index(self.root))

    def test_rejects_traversal_and_missing_directory(self):
        self.catalog["projects"][0]["path"] = "projects/../../outside"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "Unsafe catalog path"):
            load_catalog(self.root)
        self.catalog["projects"][0]["path"] = "projects/not-there"
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "missing or is a symlink"):
            load_catalog(self.root)

    def test_rejects_duplicate_paths(self):
        self.catalog["tooling"][0]["path"] = self.catalog["projects"][0]["path"]
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, "Duplicate catalog path"):
            load_catalog(self.root)


if __name__ == "__main__":
    unittest.main()
