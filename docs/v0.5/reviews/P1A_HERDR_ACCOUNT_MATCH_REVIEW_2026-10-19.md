# V0.5 P1A — Herdr account-match review

Date: 2026-10-19 IST
Decision: **P1A ACCOUNT-MATCH GATE SATISFIED BY OWNER ATTESTATION; EXECUTION STILL HOLD**.

## Grounded, non-secret report

Owner reports a second Herdr terminal tab `Codex Status Check` was created in the **existing** workspace and the original Codex High pane remained intact.

- OS account on status tab: `openclaw` (UID 1000).
- Executable: `/home/openclaw/.npm-global/bin/codex`.
- CLI version: `codex-cli 0.163.0`.
- No `CODEX_HOME` override. The shell's effective Codex home matched the original checked reference without disclosing the home path hash as an identity.
- An interactive `codex --no-alt-screen` /status screen exposed an account and plan; **owner privately confirmed matching the intended account**. This is `OWNER_MATCHED`, an **operator attestation**, not cryptographic identity proof or an independent proof that subsequent headless worker uses the same authentication profile.
- Local result commit reported: `03de8bdccee2316ee27b3ebdcf2182f46c242614` on isolated local `planning/v0.5-p02-adr-20261019`. Cannot inspect it via GitHub while PUSH_HOLD remains.
- No model prompt, no `codex exec`, no fixture, no new worker, no login change, no Git push. `TEST_ADD=NOT_RUN`.

**Privacy:** Do not store or quote the displayed account identifier/email, TUI session ID or full screenshot in project docs. This file preserves only the attested match and executable context.

## Remaining blocker: isolation

The inspected interactive TUI reported **YOLO / Full Access**. That status describes that session's permissions; do not automatically equate it with the proposed headless `codex exec --sandbox workspace-write --ephemeral --json -` policy. The actual headless sandbox would need separate verification.

More importantly, the existing V0.4 `scripts/nightshift.py` passes the parent process environment to children via `env = dict(os.environ)`. `workspace-write` ordinarily constrains **writes** but not necessarily reads of unrelated files. It is NOT a boundary against reading the same Unix user's home, other apps' credentials or reaching local services. A Git `allowed_paths` after-the-fact audit cannot undo external effects.

Official reference for distinction between workspace-write and full-access:
- https://github.com/openai/codex/blob/main/sdk/python/docs/api-reference.md
- https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/permissions/sandbox_mode/workspace_write.md

## Review disposition

- `ACCOUNT_OWNER_MATCHED=YES` (privately attested in a status-only tab).
- `HEADLESS_PROFILE_PARITY=REPORTED` (OS user / binary / config match, no headless trial).
- `ISOLATION=NOT_VERIFIED`.
- `TEST_ADD=NOT_RUN`.
- `PUSH_HOLD=ACTIVE`.

The owner previously approved **one** disposable Codex TEST_ADD conditioned on identity **and** isolation. That does not authorize weakening isolation or modifying the runner, worker OS login or production permissions.

**Next recommended owner choice:** authorize **one bounded, read-only isolation preflight** under `prompts/V0.5_P1A_ISOLATION_PREFLIGHT_ONLY.md`. If this check requires changes or real worker execution, STOP and ask separate permission. Do not start the fixture in the isolation audit itself.
