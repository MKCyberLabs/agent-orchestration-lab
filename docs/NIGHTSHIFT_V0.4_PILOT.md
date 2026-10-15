# V0.4: fail-closed night-shift pilot (NOT release-approved)

This is a single-task-per-project controller, not yet a complete autonomous night-shift system. Its purpose is to prove durable cbds dispatch, quota gating, crash safety and recovery without using an LLM to watch terminal output.

## What is implemented

- Owner-controlled schedule and explicit approved: false by default.
- Exactly one task/dispatch per persistent project state; no implicit reset on the next date.
- Fsync + atomic JSON journal before every non-idempotent cbds operation.
- After an ambiguous crash, stop in NEEDS_RECONCILIATION. Never redispatch blindly.
- WAITING reports are inspected through cbds on a later timer tick; accepted succeeded reports become REVIEW_REQUIRED, not deployment approval.
- Strict provider quota snapshot checks; stale, missing or unknown numbers fail closed.
- Clean feature worktree check, per-project lock, bounded task text and private state permissions.
- No merges, deployment, production database writes, physical device flash, model review, or auth/credential scraping.

## Unimplemented, intentionally

- Gemini Argon chat browser automation. Argon is an interactive web reviewer; it is not a CLI process.
- A supported automatic provider quota collector.
- Automatic recovery of ambiguous run/task/dispatch creation, automated ticket repair or independent Codex review.
- Validated OpenClaw Herdr/cbds live integration or multi-project global capacity scheduling.

Unit tests mock cbds and cannot prove its live JSON shape. The exact adapter must be checked against the installed cbds build, especially command envelope and report acceptance fields.

## Safe first use on the OpenClaw host

1. Complete V0.2 G4/G5 Herdr/cbds plugin and crash-recovery gates first. Preserve existing .cbds directories.
2. Create a clean isolated feature worktree (never main/master).
3. Copy config/nightshift.example.json to ~/.config/mk-nightshift/nutrisnap-pilot.json, with absolute paths to a separately approved bounded task and isolated worktree. Leave approved false.
4. Supply a fresh quota snapshot from a verified trusted source; never fabricate numbers. Snapshot example:

    {
      "checked_at": "2026-10-16T00:10:00+05:30",
      "agents": {"gemini": {"authenticated": true, "remaining_percent": 70}}
    }

5. Confirm the Herdr agent kind actually launches the intended AGY profile. The example 'gemini' is not proof that agy-manickam or agy-rohit was selected.
6. Run the following manually (none dispatch with approved false):

    python3 -m unittest discover -s tests -p 'test_nightshift.py' -v
    cbds doctor --json
    herdr plugin list --json
    cbds skill status
    python3 scripts/nightshift.py status --config ~/.config/mk-nightshift/nutrisnap-pilot.json
    python3 scripts/nightshift.py doctor --config ~/.config/mk-nightshift/nutrisnap-pilot.json

7. In a disposable test repo, verify actual JSON for cbds run create, task create --run, dispatch start, and report list; check accepted result and timeout paths. Do NOT activate automatically before this real integration experiment.

Only after host validation and explicit approval should approved become true.

## Optional systemd user timer

    mkdir -p ~/.config/systemd/user
    cp systemd/mk-nightshift@.* ~/.config/systemd/user/
    systemctl --user daemon-reload
    systemctl --user enable --now mk-nightshift@nutrisnap-pilot.timer
    systemctl --user list-timers 'mk-nightshift*'

Keep it disabled until the pilot passes. The host timezone must be Asia/Kolkata. The timer ticks every 15 minutes during hours 00–05; code enforces the narrower 00:15–05:15 window. Unfinished work stays in Herdr, not the oneshot service. This does not start new tasks every 15 minutes.

## Recovery and approval gates

If phase is NEEDS_RECONCILIATION, disable the timer and inspect cbds run/task/dispatch/report ledgers. Do not delete state.json to retry. WAITING preserves the existing dispatch. A succeeded cbds report is REVIEW_REQUIRED: exact-SHA independent reviewer, software tests, existing ticket ledger and human release approval are still mandatory.

Argon review: paste the linked branch diff and test evidence into the existing Gemini chat. Request concrete bug findings with exact paths and regressions. Return findings as tickets for implementation; do not pretend its chat has an unattended CLI integration.

## Next milestones

- Host integration tests for the actual cbds CLI schema and identity binding.
- Secure automated quota snapshots (provider-supported, no scraping).
- Verified crash recovery of interrupted cbds operations.
- Capacity locks, approved ticket queue, independent review/test pipeline and morning Telegram digest.
- Only then expand to multiple projects and claim a production night shift.
