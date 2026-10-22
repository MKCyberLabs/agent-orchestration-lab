# Nightshift — 20:30 scheduler PASS, Codex interaction BLOCKED: targeted repair
**Date:** 2026-10-22 IST. **Status:** diagnostic and repair specification only, no new timer created or code changes run through this GitHub file.

## Outcome and preserved evidence
- One-shot systemd timer `mk-nightshift-w03-20261022-2030.timer` **fired at 20:30:00.040 IST**. Unit is now inactive and has no next trigger.
- Existing authenticated Codex process reported idle; launcher **rejected sending** because observed TUI footer contained `xhigh` and **copy-selection controls instead of the expected normal composer**. Saved-evidence evaluation says changing `xhigh` to `High` alone does not fix composer readiness.
- **0 coordinator prompts**, **0 W03 work**, **0 retries**. Thus scheduler time firing PASS, unattended Codex dispatch NOT PROVEN, W03 NOT STARTED. Do not mislabel V0.5's earlier *manual* one-shot proof as failed.
- Evidence (OpenClaw host only):
  - `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2030-ist/scheduler-final-status.json`
  - `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2030-ist/post-trigger-review.json`
- Original NutriSnap dirty checkout, unmerged W04 PASS, `PUSH_HOLD` remain unchanged.

## ONE focused local repair, not another architecture phase

**1. Reproduce from saved evidence before touching the real seat.** Existing Codex High/Herdr operator inspects actual local launcher, readiness detector, snapshots and explicit manifest evidence. Determine whether copy-selection is a temporary TUI input mode, a terminal/Herdr selection layer, stale snapshot, or a different recognized screen. **Do not assume it is tmux or safe to dismiss it.** Inspect supported Herdr `agent explain --json`, `agent read --source visible` and `pane process-info`, as applicable. `idle` or `done` alone is not proof the composer will accept a task (Herdr fallback screen matching can misclassify prompts). Determine if readiness gate is too strict for benign UI vs correctly refusing a noninteractive mode.

**2. Separate effort policy from transport readiness.** `xhigh` may be an owner-preferred model setting and is NOT a substitute for composer readiness. If task packet specifically requires `High`, enforce it honestly or receive the owner's explicit change; don't silently elevate/reduce effort. A small code-level policy change may allow enumerated approved efforts, but NEVER use effort alone to declare safe input.

**3. Repair the smallest thing with tests.** Prefer a reliably supported Herdr agent prompt surface after **positive** safe-input evidence rather than timing-sensitive terminal footer checks. If the copy-selection view has a documented, reversible way to return to normal composer without submitting anything (for example, a verified safe `esc` action for a particular known mode), test it once against an exact, unambiguous state and re-read screen; never inject Enter, auto-Yes or cycle keys on unrecognized interfaces. Do NOT restart/kill the occupied authenticated Codex seat, replace Herdr, build a Python seat manager or switch globally to CBDS. Add deterministic fixture tests for (a) observed saved failing snapshot => no send, (b) verified normal composer => one send, (c) explicit blocked/unknown/fallback => no send, (d) xhigh and High labels independent of composer mode, (e) no duplicate dispatch on stalled/uncertain delivery.

**4. One local offline proof.** Run existing launcher tests + these focused cases; `git diff --check`. Commit minimal code/tests locally with SHA, preserve original scheduled run receipts and prior Nightshift commits. Report `READINESS_REPAIR_OFFLINE_PASS` only when real saved evidence and normal control snapshots both behave correctly. If unable to establish safe normal composer semantics, report `REQUIRES_INTERACTIVE_INSPECTION` and one precise, human-visible next action. Do not weaken the check to force PASS.

**5. Retest automatic submission separately.** A **new one-time calendar trigger** (not daily) is required for true end-to-end scheduler proof; do NOT silently rearm tonight's elapsed timer. Once repair passes, propose one exact next date/time for owner approval, and use the existing scheduler and launcher with a **fresh run ID**. If a simple manual handoff is used first, label it `MANUAL_DISPATCH_PASS`, **not** `SCHEDULER_PASS`. For W03, locate and verify the actual bug specification before writing an app change; do not invent a fix to demonstrate automation.

## Return one actionable receipt
`READINESS_REPAIR_OFFLINE_PASS` / `REQUIRES_INTERACTIVE_INSPECTION` / `BLOCKED` + verified root cause, exact changed file(s), local commit SHA, tests, what the 20:30 timer proved, and the next recommended **one-time scheduled** test. No push/merge/deploy/timer installation or CBDS.
