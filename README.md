> **V0.5 planning handoff:** Start at [docs/v0.5/START_HERE.md](docs/v0.5/START_HERE.md). The [roadmap](docs/v0.5/ROADMAP.md), [P0 checklist](docs/v0.5/P0_CHECKLIST.md), [knowledge map](docs/v0.5/KNOWLEDGE_MAP.md), [status](docs/v0.5/STATUS_AND_DECISIONS.md) and [Codex High P0.1 prompt](prompts/V0.5_P0_MASTER_PROMPT.md) are documentation-only. **P0.1 inventory passed for planning; P0.2 documentation-only ADR is now authorized.** See [P0.2 prompt](prompts/V0.5_P02_ADR_MASTER_PROMPT.md). No Nightshift/session/timer activation.

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

## V0.3 Adaptive Ticket Routing (current pilot)

After every **validated independent Sol review**, run the offline
`scripts/route-repair.py` selector. It chooses automatically:

- **1–4 unresolved tickets:** one Codex GPT-6.1 Sol High implementer,
  `workspace-write`, in an isolated repair worktree.
- **5+ unresolved tickets:** up to two AGY workers with real Herdr/cbds
  accepted completion reports and disjoint source file ownership.
- **0 tickets:** no implementation required; evaluate independent release gates.
- **P0 / disputed:** explicit triage before automatic editing.

The read-only independent Codex review is ALWAYS separate from writable
implementation; test/build and exact-SHA gates still apply. The router
does not invoke models, bypass previous round caps, merge, or deploy.

Quick command:

```bash
python3 scripts/route-repair.py --tickets /absolute/path/to/validated/tickets.json \
  --state /absolute/path/to/checkout/.cbds/review-loop-v02.json
bash tests/test_v02_shell.sh
```

Read `docs/V0.3_ADAPTIVE_REPAIR_ROUTING.md` and
`prompts/V0.3_ADAPTIVE_REPAIR_MASTER.md` for the full coordinator policy,
Codex-direct evidence schema, and integration gate.
The old R004 campaign's five-round budget remains exhausted; it must
not be reset to obtain additional reviews.

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
