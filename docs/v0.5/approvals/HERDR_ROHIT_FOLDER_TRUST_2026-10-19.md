# Owner authorization — Herdr AGY-Rohit folder trust only

Date: 2026-10-19 (Asia/Kolkata)

## Explicit owner decision
> Yes—trust and verify this seat only.

**Authorized scope:** If and **only if** the existing AGY-Rohit Herdr pane `wD:p4` is **currently** showing the trust dialog for the **exact folder** `/home/openclaw/worktrees/agent-orch-v05-p0`, select **“Yes, I trust this folder” once**. Then observe the existing Herdr AGY-Rohit agent's recognized process/interactive readiness and idle state. This grants the existing AGY profile file read/edit/execute trust on that worktree only. **Do not apply this approval to a different folder, pane, agent or project.**

## Current owner-reported state
- Existing Herdr operator Codex High `wD:p1` preserved.
- AGY-Rohit `wD:p4`, PID `225508`, Herdr reports `idle` and `interactive_ready=true`.
- Nightshift log/status `wD:p5`.
- H1+H2 `HERDR_SEAT_1_READY`, one startup and **one already owner-approved trust acceptance** reported; local evidence commit `2901d2af391f10a0392cecc8d3bf09b3add2f2fc`. An earlier local blocked-state evidence commit `75294b3c0a4445d4ceacee0fe26dee705ee2bfee` remains preserved.
- Above local commits cannot be independently inspected through this remote instruction branch while `PUSH_HOLD` remains.

**Idempotency is mandatory:** If `wD:p4` is already idle/ready and the dialog is gone, **do nothing**—do not try to reopen the dialog, accept trust again, start a second agent, restart Herdr or create more panes. If a different path is displayed, hold and ask again. Trust acceptance is an explicit UI permission, not authorization to give AGY a coding task.

## Still prohibited
No model coding prompt, Python Nightshift task, second worker, login change, profile/credential read, push, merge, timer, deployment or scheduler activation. The separately scoped H3 handoff remains **NOT_STARTED** and requires owner authorization.

## Recording
If no new action occurs, do not manufacture a new local commit. If the dialog was genuinely still pending and owner-authorized trust was accepted, update the existing local `docs/v0.5/evidence/HERDR_SEAT1_BOOTSTRAP.md` and status with exact observed result, commit **locally** only and stop.
