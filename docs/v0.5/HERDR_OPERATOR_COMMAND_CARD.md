# Nightshift ↔ Herdr: small operator command card

**Scope:** Herdr is the **visible agent/UI state surface**. Python Nightshift is the **only task dispatcher, verification and Git/state authority**. Use installed `herdr ... --help` to check local flags; this card is based on Herdr's current official CLI:
https://herdr.dev/docs/cli-reference/
https://herdr.dev/docs/agent-automation/
https://herdr.dev/docs/agents/

## One existing AGY-Rohit seat

- Existing operator (Codex High): `wD:p1`. Do not replace.
- AGY-Rohit live named process: `wD:p4` (owner reported `idle`, `interactive_ready=true`).
- Plain Nightshift status/log pane: `wD:p5`. It is **not a model agent**.
- AGY-Rohit already trusted the orchestration folder `/home/openclaw/worktrees/agent-orch-v05-p0` once, with owner approval. **New folder trust is a NEW approval**.
- AGY-Manickam and independent Codex reviewer task remain pending; H3 = one AGY-Rohit task only.

## Supported minimal Herdr CLI commands

| Goal | Herdr CLI |
|---|---|
| Get live seats | `herdr agent list` |
| Get AGY-Rohit state | `herdr agent get wD:p4` |
| Explain detection / false-idle fallback | `herdr agent explain wD:p4 --json` |
| Read current UI / approval prompt | `herdr agent read wD:p4 --source detection --lines 60` |
| Read readable recent transcript | `herdr agent read wD:p4 --source recent-unwrapped --lines 90` |
| Submit **one** approved prompt and wait boundedly | `herdr agent prompt wD:p4 "ONE_APPROVED_TASK_TEXT" --wait --until idle --until done --until blocked --timeout 180000` |
| Observe a live agent without submitting anything | `herdr agent wait wD:p4 --until idle --until done --until blocked --timeout 180000` |
| Read Nightshift task state (plain shell) | `herdr pane run wD:p5 "python3 -m json.tool /absolute/path/to/state.json"` (only if operator permits; avoid raw secrets) |

**No** `agent send-keys ... enter` for owner/trust approvals in unattended code. Owner must inspect the exact visible dialog and approve separately. `herdr agent prompt` rejects a presently `blocked` agent with `agent_blocked` and does not send input. `--until` only works with `--wait`. Waiting without `--timeout` can hang indefinitely.

## Herdr state → Python task state

| Herdr | Meaning | Python / owner-facing action |
|---|---|---|
| `working` | Model turn active | `WORKER_RUNNING`; bounded wait, not automatic success |
| `blocked` | Approval, permission, question UI detected | `WAITING_FOR_HUMAN` **red**, preserve screen excerpt and task context; no auto-approve, no prompt retry |
| `done` or `idle` | Turn ended/ready (viewed vs unseen) | Run **host file audit + acceptance tests**; only then `VERIFIED_COMMITTED` |
| `unknown`, missing agent, malformed JSON | Status cannot be safely classified | `NEEDS_INSPECTION`; inspect detection screen; no new prompt |
| Timeout, `agent_prompt_stalled`, transport error | Turn may have been sent, state uncertain | `NEEDS_INSPECTION`/HOLD, do not retry; check state and logs |
| Host tests fail / out-of-scope diff | Task not verified | `BLOCKED` / `FAILED`, preserve changes for manual inspection |
| No task actually dispatched | Seat `idle` or `done` alone | `NOT_STARTED`; startup readiness does NOT mean task success |

**Important detection caveat:** Herdr's `idle` fallback can miss unfamiliar permission dialogs. Before sending a prompt, and whenever `idle` is unexpected, read `agent explain` and the **detection** snapshot. Do not interpret a screenshot's red badge as a generalized signal of safety; persist the exact blocked classification and one owner action.

**Authority rule:** Herdr `done/idle` is not Git `VERIFIED_COMMITTED`; Python's tests and local Git SHA are authoritative. Similarly, a local Git SHA is not proof that the Herdr seat ran unless there is a matching pane/process and **one-prompt** dispatch receipt.

## H3 one-prompt sequence, for Python

1. Confirm owner approval + single eligible task; check clean isolated linked worktree, scoped allowed paths and existing AGY `wD:p4`.
2. `herdr agent get`, `agent explain` + `agent read --source detection`; if visible trust/permission dialog or `blocked` → HOLD.
3. Execute `herdr agent prompt ... --wait ... --timeout` **once** via `subprocess.run(argv=list, capture_output=True, timeout=...) `; capture JSON success/error as nonsecret receipts. Do not rerun after any ambiguous failure.
4. If settled as `blocked`, write `WAITING_FOR_HUMAN`, print the actionable path/question and STOP. If `idle/done`, check for false idle, then run Python's allowlist audit and host acceptance. On pass, commit local code and update runner report.
5. Write the authoritative `state.json`, morning-style report, and local documentation evidence. **STOP for owner review**; no push/merge/timer.

## Product note

The original V0.4 Python runner only supports `worker: codex|agy` and launches AGY directly as `agy -p`; that is **not** the named `wD:p4` seat. H3 requires a **minimal opt-in adapter/mode** to route the one worker to the existing Herdr agent. It should not replace the existing successful `codex` or `agy` paths, or create a second state writer.

**Reference:** official Herdr docs as of 2026-10-19. Exact CLI output schemas should be verified on the installed OpenClaw Herdr version; never hardcode guessed nested JSON fields.
