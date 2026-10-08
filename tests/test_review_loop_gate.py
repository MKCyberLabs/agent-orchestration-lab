#!/usr/bin/env python3
"""Offline state-machine contract tests: fake reviewer/cbds reports, NO model calls."""
import json
import subprocess
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts/review-loop-gate.py"
AREAS = (
    "authorization", "money_math", "loan_lifecycle", "credit_card_lifecycle",
    "concurrency_idempotency", "recurrence_timezone", "reminder_delivery",
    "ui_backend_boundary", "tests_build",
)


class StateMachineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.call_git("init", "-q")
        self.call_git("config", "user.email", "lab@example.test")
        self.call_git("config", "user.name", "Lab Tests")
        self.call_git("branch", "-M", "orchestration/finance-crud-reminders-r001")
        (self.repo / ".gitignore").write_text(".cbds/\n")
        (self.repo / "finance.ts").write_text("export const value = 1;\n")
        self.commit("initial commit")
        self.evidence = self.root / "tests.txt"
        self.evidence.write_text("PASS: DB test and build test evidence\n")

    def call_git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), *args], text=True).strip()

    def commit(self, message):
        self.call_git("add", ".")
        self.call_git("commit", "-qm", message)
        return self.call_git("rev-parse", "HEAD")

    def cli(self, action, *args, success=True):
        p = subprocess.run(
            ["python3", str(SCRIPT), action, "--repo", str(self.repo), *args],
            capture_output=True, text=True
        )
        if success:
            self.assertEqual(p.returncode, 0, p.stderr)
            return json.loads(p.stdout)
        self.assertNotEqual(p.returncode, 0)
        self.assertIn("BLOCKED", p.stderr)

    def report(self, verdict, sha, name, prior=None):
        finding = {
            "id": "SOL-R001-001", "severity": "P1", "status": "OPEN",
            "title": "Concurrent EMI payment duplicate",
            "file": "finance.ts", "line": 1,
            "observed": "Concurrent same-key requests insert two payments",
            "expected": "Concurrent same-key requests insert exactly one payment",
            "reproduction": "Send two transactions at the same time with a common idempotency key",
            "root_cause": "Nontransactional precheck executes before row locking",
            "impact": "Principal accounting becomes incorrect and overstated",
            "fix_strategy": "Lock row, recheck uniqueness and enforce database uniqueness",
            "acceptance_criteria": ["Single payment persists after simultaneous requests"],
            "regression_tests": ["Two concurrent PostgreSQL clients with identical idempotency key"],
        }
        packet = {
            "schema_version": "1.0", "reviewed_commit": sha, "verdict": verdict,
            "coverage": [
                {"area": x, "status": "EXAMINED", "evidence": f"Inspected finance.ts for {x} code path"}
                for x in AREAS
            ],
            "findings": [finding] if verdict == "FAIL" else [],
            "prior_ticket_dispositions": prior or [],
            "tests_run": [{"command": "npm run typecheck", "result": "PASS"}],
            "not_run": ["PostgreSQL runtime was not available inside review sandbox"],
            "release_risks": [],
        }
        fence = chr(96)*3
        path = self.root / name
        path.write_text(
            f"VERDICT: {verdict}\nReviewed commit: {sha}\nFindings included below.\n"
            f"{fence}json\n{json.dumps(packet)}\n{fence}\n"
        )
        return path

    def test_two_round_fail_then_pass_with_prior_disposition(self):
        first_sha = self.call_git("rev-parse", "HEAD")
        state = self.cli("init", "--max-rounds", "2")
        self.assertEqual(state["stage"], "review_ready")
        one = self.report("FAIL", first_sha, "one.md")
        state = self.cli("review", "--report", str(one))
        self.assertEqual(state["stage"], "repair_required")
        self.assertEqual(state["open_tickets"], ["SOL-R001-001"])
        self.cli("review", "--report", str(one), success=False)
        self.cli("integrate", "--test-evidence", str(self.evidence), "--cbds-report-ids", "rpt_123", success=False)
        (self.repo / "finance.ts").write_text("export const value = 2;\n")
        second_sha = self.commit("fix concurrency")
        self.cli("integrate", "--test-evidence", str(self.evidence), "--cbds-report-ids", "rpt_123")
        two = self.report("PASS", second_sha, "two.md", prior=[
            {"id":"SOL-R001-001","status":"VERIFIED_FIXED","evidence":"Verified finance.ts logic and concurrency test"}
        ])
        state = self.cli("review", "--report", str(two))
        self.assertEqual(state["stage"], "review_pass_pending_gates")
        self.assertEqual(state["review_count"], 2)
        self.assertEqual(state["open_tickets"], [])
        self.cli("integrate", "--test-evidence", str(self.evidence), "--cbds-report-ids", "rpt_456", success=False)

    def test_prior_ticket_cannot_disappear_and_hard_cap(self):
        sha = self.call_git("rev-parse", "HEAD")
        self.cli("init", "--max-rounds", "2")
        self.cli("review", "--report", str(self.report("FAIL", sha, "fail1.md")))
        (self.repo / "finance.ts").write_text("export const value = 3;\n")
        sha2 = self.commit("attempt repair")
        self.cli("integrate", "--test-evidence", str(self.evidence), "--cbds-report-ids", "rpt_123")
        no_prior = self.report("PASS", sha2, "invalidpass.md")
        self.cli("review", "--report", str(no_prior), success=False)
        with_prior_open = self.report("FAIL", sha2, "fail2.md", prior=[
            {"id":"SOL-R001-001","status":"OPEN","evidence":"Still reproduced the concurrency accounting defect"}
        ])
        stage = self.cli("review", "--report", str(with_prior_open))
        self.assertEqual(stage["stage"], "max_rounds_reached")
        self.cli("review", "--report", str(with_prior_open), success=False)

    def test_existing_history_uses_total_budget(self):
        sha = self.call_git("rev-parse", "HEAD")
        state = self.cli(
            "init", "--max-rounds", "5", "--completed-rounds", "3",
            "--last-reviewed-sha", sha, "--prior-result", "FAIL",
            "--initial-ticket-ids", "SOL-R001-001",
            "--run-id", "run_existing"
        )
        self.assertEqual(state["stage"], "repair_required")
        self.assertEqual(state["review_count"], 3)
        self.cli("init", success=False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
