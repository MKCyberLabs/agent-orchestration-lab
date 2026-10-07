# Experiments and Metrics

## What to record for every run

| Metric | Why |
|---|---|
| Orchestrator input/output tokens | Main optimization target |
| Worker tokens per agent | Compare useful work vs coordination overhead |
| Orchestrator wake-ups | Should be small and event-driven |
| Manual interventions | Reliability signal |
| Worker retries | Detect unstable delegation |
| Wall-clock duration | Ensure savings do not create excessive latency |
| Test result | Quality gate |
| Merge conflicts | Isolation/design signal |

Create one row in `runs.csv` after each experiment.

## Experiment E0 — Local baseline

Run existing tests without agents.

Expected: all tests pass.

## Experiment E1 — One worker

Use one worker to implement Task T001.

Pass conditions:
- exactly one dispatch
- no model-based polling
- worker emits one durable completion report
- tests pass

## Experiment E2 — Two parallel workers

Use Task T002.

Suggested assignment:
- agy-manickam: implementation
- agy-rohit: tests/review

Pass conditions:
- both can work concurrently
- orchestrator waits mechanically
- integration happens after both reports
- tests pass

## Experiment E3 — Blocked worker

Use Task T003.

The task intentionally lacks one design choice. Worker must return `blocked` with one concise question rather than guessing or spinning.

## Experiment E4 — Failed worker

Give one worker an intentionally failing acceptance check. The orchestrator must reject the result and either redispatch once or stop with evidence.

## Experiment E5 — Gas City comparison

Repeat E1/E2 using Gas City routing/formulas. Compare:
- orchestration tokens
- configuration complexity
- recoverability
- manual intervention

Adopt Gas City only if the control-plane benefits are measurable.
