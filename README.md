# Agent Orchestration Lab

A small, measurable lab for testing low-token multi-agent coding orchestration with:

- **Codex** as architect/integrator
- **agy-manickam** as implementation worker
- **agy-rohit** as implementation/review worker
- **Herdr** as the persistent terminal/session runtime
- **cbds** as the durable dispatch/completion protocol
- **Gas City** as a later control-plane experiment after the baseline works

The rule of this repo is simple:

> The orchestrator must not continuously read worker terminal output.

Workers do their work independently and explicitly report completion. The orchestrator wakes only for a durable result, blocker, timeout, or final integration gate.

## Why this repo exists

Previous orchestration attempts spent too many tokens watching terminal output and repeatedly reasoning about partially-complete worker sessions. This lab isolates the orchestration problem from production projects and measures whether event/checkpoint-based coordination actually reduces cost and manual intervention.

## Experiment order

1. **Phase 0 — Environment check**
   Verify `git`, `herdr`, `cbds`, `codex`, and `agy` are available.
2. **Phase 1 — Herdr + cbds**
   Run one worker, then two workers, using durable completion reports rather than terminal watching.
3. **Phase 2 — Codex architect/integrator**
   Codex decomposes a small coding task, dispatches workers, waits once, verifies, and integrates.
4. **Phase 3 — Gas City evaluation**
   Add Gas City only after Phase 1/2 are stable. Compare its workflow/DAG layer with the simpler cbds baseline.
5. **Phase 4 — Real project pilot**
   Repeat on a small MK Desk Pet issue before trusting the stack with larger work.

## Quick start

```bash
./scripts/check-env.sh
python -m unittest discover -s tests -v
```

If Herdr and cbds are already installed:

```bash
./scripts/smoke-cbds.sh
```

Then give `prompts/MASTER_PROMPT.md` to Codex or AGY and ask it to execute **Task T001** only.

## Success criteria

The first pilot passes only if all are true:

- No LLM repeatedly polls or reads worker terminal output.
- Worker completion is represented by a durable structured report.
- A blocked worker surfaces one explicit question rather than spinning.
- Parallel workers can complete without corrupting each other's work.
- The integrator verifies tests before declaring success.
- We record token usage and number of orchestrator wake-ups.

## Repo layout

```text
AGENTS.md                    Agent rules shared by Codex/AGY
docs/ARCHITECTURE.md        Target architecture and boundaries
docs/EXPERIMENTS.md         Test matrix and metrics
docs/ROADMAP.md             Phased adoption plan
prompts/MASTER_PROMPT.md     Prompt to hand to the orchestrator
schemas/                     Stable task/result contracts
scripts/check-env.sh         Dependency check
scripts/smoke-cbds.sh        Minimal cbds smoke test
tasks/                       Small reproducible orchestration tasks
sample_app/                  Tiny safe codebase used for experiments
tests/                       Verification for the sample app
```

## Safety boundary

Do not point the first experiments at a production repository. Do not auto-merge. Do not give workers secrets. Keep changes in isolated branches/worktrees until the final integration gate passes.
