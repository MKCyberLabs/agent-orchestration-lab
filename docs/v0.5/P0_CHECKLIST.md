# V0.5 P0 — Six reviewable steps (STOP between steps)

Status: PROPOSED. The owner currently authorizes **P0.1 read-only observation only** by Codex High. Do not infer authority for P0.2–P3 from this document.

## Evidence conventions

For each claim: mark **VERIFIED** (command + full SHA + output path), **OBSERVED** (not independently confirmed), **UNVERIFIED**, **BLOCKED**, or **NOT_RUN**. Never record a password, session cookie, OAuth token, private prompt transcript, full user email address or other secret. Inspect logs locally and share only redacted excerpts.

Target host workspace is expected at `/home/openclaw/agent-orchestration-lab` but **verify it exists**; the worktree used for this plan may live elsewhere. Never silently switch branches in a dirty or running Herdr workspace.

### P0.1 — Read-only inventory [AUTHORIZED to inspect, NOT to edit]

**Question:** What is really deployed/installed, which Git objects and documentation are active, and what happened in the previous fixture trial?

Inspection items:
1. Current checkout: `pwd`, `git rev-parse --show-toplevel`, `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git remote -v` (redact credentials), `git worktree list`, `git branch -a`. Do not checkout/merge/rebase/stash/reset.
2. V0.4 source: read `scripts/nightshift.py`, `scripts/openclaw-v04-smoke.sh`, `docs/NIGHTSHIFT_V0.4_PILOT.md`, `config/*.example.json`, `systemd/mk-nightshift@.*`, `tests/test_nightshift.py`, `tests/test_openclaw_smoke.py`. Record runner's actual authority and documented limits.
3. Commands **without launching workers**: `command -v codex agy herdr cbds git python3`; `codex --version`, `agy --version`, `herdr --version`, `cbds --version` (use tool `--help` where necessary, don't assume unsupported flags). Identify whether version/help is not obtainable.
4. Read-only Herdr/cbds inspection: `herdr --help`, `cbds --help` and only verified list/status commands. **Do not create panes, dispatch, ask, done, reply, gate or interrupt existing sessions**. Do not read credentials.
5. Runner host state: inspect whether `~/.config/mk-nightshift` exists, config file names, approval flags (redact paths/secrets), current user timers (`systemctl --user list-timers --all`), timezone (`timedatectl`), and systemd linger state when discoverable. No `systemctl enable/start`.
6. **Evidence from smoke:** look for `~/.local/state/mk-nightshift-smoke/fixture.*/state/fixture/state.json`, a matching morning report, fixture worktree Git history and test logs. Record whether **both** `TEST_ADD` and `TEST_LABEL` are `VERIFIED_COMMITTED`. A top-level `REVIEW_REQUIRED` or exit 0 is insufficient. Never execute the smoke during P0.1.
7. NutriSnap context: determine accessible local clone(s), current branch/HEAD/status and remote branch names without mutating anything; inspect `AGENTS.md`, `README.md`, current known issue/decision/status files, relevant tests/build configuration. **Do not assume main is newest**. If repo absent, mark NOT_AVAILABLE rather than invent.
8. Risks: unexpected active worktrees/panes, the separate 6 AM merge mechanism, production database connections, secret exposure, account-selection ambiguity and stale V0.1 pointers.

**P0.1 output in the Codex chat only** (unless owner separately approves writing an evidence report):
- exact inspected location, branch and SHA;
- source/host inventory table with evidence for each item;
- actual V0.4 smoke task states and tests or NOT_FOUND;
- NutriSnap active-state uncertainty, canonical doc conflicts;
- blockers, safe next decision, proposed **P0.2** only;
- verdict `PASS_FOR_PLANNING` or `BLOCKED` (not `V0.5_PASS`).

**P0.1 negative check:** No code/docs/config file modifications, no CLI worker executions, no new cbds tasks, no deployed jobs, no changed Git HEAD, no credentials revealed.

**Approval checkpoint:** Show owner the above before any P0.2 action.

### P0.2 — Resolve competing orchestration state [NOT AUTHORIZED]
- Confirm separate lifecycle of `nightshift.py` JSON and historic Herdr/cbds runs.
- Draft one-page ADR selecting **exactly one** night dispatcher/state authority for V0.5. Proposed: Python JSON runner; Herdr is only operator UI.
- Identify 6 AM merge-safety interaction and approval boundaries.
- Exit: no double-dispatch scenario, owner accepts ADR; otherwise HOLD.

### P0.3 — NutriSnap entrypoint / stale-context repair [NOT AUTHORIZED]
- Identify real current NutriSnap branch/SHA and relevant already-existing docs.
- Draft minimal edits to NutriSnap `AGENTS.md`, replacing v0.1-only startup bias with version-agnostic pointer **without destroying historical knowledge**.
- Run fresh-session navigation test: agent finds current milestone and approved issue.
- Exit: links resolve against pinned source; owner approves target branch and change list.
- No NutriSnap writes until separate explicit authorization.

### P0.4 — Source-location map [NOT AUTHORIZED]
- Map Today/Food/Water/Finance/Reminders, Prisma/schema, scheduler, Telegram adapter, Python image-analysis service, auth and isolated test harness.
- For each item: path, purpose, canonical document, trust/verification, owner, what NOT to duplicate.
- Exit: an unrelated agent can find the correct reminder subsystem in fewer than three hops. No full-repo dumping.

### P0.5 — Evidence and knowledge authority [NOT AUTHORIZED]
- Define evidence provenance fields and trust labels (PROPOSED, OBSERVED, VERIFIED, APPROVED, plus BLOCKED/NOT_RUN).
- Clarify whether current state lives in Git, Nightshift JSON, cbds, or a decision log — **per fact type**, not two equal task ledgers.
- Exit: fresh session distinguishes a worker self-report from a verified commit/test.

### P0.6 — Host readiness and blocker report [NOT AUTHORIZED]
- Validate mock test coverage vs **actual live smoke**, process/profile identity, quota, timeout, worktree and manual crash recovery.
- List future test actions without performing worker execution or installation.
- Exit: documented GO/HOLD for P1 design with owner decision.

## Gate between steps

Do not start the next step simply because you finished the previous report. The owner checks: source validity, explicit unknowns, no accidental modifications, scoped proposed action, and whether outcomes genuinely met the step's acceptance criteria.

## Five questions every fresh agent must eventually answer at P0 exit

1. Which **verified** NutriSnap branch + SHA represent the current work (not a stale v0.1 note)?
2. Where does the existing reminder logic live, and what must not be duplicated?
3. Which file/command proves project build and tests, and which were actually run?
4. What is owner-approved vs merely planned?
5. What is the next bounded approved issue, who owns it, and how is it verified?
