# V0.5 — ONE GO: recover AGY seat, finish W04, prove reusable runs
**Date:** 2026-10-22 IST · **Owner direction:** No more fragmented plans or false blockers. Use GPT-6.1-Sol at the highest practical effort, recover exited/missing workers, independently verify, finish the real W04 task, and make future Nightshift tasks repeatable. **One integrated manual execution**, no new framework.

## Important: proven V0.5 vs missing capability

- **Already PASS — do not repeat:** first Nightshift V0.5 one-shot launch, Codex→Manickam build/review/repair, local Git and morning report. Gate C final launcher exited 0 with `REVIEW_REQUIRED` (Astra read-only audit, owner-reported). Key local code: launcher `b3e91d44d0ab5d474578ccc0de5f62f2a3e7402f`, detection repair `45d7e8285617d1c231417d2ed643d7581d740911`, NutriSnap bill/reminder implementation `9934c6261c728c5a0dba9954b781a8b03fe29c12`. **These commits and evidence are unpushed local source**. `PUSH_HOLD` remains.
- **New reproducible gap (W04):** last Codex report `W04_BLOCKED`; `herdr` contained **only Codex `wE:p1`**, `ns01_manickam` and old `wD:p2` produced `agent_not_found`. NutriSnap `nightshift/2026-10-20-ns01` was clean at `9934c6261c728c5a0dba9954b781a8b03fe29c12`; **0 builder sends, 0 implementation, tests NOT_RUN**. Local blocker evidence `/home/openclaw/worktrees/agent-orch-v05-p0/docs/v0.5/evidence/W04_HYDRATION_WEEKLY_AVERAGE_RESULT.md` at docs-only commit `1b5303c9cf695f7e243e52055d69d03288bd6862` (owner-provided host report).
- **Root distinction:** `agent_not_found` means that named target is not currently a live agent; **not proof that the pane, underlying shell or authenticated AGY account disappeared**. Old pane IDs move and agent names clear on exit. Use current Herdr introspection, not historical mapping. The previous W04 document's "no extra seats" should be read as **no unnecessary extra models**; its unintended "STOP as soon as intended agent is absent" is **SUPERSEDED BY THIS OWNER-APPROVED RECOVERY**.
- **Today's outcome:** the same run must fix the **reusable AGY seat recovery path** and ship **W04 Hydration Weekly Average** with independently verified code. No second architecture round, H1–H5 rework, CBDS or Python-driven AI seat-orchestration redesign.

## One-run high-level plan: 4 milestones handled inside one Codex execution

### 1. Recover active Herdr machine/session and ONE intended AGY-Manickam builder

- From the actual OpenClaw host, inspect `herdr --help`, `herdr workspace list`, `herdr pane list`, `herdr agent list`, and `herdr pane process-info` as supported by installed version; inspect current Codex seat **`wE:p1`** as reported, but do not assume it stays `wE:p1`. Inspect startup history/local H3/H5 evidence for the **already authenticated Manickam AGY profile** and known working launch arguments. Do not guess a profile, create a new login, bypass approval or expose tokens.
- If a genuinely live, authenticated AGY-Manickam builder is already present: reuse that process. Else if an available **interactive shell** pane exists: choose it; if its pane CWD is wrong, move it to the existing NutriSnap isolated worktree using supported shell command before startup. Else **create exactly one** available shell pane in the existing OpenClaw Herdr workspace, or one workspace with root shell **only if no suitable workspace exists** (Herdr's separate layout primitive). Capture the returned fresh pane ID; **never infer `wD:p2`**. This layout recovery is explicitly permitted as necessary for the intended one builder role; no third/fourth model or Seat Creator.
- Start **at most one** AGY-Manickam process via actual installed Herdr CLI in the available shell, with `--kind agy` and existing verified profile arguments. Current Herdr documented shape: `herdr agent start manickam --kind agy --pane "$PANE_ID" -- <verified-existing-AGY-args>`; omit `-- <args>` if no args required. Verify the exact running model/account, approved worktree cwd and explicit safe idle; if alias `manickam` conflicts with stale name, resolve safely from live list rather than blindly retry. DO NOT prompt builder twice based on CLI timeout.
- **Normal folder trust:** Owner authorizes one ordinary exact-match first-use folder trust only for the **already used isolated NutriSnap W04 worktree** `/home/openclaw/worktrees/nutrisnap-nightshift-20261020-ns01` by the correct Manickam AGY identity, if the interface explicitly displays that folder and ordinary `Yes, I trust this folder`. Perform deliberately after verifying the dialog; log it. New path/account, broader privileges, login, secret, survey or any unclear dialog → `WAITING_FOR_HUMAN` once with exact pane and reason; never generic auto-Yes/Enter.
- **Visibility:** Keep one readable Codex coordinator pane, one Manickam builder pane and optionally existing status shell in the **same actual OpenClaw Herdr machine/session**. If the owner's Omarchy Herdr UI is attached to a different machine/session, explain exact UI target rather than spawning agent tabs for decoration. Do not claim a desktop tab opened unless verified.

### 2. Deliver W04 as real product code (no more preflight-only loop)

- Read `docs/v0.5/W04_HYDRATION_COMPLETE_RUN_PLAN_2026-10-22.md` from instruction Git; verify current **local** NutriSnap source at `9934c6261c728c5a0dba9954b781a8b03fe29c12` is clean. The **original** NutriSnap checkout has unrelated dirty files; DO NOT clean/stash/reset/switch it.
- A confirmed defect on remote NutriSnap main `src/app/hydration/page.tsx`: `weeklyStats.avgTotal = Math.round((totalWater + totalOther) / 7)`, incorrectly counts not-yet-elapsed days in the current week; remote source context only, check current local code.
- Task **W04**: elapsed current-week days **inclusive of today** are denominator (Monday 1, Thursday 4, Sunday 7). Completed historical weeks use 7, absent elapsed days count zero, future dates excluded/handled safely, no NaN/zero division; preserve weekday boundaries, local date semantics, water + other drink total, relevant progress widgets. Example: 6000 ml through Thursday → 1500 ml/day, not 857. Keep implementation focused on hydration page and tiny test helper if needed.
- **AGY-Manickam** is implementation author; coordinator sends one bounded developer prompt, author edits and creates local Git commit; Codex does **not** silently write implementation then claim its own review is independent. At most 2 concrete fix/retest cycles. On quota or ambiguous prompt delivery, inspect existing code/artifacts before any action; do not blindly resend.

### 3. Codex independent QA and repeat-run recovery proof

- Codex reads actual committed W04 diff/changed paths; independently executes deterministic focused tests (partial Thursday, current Monday, Sunday, old week, no logs, date boundary, stale/future logs, drink types), relevant preexisting tests, `npm run typecheck`, `git diff --check`, and local browser weekly UI check if test environment exists. Report browser `PASS`/`FAIL`/`NOT_RUN` honestly. No live production DB or deployment.
- For **repeat-run reliability**, verify **without another real coding prompt** that the newly running agent is discoverable through fresh `herdr agent list/get/explain`, the actual shell/pane can be targeted, and a *second task launch* could rediscover the seat dynamically rather than depending on deleted `wD:p2`. Run one read-only posttask readiness inspection (not a whole second W04 run). Codex can document one small role-discovery/reattach snippet if existing CLI lacks convenient behavior; **do not add a Python seat manager or scheduler**.
- If a newly started AGY process exits after completing W04, that's not a QA failure. Confirm the current shell/process state and state the exact supported reactivation command/steps next time. No need to keep burning tokens to prove model stays alive indefinitely.

### 4. One final report, one local code SHA and stop

- Write/update W04 local report with: `WORKER_RECOVERY_PASS` or precise reason, new/old pane IDs and profile verification result (never secrets), number of new shells/workspaces/process startups, prompts/repairs, exact W04 source commit, changed files, test commands/counts, browser verdict, local branch/clean status, next-run discovery/invocation instructions and any owner-only items.
- Return `W04_PASS + REPEAT_RUN_RECOVERY_PASS` only with real AGY implementation commit and genuine independently executed Codex checks. If either fails, report `PARTIAL` once with real code committed so far and exactly one unresolved hard blocker. **Do not call V0.5 unproven again**: one-shot V0.5 was already proven; this run closes the subsequent worker-recovery operational gap.
- Keep local worktrees/commits, `PUSH_HOLD` and user changes untouched. **Not authorized:** push, PR, merge, deploy, code changes to production DB/Telegram, new full Python agent orchestration, CBDS, separate agents beyond necessary intended builder recovery, scheduled/recurring background runs or auto-approvals.

## Exact boundaries so the team doesn't stop for every reversible step

**The owner explicitly authorizes** existing Herdr pane/shell inspection; creation of one necessary available shell pane or a workspace root shell if no workspace exists; one proper Manickam AGY startup using existing authenticated profile; one *exact matching* normal trust for the known NS-01/NS-02/W04 isolated NutriSnap worktree if visibly confirmed; W04 code/tests/local commit; Codex QA and up to two repair cycles; one final report. **No separate owner permissions required for those steps.** If a hardware/system credential, unrelated new folder, new account or elevated privilege appears, stop with details—not a general "we need approval" loop.

**Commit/evidence policy:** instruction documents in GitHub are not live OpenClaw scripts. Code commits are local; don't push because `PUSH_HOLD`. Do not create "proof" commits solely to mark a blocked check. Existing W04 blocker report stays as historical evidence and final success is a separate/result continuation.

## Verify feature and recovery, not abstract architecture

| Final evidence | Required |
|---|---|
| Live AGY-Manickam recovered/started in existing or one new shell | Yes |
| Correct worktree and actual authenticated profile/seat | Yes |
| One real W04 code commit authored by builder | Yes |
| Codex independent focused/related unit tests + typecheck | Yes |
| UI screenshot/browser smoke | If existing safe local harness available; otherwise exact NOT_RUN |
| No blind retries, bounded ≤2 repairs | Yes |
| Next-run live agent rediscovery method demonstrated | Yes |
| Final local branch clean, unmerged, report with SHAs | Yes |
| No push, deploy, scheduler or unrelated permissions | Yes |

## One small command to feed to Codex, not a copied mega-prompt

Open the **existing Codex agent-orchestration-lab project**, select **GPT-6.1-Sol, highest available effort (Extra High/xhigh preferred)**, fetch the instruction branch and ask:

> **Execute V0.5 one-go recovery + W04** from `docs/v0.5/V05_ONE_GO_SEAT_RECOVERY_W04_2026-10-22.md` on `origin/planning/v0.5-p0-handoff-20261019`. Owner approves recovery of one existing Manickam worker seat (including one shell pane if necessary) and W04 implementation/testing within the documented constraints. No separate preflight-only phase, no new architecture, no push/merge/deploy. Execute end to end and return code SHA, independent tests, repeat-run seat recovery proof and one final report. Stop only for a real unavoidable blocker.

**A model choice or a plan does not by itself execute OpenClaw.** This file is ready for that Codex invocation.
