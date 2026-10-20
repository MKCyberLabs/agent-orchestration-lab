# MK Nightshift V0.5 — Owner authorization, Gate B only

**Date:** 2026-10-20 (Asia/Kolkata)
**Status:** **OWNER APPROVED FOR ONE BOUNDED LOCAL IMPLEMENTATION AND OFFLINE TESTS.** Execution on the OpenClaw host is **not yet confirmed**.

## Owner's exact instruction

> I authorize V0.5 Gate B: use Codex High to implement and locally test a minimal one-shot Python/OS launcher for the already-proven Codex→Manickam→independent QA workflow. Reuse existing code and Herdr seats. Enforce one dispatch, timeout, logs and report checks. No new framework, CBDS, extra seats, automatic trust, push, merge, deployment or recurring scheduling. Commit locally and stop for review.

## Allowed once

- Use the **existing Codex High operator** to inspect and minimally extend the **maintained OpenClaw-local Nightshift implementation** and already-proven Herdr integration where reusable (H4 local source `005b596581128925d11c0ab53e20fda6e1f44d5b`). Do not fetch/uncritically overlay a remote instruction branch onto the host's private local code.
- Implement a **single entrypoint** taking an owner-approved, bounded coordinator instruction/task file and local report destination. Launch/hand it to the **existing** authenticated Codex coordinator seat **at most once**, using the real installed Herdr CLI/adapter; fail closed if that seat is unavailable, unknown, busy, or permission-blocked.
- Persist a one-run/one-dispatch intent **atomically before sending**, with unique run ID/task identifier, seat ID checked from current state, attempt count and output paths. No repeated dispatch after a timeout, restart, transport error, blocked screen or unclear result.
- Bounded process wait/timeout; local stdout/stderr/structured outcome capture, with secrets omitted; distinguish `SENT`, `WAITING_FOR_HUMAN`, `UNKNOWN_DELIVERY`, `TIMED_OUT`, `REPORT_MISSING`, `REVIEW_REQUIRED` as justified by observed results.
- Inspect whether the coordinator wrote a **real, matching** `morning.md` for that run and supplied expected task/test/code commit receipts. Do **not** infer code quality or PASS from Herdr idle/exit code or simply from a report filename. Codex/AGY perform planning, delegation, coding, independent testing, repairs and local Git decisions.
- Use offline mocked/fake Herdr scenarios only: safe idle, blocked/permission prompt, fallback idle, busy/missing seat, dispatch uncertainty, timeout, duplicate invocation, missing/stale/mismatched report, successful report. No real agent prompts as part of Gate B.
- Commit the small launcher, focused tests and one local evidence receipt in a **safe, clean local branch/worktree**. No reset/stash/branch switch in an already dirty or occupied checkout. Stop and report actual local SHA and tests.

## Explicitly withheld

**No live task dispatch at Gate B**, no new AGY/Codex startup, no new Herdr panes or agent trust, no AGY coding prompt, no CBDS or second ledger, no new Python task-state orchestration/review framework, no production/NutriSnap changes, no push/merge/deploy, no cron/systemd/timer/night scheduling. `PUSH_HOLD` stays.

The next **Gate C one real launcher-triggered run** requires a **separate owner-approved task and go-ahead**, and must actually demonstrate the previously proven Codex→Manickam build/test/report chain.

**Execution prompt:** `prompts/V0.5_GATE_B_MINIMAL_ONE_SHOT_LAUNCHER_2026-10-20.md` on `origin/planning/v0.5-p0-handoff-20261019`. Reading the approval does not prove code was built.
