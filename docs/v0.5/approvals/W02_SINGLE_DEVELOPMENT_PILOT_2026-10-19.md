# Owner authorization — one NutriSnap W02 development pilot

**Date:** 2026-10-19 (Asia/Kolkata)
**Authority:** Project owner, explicit approval in the current ChatGPT conversation.
**Status:** APPROVED FOR **ONE BOUNDED MANUAL CODING PILOT**, not production, merge or unattended operation.

## Owner's authorization

> I authorize one bounded NutriSnap W02 330 ml development pilot using the existing Codex account and V0.5 Nightshift runner, following prompts/V0.5_PILOT_W02_NUTRISNAP.md. Use the pinned source and an isolated worktree, run safe tests, commit locally, no push, merge, deployment or scheduler activation. Stop for review.

## Specific permitted execution

- **Repository:** `MKCyberLabs/NutriSnap`.
- **Source:** exact pinned `main` planning commit `ee135be8173eea5ad499b23838e0a049c814e991`, not whatever `main` points to later.
- **Issue:** `#171` **W02 only** — precise 330 ml entry in existing Water custom drink flow; preserve slider, presets, edit behavior, authentication and Water/Today calculation.
- **Executor:** existing OpenClaw development host, existing owner-matched Codex account; a **single** real headless Codex coding task launched using the existing Python sequential Nightshift runner (V0.4 implementation underpinning V0.5 pilot). No rerun, AGY fallback, second worker, new login or user, new architecture.
- **Worktree:** new isolated NutriSnap Git worktree/branch from the pinned SHA. Preserve every existing project and orchestration checkout/worktree, including dirty ones; no main checkout edits.
- **Allowed code:** smallest applicable W02 UI, validation and focused test files discovered from the owner-approved contract. Do not expand into W03–W09, finance, scheduler, Telegram, database schema, migrations, unrelated services or deployment.
- **Tests:** run deterministic safe unit/type checks if available. Persistence, Water/Today reload totals and cross-user authorization tests **only against a verified isolated disposable DB and synthetic accounts**. If unavailable, record `NOT_RUN` and **PARTIAL/REVIEW_REQUIRED**; never substitute production/owner data or claim full acceptance.
- **Evidence:** actual worker launch, bounded task, full source/implementation Git SHA, allowed-path diff, tests commands/exits or `NOT_RUN`, risk/blocked details, local runner state/report and one local orchestration documentation commit.
- **Outcome:** STOP after one task/result for independent owner review. No unapproved follow-on code task.

## Prior result and risk boundaries

- Disposable `TEST_ADD` was **reported PASS**, fixture commit `06c84ae2bc1788c8c42046ad13b8de08cb387b97`; local orchestration evidence commit `2f772d8eb691f81abeabf4ff22f25aeb5730fd4d`. This supports attempting a small product pilot, but does **not** certify unattended operation.
- The owner explicitly chose a **dev-first MVP** with the current OpenClaw/Codex account. The same-user host isolation remains `NOT_VERIFIED`; this narrower, manual development experiment is authorized without requiring another account or container. Do not imply the worker is securely confined to the worktree merely because its edits are audited.
- No reading/revealing unrelated credentials or interacting with private services/sockets.
- The outstanding **`PUSH_HOLD`** for local orchestration results persists because the 6 AM scheduler execution context is unverified. This remote instruction/approval receipt is not a push of the OpenClaw local result branch.

## Explicitly not approved

Automatic job/scheduler/systemd, multiple tasks/workers, AGY fallback, production data access, credential/config changes, Prisma migration, outbound reminders, GitHub PR/push/merge, deployment or release. Any implementation that needs these must stop and ask for a separate owner decision.

**Next instruction:** `prompts/V0.5_PILOT_W02_NUTRISNAP.md`, read via `git show` from `origin/planning/v0.5-p0-handoff-20261019`. Verify local history and run the one-task pilot; return report and commit SHA only. 
