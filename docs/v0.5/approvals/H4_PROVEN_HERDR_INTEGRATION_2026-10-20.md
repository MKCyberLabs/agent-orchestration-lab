# H4 owner authorization — integrate proven Herdr path (offline only)

**Date:** 2026-10-20 (Asia/Kolkata)
**Authority:** Explicit owner approval in the current ChatGPT conversation.

> I authorize one bounded H4 integration of the already-proven Herdr H3 adapter into the maintained Python Nightshift runner, following prompts/V0.5_H4_INTEGRATE_PROVEN_HERDR_PATH.md. Run offline tests, preserve human-attention holds and existing sessions, commit locally and stop for review. No new agent prompt, push, merge, deployment or scheduling.

## One authorized change

- Inspect the actual local H3 code and evidence once: adapter `ab4917a2c3368e5c80a5d92ac208be731fb1903e`, verified H3 task commit `0a1fce571b3b0f7d6ee8f4460ddc04c9bb5f6430`, evidence `4d0cc99c101321b335314a0c4b09f3d9873eb6c9`. These are **local** OpenClaw commits, not available via this remote instruction branch while `PUSH_HOLD` is active.
- Integrate the smallest reusable already-tested adapter/path into the maintained Python Nightshift code in a clean isolated integration worktree where needed. Keep Python the sole dispatcher/verification/Git authority. Preserve existing direct `codex`/`agy` paths. No second state store or broad refactor.
- Preserve `WAITING_FOR_HUMAN` on survey/permission/trust dialogs, explicit matched Herdr idle rule, `NEEDS_INSPECTION` on fallback/unknown/stalls, **no auto-Yes**, and **no retry** when prompt delivery is uncertain.
- Run offline/host-only tests, including existing H3 regressions/detector cases where applicable; inspect scoped diff and commit integration code locally. Record results under `docs/v0.5/evidence/H4_HERDR_INTEGRATION.md`, update the local status/roadmap only on real verified PASS. Stop for owner review.

## Preserve existing Herdr topology

- Operator Codex High `wD:p1`; AGY-Rohit `wD:p4`; plain Nightshift status `wD:p5`.
- No new panes, seats, login/profile changes, Herdr manifest modifications or reloads. No AGY-Rohit coding prompt. Do not resolve the old survey hold by blindly sending keys or launching another task.
- One task = one separate Git worktree/report; Python may select existing seat by configured identifier but first-run seat provisioning is deferred.

## Not authorized

No new AGY/Codex headless worker execution; no task dispatch to any agent; no push, PR, merge, NutriSnap changes, production DB, deployment, timer/systemd/cron, unattended night run, login changes or new account. `PUSH_HOLD` remains.

**Execution master prompt:** `prompts/V0.5_H4_INTEGRATE_PROVEN_HERDR_PATH.md` on `origin/planning/v0.5-p0-handoff-20261019`.

**Success:** local integration commit, offline tests and human-attention negative checks PASS, evidence commit, worktrees clean, `H4_INTEGRATED_PASS` or honest blocker. This receipt is authorization, **not evidence that H4 has run**.
