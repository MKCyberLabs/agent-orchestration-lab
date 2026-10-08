#!/usr/bin/env python3
"""Offline unit tests: current Codex profile installation/migration, no model calls."""
import os
from pathlib import Path
import subprocess
import tempfile
import tomllib
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "install-sol-review-profile.sh"
EXPECTED = tomllib.loads((ROOT / "config/codex/sol-review.config.toml").read_text())

class ProfileInstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.config = self.home / "config.toml"
        self.profile = self.home / "sol-review.config.toml"

    def install(self):
        return subprocess.run(
            ["bash", str(SCRIPT)], env={**os.environ, "CODEX_HOME": str(self.home)},
            text=True, capture_output=True,
        )

    def test_new_profile_and_idempotent_rerun(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.config.exists())
        self.assertEqual(tomllib.loads(self.profile.read_text()), EXPECTED)
        second = self.install()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertFalse(self.config.exists())
        self.assertEqual(tomllib.loads(self.profile.read_text()), EXPECTED)

    def test_legacy_table_and_selector_migrate_without_erasing_others(self):
        self.config.write_text(
            'profile = "sol-review"\nmodel = "gpt-6"\n\n'
            "[profiles.sol-review]\n"
            'model = "gpt-6.1-sol"\n'
            'model_reasoning_effort = "high"\n'
            'sandbox_mode = "read-only"\n'
            'approval_policy = "never"\n'
            'web_search = "disabled"\n\n'
            "[projects.test]\n"
            'trust_level = "trusted"\n'
        )
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        cfg = tomllib.loads(self.config.read_text())
        self.assertEqual(cfg["model"], "gpt-6")
        self.assertEqual(cfg["projects"]["test"]["trust_level"], "trusted")
        self.assertNotIn("profile", cfg)
        self.assertNotIn("sol-review", cfg.get("profiles", {}))
        self.assertEqual(tomllib.loads(self.profile.read_text()), EXPECTED)
        self.assertEqual(len(list(self.home.glob("config.toml.backup.v02.*"))), 1)
        again = self.install()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertEqual(len(list(self.home.glob("config.toml.backup.v02.*"))), 1)

    def test_conflicting_profile_not_overwritten(self):
        original = 'model = "gpt-custom"\n'
        self.profile.write_text(original)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.profile.read_text(), original)

    def test_custom_legacy_table_is_not_silently_removed(self):
        original = '[profiles.sol-review]\nmodel = "gpt-custom"\n'
        self.config.write_text(original)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.config.read_text(), original)
        self.assertFalse(self.profile.exists())

    def test_unrelated_user_config_untouched(self):
        original = 'model = "gpt-6"\n[projects.test]\ntrust_level = "trusted"\n'
        self.config.write_text(original)
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.config.read_text(), original)

if __name__ == "__main__":
    unittest.main(verbosity=2)
