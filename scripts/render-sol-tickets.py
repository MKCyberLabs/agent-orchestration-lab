#!/usr/bin/env python3
"""Render validated Sol ticket JSON to individual GitHub-ready Markdown tickets.

No GitHub API calls. No repository mutations. The orchestrator deduplicates
against existing issues before publication to prevent duplicate GitHub issues.
"""
import argparse
import json
from pathlib import Path
import re
import sys


def esc(value) -> str:
    return str(value).replace("\r", "").strip()


def render(packet: dict, ticket: dict) -> str:
    ref = packet["reviewed_commit"]
    fields = [
        f"# [{ticket['severity']}] {esc(ticket['title'])}",
        "",
        f"- **Ticket ID:** {ticket['id']}",
        f"- **Review SHA:** {ref}",
        f"- **Evidence:** {ticket['file']}:{ticket['line']}",
        f"- **Status:** {ticket['status']}",
        "",
        "## Actual / observed behavior", "",
        esc(ticket["observed"]), "",
        "## Expected invariant", "",
        esc(ticket["expected"]), "",
        "## Reproduction", "",
        esc(ticket["reproduction"]), "",
        "## Root cause / call path", "",
        esc(ticket["root_cause"]), "",
        "## User / financial / security impact", "",
        esc(ticket["impact"]), "",
        "## Proposed fix strategy (not yet implemented)", "",
        esc(ticket["fix_strategy"]), "",
        "## Acceptance criteria", "",
    ]
    fields += [f"- [ ] {esc(x)}" for x in ticket["acceptance_criteria"]]
    fields += ["", "## Required regression tests", ""]
    fields += [f"- [ ] {esc(x)}" for x in ticket["regression_tests"]]
    fields += [
        "",
        "## Closure requirements", "",
        "- [ ] Worker code and Git SHA linked; isolated DB-backed test evidence included.",
        "- [ ] No collateral regression; prior ticket ID preserved across reviews.",
        "- [ ] Independent Codex reviewer verifies fix on the final integration SHA.",
        "- [ ] Full product release gates completed; no automatic merge or production deploy.",
        "",
    ]
    return "\n".join(fields)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--packet", type=Path, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    args = p.parse_args()
    packet = json.loads(args.packet.read_text(encoding="utf-8"))
    out = args.out_dir
    out.mkdir(mode=0o700, parents=True, exist_ok=True)
    findings = packet["findings"]
    for ticket in findings:
        ident = ticket["id"]
        if not re.fullmatch(r"[A-Z0-9][A-Z0-9_-]{3,70}", ident):
            raise ValueError(f"Invalid ticket ID for filename: {ident}")
        (out / (ident + ".md")).write_text(render(packet, ticket), encoding="utf-8")
    lines = [
        "# Validated Codex Ticket Index", "",
        f"Reviewed commit: {packet['reviewed_commit']}",
        f"Verdict: {packet['verdict']}",
        f"Unresolved issue count: {len(findings)}", "",
    ]
    lines += [f"- {t['id']}: {t['title']} ({t['severity']})" for t in findings]
    (out / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Rendered {len(findings)} GitHub-ready issue files in {out}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"BLOCKED: ticket rendering failed: {exc}", file=sys.stderr)
        sys.exit(2)
