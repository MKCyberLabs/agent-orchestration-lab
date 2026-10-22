# V0.6 — Stop injecting scheduled prompts into the Codex TUI

**Date:** 2026-10-22 IST. **Status:** targetted repair specification. **This document does NOT arm a third timer or claim code was changed on OpenClaw.** The last two calendar-triggered probes failed **before** prompt submission. The correct next task is to prove a supported *non-interactive* transport, not loosen safety checks.

## Frozen ground truth

| Attempt | Timer | Composer | Actual sends | Conclusion |
|---|---|---|---:|---|
| 2026-10-22 20:30 IST | Fired 20:30:00.040 IST | Transcript-selection + xhigh | 0 | systemd PASS, interactive dispatch BLOCKED |
| 2026-10-22 21:05 IST | Fired 21:05:00.039 IST | High correct; transcript-selection reappeared after preflight | 0 | systemd PASS, interactive dispatch BLOCKED |

At the end of second attempt, existing user timer inactive/no next trigger; W03 read-only discovery and all NutriSnap code **NOT RUN**. Don't interpret this as a failed AGY worker or failed timer. The launcher's TUI-safe blocking was correct; no hacks to press Enter/Esc repeatedly. Offline repaired readiness commit `973616b802f44fc3fce15a34d70f7e731c524b5b` remains intact and is **not** a fix for spontaneous UI mode changes. `PUSH_HOLD`, original dirty checkout, prior W04 PASS preserved.

Failure receipts:
- `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2030-ist/scheduler-final-status.json`
- `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2105-ist/scheduler-final-status.json`
- `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2105-ist/W03_SCHEDULE_PROOF_20261022T2105IST/receipt.json`

## Chosen smallest architecture: noninteractive Codex transport

Official Codex docs support **`codex exec` for CI/scheduled scripts** without a terminal composer. It reuses existing saved CLI authentication, supports `--sandbox read-only`, `--json` event output and `--output-last-message` (verify installed flags). Reference: https://learn.chatgpt.com/docs/non-interactive-mode and https://learn.chatgpt.com/docs/cli/reference .

Keep **systemd one-time timer → existing run lock/wrapper → one headless Codex invocation → existing validated receipt/report**. For future real coding, Codex may coordinate AGY-Manickam if proven accessible through the sandbox/service context. **Do not migrate AGY or integrate CBDS as a prerequisite.** The old Herdr interactive mode stays available for manual work, but should NOT be used as scheduled input transport.

`codex queue --thread <uuid> --message ...` may avoid TUI injection and reuse session context on supported CLI versions, but is not this pilot's assumed primary path: verify installed support AND whether it actually starts a turn in an idle session rather than merely queuing, or defer it. Avoid making scheduled completion depend on that ambiguity.

## One-go repair: 3 small steps (stop after real proof)

### 1. Inspect installed CLI and host (read-only, no premature timer)

From **OpenClaw's same unprivileged user** in existing plain shell/service environment:
- `command -v codex; codex --version; codex exec --help`, plus `codex login status` if locally supported. Don't print/scrape `~/.codex/auth.json`, tokens, cookies or session secrets; don't relogin/reinstall/upgrade.
- Confirm installed `codex exec` accepts the documented flags for `--sandbox read-only`, `--json` and final-message output; verify actual model choice and `model_reasoning_effort="high"` with installed `--help`/active config (do not infer from the original terminal TUI footer).
- Record existing runner's one-run lock/timeout and run-id/receipt/report validation contract. Do **not** rewrite the Python agent-coordination workflow or delete Herdr detection.

If `codex exec` cannot reuse authenticated owner account, or the systemd user service cannot access the same CLI auth/home, mark `HEADLESS_BLOCKED` with exact evidence. No new API key or approval-policy bypass.

### 2. ONE read-only headless run, first from plain shell and ideally equivalent systemd user context

- Make unique directory under `/home/openclaw/.local/state/mk-nightshift/headless-smoke/2026-10-22/`; permission-restricted; use one unique run id. Exactly one short, non-destructive task: read the existing NutriSnap W04 branch HEAD and one hydration file, return a compact JSON final answer including run ID, actual observed path and HEAD, plus plain language state. **No W03 implementation**, local code edits, AGY starts, Git operations that alter state or production services.
- Use the actual supported headless flags and **`--sandbox read-only`**, non-escalating/denied approvals, a **bounded systemd/OS-level runtime** and unchanged owner auth. Start the actual `codex exec` from **a plain shell** (not by sending input into the Codex TUI). Capture JSONL/stdout, redacted stderr, exit code and final message *into files owned by wrapper*; no repeated full terminal reads. Parse only actual documented event schema; CLI process exit 0 alone is not a validated task completion.
- Validate exactly one run, a matching run ID and actual branch SHA, no modifications, final message received and event receipt present. Check process termination and no unhandled active Codex process. Record session token usage only if actual CLI reports it. **Do not invent cost savings**.
- If a smoke test from the shell succeeds, validate **same authenticated CLI+filesystem under `systemd --user`** without arming a new timer (e.g., a one-shot immediate user service using the same wrapper if safe). Be explicit: this service proof is **NOT** proof of *scheduled* calendar activation.
- Distinguish `HEADLESS_SHELL_PASS`, `HEADLESS_USER_SERVICE_PASS` and `HEADLESS_BLOCKED`.

### 3. Minimal transport fix ONLY if headless test passes

- Update **one** dispatch boundary of existing one-shot launcher (or its existing service wrapper if even smaller) to support a **verified headless Codex execution** without Herdr TUI input. Keep current one-run lock, timeout, unique run-id, failure receipts, redacted logging, report validation and NO resend under ambiguity; don't add a new AI planning agent, multiple ledgers, new process manager, external API client or a second generic scheduler.
- Make proper CLI output/exit/fresh report validation independent of brittle string searches or improvised JSON. A read-only discovery task can report `W03_NEEDS_SPEC` without a code commit. Never equate `model completed` with `W03_PASS`.
- Add **small offline regression checks**: correct one headless launch; auth unavailable → 0 dispatch; timeout → preserve evidence/no duplicate; malformed/mismatched report → BLOCKED; hostile untrusted output can't supply new instructions; old TUI transport remains safe; systemd environment mismatch blocks rather than bypasses safety.
- Commit minimal local implementation/test code and one short evidence report if run succeeds. Preserve historical timer and run receipts. **NO new calendar timer**, Git push/merge/deploy, new worker process, automatic trust, `danger-full-access`, credential-copy step, CBDS integration or recurring schedule.
- Return **`HEADLESS_TRANSPORT_READY`** only if real headless smoke + same-user systemd context + offline regression tests prove it. Otherwise `HEADLESS_PARTIAL` with one concrete blocker.
- Following a PASS, ask the owner for the **next exact one-time date/time**. Then arm one new calendar trigger, same run packet, no repeat of the earlier expired timers, and prove `SCHEDULED_END_TO_END_PASS`. No inferred time or silent immediate retry.

## Limits / risks

- Headless `codex exec` may create a fresh Codex session; session startup/context cost may be higher than keeping interactive TUI open. Reliability first; measure tokens later. Don't promise cheaper quota.
- The new headless Codex process must be run under the same authorized account without printing auth. A read-only sandbox may not have necessary permissions to command the Herdr/AGY Unix socket later. **Do not silently bypass sandbox for the builder handoff**; test exact required scope as a separate bounded acceptance before using this path for real app writes.
- Don't mark the scheduling capability complete based on another manual/shell test. Success requires a *fresh external calendar timer* actually starting and completing a matching Codex turn.
- Nothing requires starting over with Nightshift V0.5: historical interactive Gate C and W04 development loops remain proven.

## One short instruction to Codex

> Read `docs/v0.6/STOP_TUI_POLLING_HEADLESS_CODEX_DISPATCH_2026-10-22.md` from `origin/planning/v0.5-p0-handoff-20261019`. Stop injecting scheduled jobs into the Codex TUI. Verify the installed `codex exec` non-interactive interface, run one bounded **read-only** headless W04-status probe using saved CLI authentication, prove the same-user systemd service environment, and adapt only the minimal one-shot dispatch boundary if evidence supports it. Preserve old timer evidence, existing launcher locks/report validation and all NutriSnap branches. Return real code SHA/test result or one precise blocker. **Do not arm another timer** or change production.
