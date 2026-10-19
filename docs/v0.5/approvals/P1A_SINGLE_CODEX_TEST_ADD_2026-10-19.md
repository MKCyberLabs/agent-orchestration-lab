# Owner authorization — P1A single disposable Codex TEST_ADD

Approval date: 2026-10-19, Asia/Kolkata.

## Owner-approved action (verbatim intent)

> I authorize one disposable Codex TEST_ADD run with verified account identity, under the P1A Git instructions. No other worker tasks, no push, and no Nightshift activation.

This approval is provided by the owner in the current ChatGPT conversation. It is recorded here as a durable **owner authorization receipt**, not as evidence that any CLI process has launched or passed tests.

## Exact approved scope

- Execute on OpenClaw **only after** independent non-secret verification of intended Codex headless account/profile AND practical sandbox isolation.
- **One new disposable TEST_ADD only**. One real Codex CLI headless worker invocation, at most once, no retry/fallback/second task.
- Target a newly created private disposable Git fixture outside NutriSnap and existing user/production worktrees. Its acceptance assertions are integer addition (+5, -4, zero) and Python syntax.
- A fixture with `TEST_LABEL`, `max_tasks > 1`, unknown authentication identity, unsafe inherited credentials/mounts, dirty/conflicting worktree or unverified isolation is **NOT AUTHORIZED TO RUN**. Mark BLOCKED and preserve evidence.
- Host tests and receipt collection only after all preflight gates pass. A successful task reaches `VERIFIED_COMMITTED`, not deploy/release authorization.
- Document actual results, failure, NOT_RUN and evidence under `docs/v0.5/evidence/` and commit on existing **local** orchestration planning worktree. NO PUSH; prior commits untouched.

## Important confirmed code risk

At V0.4 source `scripts/nightshift.py`, `process()` constructs its child environment using `dict(os.environ)`; `worker()` launches `codex exec --sandbox workspace-write --ephemeral --json -`. **The worker inherits parent environment variables**. Workspace-write and allowed-path post-run audit are not proof that the child cannot read secrets or contact services.

Codex must verify the concrete command's OS/container sandbox and what environment is inherited before running. If intended Codex login would require access to production credentials, or reliable sandbox isolation cannot be achieved without unapproved runtime modifications, STOP as `ISOLATION_UNVERIFIED` and report a narrow safe remedy for separate owner approval. Never dump authentication material to prove identity.

## Separate actions still prohibited

No AGY accounts; no Nightshift scheduled job; no local NutriSnap edits; no production DB, Telegram or hardware access; no PR/merge/deploy; no broader V0.5 progression; no push while `PUSH_HOLD` unresolved.

## Execution protocol

Primary staged instruction:
`prompts/V0.5_P1A_SINGLE_CODEX_TEST_ADD.md`.

Check preflights, run one task only if verified, commit LOCAL audit and STOP for owner review.
