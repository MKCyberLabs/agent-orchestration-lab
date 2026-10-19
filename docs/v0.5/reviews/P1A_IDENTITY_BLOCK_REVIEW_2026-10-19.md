# V0.5 P1A — Identity blocker review (2026-10-19 IST)

**Review finding:** `IDENTITY_UNVERIFIED` is a **correct fail-closed outcome** for the user-authorized single disposable Codex `TEST_ADD` trial. Do NOT record it as failed software or as an actual worker run.

Reported local Codex evidence:
- P1A local audit commit `810f4c485d60a367e8194e5907099a80563b4535` (currently OpenClaw-local; **not independently fetchable from GitHub**).
- `codex login status` indicated ChatGPT authentication mode only; intended authenticated account/profile could not be determined.
- Fixture absent; real worker invocations **0**; `TEST_ADD=NOT_STARTED`; isolation/tests `NOT_RUN`; no push; `PUSH_HOLD` remains.
- Prior commits preserved and local worktree reported clean.

## Why the block is expected

Public Codex CLI reports indicate `codex login status` may display only `Logged in using ChatGPT`, without telling which account. `/status` inside the interactive Codex TUI has historically displayed account information but availability is version-dependent, and recent CLI reports document loss of email in some versions.

Sources (public technical context; **not** authorization):
- https://github.com/openai/codex/issues/53435
- https://github.com/openai/codex/issues/4493
- https://github.com/openai/codex/issues/48433

**Do not read `~/.codex/auth.json` or decode JWT/access/id/refresh tokens** as a workaround. Do not store emails, account IDs, access tokens, profile secrets, cookie content or unredacted terminal logs in Git. `codex login status` alone is AUTH_METHOD_OBSERVED, not ACCOUNT_VERIFIED.

## One bounded resolution path

1. In the **same intended OpenClaw OS user and Codex configuration** planned for the fixture, attempt an *interactive status-only* `codex` TUI session and `/status` locally **without submitting a model prompt**. The owner may personally compare any displayed account to the intended account. Verify executable path/version, OS user and effective `CODEX_HOME` agree with the future headless process. Record only `OWNER_MATCH_CONFIRMED` + method + timestamp; no identifier values.
2. If the TUI explicitly exposes a usable current account identity and the owner confirms it, mark `CLI_ACCOUNT_OBSERVED_AND_OWNER_MATCHED`. This is a **bounded operator-attested match**, *not* generalized independent cryptographic proof.
3. If the TUI omits identity or cannot be tied to the headless CLI credentials, mark `IDENTITY_UNVERIFIED` again, but **do not repeat searches, change login, run Codex exec, decode tokens, or work around the gate**. Escalate one concrete choice to owner: approve a separately isolated OS user/CLI profile and an owner-controlled fresh login in that new profile, or keep the trial HOLD until a supported account identity status exists. That login/provisioning requires **new explicit owner permission**; do not perform it under current authorization.
4. Regardless of identity result, prior `P1A` source safety finding remains: `scripts/nightshift.py:process()` passes `env = dict(os.environ)`; CLI `workspace-write` and Git allowed_paths auditing **do not prove isolation from production credentials**. Thus the fixture remains `NOT_RUN` until the **separate isolation preflight** passes.
5. Retain the original **one TEST_ADD only** authorization; this note does **not** authorize re-running/expanding work or bypassing safety gates.

## Outcome

- P1A result **BLOCKED SAFELY**; no actual worker or task acceptance tests.
- Next narrow owner/operator step: attempt **one status-only account check** and record a non-secret outcome.
- Instruction: `prompts/V0.5_P1A_IDENTITY_STATUS_ONLY.md`.
- No P1B, W02 implementation, Git push, timers, Nightshift or deployment. `PUSH_HOLD` unchanged.
