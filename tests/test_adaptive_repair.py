#!/usr/bin/env python3
"""Offline contract checks for adaptive routing (no model/API calls)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "route-repair.py"
spec = importlib.util.spec_from_file_location("adaptive_repair", SCRIPT)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)
SHA = "e" * 40


def packet(ids, *, verdict="FAIL", prior=None):
    return {
        "schema_version": "1.0",
        "reviewed_commit": SHA,
        "verdict": verdict,
        "findings": [
            {"id": tid, "status": "OPEN", "severity": "P1", "file": "src/loan.ts",
             "fix_strategy": "Apply one guarded transactional fix", "regression_tests": ["Run a real database test"]}
            for tid in ids
        ],
        "prior_ticket_dispositions": prior or [],
    }


def state(ids, used=1, maximum=5, stage="repair_required"):
    return {
        "last_reviewed_sha": SHA, "open_tickets": ids,
        "review_count": used, "max_rounds": maximum, "stage": stage,
    }


class TestRepairRouter(unittest.TestCase):
    def test_four_go_to_direct_codex(self):
        p = packet(["SOL-R001-007", "SOL-R004-016", "SOL-R004-017", "SOL-R004-018"])
        outcome = router.plan(p, state([x["id"] for x in p["findings"]], 5, 5, "max_rounds_reached"))
        self.assertEqual(outcome["route"], "CODEX_DIRECT")
        self.assertEqual(outcome["unresolved_count"], 4)
        self.assertEqual(outcome["implementation_sandbox"], "workspace-write")
        self.assertTrue(outcome["review_budget"]["exhausted"])
        self.assertFalse(outcome["review_budget"]["review_authorized_by_this_router"])
        self.assertFalse(outcome["may_merge_or_deploy"])

    def test_five_route_to_herdr_workers(self):
        self.assertEqual(router.plan(packet([f"SOL-R004-{i:03}" for i in range(1, 6)]))["route"],
                         "AGY_PARALLEL")

    def test_one_routes_codex(self):
        self.assertEqual(router.plan(packet(["SOL-R004-001"]))["route"], "CODEX_DIRECT")

    def test_zero_pass_no_repair(self):
        self.assertEqual(router.plan(packet([], verdict="PASS"))["route"], "NO_REPAIR")

    def test_prior_open_is_not_silently_discarded(self):
        p = packet(["SOL-R004-001"], prior=[
            {"id": "SOL-R003-001", "status": "OPEN", "evidence": "Still fails"}
        ])
        self.assertEqual(router.plan(p)["ticket_ids"], ["SOL-R003-001", "SOL-R004-001"])

    def test_state_unresolved_is_not_dropped(self):
        p = packet(["SOL-R004-001"])
        self.assertEqual(router.plan(p, state(["SOL-R004-001", "SOL-R004-002"]))["unresolved_count"], 2)

    def test_verified_prior_not_counted(self):
        p = packet(["SOL-R004-001"], prior=[
            {"id": "SOL-R003-001", "status": "VERIFIED_FIXED", "evidence": "Regression passed"}
        ])
        self.assertEqual(router.plan(p)["unresolved_count"], 1)

    def test_disputed_needs_triage(self):
        p = packet(["SOL-R004-001"], prior=[
            {"id": "SOL-R003-001", "status": "DISPUTED", "evidence": "Requirements unclear"}
        ])
        self.assertEqual(router.plan(p)["route"], "MANUAL_TRIAGE")

    def test_critical_needs_triage(self):
        p = packet(["SOL-R004-001"])
        p["findings"][0]["severity"] = "P0"
        self.assertEqual(router.plan(p)["route"], "MANUAL_TRIAGE")

    def test_force_multi(self):
        self.assertEqual(router.plan(packet(["SOL-R004-001"]), force_multi=True)["route"],
                         "AGY_PARALLEL")

    def test_duplicate_rejected(self):
        p = packet(["SOL-R004-001", "SOL-R004-001"])
        with self.assertRaises(router.RouteError):
            router.plan(p)

    def test_inconsistent_review_sha_rejected(self):
        bad = state(["SOL-R004-001"])
        bad["last_reviewed_sha"] = "a" * 40
        with self.assertRaisesRegex(router.RouteError, "SHA"):
            router.plan(packet(["SOL-R004-001"]), bad)

    def test_blocked_review_rejected(self):
        with self.assertRaisesRegex(router.RouteError, "BLOCKED"):
            router.plan(packet(["SOL-R004-001"], verdict="BLOCKED"))

    def test_broken_ticket_contract_rejected(self):
        p = packet(["SOL-R004-001"])
        p["findings"][0]["regression_tests"] = []
        with self.assertRaisesRegex(router.RouteError, "regression"):
            router.plan(p)

    def test_cli_output_and_invalid_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            filename = Path(tmp) / "tickets.json"
            filename.write_text(json.dumps(packet(["SOL-R004-001"])))
            result = subprocess.run([sys.executable, str(SCRIPT), "--tickets", str(filename)],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["route"], "CODEX_DIRECT")
            filename.write_text("{bad json")
            result = subprocess.run([sys.executable, str(SCRIPT), "--tickets", str(filename)],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("BLOCKED", result.stderr)


if __name__ == "__main__":
    unittest.main()
