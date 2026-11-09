"""Safety tests for the repository-wide Termux GitHub sync helper."""

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
        self.env = os.environ.copy()
        self.env.update(
            {
                "GIT_AUTHOR_NAME": "CI Test",
                "GIT_AUTHOR_EMAIL": "ci-test@example.invalid",
                "GIT_COMMITTER_NAME": "CI Test",
                "GIT_COMMITTER_EMAIL": "ci-test@example.invalid",
                "GIT_TERMINAL_PROMPT": "0",
            }
        )
        self.git(None, "init", "--bare", "--initial-branch=main", str(self.remote))
        self.git(None, "init", "--initial-branch=main", str(self.repo))
        self.git(self.repo, "config", "user.name", "CI Test")
        self.git(self.repo, "config", "user.email", "ci-test@example.invalid")
        (self.repo / "README.md").write_text("baseline\n", encoding="utf-8")
        self.git(self.repo, "add", "README.md")
        self.git(self.repo, "commit", "-m", "baseline")
        self.git(self.repo, "remote", "add", "origin", str(self.remote))
        self.git(self.repo, "push", "-u", "origin", "main")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, cwd: Path | None, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=self.env,
            check=True,
            capture_output=True,
            text=True,
        )

    def run_sync(self, answers: str = "") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT)],
            cwd=self.repo,
            env=self.env,
            input=answers,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_shell_syntax_is_valid(self) -> None:
        result = subprocess.run(
            ["bash", "-n", str(SCRIPT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_main_creates_feature_branch_and_never_pushes_main(self) -> None:
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        branch = self.git(self.repo, "branch", "--show-current").stdout.strip()
        self.assertRegex(branch, r"^feat/termux-sync-\d{8}-\d{6}$")
        remote_main = self.git(
            None, "--git-dir", str(self.remote), "rev-parse", "refs/heads/main"
        ).stdout.strip()
        local_head = self.git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.assertEqual(remote_main, local_head)
        self.assertIn("Tidak ada commit baru", result.stdout)

    def test_existing_staging_is_preserved_and_operation_aborts(self) -> None:
        note = self.repo / "note.txt"
        note.write_text("already staged\n", encoding="utf-8")
        self.git(self.repo, "add", "note.txt")
        before = self.git(self.repo, "diff", "--cached", "--name-only").stdout

        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("perubahan yang sudah di-stage", result.stderr)
        after = self.git(self.repo, "diff", "--cached", "--name-only").stdout
        self.assertEqual(after, before)
        self.assertEqual(
            self.git(self.repo, "branch", "--show-current").stdout.strip(), "main"
        )


if __name__ == "__main__":
    unittest.main()
