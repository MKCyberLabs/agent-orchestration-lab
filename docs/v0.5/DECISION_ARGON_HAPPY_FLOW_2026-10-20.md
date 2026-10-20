# Decision — MK Nightshift V0.5 happy-flow architecture

**Date:** 2026-10-20 (Asia/Kolkata)  
**Verdict:** **GO: deterministic Python + Herdr CLI, NO AI Seat Creator.** Reviewed Argon 4's completed one-time architecture assessment (its verdict: **APPROVE WITH SMALL CHANGES**). This records an architecture choice; it is **not** approval to launch agents, switch Git branches or run new coding tasks.

## Choices — stop the debate

- [x] **A / Seat owner:** Python Nightshift implements a **tiny opt-in** `ensure_workspace_and_seat()`: discover/reconcile the **current** Herdr server/agents/panes, reuse a real live seat, start an existing configured CLI profile in an available shell pane **only if bootstrap for that exact seat was authorized**, and create one missing pane only if needed. Cached IDs are hints, not identity. Herdr remains the UI/process layer; Python remains the only task/state/test/local-Git authority. No second LLM.
- [x] **1 / Worktree choice:** one **stable, persistent worktree path per builder**, sequential tasks as local `nightshift/<task_id>` branches in that path. One task per builder at a time. This limits ongoing trust churn. Never accept any agent's permission dialog automatically; any **new initial builder path** requires separate, exact owner trust once.
- [x] **Small adjustment to Argon's proposed initial path:** `/home/openclaw/worktrees/agent-orch-v05-p0` is the existing **planning/results worktree**, not a disposable task workspace. Manickam's prior trust approval there applies **only to that path and pane**; do **not** interpret it as permission for a new path or to check out task branches under the Codex operator's live working directory. Before the first coding pilot, create/select a **dedicated persistent builder worktree** with a pinned clean source and separately approved trust if its path is new. This adds **one** deliberate bootstrap trust per builder, not per task, and protects the H3/H4 planning/results branch.
- [x] **At-most-once task:** persist task ID / branch / prompt digest as `DISPATCH_INTENT` **before** the send (not proof of delivery); no second send after timeout/stall/unknown until owner reconciliation. Safe `idle` requires real matched agent detection and screen. `blocked` / survey / trust = `WAITING_FOR_HUMAN`; fallback `idle` = `NEEDS_INSPECTION`. Python's allowed-path audit, host tests and local Git SHA—not Herdr idle/done—prove completion.
- [x] **Window choice:** persistent Herdr workspace and pane per builder; no new tab per task, no status polling LLM, no separate AI reviewer launched merely for UI.
- [x] **Release safety:** `PUSH_HOLD` remains, no production / auto-push / auto-merge / deployment / cron / systemd without separate owner approval.

## What has already passed — NEVER reopen

- [x] Python → actual Codex CLI → host tests → local Git.
- [x] H3 manual Python → Herdr AGY-Rohit real task: 1 prompt, 0 retries, host acceptance PASS despite transient survey hold.
- [x] H4 adapter integration: 49 integration + 11 detector checks PASS, local code `005b596581128925d11c0ab53e20fda6e1f44d5b`.
- [ ] H5 existing Manickam `wD:p2` **post-trust readiness** has not yet been reported; owner already approved one exact trust acceptance in the **planning** worktree. Rohit `wD:p4` most recently appeared shell-only. Do not assume two live seats.
- [ ] Persistent builder worktree bootstrap and **two sequential approved tasks reusing one seat** have not been demonstrated.
- [ ] Unattended one-time run and recurring scheduling have not been demonstrated or authorized.

## The only implementation scope worth building next — 3 outcomes

1. **Finish the already-approved H5 gate**: accept the precise existing Manickam folder trust **only if it is still pending for the exact pane/path**, verify explicit nonfallback ready state and commit local evidence. No additional agent startup/task.
2. **One bounded Python improvement, offline tests:** extend the existing H4 adapter (not replace it) with `ensure_workspace_and_seat()`, a tiny explicit seat config and branch/clean-worktree preflight; persist dispatch intent once and fail closed. Do not make a new window/seat creator framework. Work in an isolated development branch/worktree with owner approval, not by changing the live planning worktree.
3. **Pilot after separate exact task authorization:** initialize ONE dedicated stable AGY-Manickam builder path, get one owner approval if new folder trust appears, then run **two small approved tasks sequentially** on clean local task branches, reusing one Herdr seat; record 0 repeated startups/trusts, test results, local Git SHAs and morning-style report. Stop for review. No timer; do not recruit Rohit/second worker until this single-seat pilot works.

### Success = one short receipt

`SEAT_REUSED=YES | NEW_PANES=0 after bootstrap | AGY_STARTUPS=0 after bootstrap | TASKS=2 | PROMPTS=2 (one each) | HUMAN_APPROVALS=0 after first path trust | TESTS=PASS | LOCAL_COMMITS=2 | REPORT=PASS | PUSH=0`

If a real new trust/survey appears, stop and report the **actual** owner action; do not force the optimistic receipt.

## One concise Codex instruction (PROPOSAL — NOT EXECUTION AUTHORIZATION)

> Read `docs/v0.5/DECISION_ARGON_HAPPY_FLOW_2026-10-20.md` via `git show`. Preserve H3/H4 and H5 evidence. Once separately authorized, add a small deterministic `ensure_workspace_and_seat` to the maintained H4 Python runner: inspect live Herdr JSON, reuse genuine existing AGY profile/pane, start in a free shell only if configured/owner-approved, never auto-trust; pin clean dedicated persistent builder worktree, make one sequential `nightshift/<task_id>` branch per task, persist at-most-once dispatch intent before send. Offline tests first; then stop. Do not run worker tasks, change the planning worktree, open more than one missing pane or enable timers without new scoped authorization.

## Why this beats Argon's unmodified worktree example

Argon chose **A + 1**, correctly prioritizing deterministic CLI and a stable path. Its example reusing the current `agent-orch-v05-p0` planning worktree for branch checkouts is acceptable only if that directory is truly dedicated and free; in our real deployment it holds important H3/H4 results and can be open in the operator's own process. We therefore dedicate a separate stable path per builder **once**, preserving the no-trust-prompt-per-task benefit while avoiding hidden cross-agent Git branch switching. This is the only substantive small change.

**No new planning framework. Next measurable result: first two approved tasks in one reusable builder seat.**
