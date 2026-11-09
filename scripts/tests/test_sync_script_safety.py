"""Integration tests for the preview Git synchronization script."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = REPOSITORY_ROOT / "projects" / "preview" / "SYNC - 26.11.03.sh"


class SyncScriptSafetyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "working"
        self.remote = self.root / "remote.git"
        self.project = self.repo / "projects" / "preview"
        self.project.mkdir(parents=True)

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

        (self.project / "index.html").write_text("<!doctype html><title>Baseline</title>\n", encoding="utf-8")
        shutil.copy2(SYNC_SCRIPT, self.project / SYNC_SCRIPT.name)
        self.git(self.repo, "add", "-A")
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

    def run_sync(self, answers: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(self.project / SYNC_SCRIPT.name)],
            cwd=self.repo,
            env=self.env,
            input=answers,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_only_stages_preview_changes_and_requires_push_confirmation(self) -> None:
        syntax = subprocess.run(
            ["bash", "-n", str(self.project / SYNC_SCRIPT.name)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(syntax.returncode, 0, syntax.stderr)

        (self.project / "index.html").write_text("<!doctype html><title>Updated</title>\n", encoding="utf-8")
        unrelated = self.repo / "unrelated-local-notes.txt"
        unrelated.write_text("must remain untracked\n", encoding="utf-8")

        # Confirm commit, accept the default commit message, then confirm push.
        result = self.run_sync("y\n\ny\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Lanjutkan push ke 'origin/main'?", result.stderr)

        remote_files = self.git(
            None,
            "--git-dir",
            str(self.remote),
            "show",
            "--pretty=format:",
            "--name-only",
            "refs/heads/main",
        ).stdout.splitlines()
        self.assertEqual(remote_files, ["projects/preview/index.html"])
        self.assertTrue(unrelated.exists())
        self.assertEqual(
            self.git(self.repo, "status", "--porcelain").stdout.strip(),
            "?? unrelated-local-notes.txt",
        )

    def test_aborts_when_unrelated_file_is_already_staged(self) -> None:
        unrelated = self.repo / "unrelated-staged.txt"
        unrelated.write_text("must not be committed\n", encoding="utf-8")
        self.git(self.repo, "add", "unrelated-staged.txt")
        previous_head = self.git(self.repo, "rev-parse", "HEAD").stdout.strip()

        result = self.run_sync("")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Ada perubahan staged di luar 'projects/preview'", result.stderr)
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD").stdout.strip(), previous_head)
        self.assertEqual(
            self.git(self.repo, "diff", "--cached", "--name-only").stdout.splitlines(),
            ["unrelated-staged.txt"],
        )

    def test_refuses_to_push_existing_unrelated_local_commits(self) -> None:
        unrelated = self.repo / "unrelated-committed.txt"
        unrelated.write_text("must remain local\n", encoding="utf-8")
        self.git(self.repo, "add", "unrelated-committed.txt")
        self.git(self.repo, "commit", "-m", "unrelated local work")

        (self.project / "index.html").write_text(
            "<!doctype html><title>Preview update</title>\n",
            encoding="utf-8",
        )
        result = self.run_sync("y\n\n")
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Commit lokal yang belum terkirim mengubah file di luar", result.stderr)
        self.assertIn("Push dibatalkan", result.stdout)
        self.assertEqual(
            self.git(None, "--git-dir", str(self.remote), "rev-parse", "refs/heads/main").stdout.strip(),
            self.git(self.repo, "rev-parse", "HEAD~2").stdout.strip(),
        )


if __name__ == "__main__":
    unittest.main()
