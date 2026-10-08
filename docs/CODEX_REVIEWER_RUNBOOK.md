# Codex Sol reviewer runbook — Ubuntu/OpenClaw

## There are TWO independent failures

1. Interactive Herdr Codex: `Cannot use the shared background server ... rerun ... --no-daemon`. A launch flag or profile alone does not guarantee a healthy worker; avoid interactive reviewer dispatch until verified. For reviews, use **non-interactive `codex exec`** instead.
2. Standalone `codex exec`: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. This is an **OS sandbox / user namespace** issue. A model or config profile does not fix it. The reviewer must be BLOCKED until it can access `git rev-parse HEAD` under its read-only sandbox.

## Safe diagnostic (no LLM tokens)

```bash
cat /etc/os-release
command -v codex; codex --version
command -v bwrap || true
sysctl kernel.unprivileged_userns_clone kernel.apparmor_restrict_unprivileged_userns 2>/dev/null || true
codex sandbox -- /bin/true
```

On Ubuntu/Debian, first install the distribution package if absent:

```bash
sudo apt update
sudo apt install bubblewrap
```

On Ubuntu 24.04 specifically, if necessary, follow the *official* targeted AppArmor bwrap profile guidance at https://developers.openai.com/codex/sandboxing . Only copy a profile when its source path exists, and prefer a narrow bwrap profile. Do not globally set `kernel.apparmor_restrict_unprivileged_userns=0`; do not disable Codex's sandbox or elevate permissions to work around review-only access.

After changing bwrap/AppArmor, repeat:

```bash
bash scripts/preflight-codex-reviewer.sh
```

## User profile

`bash scripts/install-sol-review-profile.sh` appends a single `[profiles.sol-review]` block to `~/.codex/config.toml` without overwriting an existing file/profile. It validates TOML and backs up the prior config; if a profile already exists, it stops for human review. It does not carry credentials. The profile is never committed from the user's home directory.

## Dedicated invocation

```bash
bash scripts/run-sol-review.sh \
  /home/openclaw/Projects/NutriSnap-finance-orch \
  origin/main
```

The script refuses to invoke Codex after a failed preflight. The result is saved to `${XDG_STATE_HOME:-~/.local/state}/agent-orchestration-lab/reviews/<HEAD>/<timestamp>/`, never in the source checkout.

Codex must include:
- `VERDICT: PASS`, `VERDICT: FAIL`, or `VERDICT: BLOCKED` on its own line.
- `Reviewed commit: <exact 40-char SHA>`.
- Any actionable findings with `path:line` evidence.
- Test commands actually run (not guessed).

A review is not accepted if the SHA does not match the pinned HEAD. A passing review on an old SHA is obsolete after any repairs.

## cbds adapter

The wrapper automatically invokes `cbds done` once **only when genuinely invoked with cbds-injected `CBDS_TASK_ID` and `CBDS_DISPATCH_ID`**. A code verdict `FAIL` is an accepted execution result with report body `VERDICT=FAIL`. A preflight/auth/tool failure is `blocked`. Otherwise it operates as a standalone review (no fake cbds report).

The orchestrator must consume the report's verdict, not infer it from `cbds succeeded` or Herdr pane idle. Never inject the `cbds done` instruction as raw Bash input. Do not auto-retry permanently broken reviewers. An interrupted orchestrator should read durable task/report state first.

## References

- https://developers.openai.com/codex/config-basic/
- https://developers.openai.com/codex/config-reference/
- https://developers.openai.com/codex/sandboxing
- https://github.com/openai/codex/issues/15057
