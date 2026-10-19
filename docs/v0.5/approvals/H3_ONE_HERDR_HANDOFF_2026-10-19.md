# Owner authorization — one H3 AGY-Rohit handoff

**Date:** 2026-10-19, Asia/Kolkata
**Decision:** Authorized **one** small development-host H3 task routed from Python Nightshift to the already running Herdr AGY-Rohit seat. The owner explicitly said “yes ... lets contine next step” after H3 was proposed, and asked to ensure Python understands Herdr working / completed / red attention-required statuses, with a tiny approachable command reference. That is permission for this bounded test, not broader automation.

## Exact seat / host
- Existing Herdr: AGY-Rohit **wD:p4** (reported PID 225508), Codex High operator **wD:p1**, Nightshift log/status **wD:p5**.
- Existing trusted cwd for AGY seat: `/home/openclaw/worktrees/agent-orch-v05-p0` (owner-approved once). This is the **orchestration** project, not NutriSnap. Preserve all existing local commits and dirty worktrees.
- Use existing AGY-Rohit profile and real live Herdr-recognized process; **do not start another AGY session, log in, migrate credentials or rename a different profile**.

## Allowed one-task scope
- Codex High may implement the **smallest opt-in Python→Herdr adapter** needed to dispatch *one* bounded prompt to `wD:p4`, read reliable Herdr agent state, fail closed on `blocked`, inspect ambiguous `idle/unknown`, wait with an explicit timeout, and hand successful changes back to **existing Nightshift Python** host verification and local Git evidence. Build focused offline mocked tests of Herdr JSON parsing and state transitions, including fake blocked/unknown/timeout, before the live task.
- One real AGY-Rohit coding task: add a **small testable Herdr status classification/command helper** for the orchestration project only, in a new isolated, clean, non-sensitive `nightshift/h3-...` linked worktree if the existing Python runner requires that branch format. No NutriSnap source or production/owner data.
- The existing trusted AGY process may request separate folder trust or tool approval for the new worktree. **Do not automatically accept**. If a new approval is requested, Herdr `blocked` is `WAITING_FOR_HUMAN`; show exact folder/action, stop dispatch, and request a fresh, scoped owner decision. Approval of the original orchestrator directory is **not** permission to trust another directory.
- Exactly one `herdr agent prompt` submission for one approved task; **never re-submit on a timeout, blocked dialog or unknown status** until separate reconciliation. AGY quota consumption is allowed for this one task.
- Python remains sole dispatcher/state writer; Herdr reports live agent state/UI; host file audit and tests determine success and Python performs any verified local Git commit.

## Explicitly forbidden
No auto-yes/trust dialog, blind Enter or other approval key, second coding task, second worker/AGY-Manickam, credential reads, production access, Git push, merge, deploy, cron/systemd, automatic morning scheduling, rewriting the orchestrator framework or CBDS, broad “security hardening” phase.

**Local evidence and stop:** H3 `WORKING`, `WAITING_FOR_HUMAN`, `BLOCKED`, `REVIEW_REQUIRED` or truthful failed status, with actual Herdr pane, one-prompt receipt, host tests (PASS/FAIL/NOT_RUN), code SHA if committed and a local orchestration evidence commit. `PUSH_HOLD` stays. Stop for owner review.
