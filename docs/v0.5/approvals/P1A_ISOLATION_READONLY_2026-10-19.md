# V0.5 P1A — Owner authorization for one read-only isolation preflight

**Date:** 2026-10-19 (Asia/Kolkata)
**Authorizing actor:** Project owner, via current ChatGPT conversation
**Authorization type:** **READ-ONLY HOST INSPECTION + LOCAL GIT EVIDENCE COMMIT ONLY**

## Owner approval

> I authorize the V0.5 P1A read-only isolation preflight under the Git master prompt. No TEST_ADD, login changes, provisioning, push or Nightshift activation. Record the findings locally in Git and stop for review.

This is an owner approval **to inspect**, not evidence of successful isolation, a worker execution, or runtime readiness.

## Permitted once

- In the existing Codex High/Herdr session, follow `prompts/V0.5_P1A_ISOLATION_PREFLIGHT_ONLY.md` from `origin/planning/v0.5-p0-handoff-20261019`, after verifying existing local worktree/branch and prior P1A identity result.
- Read only the minimum non-secret process, OS and Codex CLI metadata needed to decide whether the intended **headless** worker could access production files, credentials, network/sockets or privileged mounts.
- Assess actual enforced boundaries, identify the smallest missing control; do not infer a proven boundary from prompts, workspace-write flags, allowed_paths or a successful auth-status check.
- Write a brief redacted `docs/v0.5/evidence/P1A_ISOLATION_PREFLIGHT.md`, update `docs/v0.5/STATUS_AND_DECISIONS.md`, run documentation checks, commit on the existing **local** orchestration planning branch and stop.
- Preserve all previous local commits and the original Herdr pane.

## Explicit exclusions

- **No `TEST_ADD`, `codex exec`, AGY, other model worker, fixture creation, timer/systemd/cron setup, or Nightshift activation.**
- No password/token/auth.json/JWT/cookie reads, login/logout, new `CODEX_HOME`, account/profile changes, `sudo`, network probes, production access, service modification or container/OS provisioning.
- No code changes to NutriSnap or orchestration runtime, no Git push/merge/reset/clean, and no modification to the pre-existing 6 AM scheduler.
- `PUSH_HOLD` remains until its separate gate is resolved. The remote **instruction branch** receipt here does not authorize publishing the local result branch.

## Stop condition

If existing boundaries cannot be verified safely, outcome = `ISOLATION_NOT_VERIFIED` and execution remains on HOLD. Report the smallest safe isolation remedy for **separate owner permission**. If local branch/HEAD/status mismatches or secret access would be needed to evaluate safety, stop as BLOCKED.
