# Nightshift — 21:50 IST headless calendar trigger: SINGLE END-TO-END PROOF

**Owner authorization:** One-time Nightshift test at **Thursday 22 October 2026, 21:50 IST** (**16:20 UTC**) on the existing OpenClaw VM. **This is NOT a daily/nightly recurring schedule**, and it does not approve merge, push or production actions.

**Task of this run:** prove that the real calendar timer invokes the proven **noninteractive** Codex transport, that it delivers **exactly one** approved read-only W03 discovery task, and that a matching fresh completion report is validated. **Do not touch interactive Codex TUI or Herdr pane, auto-dismiss selection mode, or start AGY-Manickam.** A shell/systemd probe pass alone is not this final calendar proof.

## Known source / status

- 20:30 & 21:05 IST **systemd timers both fired on time**, both blocked *prior to sending* because the interactive Codex terminal switched to transcript-selection mode; 0 sends, 0 W03 work. **Do not reuse those expired timers, receipts or old mode.**
- **HEADLESS_TRANSPORT_READY (owner-reported):** local OpenClaw `agent-orchestration-lab` code `0a287c691a8dcd80f5b577bfa8db159ba0948bcf`, **shell and same-user systemd real headless smoke PASS, 84 regression tests PASS**, preserves lock, timeout, reports and safe failures. Evidence `/home/openclaw/worktrees/agent-orch-headless-20261022/docs/v0.6/HEADLESS_TRANSPORT_RESULT_2026-10-22.md`. Local-only commit; do not presume GitHub instruction branch includes code.
- NutriSnap W04 PASS at local isolated branch `nightshift/2026-10-20-ns01`, SHA `8a13c3c77250b829292fd47f28365b34cda6425e`; prior Manickam recovery PASS. `PUSH_HOLD`, no merges. W03 specific behavioral bug not yet confirmed in remote backlog.
- The required transport is **headless**, using the **already committed** implementation, not a new `codex exec` wrapper or separate scheduler.

## Exactly one 21:50 setup — MUST finish before trigger

1. In an **existing plain OpenClaw shell**, check the actual `date -Is`, OpenClaw username, `systemctl --user` access, current Nightshift headless code/worktree and clean git status at `0a287c691a8dcd80f5b577bfa8db159ba0948bcf`. Read the existing headless result file to reuse the **tested CLI/launcher contract**. No source edits or new regressions required.
2. Prepare a **fresh unique run** `W03_HEADLESS_SCHEDULE_PROOF_20261022T2150IST` with evidence under
   `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2150-ist/`.
   Use a single run packet, one existing launcher/wrapper invocation, safe timeout/lock and separate stdout/stderr and exit receipt. Avoid printing secrets. The packet must explicitly select **headless Codex High** with the authenticated existing account as supported by actual installed headless code; do not depend on any interactive footer or compose screen.
3. The **read-only task** for Codex:
   - Inspect the local isolated NutriSnap night branch and confirm reported W04 SHA and current cleanliness without modifying it.
   - Find actual available W03 hydration date/time specification, observed defect/repro or exact missing requirement from local backlog/docs/source. If underspecified, return `W03_NEEDS_SPEC` with short evidence and acceptance question—not a guessed fix.
   - Produce run-specific fresh structured completion and `morning.md` as required by the real launcher validation contract, including the correct run ID, no code edits/AGY prompts, source evidence, completion status and result. Keep final answer concise.
   - No commits, database mutations, browser interactions, service startup, external messages or production actions.
4. Install **exactly ONE** new one-shot `systemd --user` timer/service, e.g. `mk-nightshift-headless-20261022-2150.timer`. No `Persistent=true`, `Restart=always`, `OnUnitActiveSec`, recurring `OnCalendar`, cron, or extra timers. Use the **verified same-user service environment** and stored auth without copying secret files. Validate effective trigger with `systemd-analyze calendar` (or installed equivalent) and `systemctl --user list-timers`: **2026-10-22 21:50:00 IST / 2026-10-22 16:20:00 UTC** and exactly one activation. Review actual service `ExecStart` and executable/env before enabling.
5. If local time has already reached/passed **21:50 IST** before arming, **DO NOT** execute immediately or silently defer: `MISSED_WINDOW`, return precise status. If a wrong user/systemd auth/context or unexpected privilege is required, return `BLOCKED`; do not reauthenticate, escalate, or change linger. After `SCHEDULE_ARMED` is verified, **end this setup Codex turn promptly** so it doesn't consume available quota; headless execution does not need an interactive composer to be idle.

## After trigger — one externally fired Codex execution

- systemd user timer fires 21:50; starts existing wrapper **exactly once**; wrapper runs **existing headless Codex transport**. No TUI readiness checks or pane-input path. No blind retries on unknown process delivery; retain run lock and timeout.
- Validate **independent observed calendar timestamp** + one unique launcher/headless invocation + actual prompt/task received and completed + matching `run-id` structured receipt and `morning.md`. Process exit 0 alone is insufficient. Report differences between `SCHEDULER_FIRED`, `HEADLESS_DISPATCHED`, `TASK_COMPLETED`, and `REPORT_VALIDATED`.
- Output final status to `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2150-ist/scheduler-final-status.json` per existing wrapper contract, with run ID, observed timestamps, service/process exit, delivered prompt count, report paths, terminal verdict. If original wrapper names differ, follow **actual implementation** and include exact paths in arming receipt.
- On partial failures, capture **one** concrete blocker; do not schedule retry, alter auth, force default sandbox or bypass account/safety gates.

## Required verdicts

- `SCHEDULE_ARMED`: exact single 21:50 timer active/waiting; verified service runs headless, unique run state paths. No code change.
- `SCHEDULED_HEADLESS_END_TO_END_PASS`: actual calendar trigger + exactly one successful authenticated headless Codex task + real fresh validated matching report, no forbidden actions.
- `SCHEDULED_HEADLESS_PARTIAL`: triggered but dispatch/report incomplete, with precise receipts.
- `MISSED_WINDOW` / `BLOCKED`: no timer installed or task run.
- `W03_NEEDS_SPEC` is an acceptable **task outcome** for read-only discovery if backed by evidence; **never call that a W03 code-implementation PASS**.

## Hard safety boundary

No AGY builder/startups, no CBDS integration, no interactive Codex TUI, no third-party access, no production DB/app writes, no git push/merge, no auto trust, no remote deployment, **no recurring timer**, no new framework or launcher rewrite. Keep `PUSH_HOLD`. Successful scheduled dispatch is a capability proof, not authorization for unattended write-capable development until that additional end-to-end path is verified safely.
