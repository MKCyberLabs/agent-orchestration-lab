# MK Nightshift V0.5 — FINAL direction: agent-led, Python-light

**Date:** 2026-10-20 (Asia/Kolkata)  
**Decision:** **AI Orchestrator → Builder → Independent Tester → Owner merge**. Herdr hosts the seats. A small Python launcher/guard is support infrastructure, **not the brains of orchestration or code review**.

**Supersedes the Python-as-orchestrator portions of:** `DECISION_ARGON_HAPPY_FLOW_2026-10-20.md`, `SEAT_TOPOLOGY_MVP.md` and old H1–H5 future plans. Preserve H3/H4 verified evidence and code; do not rerun completed tests solely because the direction changed. This is an architectural decision **not** authorization to launch agents, modify Git branches, run another worker task or schedule cron.

## Owner's actual target

Owner approves up to 1–2 bounded project tasks *before night*. One dedicated **AI team lead** receives project context and task policy, starts from pinned Git base, opens/reuses real Herdr agents, assigns coding and testing to **different seats**, coordinates a limited repair loop, commits code to a **date-based night branch**, and leaves a concise morning report. **Owner alone authorizes final merge.** No automatic push, merge, production deploy, or recurring timer yet.

## Minimal role map

| Seat/role | Example agent | Responsibility |
|---|---|---|
| **AI Orchestrator / team lead** | **AGY-Manickam** (candidate) | Read requirements, plan minimal work, create `nightshift/YYYY-MM-DD` branch, use Herdr agent CLI to dispatch/collect tasks, interpret tester feedback, authorize bounded revisions, write morning report |
| **Builder** | **AGY-Rohit** (candidate) | Implement one assigned task; run developer-level checks; commit scoped changes to night branch; return SHA and notes |
| **Independent tester / reviewer** | **Codex High** (candidate) | Independently review code diff, run tests and focused negative cases, report **PASS/FAIL**, evidence and defect list; **not** the same agent that wrote the feature |
| **Python, optional starter/watchdog** | Non-AI script | Start/attach existing orchestrator once when approved; cap execution time, collect stdout/status/exit, record run ID, stop or flag quota/attention. **Does not decide code quality, create tasks, run review loops or manage all agent seats.** |
| **Owner** | Human | Approve tasks, project directory/folder trust, exceptional permission, final merge/release |

**These labels are proposed role assignments, not proof of live sessions.** Most recent H5 evidence: AGY-Manickam existing `wD:p2` with one exact folder trust owner-approved but outcome not reported; Rohit `wD:p4` shell-only; Codex High `wD:p1` active. Actual profiles, readiness and available quota must be verified before the pilot. A single person/agent cannot claim independent testing of its own work.

## Exactly one happy flow (one project / one night branch)

1. **Owner:** Approves project path, 1–2 task descriptions, safe file scope, pinned base SHA, branch prefix, max time/model budget, **at most 2 bounded repair iterations**, and manual-merge policy.
2. **Start:** Owner manually asks the existing **orchestrator seat** to begin. Python scheduler comes **later**: at most one start + watchdog + report. Orchestrator consults Herdr CLI, reuses known existing agent seats and creates missing *pane only if authorized*; no separate Seat Creator LLM. New trust/permission/survey prompts always ask owner; no auto-Yes.
3. **Branch:** Orchestrator, using ordinary Git under the approved repo, creates **one date-based local `nightshift/YYYY-MM-DD` branch** from the approved base **in an isolated task workspace**. If the branch already exists, stop/reconcile rather than reset or overwrite. Preserve all existing planning/results worktrees and `PUSH_HOLD`. One active Git writer at a time; tester works from the committed revision, not simultaneously editing the same working directory.
4. **Build:** Orchestrator sends one bounded scoped instruction to **Builder** through `herdr agent prompt`. Builder implements and commits in night branch (or hands patch/commit to orchestrator if operating in an isolated checkout). Return code SHA and tests run. No uncontrolled recursive delegation.
5. **Test:** Orchestrator sends the committed revision/diff and criteria to **independent Tester**. Tester runs executable checks, examines changed behavior and failure cases, returns clear PASS/FAIL with evidence. **Python exit code alone is not independent review.**
6. **Repair, bounded:** On FAIL, orchestrator sends *specific tester findings* back to Builder; at most **2** fix/retest cycles during the approved run. On quota, timeout, trust/approval/survey, unavailable seat or unknown Herdr state → **STOP, preserve branch and report**, no silent prompt retry. Avoid unlimited loops.
7. **Report/owner merge:** Orchestrator records branch, per-task commits, test results, remaining risks and exact next action in `morning.md`. Leave local branch untouched for owner approval. **No automatic push/merge/deploy**; separate owner permission required for any promotion.

## Constraints that make it simple and safe

- No AI Seat Creator. No Python `ensure_workspace_and_seat()` framework in the immediate pilot; **use Herdr's existing agent commands** from the orchestrator seat.
- Herdr explicitly supports **one agent creating work for other agents, inspecting status and collecting results**: https://herdr.dev/docs/agent-automation/ . `agent start` needs an existing available shell pane. Agent status can be `blocked`/`idle`/fallback; never infer code PASS from it.
- One **night branch per project per date**, e.g., `nightshift/2026-10-20`; multiple scoped task commits; owner chooses merge. Branch content is *not* automatically promoted to `main`.
- Avoid copying a date branch between two live worktrees (Git rejects a branch checked out in multiple linked worktrees). **One writer checkout per branch; reviewer reads committed SHA and uses a separate read-only checkout or tests after writer is idle.** No automatic branch switches under a running AGY process without checked clean state.
- Per-agent directory trust is separate. A pane can exist without trust; an AGY prompt may block. **Owner explicitly authorizes exact new trust scope**, not all future Yes dialogs.
- A delivery receipt says what truly happened: dispatched task(s), branches, builder/tester seats, code/test SHAs, PASS/FAIL, repair count, warnings, approval holds; not fictional completed work.
- At-most-once prompt submission after uncertain timeout/stall. Max task run time + max repair count. No additional roles, plugins, queues, databases or custom orchestration platform.

## Acceptance: stop analyzing and run a REAL proof

- [ ] Team-lead seat has an actual configured AGY profile and can issue one Herdr handoff.
- [ ] Builder receives **one owner-approved task**, makes a scoped local Git commit on `nightshift/YYYY-MM-DD`.
- [ ] Different real tester/reviewer receives the committed SHA/diff, runs checks and returns evidence-based PASS/FAIL.
- [ ] On one test FAIL, lead can direct **one** bounded fix/retest, or otherwise demonstrate STOP safely (do not invent a failure).
- [ ] Owner receives one morning-style report and alone decides merging.
- [ ] **Zero** automatic pushes, merges, deployments, folder approvals or recurring timers.

**Next implementation step (needs owner approval):** configure one real orchestrator seat with a **single stable role instruction file** and demonstrate ONE small approved project task through real builder + tester. Do **not** first build a new Python seat manager. Once the manual 3-seat happy path works, add the tiny Python launcher/timer only with separate approval.

## Why previous design drifted

We elevated a **Python dispatcher implementation detail** into the architecture's decision-making authority, treated "test command exited 0" as synonymous with independent quality verification, and created a new approval milestone for each local UI blocker. These are the lessons; stop expanding Python to fix a coordination problem. Keep the AI lead accountable for task assignment/review and limit Python to a minimal launch/guard role.
