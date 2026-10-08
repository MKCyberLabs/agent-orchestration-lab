---
name: cbds-orchestrator
description: Coordinate bounded Herdr coding workers with cbds durable results and an independent Sol reviewer.
---

# cbds orchestration V0.2

Read the project's `AGENTS.md` and the bounded task first. **Git commits and accepted cbds reports are truth; terminal text is not.**

1. ONE coordinator owns a cbds run. Before dispatch, inspect existing run/tasks/reports; reuse completed work and do not race another coordinator.
2. Classify tasks, assign nonoverlapping files, create isolated Git worktrees, dispatch named AGY identities. Record IDs.
3. Call ONE blocking `cbds wait` with an explicit timeout. No `herdr agent read`, idle loops, screen scraping, or repeated model "still waiting" commentary.
4. On an accepted report, independently verify Git SHA, worktree state, allowed files, test evidence and task outcome before integrating.
5. `BLOCKED` for missing product decisions. `FAILED` for execution faults. Timeout is **not** failure or completion: diagnose actual lifecycle mechanically, use bounded retry and stale-dispatch revocation.
6. Integrate into separate worktree; no merge to main; no prod credentials, DB writes or deployment.
7. Complex security/financial/invariant changes trigger Sol review against the **exact integration SHA**. First run token-free `scripts/preflight-codex-reviewer.sh`. Use `scripts/run-sol-review.sh` with noninteractive `codex exec`; no interactive Codex pane.
8. Read review `VERDICT` and `Reviewed commit`. Code FAIL means remediation; environment BLOCKED means fix tooling without lying about review. Do not call a cbds transportation `succeeded` an approval.
9. After interruption, create a fresh *conversation*, not a new cbds run; reload accepted reports and Git history; never redispatch completed tasks.
10. Record PASS/FAIL/BLOCKED/NOT_RUN for every gate, wake-ups, retries, manual interventions, duration, token counts if available and exact SHA.

**Stop conditions:** unverified identity, duplicate coordinator, shared checkout collision, CLI startup error, broken Codex sandbox, secret exposure, missing requirement, or reviewer SHA mismatch. Stop and surface a bounded blocker instead of guessing.
