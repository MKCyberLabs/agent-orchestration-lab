# Agent Operating Rules

These rules apply to Codex, agy-manickam, agy-rohit, and any future worker used in this lab.

## Core rule

**Do not use an LLM to continuously watch another agent's terminal output.**

The runtime may capture logs, but the orchestrator should block mechanically on a durable completion event/report and wake only when necessary.

## Roles

### Codex — architect / integrator
- Read the task and acceptance criteria.
- Decompose only when parallelism is useful.
- Dispatch bounded worker tasks with explicit file scope and verification.
- Do not poll live terminal output for progress.
- Wait on cbds/task state or another non-model completion primitive.
- On completion, inspect worker reports, diffs, and tests.
- Integrate only after verification.

### agy-manickam — implementation worker
- Implement the assigned bounded task only.
- Stay inside the assigned file scope unless blocked.
- Run the requested verification.
- Report exactly one final status: succeeded, failed, or blocked.
- Do not claim completion without evidence.

### agy-rohit — implementation/review worker
- Implement or independently review the assigned bounded task.
- Prefer tests, edge cases, and regression checks.
- Report exactly one final status: succeeded, failed, or blocked.

## Completion contract

Every worker result must include:

- task id
- outcome: `succeeded | failed | blocked`
- short subject
- concise body
- files modified
- verification performed
- branch/worktree when applicable
- blocker/question when outcome is blocked

When cbds is available, use `cbds done` as the authoritative completion signal.

## Token-control rules

- No terminal-output polling loops driven by a model.
- No repeated full-repo summaries between workers.
- Give workers the minimum task context required.
- Prefer paths, commit SHAs, diffs, tests, JSON reports, and task IDs over pasted transcripts.
- The orchestrator should normally reason at four points only: plan, dispatch, integration, final report.

## Git rules

- Never force-push shared branches.
- Prefer one branch/worktree per implementation worker.
- Do not merge until tests pass.
- Keep commits small and task-scoped.
- For experiments, never modify another repository unless the task explicitly names it.
