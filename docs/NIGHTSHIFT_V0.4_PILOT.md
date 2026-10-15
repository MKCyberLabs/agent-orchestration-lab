# V0.4 — Sequential coding night shift (pilot; no unattended activation)

This branch implements a zero-LLM **orchestrator**: a deterministic Python runner sequentially invokes **Codex CLI** or **Antigravity CLI** for approved, narrowly scoped tasks. Coding workers still spend model tokens. The runner itself does not call a coordinator model.

It replaces Herdr/cbds in the *new* script; legacy experimentation files remain untouched.

## Actual functionality

- One direct headless worker process at a time: codex exec --json or agy -p --output-format json.
- Up to max_tasks from an approved JSON backlog, respecting dependencies, per-task and campaign deadlines.
- Dedicated linked Git worktree with exact nightshift/* branch, clean start and explicit approved:true.
- Strict changed-path and forbidden-path checks (including untracked files), diff line budget, test-weakening guard, and host-run acceptance and project verification commands before **local commit**.
- Atomic 0600 project state; fsync, advisory lock, no accidental dispatch after interrupted/failed state.
- Static morning report listing completed commits, blocked work and future approved tasks.
- No auto-merge, push, production DB, secrets, hardware flashing, arbitrary shell verification, or background command supervision.

### Deliberate limitation: no automatic destructive rollback

If a worker fails, commits unexpectedly, times out, edits a forbidden path or fails tests, **STOP and preserve that isolated worktree for human inspection**. We deliberately rejected the proposed blanket git reset --hard/git clean -fd because it can destroy owner work or evidence. Only an owner-approved, path-limited recovery procedure should clean the worktree and mark the state ready for another run.

### CLI reality

Codex and AGY support noninteractive execution, but exact command compatibility, account identity, sandbox nesting, authentication and quota policy **must be verified on the OpenClaw host**. JSON token fields are saved when exposed. A quota error currently BLOCKS; automatic account switching and preflight quota probing are not implemented. Worker logs may contain sensitive content and are private under the local state directory.

### Setup — NO job is enabled by this branch

1. Use a **separate disposable test repository** for Night 1. Ensure git worktree and tests pass with fake worker commands before granting coding work.
2. Copy config/nightshift.example.json into ~/.config/mk-nightshift/ and create the backlog JSON with correct paths. Leave approved=false until the host pilot is reviewed.
3. Create a dedicated feature worktree for the target project (not main/master/develop), e.g.:

       git -C /absolute/repo worktree add -b nightshift/pilot /absolute/nightshift-worktrees/project-pilot <verified-source-ref>

4. Edit the project/backlog context_files and allowed_paths for the *current* version. Do not reuse stale AGENTS.md branch pointers without auditing them. Put every state/backlog path **outside the worktree**.
5. Confirm that the same systemd user can invoke both CLIs without an interactive terminal:

       codex exec --help
       agy --help
       python3 scripts/nightshift.py doctor --config /absolute/config.json
       python3 scripts/nightshift.py status --config /absolute/config.json

6. Run offline tests:

       python3 -m unittest discover -s tests -p 'test_nightshift.py' -v

7. Use real sandbox trials in a disposable Git repo before editing a real project. Only after approval, set approved=true and manually trigger a controlled run inside the planned window.

       python3 scripts/nightshift.py run --config /absolute/config.json
       python3 scripts/nightshift.py report --config /absolute/config.json

### Optional one-shot systemd user timer

Files systemd/mk-nightshift@.service and .timer run exactly once at **00:15 local system time**. Confirm the OS timezone is Asia/Kolkata (the Python runner independently verifies its IST window). The timer is NOT installed or enabled by this repository. Do not enable it until manual headless CLI, sandbox, user session/auth and real Git-worktree gates pass.

       mkdir -p ~/.config/systemd/user
       cp systemd/mk-nightshift@.* ~/.config/systemd/user/
       systemctl --user daemon-reload
       # ONLY after pilot approval:
       systemctl --user enable --now mk-nightshift@nutrisnap-pilot.timer

Timer Persistent=false avoids starting overdue work after an unrelated daytime boot. The service has a 125-minute timeout; the Python campaign itself is capped at max_minutes <=120.

### Safe project boundaries

- NutriSnap: only an isolated DB; any production Prisma DB push, finance mutations, deployment and live Telegram sends forbidden.
- MK Desk Pet: simulator/unit-test/firmware **compilation only**, never esptool flash or USB operations. Hardware validation stays manual.
- Project instructions must reference the latest approved branch/version.
- Worker model may still attempt undesirable commands; this runner is **not a security sandbox**. Use Codex sandbox/AGY permissions and a dedicated unprivileged Linux account with no production credentials or hardware access. A post-run path audit cannot undo external side effects.

### Acceptance gate

Offline unit tests use real temporary Git worktrees but **mock both coding CLIs**. They are not evidence of real Codex/AGY, subscription auth or OpenClaw/systemd reliability. Initial status remains HOLD until at least one real headless worker completes two approved fixture tasks and reports correctly, with a simulated interruption and manual recovery.

The former Argon review includes two false positives: script never contained the reported stray "c" argument in cbds report calls, and STATES already included BLOCKED and NEEDS_RECONCILIATION. The larger sequential-runner simplification was justified.

### Later only if the pilot delivers value

Trusted quota sampling, optional profile fallback, automated artifact upload/Telegram notification, multiple project configuration files and backlog authoring support. No Paperclip, Gas Town, or separate dashboard.
