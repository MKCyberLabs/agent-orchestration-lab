# V0.6 next step — Headless Codex → Herdr → AGY-Manickam, real W03 coding

**Owner direction 22 Oct 2026:** "Continue; tell Codex to use Herdr for calling AGY." This is a single **owner-approved local development trial**, not permission for global config changes, production deployment, push/merge or recurring night scheduling.

## Current truth — stop reopening completed tests

- **SCHEDULED_HEADLESS_END_TO_END_PASS:** 2026-10-22 **21:50–21:51:11 IST**; one systemd calendar activation, one authenticated headless Codex task, fresh validated run-specific completion. Outcome `DISCOVERY_COMPLETE` **read-only**. Code used: local headless launcher `0a287c691a8dcd80f5b577bfa8db159ba0948bcf`; 84 earlier regression tests. No AGY work in that proof.
- **Previous real interactive AGY-Codex work PASS:** NS-01/02, Gate C, W04 implementation `8a13c3c77250b829292fd47f28365b34cda6425e` on isolated NutriSnap night branch (locally unmerged); W04 independent tests and browser checks PASS. Existing Herdr AGY-Manickam worker could be safely rediscovered/restarted; pane IDs are ephemeral.
- **CBDS pilot only:** durable AGY dispatch succeeded but token savings UNPROVEN; do not make CBDS a new dependency.
- **Important distinction:** proving `codex exec --sandbox read-only` can read and report does **not** prove it can make controlled Herdr write-side calls, delegate to AGY, wait for worker, or independently run application tests. This ONE run proves that missing link.
- Existing `PUSH_HOLD` and original dirty NutriSnap checkout remain untouched. **No timer is armed by this plan.** A specific next calendar clock time is still a separate owner decision; do not invent one.

## Exact W03 source and scope

Start by reading actual saved W03 discovery `/home/openclaw/.local/state/mk-nightshift/scheduled/2026-10-22-2150-ist/W03_HEADLESS_SCHEDULE_PROOF_20261022T2150IST/morning.md`, its receipt and, if present, actual local notes/source links. The discovery concluded `DISCOVERY_COMPLETE` but **that status alone does not prove the defect is specified or reproducible**.

- If local evidence identifies a **precise hydration date/time bug**, choose the smallest reproducible W03 case with expected vs actual behavior, including timezone/calendar-day/edit-reload boundary where relevant. Protect the existing W04 weekly-average fix; do not invent data-model changes, user expectations or production histories.
- If the source is ambiguous, the complete bounded deliverable becomes **one real AGY delegated, read-only W03 code investigation + independent Codex assessment** and report `W03_NEEDS_SPEC`; no invented implementation or fake code SHA.
- **No unrelated feature work.** Use existing isolated NutriSnap night worktree `/home/openclaw/worktrees/nutrisnap-nightshift-20261020-ns01` after confirming actual HEAD, cleanliness and ownership. No reset/stash/rebase of original checkout.

## Exactly one integrated manual headless→Herdr→AGY exercise (no timer yet)

### 1. Coordinator preflight — verify working API, not terminal UI

From an **existing plain OpenClaw shell**, inspect actual `codex exec --help`, current `scripts/nightshift_once.py` help and verified headless wrapper, Herdr `--help`, `herdr agent list`, `herdr pane list`, installed prompt/wait/status command syntax, existing AGY-Manickam authenticated profile, W03 discovery, NutriSnap worktree Git state, and the current run lock. Use actual installed flags; don't guess.

Use the **proven noninteractive Codex transport**, **High** effort. A headless process may not access Herdr socket or app worktree in a read-only sandbox. Test actual access safely (read-only Herdr agent list and target worktree). **Never silently bypass sandbox**: if a controlled write-capable executor/workspace-scoped permission is required for local Herdr invocation, use only already approved/user-granted minimal scope; otherwise report `HEADLESS_HERDR_ACCESS_BLOCKED` and the exact authorization/config needed. No `danger-full-access`, `--yolo`, login refresh, global privilege or new credentials.

### 2. Codex calls AGY via Herdr ONE time

Coordinator = **headless Codex**, builder = **existing authenticated AGY-Manickam**, transport = **Herdr CLI** (not CBDS, not an interactive Codex composer and not a new agent orchestrator).

Find a genuinely live ready AGY process from current Herdr registry, not historic `wE:p2`. If exited, use prior demonstrated recovery in one available shell or at most one necessary new shell, at most one agent startup, verified existing profile and exact known NutriSnap worktree. Don't create duplicate running AGYs.

Send **one** scoped W03 task via supported Herdr prompt command; capture dispatch identifier, pane/agent id and local timestamp. No blind resend after a timeout/uncertain send. Let AGY investigate/implement within identified allowed hydration paths, add deterministic regression tests, and make a **local-only Git commit** if a real defect is fixed. At most **two targeted repair/retest iterations** across this task. Bounded timeout/lock, one owner-ready output directory and short structured handoff. Do not repeatedly read full transcript output; wait for completion using installed supported wait/status or a bounded single read and check committed artifact/report.

### 3. Independent Codex QA + final artifact

After the builder returns, Codex **separately** reviews actual diff/commit and independently runs focused W03 hydration tests, W04 regression, `npm run typecheck` and `git diff --check`; browser smoke only if an existing safe isolated dev test environment is available. Report exact tests/counts and browser PASS / NOT_RUN / FAIL. Don't treat builder claims as independent QA or read-only discovery as W03 implementation.

Save run-specific `receipt.json`/`morning.md` under the existing mk-nightshift state directory using a unique run ID, plus concise result document in safe local orchestration worktree if appropriate. Include **Codex headless run id**, Herdr AGY identity/pane, prompts/starts/repairs, all code SHA(s), local branch, actual tests, context/tool calls if available, no-push/merge/deploy assertion, and how the next scheduled run can invoke this **same** coordinator transport without TUI. Keep logs redacted.

Final verdict:
- `HEADLESS_HERDR_AGY_W03_PASS` only if headless Codex actually delegates to AGY through Herdr, real W03 code commit exists, independent QA passes and fresh report is validated.
- `HEADLESS_HERDR_DELEGATION_PASS_W03_NEEDS_SPEC` if same delegation works but local W03 lacks an actionable verified bug and no code is changed.
- `HEADLESS_HERDR_PARTIAL` with one **precise** permission/sandbox/seat/test blocker otherwise; preserve evidence/no duplicate sends. Do not claim scheduled **write-capable** proof from this manually invoked integration.

## After this run (not automatically)

If integrated headless→Herdr→AGY QA PASS, **next owner choice** is one exact clock time for a **single** calendar-triggered W03 or another approved task. Only then arm an isolated one-shot systemd timer; reuse proven infrastructure and require same end-to-end evidence. No recurring nightly timer until **scheduled write-capable** task PASS and owner approves frequency.

**Do not** implement a new framework/CBDS adapter, replace proven Python wrapper, start extra AI workers, merge/push/deploy, modify production DB, disable readiness/locking or create scheduled tasks during this manual integration proof.
