"""Safety and upstream-integration tests for the Termux GitHub sync helper."""

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

    def test_behind_feature_branch_fast_forwards_after_confirmation(self) -> None:
        self.git(self.repo, "switch", "-c", "feat/behind")
        self.advance_remote_main()

        result = self.run_sync("y\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Branch berhasil diperbarui", result.stdout)
        self.assertEqual(
            self.git(self.repo, "branch", "--show-current").stdout.strip(),
            "feat/behind",
        )
        self.assertEqual(
            self.git(self.repo, "rev-parse", "HEAD").stdout.strip(),
            self.git(self.repo, "rev-parse", "origin/main").stdout.strip(),
        )

    def test_diverged_feature_branch_merges_main_and_pushes_without_rewriting(self) -> None:
        self.git(self.repo, "switch", "-c", "feat/diverged")
        (self.repo / "local.txt").write_text("local change\n", encoding="utf-8")
        self.git(self.repo, "add", "local.txt")
        self.git(self.repo, "commit", "-m", "feature work")
        feature_commit = self.git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.advance_remote_main()

        result = self.run_sync("y\ny\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("memiliki commit masing-masing", result.stdout)
        self.assertIn("Branch berhasil diperbarui", result.stdout)
        self.assertIn("Push berhasil", result.stdout)
        self.assertEqual(
            self.git(self.repo, "rev-parse", "HEAD^1").stdout.strip(), feature_commit
        )
        self.assertEqual(
            self.git(self.repo, "rev-parse", "HEAD^2").stdout.strip(),
            self.git(self.repo, "rev-parse", "origin/main").stdout.strip(),
        )
        self.git(None, "--git-dir", str(self.remote), "show-ref", "--verify",
                 "refs/heads/feat/diverged")

    def test_untracked_dotenv_variant_is_rejected_before_staging(self) -> None:
        self.git(self.repo, "switch", "-c", "feat/secret-guard")
        secret = self.repo / ".env.local"
        secret.write_text("TOKEN=do-not-commit\\n", encoding="utf-8")

        result = self.run_sync()
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("berpotensi rahasia", result.stderr)
        self.assertEqual(
            self.git(self.repo, "diff", "--cached", "--name-only").stdout, ""
        )
        self.assertTrue(secret.exists())

    def test_declining_upstream_integration_leaves_branch_unchanged(self) -> None:
        self.git(self.repo, "switch", "-c", "feat/decline")
        before = self.git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.advance_remote_main()

        result = self.run_sync("n\n")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Sinkronisasi dibatalkan", result.stdout)
        self.assertEqual(self.git(self.repo, "rev-parse", "HEAD").stdout.strip(), before)
        self.assertEqual(
            self.git(self.repo, "branch", "--show-current").stdout.strip(),
            "feat/decline",
        )


if __name__ == "__main__":
    unittest.main()
