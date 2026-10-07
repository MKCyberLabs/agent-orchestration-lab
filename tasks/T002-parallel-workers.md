# T002 — Two Parallel Workers

Run only after T001 passes.

## Worker A — agy-manickam
Implement `divide(a, b)` in `sample_app/calculator.py`.

Rules:
- raise `ZeroDivisionError` for zero divisor
- no dependencies

## Worker B — agy-rohit
Create/extend tests in `tests/test_calculator_divide.py` for:
- normal division
- negative values
- zero divisor

## Integration gate
Codex waits for both durable reports, reviews both diffs, then runs:

```bash
python -m unittest discover -s tests -v
```

No model-driven terminal polling is permitted.
