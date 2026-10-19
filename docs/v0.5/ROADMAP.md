# MK Nightshift — phased roadmap

Planning baseline: 2026-10-19. **Current status: MANUAL SINGLE-CODEX DEVELOPMENT LOOP PROVEN (per OpenClaw execution receipts); UNATTENDED NIGHTSHIFT NOT YET APPROVED.** Later roadmap items remain proposals, not implementation permission.

## ✅ Progress scoreboard — owner review, 2026-10-19

This scoreboard is the short status summary. Historic phase descriptions below are future-oriented; **do not reset checked milestones** because an older plan mentions more ambitious tests.

| Outcome | Check | Evidence / scope |
|---|---|---|
| P0 — source, task contract, runner choice | ✅ **DONE** | Local planning/report commits reviewed via user-provided host reports; Python is sole task dispatcher |
| P1A — real Codex CLI launched by Python | ✅ **DONE** | One `TEST_ADD` real headless execution and host assertions PASS; fixture `06c84ae2bc1788c8c42046ad13b8de08cb387b97` |
| P1A — real worker logs/test/commit/stop | ✅ **DONE** | Evidence commit `2f772d8eb691f81abeabf4ff22f25aeb5730fd4d`; no retry or push |
| W02 — one real NutriSnap coding task through Python runner | ✅ **DONE** | Native Codex child PID 188615, launcher PID 188608; JSON `turn.completed`; runner exit 0; `W02_330ML=VERIFIED_COMMITTED` and campaign `REVIEW_REQUIRED` |
| W02 — exact 330 ml input implemented, local code committed | ✅ **DONE (implementation)** | NutriSnap `ee135be8173eea5ad499b23838e0a049c814e991` → local `e072c80cc50b5a5fe9a199d2b93b4059807331ba`; evidence `bb2c84a63197038734c9fe14297f203197c44093` |
| W02 — offline component / validator tests | ✅ **DONE** | PASS per OpenClaw W02 result; broader project typecheck FAILED with reported unchanged baseline diagnostics (not evidence of a W02-introduced regression) |
| W02 — browser reload, Water/Today totals and cross-user DB UAT | ☐ **PENDING — product acceptance lane** | No verified isolated disposable database; tests correctly `NOT_RUN` |
| Herdr — visible real AGY/Codex seats and handoffs | ☐ **NEXT PRIORITY — seats lane** | Existing Herdr pane worked, but headless Nightshift processes are NOT yet live named Herdr seats. Next test one real recognized CLI seat, then Python↔Herdr handoff. [Seat MVP](../../prompts/V0.5_HERDR_SEATS_MVP.md) |
| Nightshift — unattended one-time no-push trigger and recovery | ☐ **AFTER SEAT PROOF — automation lane** | Manual runs proven. No timer installed or night automation activated |
| GitHub push, auto-merge, deployment, sensitive environment hardening | ⏸ **HOLD / LATER** | `PUSH_HOLD` persists; 6 AM merge scheduler context unverified; no production changes authorized |

**Meaning of DONE:** A completed scope stays checked. The **Nightshift manual build → host tests → local Git commit → report loop is demonstrated** on both a disposable fixture and a real W02 code task. The **full W02 product behavior is not accepted** until isolated DB/browser UAT; it is a **separate product lane**, not grounds to re-open the worker-launch milestone.

**Source qualification:** These detailed process receipts, Git SHA results and test outcomes were supplied from OpenClaw by the owner. The remote instruction-branch reviewer cannot independently fetch OpenClaw-only commits/logs while `PUSH_HOLD` is active. Preserve this distinction without reopening redundant verification.

### Next outcomes — ordered tracks (not extra planning phases)

1. **Finish NutriSnap W02 product UAT:** using [focused UAT instruction](../../prompts/V0.5_W02_ISOLATED_DB_BROWSER_UAT.md), run one disposable PostgreSQL + real browser test (entry, persistence, reload, Water/Today totals, cross-user denial). Close the W02 UAT checkbox only with observed results. This does NOT reopen completed W02 implementation or Python worker milestones.
2. **Herdr + real seats: next main Nightshift milestone:** use [minimal Herdr seat milestone](../../prompts/V0.5_HERDR_SEATS_MVP.md). Reuse current Herdr instance, visible operator/log/build/review panes, verify a **real** AGY-Rohit builder CLI seat and AGY-Manickam separately, plus Codex reviewer. A named tab is not an authenticated seat. Python remains sole dispatch/commit authority; one separately approved Herdr-visible work handoff must actually finish to check the seat milestone. Do not demand a new OS user or new agent framework.
3. **Unattended operation:** one approved time-bounded **no-push, no-merge** task starts without an operator prompt, recovers/stops safely, and produces morning report. Only then consider a daily timer, with clear owner approval and 6 AM Git scheduler safety.
4. **Release / expansion:** owner reviews and promotes local changes; only later broaden to two builders/two projects, production, push/merge and environment hardening.

**Working rule:** Keep checkmarks for completed manual worker/W02 implementation. Each follow-up phase should produce one visible running capability, not another broad security/architecture dossier. Stronger isolation and production push safety are deferred; they are not silently considered solved.


## Owner update — 2026-10-19: DEV-FIRST MVP (applies to one disposable P1A fixture)

The owner prioritizes **proving a working V0.5 Nightshift coding loop** on the existing OpenClaw development server, rather than further security-framework or multi-user setup. For **one manual disposable Codex TEST_ADD only**, use the existing `openclaw` user and privately owner-matched Codex CLI account, accept the explicitly documented residual same-user isolation risk, and run a single task with time/path limits, real host tests and local Git evidence. No new user, re-login, container, token decoding or renewed isolation reviews for this fixture. See [decision](decisions/DEV_FIRST_FIXTURE_POLICY_2026-10-19.md) and [one-task instruction](../../prompts/V0.5_P1A_DEV_SINGLE_TEST_ADD.md).

**Future hardening before broader unattended/sensitive use:** unprivileged worker isolation; reduced environment, mounts/sockets and egress; proof of headless identity where materially needed; service/timer and 6 AM Git merge safety. Existing `ISOLATION_NOT_VERIFIED` remains factually true. This temporary dev-first exception is not permission to access unrelated credentials, DBs, Telegram, services, or to push/merge/deploy.

## Definition of success

In the evening the owner approves one or two bounded issues. Overnight a verified, intended CLI account produces isolated, test-backed commits, or an honest blocker. In the morning a concise report cites real commits, commands, outcomes, identity evidence and next decisions. No unapproved promotion to production.

## Dependency graph

```mermaid
flowchart TD
  A["V0.5 P0 — Discover truth"] --> B["P1 — Seat / account integrity"]
  B --> C["P2 — Task contracts and knowledge"]
  C --> D["P3 — Real night-run proof"]
  D --> E{"V0.5 gate passed?"}
  E -->|Yes, owner authorizes| F["V0.6 — Herdr/cbds coordination experiment"]
  E -->|No| G["Repair only failed acceptance criteria"]
  G --> D
  F --> H["V0.7 — Context maturity / refocus"]
  H --> I["V0.8 — Risk-based SDLC skills"]
  I --> J["V0.9 — Two workers / two projects"]
  J --> K["V1.0 — Reliable nightly outcomes"]
```

## V0.5 — Four gated phases

### P0: Verify truth and make project knowledge navigable (NO code edits in P0.1)
- **P0.1** Read-only inventory: orchestrator branch/HEAD/status, V0.4 runner/smoke/tests/timer, CLI help and auth viability (without exposing secrets), Herdr/cbds installed facts, existing host fixture evidence; NutriSnap branch pointers and conflicting docs.
- **P0.2** Architecture decision record: Python JSON runner is sole authoritative *night* dispatcher in V0.5; Herdr used for interactive control, cbds not dual-writing campaign state. Specify any proposed changes; no runtime edits yet.
- **P0.3** Propose a shallow NutriSnap `AGENTS.md` entrypoint to existing authoritative docs. Do not overwrite the NutriSnap repository without separate owner approval.
- **P0.4** Source-address map: app frontend/API, Prisma, shared scheduler, Python analysis API, Telegram adapter, isolated test setup, build/test commands. Each entry says verified/unverified.
- **P0.5** Evidence hierarchy: Git SHA + commands + logs for implementation, owner decisions for requirements, cbds or runner state for execution *only in the active chosen architecture*. No model narrative accepted as proof.
- **P0.6** Identify genuine blockers: verify both actual V0.4 smoke tasks `VERIFIED_COMMITTED` (not just `REVIEW_REQUIRED`), interruption recovery, account/profile, quotas, timer state, full real-project readiness.
- **P0 exit:** a fresh agent can locate the correct NutriSnap branch/SHA, reminders code, tests, non-goals and next approved issue in no more than two short entrypoint reads plus targeted links. Contradiction = HOLD.

### P1: Identity, chairs and handoffs
- Define **Owner** (intent/release), **Python Dispatcher** (only launcher), **Builder** (AGY-Rohit OR AGY-Manickam as verified selected), **Reviewer** (independent Codex when warranted).
- Registry fields: seat ID, real CLI executable/version, profile selector and redacted identity receipt, approved worktree, role/skill file, scoped task, time budget. Never store tokens, cookies or private authentication files in project docs.
- Worker requests a handoff, **dispatcher launches** real intended CLI; no nested/in-process agent substitution or undocumented quota fallback.
- Test both AGY identities in separate sandbox trials; test wrong profile, absent binary, expired login, duplicate task, invalid worktree and quota exhausted.
- **P1 exit:** attributable external launches for both account seats; wrong-identity negative test reliably BLOCKED. No real production changes.

### P2: Owner intent, issue and context contract
- One issue record: ID, desired user outcome and why, explicit approval, source branch/SHA, code/knowledge addresses, allowed paths, forbidden work, dependencies, acceptance commands, responsible seat, real question/decision route.
- Skills initially **three only**: Project Steward (find existing design first), Engineering Standards (SOLID/DRY/KISS/YAGNI/security and local conventions), SDLC Execution (plan/build/test/review/handoff). Load by task, not every skill every turn.
- Knowledge trust labels: PROPOSED (idea), OBSERVED (claim/measurement), VERIFIED (source/test backed), APPROVED (authorized product decision). VERIFIED is not automatic owner approval.
- Add a short **Lessons** note only for a reproducible failure: nested subagent substitution, stale V0.1 route, creating a second scheduler, lost review evidence, excessive architectural expansion.
- **P2 exit:** fresh AGY worker can find an existing service, explain the intended change, distinguish approved vs merely proposed behavior, ask one decision-quality question, and produce a bounded task plan.

### P3: Nightshift proof and safety
- Reproduce two disposable fixture tasks with **real headless CLI**, exact SHA, logs/tests and accepted report states. Mocked suite PASS does not satisfy live proof.
- One **separately approved** low-risk NutriSnap change in isolated Git worktree with isolated DB / mock integration. Run real deterministic tests; independent review only where risk warrants.
- Negative cases: timeout, quota, bad profile, dirty worktree, disallowed path, invalid tests, process interruption, misleading worker success, inability to continue safely.
- Fail closed; preserve evidence and changes on blocked worktree. Recovery may be **manual/explicit**. No silent reset/clean/retry.
- Verify server clock and systemd context. Timer installation/enabling requires separate owner approval and successful host preflight.
- Morning report must distinguish IMPLEMENTED/TESTED/REVIEW_REQUIRED/APPROVED/RELEASED, identify real worker label, exact commit, actual commands/results, known blockers and next owner decision.
- **V0.5 exit:** at least one real approved non-production Nightshift change verified, both account identities proved in separate trials, controlled interruption preserves evidence, no unauthorized actions, and owner explicitly authorizes V0.6.

## Later versions (ideas, not implementation permission)

| Version | Borrowed lesson | Smallest experiment | Exit |
|---|---|---|---|
| V0.6 | Durable addressable seats | Python boots Herdr panes and verified CLIs; cbds becomes sole task ledger **only for this separately authorized experiment** | Single question/reply/done handoff survives restart |
| V0.7 | Navigable world/context and epistemic maturity | Context refocus after restart/compaction; stale-pointer check; evidence-backed lessons | Fresh agent and resumed agent avoid duplicate feature |
| V0.8 | Consistent engineering | Kanban → design when needed → build → tests → risk-based review → owner acceptance; targeted skills | Feature completes SDLC without extra bureaucracy |
| V0.9 | Specialization only when useful | Two bounded non-overlapping workers and separate NutriSnap / MK Desk Pet maps | No worktree collisions or account confusion |
| V1.0 | Outcome over agent count | Short owner-approved backlog → unattended verified increments or blockers → morning review | Repeated useful night runs with traceable evidence |

## Stop conditions

Any conflicting authoritative SHA; inaccurate claim of a passed test; unexpected profile or nested agent substitution; product decision requiring owner input; failure to isolate database or credentials; dirty/unowned worktree; exhausted quota; stale/competing dispatch state; attempted auto-merge/deployment; unauthorized scope enlargement.

## Every phase report (keep compact)

1. Phase/step and date, inspected exact Git branch/HEAD.
2. Confirmed facts + evidence paths, unknowns clearly separated.
3. Tests really run (command/exit status) and NOT_RUN items.
4. Risk, blocker, owner decision required.
5. Recommendation: PASS / FAIL / BLOCKED / NOT_STARTED.
6. Only **one next proposed step**; do not dispatch it until authorized.
