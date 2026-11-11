"""Tests for the direct-to-main Termux GitHub sync helper."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "github-sync-termux.sh"


class TermuxGitHubSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.remote = self.root / "remote.git"
        self.repo = self.root / "working"
        self.upstream = self.root / "upstream"
        self.env = os.environ.copy()
        self.env.update({
            "GIT_AUTHOR_NAME": "CI Test",
            "GIT_AUTHOR_EMAIL": "ci-test@example.invalid",
            "GIT_COMMITTER_NAME": "CI Test",
            "GIT_COMMITTER_EMAIL": "ci-test@example.invalid",
            "GIT_TERMINAL_PROMPT": "0",
        })
        self.git(None, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(None, "init", "--initial-branch=main", str(self.repo))
        self.git(self.repo, "config", "user.name", "CI Test")
        self.git(self.repo, "config", "user.email", "ci-test@example.invalid")
        (self.repo / "README.md").write_text("baseline\n", encoding="utf-8")
        (self.repo / "scripts").mkdir()
        (self.repo / "scripts" / "update_project_index.py").write_text(
            (ROOT / "scripts" / "update_project_index.py").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "PROJECT_INDEX.md").write_text(
            "# Indeks Proyek\n\n| Proyek | Direktori | README |\n|---|---|---|\n| — | — | — |\n",
            encoding="utf-8",
        )
        self.git(self.repo, "add", ".")
        self.git(self.repo, "commit", "-m", "baseline")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.git(self.repo, "push", "-u", "origin", "main")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, cwd: Path | None, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args], cwd=cwd, env=self.env, check=True,
            capture_output=True, text=True,
        )

    def advance_remote_main(self, filename: str = "upstream.txt") -> None:
        self.git(None, "clone", str(self.remote), str(self.upstream))
        self.git(self.upstream, "config", "user.name", "CI Test")
        self.git(self.upstream, "config", "user.email", "ci-test@example.invalid")
        (self.upstream / filename).write_text("upstream change\n", encoding="utf-8")
        self.git(self.upstream, "add", filename)
        self.git(self.upstream, "commit", "-m", "advance main")
        self.git(self.upstream, "push", "origin", "main")

    def run_sync(self, answers: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT)], cwd=self.repo, env=self.env, input=answers,
            capture_output=True, text=True, check=False,
        )

    def test_main_stays_main_and_does_not_create_feature_branch(self) -> None:
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.git(self.repo, "branch", "--show-current").stdout.strip(), "main")
        self.assertIn("Tidak ada commit baru", result.stdout)
        branches = self.git(None, "--git-dir", str(self.remote), "branch", "--list").stdout
        self.assertNotIn("feat/", branches)

    def test_commit_and_push_happen_directly_on_main(self) -> None:
        (self.repo / "change.txt").write_text("direct change\n", encoding="utf-8")
        result = self.run_sync("y\ny\nDirect commit\ny\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Push langsung ke origin/main berhasil", result.stdout)
        self.assertEqual(self.git(self.repo, "branch", "--show-current").stdout.strip(), "main")
        local = self.git(self.repo, "rev-parse", "HEAD").stdout.strip()
        remote = self.git(None, "--git-dir", str(self.remote), "rev-parse", "refs/heads/main").stdout.strip()
        self.assertEqual(local, remote)

    def test_existing_staging_excludes_unstaged_and_untracked_changes(self) -> None:
        staged = self.repo / "staged.txt"
        unstaged = self.repo / "unstaged.txt"
        untracked = self.repo / "untracked.txt"
        staged.write_text("staged change\n", encoding="utf-8")
        self.git(self.repo, "add", "staged.txt")
        unstaged.write_text("unstaged change\n", encoding="utf-8")
        untracked.write_text("untracked change\n", encoding="utf-8")

        result = self.run_sync("y\nStaged-only commit\ny\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Perubahan unstaged/untracked akan tetap di luar commit ini", result.stdout)
        committed = self.git(self.repo, "show", "--pretty=format:", "--name-only", "HEAD").stdout.splitlines()
        self.assertEqual(committed, ["staged.txt"])
        self.assertTrue(unstaged.exists())
        self.assertTrue(untracked.exists())
        self.assertEqual(self.git(self.repo, "status", "--short").stdout.splitlines(), ["?? unstaged.txt", "?? untracked.txt"])

    def test_non_main_branch_is_rejected_without_switching(self) -> None:
        self.git(self.repo, "switch", "-c", "work")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Pindah ke main secara manual", result.stderr)
        self.assertEqual(self.git(self.repo, "branch", "--show-current").stdout.strip(), "work")

    def test_staged_user_changes_are_not_discarded_when_commit_declined(self) -> None:
        note = self.repo / "note.txt"
        note.write_text("keep staged\n", encoding="utf-8")
        self.git(self.repo, "add", "note.txt")
        result = self.run_sync("n\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("staging tetap dipertahankan", result.stdout)
        self.assertIn("note.txt", self.git(self.repo, "diff", "--cached", "--name-only").stdout)

    def test_dirty_main_is_not_fast_forwarded_when_remote_is_ahead(self) -> None:
        (self.repo / "local.txt").write_text("local work\n", encoding="utf-8")
        self.advance_remote_main()
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("working tree memiliki perubahan", result.stderr)
        self.assertTrue((self.repo / "local.txt").exists())

    def test_clean_main_fast_forwards_before_sync(self) -> None:
        self.advance_remote_main()
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("diperbarui dengan fast-forward", result.stdout)
        self.assertEqual(
            self.git(self.repo, "rev-parse", "HEAD").stdout.strip(),
            self.git(self.repo, "rev-parse", "origin/main").stdout.strip(),
        )

    def test_untracked_dotenv_is_rejected_without_staging(self) -> None:
        secret = self.repo / ".env.local"
        secret.write_text("TOKEN=do-not-commit\n", encoding="utf-8")
        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("berpotensi rahasia", result.stderr)
        self.assertEqual(self.git(self.repo, "diff", "--cached", "--name-only").stdout, "")
        self.assertTrue(secret.exists())


if __name__ == "__main__":
    unittest.main()
