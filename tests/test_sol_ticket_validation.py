#!/usr/bin/env python3
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location("ticket_validator", Path(__file__).resolve().parent.parent / "scripts" / "validate-sol-tickets.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

SHA = "a" * 40
AREAS = module.AREAS


def data(verdict="PASS"):
    return {
        "schema_version": "1.0",
        "reviewed_commit": SHA,
        "verdict": verdict,
        "coverage": [
            {"area": x, "status": "EXAMINED", "evidence": f"Inspected src/lib/finance/sample.ts for {x} invariants"}
            for x in AREAS
        ],
        "findings": [],
        "prior_ticket_dispositions": [
            {"id": "SOL-R001-OLD", "status": "VERIFIED_FIXED", "evidence": "Verified src/lib/finance/sample.ts behavior and test result"}
        ],
        "tests_run": [{"command": "npm run typecheck", "result": "PASS"}],
        "not_run": ["PostgreSQL integration suite unavailable inside read-only reviewer"],
        "release_risks": [],
    }


def report(packet):
    fence = chr(96) * 3
    return (
        f"VERDICT: {packet['verdict']}\nReviewed commit: {SHA}\n\n"
        "Performed independent full-path review.\n\n"
        f"{fence}json\n{json.dumps(packet)}\n{fence}\n"
    )


class TicketValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        (self.repo / "src/lib/finance").mkdir(parents=True)
        (self.repo / "src/lib/finance/sample.ts").write_text("export const value = 1;\n")

    def ticket(self):
        return {
            "id": "SOL-R001-101", "severity": "P1", "status": "OPEN",
            "title": "Duplicate EMI payment on simultaneous requests",
            "file": "src/lib/finance/sample.ts", "line": 1,
            "observed": "Two simultaneous identical requests produce duplicate posted payments",
            "expected": "Exactly one payment should be recorded for the idempotency key",
            "reproduction": "Launch both POST requests concurrently with identical idempotency keys",
            "root_cause": "The uniqueness check is outside the transaction lock",
            "impact": "Outstanding loan principal may be reduced twice",
            "fix_strategy": "Move uniqueness check under lock and enforce durable unique key",
            "acceptance_criteria": ["Concurrent identical commands create exactly one payment"],
            "regression_tests": ["PostgreSQL two-client duplicate key race test"],
        }

    def test_pass_requires_full_coverage(self):
        d = data()
        self.assertEqual(module.validate(report(d), SHA, self.repo)["verdict"], "PASS")
        d["coverage"].pop()
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), SHA, self.repo)

    def test_fail_requires_tickets_and_full_details(self):
        d = data("FAIL")
        d["findings"] = [self.ticket()]
        self.assertEqual(len(module.validate(report(d), SHA, self.repo)["findings"]), 1)
        d["findings"][0].pop("regression_tests")
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), SHA, self.repo)

    def test_pass_cannot_conceal_findings(self):
        d = data("PASS")
        d["findings"] = [self.ticket()]
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), SHA, self.repo)

    def test_fail_without_ticket_is_incomplete(self):
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(data("FAIL")), SHA, self.repo)

    def test_sha_and_file_evidence(self):
        d = data("FAIL")
        d["findings"] = [self.ticket()]
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), "b"*40, self.repo)
        d["findings"][0]["file"] = "../../etc/passwd"
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), SHA, self.repo)

    def test_duplicate_tickets_and_missing_json(self):
        d = data("FAIL")
        d["findings"] = [self.ticket(), self.ticket()]
        with self.assertRaises(module.InvalidPacket):
            module.validate(report(d), SHA, self.repo)
        with self.assertRaises(module.InvalidPacket):
            module.validate(f"VERDICT: PASS\nReviewed commit: {SHA}\nNo findings", SHA, self.repo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
