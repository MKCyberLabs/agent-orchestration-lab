# T001 — Single Worker Durable Completion

## Purpose
Prove one worker can receive a bounded coding task, finish it, and report completion without the orchestrator watching terminal output.

## Worker
`agy-manickam`

## Objective
Add a `multiply(a, b)` function to `sample_app/calculator.py` and add tests.

## Allowed paths
- `sample_app/calculator.py`
- `tests/test_calculator.py`

## Constraints
- Do not modify orchestration docs/scripts.
- Keep implementation trivial and deterministic.
- Do not add dependencies.

## Acceptance
- `multiply(3, 4) == 12`
- `multiply(-2, 5) == -10`
- existing `add` behavior remains unchanged
- unit tests pass

## Verification

```bash
python -m unittest discover -s tests -v
```

## Orchestration acceptance
- one dispatch only
- no LLM terminal polling
- one authoritative succeeded/failed/blocked report
- integrator independently runs tests after worker completion
