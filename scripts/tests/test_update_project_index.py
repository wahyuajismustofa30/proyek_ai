"""Tests for deterministic automatic project-index generation."""
from __future__ import annotations
import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from update_project_index import check_project_index, render_project_index, write_project_index  # noqa: E402

class UpdateProjectIndexTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        (self.root/"projects").mkdir()
        (self.root/"docs").mkdir()
    def tearDown(self):
        self.temp.cleanup()
    def test_generates_sorted_index_and_allows_missing_readme(self):
        (self.root/"projects"/"zeta-app").mkdir()
        alpha=self.root/"projects"/"alpha-site"
        alpha.mkdir()
        (alpha/"README.md").write_text("# Alpha\n",encoding="utf-8")
        rendered=render_project_index(self.root)
        self.assertLess(rendered.index("Alpha Site"),rendered.index("Zeta App"))
        self.assertIn("[README.md](../projects/alpha-site/README.md)",rendered)
        self.assertIn("| Zeta App |",rendered)
        self.assertNotIn("README.md](../projects/zeta-app/README.md)",rendered)
    def test_write_and_check_track_directory_changes(self):
        (self.root/"projects"/"first-project").mkdir()
        write_project_index(self.root)
        self.assertTrue(check_project_index(self.root))
        (self.root/"projects"/"second-project").mkdir()
        self.assertFalse(check_project_index(self.root))
        write_project_index(self.root)
        self.assertTrue(check_project_index(self.root))
        self.assertIn("Second Project",(self.root/"docs"/"PROJECT_INDEX.md").read_text(encoding="utf-8"))
    def test_rejects_invalid_names_and_symlinks(self):
        (self.root/"projects"/"Bad_Name").mkdir()
        with self.assertRaisesRegex(ValueError,"Invalid project directory name"):
            render_project_index(self.root)
        (self.root/"projects"/"Bad_Name").rmdir()
        target=self.root/"target"
        target.mkdir()
        link=self.root/"projects"/"linked-project"
        try:
            link.symlink_to(target,target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is not supported")
        with self.assertRaisesRegex(ValueError,"Symlink entries are not allowed"):
            render_project_index(self.root)

if __name__ == "__main__":
    unittest.main()
