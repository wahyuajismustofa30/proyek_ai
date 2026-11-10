"""Regression tests documenting the intentional removal of the legacy preview sync script."""

from __future__ import annotations

import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
REMOVED_SYNC_SCRIPT = REPOSITORY_ROOT / "projects" / "preview" / "SYNC - 26.11.03.sh"


class RemovedPreviewSyncScriptTests(unittest.TestCase):
    def test_legacy_preview_sync_script_remains_removed(self) -> None:
        self.assertFalse(REMOVED_SYNC_SCRIPT.exists())


if __name__ == "__main__":
    unittest.main()
