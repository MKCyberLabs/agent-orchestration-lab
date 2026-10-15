# Argon web-chat review handoff — V0.4 night-shift pilot

Gemini Argon is being used through a human-operated browser conversation, not an installed CLI.

Reviewer target:
- Repository: https://github.com/MKCyberLabs/agent-orchestration-lab
- Branch: feature/v0.4-nightshift-pilot
- Comparison base: feature/v0.2-codex-reviewer-recovery
- Entry point: scripts/nightshift.py
- Offline tests: tests/test_nightshift.py
- Operating guidance: docs/NIGHTSHIFT_V0.4_PILOT.md

## Paste into the Argon browser conversation

You are an independent reliability and security reviewer. Review the linked feature branch against the stated comparison base. Inspect the actual Python implementation, test coverage, systemd units, config defaults and cbds upstream CLI contracts. Do not assume you can execute code or inspect the OpenClaw host.

Find all substantiated defects in one pass, prioritizing:
1. Crash boundaries around run/task/dispatch creation and report reconciliation.
2. Duplicate dispatch and cross-project concurrency races.
3. Actual cbds JSON schema and Herdr agent/profile identity mismatches.
4. Ambiguous acceptance reports, missing report IDs and stale dispatch authority.
5. Timezone/schedule rules, unknown/stale quota and insecure quota-source assumptions.
6. Unsafe filesystem paths, symlinks, permissions, secret exposure and unapproved work.
7. Linux systemd timer correctness and behavior after downtime.
8. Missing deterministic tests and unsafe release claims.

Produce a compact independent review:
- VERDICT: PASS / FAIL / BLOCKED (for code-review quality, not production approval).
- Exact branch/commit inspected or UNVERIFIED.
- P0/P1/P2 findings with path:line, reproduction, impact, fix, and a test.
- Whether actual cbds/OpenClaw integration was tested (assume NOT_RUN unless proven).
- Concrete prioritized tickets for a separate implementation agent.
- STOP if the code is not accessible; never invent a review or an acceptance report.

This is a pilot. Even an Argon code-review PASS cannot authorize unattended activation, merging, production DB writes, device flashing or deployment.

## Owner workflow

After the independent Argon chat review, paste its findings into the coding workflow. Codex or AGY repairs substantiated tickets in the isolated feature branch. Re-run offline tests and the host G4/G5 integration gates. Preserve every finding and reviewed SHA; do not erase blockers for a positive verdict.
