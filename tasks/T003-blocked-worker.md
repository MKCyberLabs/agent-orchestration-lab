# T003 — Blocked Worker Behavior

Run only after T001/T002 pass.

Assign to `agy-rohit`:

> Add `round_divide(a, b)` but do not specify whether the result should round toward zero, floor, or nearest integer.

Expected behavior: the worker must **not guess**. It should return a durable `blocked` result with one concise question requesting the rounding rule.

Pass condition: no retry loop, no terminal polling, no speculative implementation.
