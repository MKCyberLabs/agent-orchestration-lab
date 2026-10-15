import importlib.util
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "nightshift.py"
spec = importlib.util.spec_from_file_location("nightshift", MODULE)
n = importlib.util.module_from_spec(spec)
spec.loader.exec_module(n)


def cmd(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


class NightshiftTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.addCleanup(self.t.cleanup)
        self.root = Path(self.t.name)
        base = self.root / "base"
        base.mkdir()
        cmd("git", "init", "-b", "main", str(base))
        cmd("git", "config", "user.email", "test@example.invalid", cwd=base)
        cmd("git", "config", "user.name", "Nightshift Fixture", cwd=base)
        (base / "src").mkdir()
        (base / "src" / "a.py").write_text("VALUE = 0\n")
        (base / "src" / "b.py").write_text("VALUE = 0\n")
        (base / "AGENTS.md").write_text("Fixture agent instructions\n")
        cmd("git", "add", ".", cwd=base)
        cmd("git", "commit", "-m", "fixture", cwd=base)
        self.repo = self.root / "nightshift"
        cmd("git", "worktree", "add", "-b", "nightshift/pilot", str(self.repo), cwd=base)
        self.clock = datetime(2026, 10, 16, 0, 30, tzinfo=ZoneInfo("Asia/Kolkata"))
        self.c = {
            "schema_version": 2, "project_id": "lab", "worktree": str(self.repo),
            "backlog_file": str(self.root / "backlog.json"),
            "state_dir": str(self.root / "state"),
            "timezone": "Asia/Kolkata", "branch": "nightshift/pilot",
            "worker": "codex", "approved": True, "max_minutes": 90,
            "task_minutes": 15, "max_tasks": 4,
            "start": "00:15", "stop": "02:15",
            "verify_commands": [["python3", "-c", "assert True"]],
        }
        self.tasks = [
            {"task_id": "A01", "approved": True, "objective": "Set VALUE to 1 in src/a.py without modifying other files.",
             "context_files": ["AGENTS.md"], "allowed_paths": ["src/a.py"], "depends_on": [],
             "max_diff_lines": 100, "acceptance_commands": [["python3", "-c", "from src.a import VALUE; assert VALUE == 1"]]},
            {"task_id": "B01", "approved": True, "objective": "Set VALUE to 2 in src/b.py without modifying other files.",
             "context_files": ["AGENTS.md"], "allowed_paths": ["src/b.py"], "depends_on": ["A01"],
             "max_diff_lines": 100, "acceptance_commands": [["python3", "-c", "from src.b import VALUE; assert VALUE == 2"]]},
        ]
        self.backlog()
        self.configpath = self.root / "config.json"
        self.config()

    def backlog(self):
        (self.root / "backlog.json").write_text(json.dumps({"schema_version": 1, "project_id": "lab", "tasks": self.tasks}))

    def config(self):
        self.configpath.write_text(json.dumps(self.c))

    def fake_worker(self, cfg, repo, task, root, timeout):
        filename = "a.py" if task["task_id"] == "A01" else "b.py"
        (repo / "src" / filename).write_text("VALUE = " + ("1" if filename == "a.py" else "2") + "\n")
        return True, 123, root / "fake-agent", False

    def run_campaign(self):
        with patch.object(n, "clock", return_value=self.clock), \
             patch.object(n, "worker", side_effect=self.fake_worker), \
             patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            with n.lock(self.c) as root:
                return n.campaign(self.c, root, self.tasks, self.clock)

    def test_schedule_window(self):
        self.assertEqual(n.window(self.c, self.clock), "2026-10-16")
        self.assertIsNone(n.window(self.c, self.clock.replace(hour=2, minute=15)))
        self.assertIsNone(n.window(self.c, self.clock.replace(hour=0, minute=14)))

    def test_strict_config(self):
        self.assertEqual(n.load_config(self.configpath)["branch"], "nightshift/pilot")
        self.c["branch"] = "main"
        self.config()
        with self.assertRaises(n.Hold):
            n.load_config(self.configpath)

    def test_reject_shell_command_string(self):
        with self.assertRaises(n.Hold):
            n.validate_commands(["npm run test"])
        with self.assertRaises(n.Hold):
            n.validate_commands([["bash", "-c", "rm -rf /"]])

    def test_unapproved_task(self):
        self.tasks[0]["approved"] = False
        self.backlog()
        self.assertFalse(n.load_backlog(self.root / "backlog.json", "lab")[0]["approved"])

    def test_duplicate_task(self):
        self.tasks.append(dict(self.tasks[0]))
        self.backlog()
        with self.assertRaises(n.Hold):
            n.load_backlog(self.root / "backlog.json", "lab")

    def test_atomic_permissions(self):
        dst = self.root / "test-state.json"
        n.atomic_write(dst, {"phase": "RUNNING"})
        self.assertEqual(dst.stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads(dst.read_text())["phase"], "RUNNING")

    def test_preflight_clean_feature_worktree(self):
        with patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            self.assertEqual(n.preflight(self.c), self.repo)
            (self.repo / "untracked").write_text("do not touch")
            with self.assertRaises(n.Hold):
                n.preflight(self.c)
        self.assertTrue((self.repo / "untracked").exists())

    def test_success_two_tasks_in_one_run(self):
        state = self.run_campaign()
        self.assertEqual(state["phase"], "REVIEW_REQUIRED", state.get("blocker"))
        self.assertEqual(state["window_completed"], 2)
        self.assertEqual(state["tasks"]["A01"]["phase"], "VERIFIED_COMMITTED")
        self.assertEqual(state["tasks"]["B01"]["phase"], "VERIFIED_COMMITTED")
        self.assertEqual(int(cmd("git", "rev-list", "--count", "HEAD", cwd=self.repo)), 3)
        with n.lock(self.c) as root:
            report = n.report(root, self.c, state, self.tasks)
        self.assertIn("A01", report.read_text())

    def test_repeat_does_not_redo_completed_tasks(self):
        self.run_campaign()
        with patch.object(n, "clock", return_value=self.clock), \
             patch.object(n, "worker", side_effect=AssertionError("duplicate worker")), \
             patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            with n.lock(self.c) as root:
                state = n.campaign(self.c, root, self.tasks, self.clock)
        self.assertEqual(state["window_completed"], 2)

    def test_out_of_scope_change_blocks_without_deleting(self):
        def wrong(cfg, repo, task, root, timeout):
            (repo / "src" / "b.py").write_text("VALUE = 89\n")
            return True, 10, root / "fake", False
        with patch.object(n, "clock", return_value=self.clock), \
             patch.object(n, "worker", side_effect=wrong), \
             patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            with n.lock(self.c) as root:
                state = n.campaign(self.c, root, self.tasks, self.clock)
        self.assertEqual(state["phase"], "BLOCKED")
        self.assertEqual((self.repo / "src" / "b.py").read_text(), "VALUE = 89\n")
        self.assertEqual(int(cmd("git", "rev-list", "--count", "HEAD", cwd=self.repo)), 1)

    def test_host_acceptance_failure_prevents_commit(self):
        def wrong(cfg, repo, task, root, timeout):
            (repo / "src" / "a.py").write_text("VALUE = 7\n")
            return True, 10, root / "fake", False
        with patch.object(n, "clock", return_value=self.clock), \
             patch.object(n, "worker", side_effect=wrong), \
             patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            with n.lock(self.c) as root:
                state = n.campaign(self.c, root, self.tasks, self.clock)
        self.assertEqual(state["phase"], "BLOCKED")
        self.assertEqual(int(cmd("git", "rev-list", "--count", "HEAD", cwd=self.repo)), 1)

    def test_interrupted_worker_never_redispatched(self):
        with n.lock(self.c) as root:
            n.atomic_write(root / "state.json", {"phase": "WORKER_RUNNING", "tasks": {"A01": {"phase": "WORKER_RUNNING"}}})
            with patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
                with self.assertRaises(n.Hold):
                    n.campaign(self.c, root, self.tasks, self.clock)

    def test_failed_worker_keeps_changes_for_inspection(self):
        def failure(cfg, repo, task, root, timeout):
            (repo / "src" / "a.py").write_text("VALUE = 5\n")
            return False, None, root / "failed", True
        with patch.object(n, "clock", return_value=self.clock), \
             patch.object(n, "worker", side_effect=failure), \
             patch.object(n.shutil, "which", return_value="/usr/bin/codex"):
            with n.lock(self.c) as root:
                state = n.campaign(self.c, root, self.tasks, self.clock)
        self.assertEqual(state["phase"], "BLOCKED")
        self.assertEqual((self.repo / "src" / "a.py").read_text(), "VALUE = 5\n")

    def test_no_changes_blocks(self):
        with self.assertRaises(n.Hold):
            n.audit(self.repo, self.tasks[0], cmd("git", "rev-parse", "HEAD", cwd=self.repo))

    def test_dependency_skipped_when_unapproved(self):
        self.tasks[0]["approved"] = False
        state = self.run_campaign()
        self.assertEqual(state["window_completed"], 0)
        self.assertEqual(state["phase"], "REVIEW_REQUIRED")

    def test_broad_glob_disallowed(self):
        self.tasks[0]["allowed_paths"] = ["**/*"]
        self.backlog()
        with self.assertRaises(n.Hold):
            n.load_backlog(self.root / "backlog.json", "lab")


if __name__ == "__main__":
    unittest.main()
