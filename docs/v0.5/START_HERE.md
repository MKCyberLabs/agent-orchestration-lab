# V0.5 — Start here (navigation, not implementation approval)

Status: PLANNING HANDOFF. Source baseline: `feature/v0.4-nightshift-pilot`. Owner approval is required before each implementation stage.

## Goal

Make one approved NutriSnap task run at night on the **intended authenticated CLI**, in a clean isolated worktree, with verified tests, a faithful morning report and no unauthorized changes. Measure useful delivery, not agent count.

## Read in this order

1. **This file** — constraints and map.
2. [ROADMAP.md](ROADMAP.md) — V0.5 phases P0–P3, dependencies, later versions.
3. [P0_CHECKLIST.md](P0_CHECKLIST.md) — exactly what P0.1–P0.6 must inspect and how each result is proven.
4. [KNOWLEDGE_MAP.md](KNOWLEDGE_MAP.md) — known locations, authority, stale-pointer warnings.
5. [STATUS_AND_DECISIONS.md](STATUS_AND_DECISIONS.md) — approvals, decisions and evidence ledger.
6. [P0.1 evidence](evidence/P0.1_INVENTORY_2026-10-19.md) — completed host inventory, actual findings and blockers.
7. [P0.2 master prompt](../../prompts/V0.5_P02_ADR_MASTER_PROMPT.md) — **current step: documentation-only authority ADR**.

## Current implementation reality

- `scripts/nightshift.py` is a **sequential Python runner**, one configured `codex` or `agy` executable per campaign, using JSON backlog + state. Its new loop intentionally does **not** call Herdr/cbds.
- Existing Herdr/cbds files document *earlier* experiments. Do not run two independent dispatchers for the same task.
- `scripts/openclaw-v04-smoke.sh` uses a disposable repo and an actual CLI when run on OpenClaw. The offline tests/mock CLIs do not prove real AGY authentication.
- Herdr may host the **interactive Codex analysis session** without becoming V0.5's night-work state authority.
- Named agent / `agy --agent` role is **not an authenticated account identity**; prove process/profile/worktree, not a prompt claim.
- NutriSnap `main:AGENTS.md` may point to historical v0.1 instructions. Never assume it describes the newest release. Verify the chosen delivery branch and SHA.

## What the agents must protect

- Original owner intent, explicit non-goals, acceptance criteria; don't build a moonbase for a doghouse.
- No production database changes, live Telegram sends, payment actions, merge to main, deployment, firmware flashing or secret disclosure.
- No internal subagent can satisfy a request to run another separately authenticated CLI seat.
- No implicit account switch, automatic new framework, destructive rollback, endless repair loop, or unattended restart after blocked state.
- No fabricated test evidence. `REVIEW_REQUIRED` is NOT release approval.
- Existing rules: [AGENTS.md](../../AGENTS.md), [V0.4 pilot](../NIGHTSHIFT_V0.4_PILOT.md).

## Our implementation cadence

For **each individual checklist item**, follow `Observe → Specify → Owner reviews → Implement (only when approved) → Verify → Record lesson`.

**P0.1 is accepted. Stop after P0.2 documentation and Git handoff.** Show the owner the proposed ADR, evidence, risks and next P0.3 scope; never self-approve P0.3–P3.

## Named deliverables

- P0: verified baseline, source locations, current branch/SHA, stale-instruction map and host readiness.
- P1: verified seat-to-CLI/profile/worktree mapping; wrong-identity negative tests.
- P2: bounded issue contract, selective skills and explicit trust levels.
- P3: disposable live proof, one approved low-risk real-project pilot, failure/recovery trials, reliable report.

All are proposed until the owner authorizes the particular stage.
