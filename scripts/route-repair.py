#!/usr/bin/env python3
"""Offline, deterministic repair routing for Herdr/cbds + Codex.

The router makes NO model calls, edits, commits, cbds dispatches or release approvals.
It only selects a repair execution strategy from an already-validated Sol packet.
"""
import argparse
import json
from pathlib import Path
import re
import sys

TICKET_ID = re.compile(r"^[A-Z0-9][A-Z0-9_-]{3,70}$")
GIT_SHA = re.compile(r"^[0-9a-f]{40}$")
OPEN = {"OPEN", "REGRESSED", "DISPUTED"}
ROUTES = {"NO_REPAIR", "CODEX_DIRECT", "AGY_PARALLEL", "MANUAL_TRIAGE"}


class RouteError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise RouteError(message)


def plan(packet, state=None, threshold=4, force_multi=False):
    require(isinstance(threshold, int) and 1 <= threshold <= 10, "threshold must be from 1 to 10")
    require(isinstance(packet, dict) and packet.get("schema_version") == "1.0",
            "requires a validated schema_version=1.0 Sol ticket packet")
    sha = packet.get("reviewed_commit")
    require(isinstance(sha, str) and GIT_SHA.fullmatch(sha), "invalid reviewed_commit SHA")
    verdict = packet.get("verdict")
    require(verdict in ("PASS", "FAIL"), "BLOCKED or invalid review cannot trigger repairs")

    findings = packet.get("findings")
    history = packet.get("prior_ticket_dispositions")
    require(isinstance(findings, list) and isinstance(history, list), "missing findings/dispositions")

    tickets = {}
    for ticket in findings:
        require(isinstance(ticket, dict), "invalid findings entry")
        tid = ticket.get("id")
        require(isinstance(tid, str) and TICKET_ID.fullmatch(tid), "invalid ticket ID")
        require(tid not in tickets, f"duplicate ticket ID {tid}")
        require(ticket.get("status") in OPEN, f"invalid status for {tid}")
        require(ticket.get("severity") in ("P0", "P1", "P2", "P3"), f"invalid severity for {tid}")
        require(isinstance(ticket.get("file"), str) and bool(ticket["file"].strip()),
                f"missing file path for {tid}")
        require(isinstance(ticket.get("fix_strategy"), str) and bool(ticket["fix_strategy"].strip()),
                f"missing fix strategy for {tid}")
        require(isinstance(ticket.get("regression_tests"), list) and bool(ticket["regression_tests"]),
                f"missing regression tests for {tid}")
        tickets[tid] = ticket

    dispositions = {}
    for item in history:
        require(isinstance(item, dict), "invalid prior disposition entry")
        tid, status = item.get("id"), item.get("status")
        require(isinstance(tid, str) and TICKET_ID.fullmatch(tid), "invalid prior ticket ID")
        require(tid not in dispositions, f"duplicate prior ticket {tid}")
        require(status in OPEN | {"VERIFIED_FIXED"}, f"invalid prior status for {tid}")
        dispositions[tid] = status
        # The current finding must not contradict its historical disposition.
        if tid in tickets:
            require(status in OPEN, f"current OPEN ticket {tid} is simultaneously VERIFIED_FIXED")

    # Review-gate carries known unresolved tickets across reviews. A missing
    # finding must not silently vanish from the routing decision.
    open_ids = set(tickets) | {tid for tid, status in dispositions.items() if status in OPEN}
    require(verdict != "PASS" or not open_ids, "PASS packet still has unresolved tickets")
    require(verdict != "FAIL" or bool(open_ids), "FAIL packet has no actionable unresolved tickets")

    budget = None
    if state is not None:
        require(isinstance(state, dict), "state must be an object")
        require(state.get("last_reviewed_sha") == sha,
                "loop state SHA differs from packet; never mix campaign histories")
        state_ids = state.get("open_tickets")
        require(isinstance(state_ids, list) and all(isinstance(s, str) for s in state_ids),
                "invalid loop state open_tickets")
        open_ids |= set(state_ids)
        maximum, used = state.get("max_rounds"), state.get("review_count")
        require(type(maximum) is int and type(used) is int and 1 <= maximum <= 5 and 0 <= used <= maximum,
                "invalid review budget in state")
        exhausted = used >= maximum or state.get("stage") == "max_rounds_reached"
        budget = {
            "review_count": used, "max_rounds": maximum,
            "exhausted": exhausted,
            "review_authorized_by_this_router": False,
        }

    count = len(open_ids)
    disputed = sorted(tid for tid, status in dispositions.items() if status == "DISPUTED")
    p0 = sorted(tid for tid, ticket in tickets.items() if ticket["severity"] == "P0")
    if disputed or p0:
        route = "MANUAL_TRIAGE"
        reason = "P0 or disputed finding needs an explicit risk/requirements decision"
    elif count == 0:
        route = "NO_REPAIR"
        reason = "No unresolved findings; release gates still apply"
    elif force_multi or count > threshold:
        route = "AGY_PARALLEL"
        reason = "More than the direct threshold or manual multi-worker override"
    else:
        route = "CODEX_DIRECT"
        reason = "Small, bounded ticket batch; one Codex implementation task avoids handoffs"

    result = {
        "strategy_version": "0.3",
        "reviewed_commit": sha,
        "route": route,
        "reason": reason,
        "unresolved_count": count,
        "ticket_ids": sorted(open_ids),
        "direct_threshold": threshold,
        "implementation_model": "gpt-6.1-sol" if route == "CODEX_DIRECT" else None,
        "implementation_sandbox": "workspace-write" if route == "CODEX_DIRECT" else None,
        "requires_independent_review": count > 0,
        "may_merge_or_deploy": False,
        "review_budget": budget,
        "notes": [
            "Router is advisory: never invokes Codex, cbds, Git or release actions",
            "One Codex implementer may fix small batches, but must not approve its own changes",
            "Use read-only independent Sol review on an exact new integrated SHA after deterministic gates",
            "A spent review-round budget remains spent; a new campaign requires explicit owner authorization",
        ],
    }
    require(result["route"] in ROUTES, "internal invalid route")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tickets", type=Path, required=True, help="Validated tickets.json")
    parser.add_argument("--state", type=Path, help="Matching review-loop state JSON (optional but recommended)")
    parser.add_argument("--threshold", type=int, default=4, help="Direct Codex maximum unresolved tickets (default 4)")
    parser.add_argument("--force-multi", action="store_true", help="Prefer AGY even for small but complicated repairs")
    args = parser.parse_args()
    try:
        packet = json.loads(args.tickets.read_text(encoding="utf-8"))
        state = json.loads(args.state.read_text(encoding="utf-8")) if args.state else None
        decision = plan(packet, state, args.threshold, args.force_multi)
        print(json.dumps(decision, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, RouteError) as exc:
        print(f"BLOCKED: adaptive repair router: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
