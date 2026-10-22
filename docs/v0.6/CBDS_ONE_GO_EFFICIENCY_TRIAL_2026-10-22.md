# V0.6 Experiment 01 — Does CBDS actually save Nightshift tokens and lost results?

**Created 2026-10-22 IST. Owner intent:** W04 and repeat-run recovery passed; stop rereading terminal output, use available model budget for durable handoffs if CBDS is genuinely cheaper and reliable. **Run ONE bounded experiment now, not another architecture review or framework rewrite.** Owner asks to try CBDS, but has not approved global upgrades, login/trust bypass, push/merge/deploy or recurring scheduling.

## 0. Freeze what already worked

- **V0.5 one-shot PASSED** with local Gate C evidence, launcher `b3e91d44d0ab5d474578ccc0de5f62f2a3e7402f`, readiness repair `45d7e8285617d1c231417d2ed643d7581d740911`; do NOT rebuild or replace Python launcher.
- **W04 + REPEAT_RUN_RECOVERY_PASS** (owner-provided Oct 22 report): local NutriSnap code SHA `8a13c3c77250b829292fd47f28365b34cda6425e`, 40 test executions + typecheck/diff + 6/6 browser checks including 1500 ml/day Thursday + historical week, 1 repair; active Manickam recovered in `wE:p2`, inspected idle after completion. Evidence `/home/openclaw/worktrees/agent-orch-v05-p0/docs/v0.5/evidence/W04_ONE_GO_RECOVERY_RESULT.md` (local docs commit `b9a4051`). These SHAs may not exist on the *remote GitHub instruction branch* due to `PUSH_HOLD`.
- **No further changes to W04** absent an actual regression. No new NutriSnap commits in this CBDS trial; preserve original dirty checkout and clean, unmerged W04 branch. First confirm the current OpenClaw/local source and receipt read-only rather than run prior suites.

## 1. Decision question (not a preconceived CBDS adoption)

**Does our installed CBDS + Herdr support a one-task, authenticated AGY builder handoff with a durable machine-readable completion report, fewer terminal reads and acceptable context/startup overhead?**

**Official CBDS public docs**, not guarantees about installed v2.3.0:
- `cbds dispatch start` normally creates a real Herdr worker pane/starts an agent and injects `CBDS_TASK_ID`/`CBDS_DISPATCH_ID`.
- `cbds done` writes authoritative on-disk completion, `cbds wait` blocks until report/timeout; prevents terminal scraping as completion detector.
- `dispatch start --pane <id>` is documented in design for a **preexisting shell pane**, not necessarily an **already-running authenticated AGY** agent. Do not assume it reuses a live Manickam process.
- CBDS published `cbds skill install` list excludes explicit AGY; Herdr `--kind agy` does not prove CBDS worker-skill loading or `--agent agy` support in the locally installed release.
- Published ~25-token anchor vs ~380-token inline completion protocol estimate is **not measured total task token usage**. Starting a fresh worker may reload more context than saved by a short preamble. Do not claim quota savings without observed evidence.
- References: https://github.com/zqkra/cbds and https://herdr.dev/docs/agent-automation/ .

## 2. ONE experiment, same Codex lead; no new Nightshift architecture

**Target:** Existing OpenClaw dev VM; existing Codex High coordinator; AGY-Manickam profile already authenticated. Use GPT-6.1-Sol **High** for this bounded investigation; reserve Ultra/Extra High for ambiguous faults or advanced coding. Do not spend quota on agent logs in chat.

### A. Fast compatibility check (read-only; do not stop for a new approval)

Run `cbds --version`, `herdr --version`, `cbds dispatch start --help`, `cbds skill status`, `cbds status`, `herdr agent list`. If installed help differs, prefer actual installed flags and record exact results. Identify: **AGY kind supported? Can use a preexisting *empty* shell pane? Can an already LIVE AGY-Manickam be attached without relaunch? Does this version support worker reporting when no skill is installed? Can completion state be kept in an isolated state directory?**

**Immediate decision:** If AGY kind is unsupported, or a dispatch needs unknown credentials/unapproved installation, or the test would disrupt a currently live Manickam task/seat, **do NOT integrate CBDS**. Record `CBDS_INCOMPATIBLE` and one honest recommendation. Do not burn time designing adapters around unsupported CLI flags.

### B. If compatible, one bounded real CBDS task

- Use an **isolated CBDS state dir** outside app repos or a disposable fixture directory, one CBDS run and one task. Do not dual-write authoritative NutriSnap campaign state. No global installations/upgrades/skill mutation unless explicitly required and already supported safely; follow installed --help for precise args.
- Assign **one read-only builder task**: inspect the already completed local W04 commit `8a13c3c77250b829292fd47f28365b34cda6425e` and list the changed paths plus how the implemented weekly average avoids including future days. Do not modify files, rerun W04 tests or make Git commits. This validates real AGY delegation and receipt without unnecessary app code churn.
- If CBDS can dispatch to existing live AGY **without killing/restarting it**, prefer that. Otherwise test with **at most one existing empty shell pane**, or one needed new shell pane if none is available; **one** additional short-lived AGY process with the verified existing Manickam profile is allowed only if no existing live coding task is disrupted. Capture pane ID and startup count. No new login/account/permissions.
- Worker must invoke **`cbds done`** with actual task status/summary; coordinator uses **`cbds wait`** with bounded timeout and `cbds report`/installed equivalent. The coordinator must **not poll full terminal transcripts**, and must not interpret Herdr idle as success. One dispatch only; no retry on uncertain send. Preserve state and report if timeout.
- If an explicit trust/login/survey/privilege dialog appears that is not covered by a prior exact approval, record `WAITING_FOR_HUMAN` without auto-Yes.
- Verify structured report task ID, dispatch ID, outcome, changed file count (expected 0), durability across a second read after the wait, no duplicate report. Do not run parallel agents or other tasks.

### C. Measure the thing the owner cares about

Record in **one** local `docs/v0.6/CBDS_TRIAL_RESULT_2026-10-22.md`:
1. Installed CBDS/Herdr versions and CLI-compatible AGY result; note public/local discrepancies.
2. New pane/process startups; total coding/worker prompts; repairs; full terminal read count; coordinator tool calls.
3. Task/report outcome, IDs, duration (if measured), completion record location, any loss/blocked flags.
4. Token usage from **actual CLI/session meter if available**, not estimated. If absent, mark **UNKNOWN** and compare qualitative overhead only. Do not equate remaining quota percentage with actual spent tokens.
5. Compare to prior direct Herdr W04 outcome without falsely pretending identical workloads. Mark inability to compare quantitatively.
6. Give ONE verdict:
   - `CBDS_ADOPT_FOR_BUILDER_HANDOFF` only if real AGY task+durable report succeed, no unforeseen prompt/recovery problems, and overhead is acceptably bounded. Proposed integration can be a future **minimal opt-in transport**, Codex still plans/tests, Python remains launcher. No second ledger.
   - `CBDS_PILOT_PASS_SAVINGS_UNPROVEN` when reliable but startup/context/token benefit unmeasured; remain optional until comparative evidence.
   - `CBDS_SKIP` if no AGY compatibility, repeated trust overhead, extra agent processes and context outweigh usefulness, or control-plane complexity.
- **No blanket architecture refactor** even if the experiment succeeds. A successful protocol pilot is not permission to auto-enable CBDS across all Nightshift runs.

## 3. If CBDS is not better: stop terminal spam without a new system

Keep Herdr + existing run-specific `receipt.json`/`morning.md`. Improve coordinator **instructions**, not tooling: one handoff → one bounded `agent prompt --wait` / `agent wait` → read the small structured report or Git SHA, not periodic `pane read 200 lines`. On ambiguous timeout inspect the durable artifact once; no blind resend. Use truncated status JSON rather than full terminal transcripts. This route can reduce expensive context ingestion without any new CBDS dependency.

## 4. Security and completion boundary

**Allowed in this single trial:** read-only tool inspection; one isolated disposable CBDS run and one read-only real AGY worker task if locally supported, one necessary shell pane/short-lived worker only when safe, structured report, one scoped local docs commit. Do not replace existing working agents, do not auto-approve new trust, no source code edits to NutriSnap, no new Python framework, no global install/upgrade, no push/merge/deploy/production actions/timer, no model credential disclosure, no automatic second trial.

**Evidence > plans:** After the experiment, stop. Return a short verdict, actual measured facts, report location, local docs SHA, and the next productive NutriSnap goal. If CBDS fails, keep V0.5 and move on instead of initiating a CBDS architecture rescue project.

## 5. Copyable invocation for Codex High (one short message)

> Read `docs/v0.6/CBDS_ONE_GO_EFFICIENCY_TRIAL_2026-10-22.md` from `origin/planning/v0.5-p0-handoff-20261019`. Execute ONE bounded CBDS-vs-Herdr experiment on the existing OpenClaw dev setup, including read-only compatibility verification and (only if supported) one read-only AGY builder dispatch with authoritative `cbds done`/wait result. Measure pane starts, terminal reads and actual tokens when available. Do not change NutriSnap or Nightshift production code, don't upgrade/install or auto-trust, and do not recreate V0.5 architecture. Save one local evidence report, commit docs locally, return ADOPT/PILOT_PASS_UNPROVEN/SKIP with measured reasons.
