# MK Nightshift — fresh one-shot 21:05 IST automatic Codex dispatch proof

**Owner authorization:** 2026-10-22, **21:05 IST = 15:35 UTC**, one run only on existing OpenClaw VM; **NOT** recurring/daily. This supersedes any suggested 21:15 retest. Do not modify/reactivate the completed 20:30 timer. **This GitHub document does not install a timer on the VM.**

## Ground truth and scope

- Earlier `mk-nightshift-w03-20261022-2030.timer` **FIRE PASS at 20:30:00.040 IST**, but coordinator prompt rejected because the real Codex UI was in **transcript-selection/copy mode** and showed `xhigh` outside approved default effort. It sent **zero prompts**. Evidence `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2030-ist/{scheduler-final-status.json,post-trigger-review.json}`.
- Later **`READINESS_REPAIR_OFFLINE_PASS`**: local Nightshift code `973616b802f44fc3fce15a34d70f7e731c524b5b`, 30 launcher tests and four captured-screen replay cases PASS. New logic correctly rejects transcript-selection and requires positive normal composer evidence; effort policy independent of readiness. Default approved effort **High**. Xhigh requires separately explicit task packet authorization; none is granted by this file. Check current local source at this SHA, clean worktree, and `docs/v0.6/W03_READINESS_REPAIR_RESULT_2026-10-22.md` before arming.
- V0.5 manual one-shot code/QA and W04 product changes already PASS. CBDS optional pilot succeeded but savings unproven; **do not introduce CBDS** or repeat feature tests tonight.
- Owner wants to verify **automatic scheduled Codex submission AND fresh matching completion report**, not yet implement a potentially underspecified W03 bug. **Tonight's packet is a short read-only W03 discovery check**. Once automated dispatch is proven, schedule coding work separately.

## Explicit one-run task packet

Title: `W03 Scheduled Auto-Dispatch Verification + Hydration Date/Time Discovery (read only)`.

Run ID: `W03_SCHEDULE_PROOF_20261022T2105IST`. State directory:
`/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2105-ist/`.

Coordinator task (Codex **High**, **no child/builder required**):
1. Confirm the local isolated NutriSnap worktree still contains already accepted W04 commit `8a13c3c77250b829292fd47f28365b34cda6425e` and preserve its Git state. Do not check out/reset/stash/rebase/commit or modify any app source.
2. Inspect **locally available** backlog/notes/source for the next candidate W03 hydration date/time problem, identify precise actual-vs-expected behavior and a reproducible acceptance example, or label `W03_NEEDS_SPEC` if local evidence is insufficient. No invented bug diagnosis, no tests that mutate database, no production usage, no agent starts or code changes.
3. Emit the launcher-required **fresh matching run-specific structured report** and concise `morning.md` for this run ID, including verified local file evidence, no-code-changes assertion, actual elapsed/attempted prompt count, and `DISCOVERY_COMPLETE` or `W03_NEEDS_SPEC`. If the launcher requires a standard report schema, follow its **exact actual local schema** rather than invent a JSON schema or bypass freshness validation. No fake builder commit.
4. Finish. The complete deliverable is a **valid scheduled task execution/report**, *not* a `W03_PASS` implementation verdict.

## Arm 21:05 precisely — one existing launcher via one-shot systemd

**NOW, before 21:05 IST**:
1. From OpenClaw, examine actual time/timezone `date -Is`; existing **corrected** launcher `scripts/nightshift_once.py --help` and its documented tests, original 20:30 schedule wrapper/units to reuse configuration, `herdr agent list` and Codex TUI's **normal empty composer**. Do not use historic pane IDs or a different Herdr machine/session. **If Codex is still in transcript-selection/copy mode, use only a verified reversible, non-submitting UI exit for that exact known mode** and confirm via fresh Herdr evidence; don't inject Enter or trust prompts. Don't bypass/reduce readiness checks. Set/verify **High** before coordinator turn exits and confirm the shell is not occupying the coordinator input seat. The selected model name or a guessed footer is not evidence of readiness.
2. Create a new run-specific packet and wrapper under `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2105-ist/` with restricted permissions. Reuse the known working launcher exactly **once** with the correct verified flags, existing run lock, bounded timeout and fresh report paths; no ad hoc new agent launcher. Wrapper records start time, exit status and exact returned receipt. No duplicate dispatch after an ambiguous timeout.
3. Install **one new exact, one-shot systemd user timer** e.g. `mk-nightshift-proof-20261022-2105.timer` (matching service `mk-nightshift-proof-20261022-2105.service`). Verify systemd calendar **2026-10-22 21:05:00 Asia/Kolkata = 2026-10-22 15:35:00 UTC** with `systemd-analyze calendar` and `systemctl --user list-timers --all`, test service executable/environment/Herdr socket accessibility without actually sending, and confirm `active (waiting)` with exactly one next activation. No recurring `RRULE`/daily `OnCalendar`, no restart and no unattended rerun. Do not modify system linger/privilege. End this Codex setup turn **before** 21:05 so Codex is positively idle and the repaired normal-composer readiness gate can pass. If time has passed, do **not** silently shift or launch manually: report `MISSED_WINDOW`.
4. The external systemd timer, **not the occupied Codex setup turn**, invokes the wrapper at 21:05. Fresh receipt must correlate same run ID, once-sent coordinator instruction, independent observed activation, and matching completed read-only discovery report. Do not claim success based on mere timer fire.

## Verdicts and verification

- `SCHEDULE_ARMED`: correct one-shot timer installed/waiting; exact 21:05 IST/15:35 UTC next activation; run ID, unit names and paths emitted; Codex setup turn ends.
- `SCHEDULED_DISPATCH_PASS`: 21:05 timer fired + valid composer/effort + **exactly one real Codex prompt delivered** with evidence.
- `SCHEDULED_END_TO_END_PASS`: above, plus **fresh matching run-specific completed report** from Codex that passes existing launcher validation; W03 product outcome **DISCOVERY_COMPLETE** or **W03_NEEDS_SPEC**, not W03 implementation PASS.
- `SCHEDULED_DISPATCH_BLOCKED`: report exact saved status (copy-selection or effort or other) and zero-send, no retry.
- `SCHEDULE_FIRED_COMPLETION_BLOCKED`: one confirmed send, no completion report; preserve evidence, no second send.
- `MISSED_WINDOW`: setup not armed before 21:05; do not reschedule without owner request.

Return event/run evidence paths and timestamps, coordinator effort and readiness verdict, prompt/send count, launcher exit, status of both report files and whether timer is inactive/no recurrence. Original local NutriSnap/nightshift branches, W04 result and `PUSH_HOLD` unchanged.

**Safety:** No CBDS integration, no new agent account/startups, no git push/merge, no production changes, no app code modifications, no auto-trust, no prompt retries, no new Python orchestration. Exactly **one** calendar-driven dispatch attempt.
