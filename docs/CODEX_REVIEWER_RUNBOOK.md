# Codex Sol reviewer runbook — Ubuntu/OpenClaw

## There are TWO independent failures

1. Interactive Herdr Codex: `Cannot use the shared background server ... rerun ... --no-daemon`. A launch flag or profile alone does not guarantee a healthy worker; avoid interactive reviewer dispatch until verified. For reviews, use **non-interactive `codex exec`** instead.
2. Earlier standalone `codex exec` failed inside its sandbox; after correcting `codex sandbox -- /bin/true` the host preflight passed (OpenClaw, 2026-10-08). A subsequent review exit=1 was traced to the **legacy Codex profile layout**, not authentication or permissions. Reinstall the current-format named profile before another model call. If future sandbox probes actually fail, treat them separately.

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

**Codex 0.134+ uses standalone named profiles.** `bash scripts/install-sol-review-profile.sh` installs `~/.codex/sol-review.config.toml` with top-level keys, **not** a `[profiles.sol-review]` block. It removes only the exact legacy `[profiles.sol-review]` table and top-level `profile = "sol-review"` selector left by the first V0.2 installer, backs up `config.toml` before any modification, and preserves unrelated settings. The installer is idempotent; if pre-existing or custom profile values disagree with the template, it stops for manual review. It never touches authentication credentials. See [Codex Advanced Configuration](https://developers.openai.com/codex/config-advanced#profiles).

To migrate the previously installed legacy profile after pulling V0.2:

```bash
bash scripts/install-sol-review-profile.sh
# Non-model sanity checks:
python3 -c 'import tomllib, pathlib; p=pathlib.Path.home()/".codex/sol-review.config.toml"; print(tomllib.loads(p.read_text())["model"])'
bash scripts/preflight-codex-reviewer.sh
```

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
