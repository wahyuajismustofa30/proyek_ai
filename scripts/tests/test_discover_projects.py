"""Tests for flexible project discovery and CI stack detection."""
from __future__ import annotations
import json, subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from discover_projects import discover_projects  # noqa: E402

class DiscoverProjectsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "projects").mkdir()
    def tearDown(self):
        self.temp.cleanup()
    def make_project(self, name, *manifests):
        project = self.root / "projects" / name
        project.mkdir(parents=True)
        for manifest in manifests:
            path = project / manifest
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{}", encoding="utf-8")
        return project
    def test_discovers_multiple_known_stacks(self):
        self.make_project("web-api", "package.json", "pyproject.toml", "composer.json")
        self.assertEqual(discover_projects(self.root)["include"], [
            {"project":"projects/web-api","slug":"web-api","stack":"node"},
            {"project":"projects/web-api","slug":"web-api","stack":"python"},
            {"project":"projects/web-api","slug":"web-api","stack":"php"},
        ])
    def test_discovers_independent_projects(self):
        self.make_project("alpha-node","package.json")
        self.make_project("beta-python","pyproject.toml")
        result = subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/"discover_projects.py"),"--root",str(self.root)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["include"]),2)
    def test_discovers_static_and_hybrid_projects(self):
        self.make_project("static-site","index.html")
        self.make_project("hybrid-site","index.html","package.json")
        self.assertEqual(discover_projects(self.root)["include"],[
            {"project":"projects/hybrid-site","slug":"hybrid-site","stack":"node"},
            {"project":"projects/hybrid-site","slug":"hybrid-site","stack":"static"},
            {"project":"projects/static-site","slug":"static-site","stack":"static"},
        ])
    def test_unknown_project_needs_no_readme_manifest_or_fixed_layout(self):
        project=self.make_project("custom-tool")
        (project/"source"/"nested").mkdir(parents=True)
        (project/"source"/"nested"/"main.go").write_text("package main\n",encoding="utf-8")
        (project/".config").mkdir()
        (project/".config"/"settings.toml").write_text("enabled = true\n",encoding="utf-8")
        (project/"dist").mkdir()
        (project/"dist"/"bundle.js").write_text("built output\n",encoding="utf-8")
        self.assertEqual(discover_projects(self.root)["include"],[
            {"project":"projects/custom-tool","slug":"custom-tool","stack":"none"}
        ])
    def test_allows_hidden_configuration_inside_project(self):
        project=self.make_project("web-app","package.json")
        hidden=project/".github"/"workflows"
        hidden.mkdir(parents=True)
        (hidden/"ci.yml").write_text("name: local-ci\n",encoding="utf-8")
        self.assertEqual(discover_projects(self.root)["include"],[
            {"project":"projects/web-app","slug":"web-app","stack":"node"}
        ])
    def test_only_readme_may_be_file_at_projects_root(self):
        (self.root/"projects"/"README.md").write_text("# Projects\n",encoding="utf-8")
        self.assertEqual(discover_projects(self.root)["include"],[
            {"project":"projects","slug":"__no_projects__","stack":"none"}
        ])
        (self.root/"projects"/"notes.txt").write_text("not a project",encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"Only README.md"):
            discover_projects(self.root)
    def test_rejects_hidden_or_invalid_project_names(self):
        for name in (".internal","MyProject","my project","my_project","project..backup","équipe"):
            with self.subTest(name=name):
                self.make_project(name)
                with self.assertRaisesRegex(ValueError,"Hidden directories|Invalid project directory"):
                    discover_projects(self.root)
                (self.root/"projects"/name).rmdir()
    def test_rejects_symlink_entries(self):
        target=self.root/"target"
        target.mkdir()
        link=self.root/"projects"/"linked-project"
        try:
            link.symlink_to(target,target_is_directory=True)
        except OSError:
            self.skipTest("Symlink creation is not supported")
        with self.assertRaisesRegex(ValueError,"Symlink entries are not allowed"):
            discover_projects(self.root)
    def test_empty_projects_uses_sentinel(self):
        self.assertEqual(discover_projects(self.root)["include"],[
            {"project":"projects","slug":"__no_projects__","stack":"none"}
        ])
    def test_github_output_must_not_be_inside_projects(self):
        output=self.root/"projects"/"matrix.txt"
        result=subprocess.run([sys.executable,str(Path(__file__).resolve().parents[1]/"discover_projects.py"),"--root",str(self.root),"--github-output",str(output)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn("must not be written inside projects",result.stderr)
        self.assertFalse(output.exists())

if __name__ == "__main__":
    unittest.main()
