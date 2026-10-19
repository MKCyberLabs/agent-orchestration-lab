# V0.5 — Owner decision: working development fixture before hardening

**Date:** 2026-10-19 IST
**Source:** Direct owner instruction in the current conversation, following P1A isolation review.
**Decision:** **DEV_FIRST / SUPERSEDES P1A HARDENED-ISOLATION GATE FOR ONE DISPOSABLE FIXTURE ONLY**.

## Intent and approved deviation

The owner has confirmed that OpenClaw is being used as a **development server**, not as a production environment, and explicitly prefers a small **working Nightshift V0.5 proof** over expanding into another access-control/security project.

- **Use the existing `openclaw` Unix user and already configured Codex CLI account**. Do not create another OS user, demand another login, repeat account verification, or make a dedicated container/VM a prerequisite for the **single TEST_ADD development fixture**.
- The owner's private TUI account comparison was previously recorded as `OWNER_MATCHED`. Do not copy account email or identity values to Git.
- The earlier user authorization for **exactly one real disposable Codex `TEST_ADD`** remains in force. The owner has now accepted the known residual same-user development-host isolation risk for this narrow test; **the previous `ISOLATION_NOT_VERIFIED` verdict must remain truthful**. Do not upgrade it to VERIFIED.
- **Security hardening moves to a future milestone before broader unattended and sensitive integrations**, not abandoned: dedicated user or container, least privilege, constrained mounts/sockets/egress, minimized inherited env, strong headless profile proof and review of auto-merge/scheduler.
- Keep the solution **doghouse-sized**: reuse the V0.4 Python runner and disposable fixture pattern, no Herdr/cbds rewrites, new account orchestration, token probes, or extra documentation phases before getting a real result.

## MVP experiment contract

- One manual, local **Codex CLI** headless task only: `TEST_ADD`, requiring `math_ops.add` to pass `add(2,3)=5`, `add(-7,3)=-4`, `add(0,0)=0` plus syntax check.
- Create a fresh disposable Git repository/worktree under user-owned state; source/backlog/state limited to that fixture. Use `worker=codex`, `max_tasks=1`, a one-entry approved backlog, `allowed_paths=[math_ops.py]`, <=50 changed lines, fixed timeout, no retries.
- **Do not run the existing `scripts/openclaw-v04-smoke.sh` unchanged**: it creates and executes TWO tasks including `TEST_LABEL`. Set up a one-task fixture safely using the V0.4 source as reference, without changing owner worktrees or runner source.
- Launch the real Codex worker in the runner's `workspace-write` mode (not interactive TUI YOLO / Full Access). Avoid passing unrelated secret-bearing env vars if possible without login changes. This is *risk reduction*, not evidence of isolation: the worker may still have same-user read/socket access to this dev host.
- No production DB, real Telegram, network-service probing, privileged socket interaction, code checkout outside the disposable fixture, arbitrary system commands, install, deployment, login changes, multi-worker dispatch, auto merge, or scheduler changes.
- No push: `PUSH_HOLD` still applies to orchestration **local results** due to unresolved 6 AM merge context. The current manual disposable test does not require a push.
- Host-run acceptance commands, actual worker process receipt, task status `VERIFIED_COMMITTED` or honest BLOCKED/FAILED, exact disposable Git SHA, logs pointer, and a new **local** orchestration evidence commit are the success criteria. Stop for owner review; do not automatically launch W02 or schedule anything.

## Gate meanings

`ACCOUNT_OWNER_MATCHED` = operator verified intended existing account in Herdr TUI (not cryptographic proof of later worker identity).
`ISOLATION_NOT_VERIFIED` = previously observed metadata; accepted as a limited development-test risk, not solved.
`TEST_ADD` = NOT_RUN until a separate actual run report exists.
`NIGHTSHIFT_UNATTENDED` / `NUTRISNAP_W02_IMPLEMENTATION` = NOT AUTHORIZED.

**Next action:** `prompts/V0.5_P1A_DEV_SINGLE_TEST_ADD.md`, read by Codex High in the existing Herdr session. No further risk-assessment steps for this single developer fixture.
