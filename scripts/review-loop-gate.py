#!/usr/bin/env python3
"""Persistent hard gate for a bounded Herdr/cbds -> Sol review loop.

This intentionally DOES NOT dispatch agents or invoke a model: the orchestrator
uses real installed cbds commands and feeds back accepted reports. It ensures
a fresh code SHA, previous ticket continuity and a hard limit on review rounds.
"""
import argparse
import fcntl
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sol_ticket_validation", ROOT / "validate-sol-tickets.py")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

SHA = re.compile(r"^[0-9a-f]{40}$")
CODE_SUFFIXES = (".ts", ".tsx", ".js", ".jsx", ".prisma", ".sql", ".py", ".sh", ".json")


def git(repo: Path, *argv: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *argv], text=True).strip()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def load_state(path: Path):
    require(path.exists(), "No state: run init first")
    return json.loads(path.read_text())


def write_state(path: Path, state: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".review-loop.")
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def check_repo(repo: Path, branch: str):
    require(git(repo, "branch", "--show-current") == branch, "Unexpected branch, refusing to continue")
    require(not git(repo, "status", "--porcelain"), "Dirty worktree, refusing to approve review SHA")
    return git(repo, "rev-parse", "HEAD")


def execute(args):
    repo = Path(args.repo).resolve()
    require((repo / ".git").exists() or git(repo, "rev-parse", "--is-inside-work-tree") == "true", "Missing Git repository")
    statefile = Path(args.state).resolve() if args.state else repo / ".cbds" / "review-loop-v02.json"
    statefile.parent.mkdir(parents=True, exist_ok=True)
    with open(str(statefile) + ".lock", "a+") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.action == "init":
            require(not statefile.exists(), "State already exists; use status/resume instead of overwriting")
            require(1 <= args.max_rounds <= 5, "Maximum must be between 1 and 5")
            require(0 <= args.completed_rounds <= args.max_rounds, "Invalid completed round count")
            head = check_repo(repo, args.branch)
            if args.completed_rounds or args.last_reviewed_sha:
                require(bool(SHA.fullmatch(args.last_reviewed_sha or "")), "Prior review SHA required")
                require(args.prior_result in ("FAIL", "PASS"), "Prior verdict required")
                stage = "repair_required" if args.prior_result == "FAIL" else "review_pass_pending_gates"
            else:
                stage = "review_ready"
            state = {
                "schema_version": "1.0", "repo": str(repo), "branch": args.branch,
                "run_id": args.run_id, "max_rounds": args.max_rounds,
                "review_count": args.completed_rounds,
                "stage": stage, "last_reviewed_sha": args.last_reviewed_sha,
                "last_integration_sha": head,
                "open_tickets": [x.strip() for x in args.initial_ticket_ids.split(",") if x.strip()],
                "history": [], "automatic_merge_allowed": False,
            }
            write_state(statefile, state)
        else:
            state = load_state(statefile)
            require(state["repo"] == str(repo), "Review loop repo mismatch")
            head = check_repo(repo, state["branch"])
            if args.action == "status":
                print(json.dumps(state, indent=2))
                return
            if args.action == "integrate":
                require(state["stage"] == "repair_required", "No repair requested: review or stop first")
                require(state["review_count"] < state["max_rounds"], "Review round cap exhausted")
                prior_sha = state["last_reviewed_sha"]
                require(bool(prior_sha), "Missing pinned previous reviewer SHA")
                require(head != prior_sha, "No new integrated SHA since the previous review")
                changed = git(repo, "diff", "--name-only", prior_sha, head).splitlines()
                require(any(s.endswith(CODE_SUFFIXES) and not s.endswith((".md", ".json")) for s in changed),
                        "New commit has no code changes; docs-only updates do not justify a new review")
                require(args.cbds_report_ids, "Accepted cbds report IDs required")
                evidence = Path(args.test_evidence).resolve()
                require(evidence.is_file() and evidence.stat().st_size > 0, "Missing new test gate evidence")
                state["last_integration_sha"] = head
                state["stage"] = "review_ready"
                state["history"].append({
                    "event": "integration_ready", "sha": head, "changed_files": changed,
                    "cbds_report_ids": [x.strip() for x in args.cbds_report_ids.split(",") if x.strip()],
                    "test_evidence": str(evidence),
                })
                write_state(statefile, state)
            elif args.action == "review":
                require(state["stage"] == "review_ready", f"Review forbidden in stage {state['stage']}")
                require(state["review_count"] < state["max_rounds"], "Maximum review rounds reached")
                require(head not in [h.get("sha") for h in state["history"] if h["event"] == "review"],
                        "Same code SHA already reviewed; do not burn more tokens")
                path = Path(args.report).resolve()
                packet = validator.validate(path.read_text(encoding="utf-8"), head, repo)
                prior_ids = set(state["open_tickets"])
                dispositions = {x["id"]: x["status"] for x in packet["prior_ticket_dispositions"]}
                require(prior_ids <= dispositions.keys(),
                        "Previous open tickets missing disposition: " + ", ".join(sorted(prior_ids - dispositions.keys())))
                open_tickets = (prior_ids - {k for k, v in dispositions.items() if v == "VERIFIED_FIXED"})
                open_tickets |= {t["id"] for t in packet["findings"]}
                if packet["verdict"] == "PASS":
                    require(not open_tickets, "Cannot PASS while prior tickets remain OPEN/DISPUTED")
                state["review_count"] += 1
                state["last_reviewed_sha"] = head
                state["open_tickets"] = sorted(open_tickets)
                if packet["verdict"] == "PASS":
                    state["stage"] = "review_pass_pending_gates"
                elif packet["verdict"] == "FAIL":
                    state["stage"] = "max_rounds_reached" if state["review_count"] >= state["max_rounds"] else "repair_required"
                else:
                    state["stage"] = "blocked"
                state["history"].append({
                    "event": "review", "sha": head, "verdict": packet["verdict"],
                    "ticket_ids": [t["id"] for t in packet["findings"]],
                    "open_tickets": sorted(open_tickets), "report": str(path),
                })
                write_state(statefile, state)
            else:
                raise ValueError(f"Unsupported action: {args.action}")
        print(json.dumps({
            "stage": state["stage"], "review_count": state["review_count"],
            "max_rounds": state["max_rounds"], "open_tickets": state["open_tickets"],
            "state_path": str(statefile),
        }, indent=2))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("init", "status", "integrate", "review"))
    p.add_argument("--repo", required=True)
    p.add_argument("--state", help="Explicit state JSON path, by default in .cbds/")
    p.add_argument("--branch", default="orchestration/finance-crud-reminders-r001")
    p.add_argument("--run-id", default="")
    p.add_argument("--max-rounds", type=int, default=5)
    p.add_argument("--completed-rounds", type=int, default=0)
    p.add_argument("--last-reviewed-sha")
    p.add_argument("--prior-result")
    p.add_argument("--initial-ticket-ids", default="")
    p.add_argument("--cbds-report-ids", default="")
    p.add_argument("--test-evidence", default="")
    p.add_argument("--report", default="")
    args = p.parse_args()
    try:
        execute(args)
    except (ValueError, OSError, subprocess.CalledProcessError, validator.InvalidPacket, json.JSONDecodeError) as exc:
        print(f"BLOCKED: review loop gate: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
