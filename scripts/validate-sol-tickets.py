#!/usr/bin/env python3
"""Validate a full Codex ticket-review report offline. No LLM calls or writes to repo."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

AREAS = (
    "authorization", "money_math", "loan_lifecycle", "credit_card_lifecycle",
    "concurrency_idempotency", "recurrence_timezone", "reminder_delivery",
    "ui_backend_boundary", "tests_build",
)
SHA = re.compile(r"^[0-9a-f]{40}$")
REPORT_PATTERN = re.compile(r"\x60{3}json\s*\n(.*?)\n\x60{3}", re.DOTALL)
STATUSES = {"OPEN", "REGRESSED", "VERIFIED_FIXED", "DISPUTED"}


class InvalidPacket(Exception):
    pass


def need(condition: bool, reason: str) -> None:
    if not condition:
        raise InvalidPacket(reason)


def nonblank(value, name: str) -> str:
    need(isinstance(value, str) and len(value.strip()) >= 6, f"{name} must contain substantive text")
    return value.strip()


def valid_path(value: str, name: str, repo: Path | None = None) -> None:
    need(isinstance(value, str) and bool(value), f"{name} missing")
    p = PurePosixPath(value)
    need(not p.is_absolute() and ".." not in p.parts and p.parts[0] != ".", f"{name} unsafe relative path")
    if repo:
        need((repo / value).is_file(), f"{name} not found at pinned checkout: {value}")


def validate(text: str, expected_sha: str, repo: Path | None = None) -> dict:
    need(bool(SHA.fullmatch(expected_sha)), "Expected SHA must be 40 lowercase hex")
    lines = text.splitlines()
    need(len(lines) >= 2, "Missing review heading")
    header = lines[0].strip()
    need(header in ("VERDICT: PASS", "VERDICT: FAIL", "VERDICT: BLOCKED"), "First line must be exact VERDICT")
    need(lines[1].strip() == f"Reviewed commit: {expected_sha}", "Reviewed commit header mismatch")
    matches = REPORT_PATTERN.findall(text)
    need(len(matches) == 1, "Expected exactly one fenced JSON ticket packet")
    try:
        packet = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise InvalidPacket(f"Invalid ticket JSON: {exc}") from exc
    need(isinstance(packet, dict), "Ticket packet must be object")
    need(packet.get("schema_version") == "1.0", "schema_version must be 1.0")
    need(packet.get("reviewed_commit") == expected_sha, "Packet reviewed_commit mismatch")
    verdict = header.removeprefix("VERDICT: ")
    need(packet.get("verdict") == verdict, "Packet verdict does not match header")

    coverage = packet.get("coverage")
    need(isinstance(coverage, list), "coverage must be an array")
    by_area = {}
    for idx, item in enumerate(coverage):
        need(isinstance(item, dict), f"coverage[{idx}] must be object")
        area = item.get("area")
        need(isinstance(area, str) and area not in by_area, "duplicate/invalid coverage area")
        need(item.get("status") in ("EXAMINED", "NOT_EXAMINED"), f"coverage {area} missing status")
        nonblank(item.get("evidence"), f"coverage[{area}].evidence")
        by_area[area] = item
    missing = set(AREAS) - by_area.keys()
    need(not missing, f"coverage missing required areas: {', '.join(sorted(missing))}")
    if verdict == "PASS":
        need(all(by_area[a]["status"] == "EXAMINED" for a in AREAS), "PASS requires every critical area examined")

    findings = packet.get("findings")
    need(isinstance(findings, list), "findings must be an array")
    if verdict == "PASS":
        need(len(findings) == 0, "PASS cannot include unresolved issue tickets")
    if verdict == "FAIL":
        need(len(findings) > 0, "FAIL requires at least one actionable ticket")

    ids = set()
    for i, ticket in enumerate(findings):
        need(isinstance(ticket, dict), f"ticket[{i}] must be object")
        id_ = ticket.get("id")
        need(isinstance(id_, str) and bool(re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{3,70}", id_)), f"ticket[{i}].id invalid")
        need(id_ not in ids, f"duplicate ticket id: {id_}")
        ids.add(id_)
        need(ticket.get("severity") in ("P0", "P1", "P2", "P3"), f"ticket {id_} invalid severity")
        need(ticket.get("status") in ("OPEN", "REGRESSED", "DISPUTED"), f"ticket {id_} invalid status")
        for field in ("title", "observed", "expected", "reproduction", "root_cause", "impact", "fix_strategy"):
            nonblank(ticket.get(field), f"ticket[{id_}].{field}")
        valid_path(ticket.get("file"), f"ticket[{id_}].file", repo)
        need(type(ticket.get("line")) is int and ticket["line"] > 0, f"ticket {id_} invalid line")
        if repo:
            nlines = len((repo / ticket["file"]).read_text(errors="replace").splitlines())
            need(ticket["line"] <= nlines, f"ticket {id_} file line beyond EOF")
        for field in ("acceptance_criteria", "regression_tests"):
            tests = ticket.get(field)
            need(isinstance(tests, list) and bool(tests), f"ticket {id_} requires {field}")
            for t in tests:
                nonblank(t, f"ticket[{id_}].{field} item")

    prior = packet.get("prior_ticket_dispositions")
    need(isinstance(prior, list), "prior_ticket_dispositions must be an array")
    seen = set()
    for t in prior:
        need(isinstance(t, dict), "prior disposition must be object")
        tid = nonblank(t.get("id"), "prior ticket ID")
        need(tid not in seen, "duplicate prior ticket status")
        seen.add(tid)
        need(t.get("status") in STATUSES, f"prior {tid} has invalid status")
        nonblank(t.get("evidence"), f"prior {tid} evidence")
    tests = packet.get("tests_run")
    need(isinstance(tests, list), "tests_run must be an array (empty is valid)")
    for t in tests:
        need(isinstance(t, dict), "test row must be object")
        nonblank(t.get("command"), "test command")
        need(t.get("result") in ("PASS", "FAIL"), "test result must be PASS/FAIL; use not_run for skipped")
    for field in ("not_run", "release_risks"):
        items = packet.get(field)
        need(isinstance(items, list), f"{field} must be an array")
        for item in items:
            nonblank(item, f"{field} item")
    need(verdict != "BLOCKED" or bool(packet.get("release_risks")), "BLOCKED needs reason in release_risks")
    return packet


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", type=Path, required=True)
    p.add_argument("--sha", required=True)
    p.add_argument("--repo", type=Path)
    p.add_argument("--export", type=Path)
    args = p.parse_args()
    try:
        packet = validate(args.report.read_text(encoding="utf-8"), args.sha, args.repo.resolve() if args.repo else None)
        if args.export:
            args.export.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"PASS: validated Sol ticket packet {packet['verdict']} for {args.sha}; {len(packet['findings'])} tickets")
        return 0
    except (InvalidPacket, OSError) as exc:
        print(f"BLOCKED: invalid Sol ticket packet: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
