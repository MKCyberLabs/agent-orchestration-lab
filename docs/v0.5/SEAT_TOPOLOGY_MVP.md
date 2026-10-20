# Nightshift V0.5 — Small Herdr seat/topology policy

**Final architecture decision (2026-10-20):** [Argon 4 happy-flow verdict — Python + Herdr CLI, no AI Seat Creator](DECISION_ARGON_HAPPY_FLOW_2026-10-20.md). This supersedes conflicting *future* statements below. **One persistent task worktree PATH per builder, one sequential Git task BRANCH per job; no new Herdr pane or new filesystem worktree per task.** The existing `agent-orch-v05-p0` results/planning worktree must not be branch-switched by worker tasks. A new dedicated builder directory needs explicit one-time owner trust; none is auto-approved. H5 existing Manickam trust permission is only for its exact earlier pane and planning directory.

Owner decision (2026-10-19): **Python chooses which existing Herdr seat handles an approved task. Do not open a new window or tab for every task. First-run bootstrap creates ONLY genuinely missing layout; subsequent runs reuse it.** This is an architectural policy / later implementation target, **not permission to create panes now**.

## Current already running cockpit — reuse in H3

| Role | Herdr pane | Responsibility | State |
|---|---|---|---|
| Operator / architect | `wD:p1` | Existing Codex High; owner-controlled planning/approval | Preserve; no new Codex session |
| Builder 1 | `wD:p4` | Existing authenticated AGY-Rohit interactive process | H1/H2 ready; H3 detector fallback currently blocks sending task |
| Status / human attention | `wD:p5` | Plain shell reading Python `state.json` and sanitized logs | Reuse; not an agent |
| Builder 2 | none yet | AGY-Manickam, real distinct authenticated CLI | Future milestone, no auto-start now |
| Reviewer | existing operator for MVP | Codex/Sol independent reviews only when worth quota | Future optional additional seat |

No virtual names masquerading as real account profiles. Status pane is NOT a worker.

## First-run / each-task happy flow

1. **Bootstrap once, only if missing and approved:** inspect Herdr workspaces/panes using read-only `herdr workspace list`, `herdr pane list`, `herdr agent list`. Reuse the current workspace and occupied panes. For a missing approved shell/status pane, Python may use documented `herdr pane split ... --no-focus` (or one named tab where layout becomes unreadable); store **returned** workspace/tab/pane/agent IDs in a tiny JSON mapping owned by Python. Never assume IDs survive all server moves or restarts; reconcile by real agent identity/process when needed.
2. **One builder = one stable dedicated task worktree PATH; one task = one local Git BRANCH and report, not a new directory or Herdr tab.** Python selects a real verified existing seat and serializes per builder; before branch switch require a clean worktree, pin and preserve prior task SHA, and ensure no other active process is using it. Never switch the orchestration planning/evidence worktree to a task branch. New fixed builder path needs exact one-time owner trust; no auto-approval.
3. **State flow:** `QUEUED → DISPATCHED → WORKING → (WAITING_FOR_HUMAN | NEEDS_INSPECTION | TESTING → VERIFIED_COMMITTED → REVIEW_REQUIRED)`. `WAITING_FOR_HUMAN` is red and pauses; no auto trust, retries or impersonated confirmations. Herdr `idle/done` only means the agent's turn appears settled; Python's allowlist/tests/Git are the success authority.
4. **Human attention:** show reason + exact pane + the action/folder being requested. Owner explicitly approves each new trust scope. Never send `yes`/Enter into an approval UI automatically.
5. **After task:** keep the same pane and agent alive and idle for the next authorized task. Preserve logs and commit SHA in Python's state. No auto-close/restart of operator panes.
6. **Future expansion:** add distinct AGY-Manickam when a real profile can be selected, then reviewer role when needed. Automatic timer, cross-project dispatch, push/merge and broader hardening are later owner-gated milestones.

## Implementation budget: happy flow first

For **H3 now**, do **not** implement first-run topology creation, a seat registry database, dashboard, multiple tabs, second AGY builder, fallback model dispatch or dedicated scheduler. Existing `wD:p1/p4/p5` are sufficient. Fix the existing Herdr detector, send the single already-approved AGY-Rohit prompt only on matched ready state, verify and commit locally, STOP.

## Source

Herdr official CLI and agent primitives:
- https://herdr.dev/docs/cli-reference/
- https://herdr.dev/docs/agent-automation/
- https://herdr.dev/docs/agents/
