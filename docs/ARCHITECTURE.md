# Architecture

## Baseline architecture

```text
User
  |
  v
Codex architect/integrator
  |
  | creates bounded tasks
  v
cbds durable task/dispatch state
  |
  +------------------+
  |                  |
  v                  v
Herdr pane          Herdr pane
agy-manickam        agy-rohit
  |                  |
  | cbds done        | cbds done
  +--------+---------+
           |
           v
    durable reports
           |
           v
Codex wakes once for integration
           |
           v
      tests + diff gate
           |
           v
       accept/reject
```

## Separation of responsibilities

### Herdr
Herdr owns persistent terminal/session execution. It is a runtime, not the source of task truth.

### cbds
cbds owns durable dispatch identity and authoritative completion reporting. Terminal transcripts are supporting evidence only.

### Codex
Codex owns decomposition, bounded specs, and final integration reasoning. It should not spend tokens idling or watching a pane.

### AGY workers
Workers own implementation/review of small assigned scopes. They report completion explicitly.

### Git
Git owns code history and isolation. Worker branches/worktrees are preferred for concurrent changes.

## Phase 2: Gas City

After the cbds baseline works, Gas City can be evaluated as the higher-level control plane:

```text
Gas City formulas / dependencies / supervisor
                 |
                 v
        task routing / state
                 |
          Herdr runtime
        /              \
 agy-manickam        agy-rohit
        \              /
         durable results
                 |
             integrator
```

Gas City should be adopted only if it reduces orchestration code/operations without reintroducing expensive transcript-driven monitoring.

## Non-goals

- Building another chat-based multi-agent framework.
- Allowing agents to freely converse without a task dependency.
- Using Paperclip as the low-level coding execution loop.
- Automatically merging unverified worker output.
