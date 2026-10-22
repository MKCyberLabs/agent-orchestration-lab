# W04 — NutriSnap Hydration Weekly Average: complete autonomous delivery run

**LATEST OWNER RECOVERY AUTHORIZATION (2026-10-22):** Initial W04 was blocked without dispatch because named AGY-Manickam had exited. **The obsolete strict no-new-pane/absent-worker STOP is superseded by [ONE-GO seat recovery + W04 instructions](V05_ONE_GO_SEAT_RECOVERY_W04_2026-10-22.md)**. It authorizes one necessary shell/pane, one verified authenticated Manickam start, W04 build and independent QA. Preserve all earlier code and reports.
**Created:** 2026-10-22 IST · **Owner objective:** Ship a useful product fix via existing Nightshift without another analysis/approval loop.
**Status:** PLAN READY, **NOT CODED**. **Source grounding:** GitHub `MKCyberLabs/NutriSnap` `main` inspected 2026-10-22; the actual local OpenClaw worktree remains authoritative and may differ.
**Model guidance:** Use currently selected GPT-6-Astra for no more architecture review; switch to GPT-6.1-Sol High for coding/coordinating. Quota reported 64% remaining (owner observation), **not** a guaranteed wall-clock or token budget.

## A. Truth before action — DO NOT recreate Nightshift

- V0.5 one-shot pipeline DONE, per owner-provided local logs: Gate C final launcher exit `0` with `REVIEW_REQUIRED`; builder commit `9934c6261c728c5a0dba9954b781a8b03fe29c12`; launcher repair `45d7e8285617d1c231417d2ed643d7581d740911`. 107 finance, 74 reminder, 13 focused, 7 browser checks PASS.
- Local review document exists at `/home/openclaw/worktrees/agent-orch-v05-p0/docs/v0.5/OCT22_VERIFIED_STATUS_AND_DECISIONS.md`, documentation commit `eb9b57a5205ba11a2d83dc791b930460d796123`, according to owner-provided screenshot. **Read it locally**. No need to paste/re-fetch its body into prompts.
- Historical NutriSnap NS-01/02 and Gate C commits are local/unmerged; `PUSH_HOLD` remains, prior dirty original checkout untouched; routine development happens in isolated NutriSnap night worktree. Herdr existing lead Codex / builder AGY-Manickam; do not start extra seats, build Python frameworks, integrate CBDS, or re-run prior H-tests.
- Open owner decisions remain **(a)** manual merge/review of the existing night branch and **(b)** whether recurring scheduling is ever enabled. Neither should block this W04 local developer task. **Do not push, merge, deploy or schedule during W04.**

## B. Reproduced code-level issue (remote main, verify local)

File: `src/app/hydration/page.tsx`, approx. lines 259–321. `weeklyStats` computes a seven-element `dayTotals` array, `totalWater` and `totalOther`, then `avgTotal = Math.round((totalWater + totalOther) / 7)`. The current week's future days are counted in the denominator despite not having elapsed. The same page uses `dailyGoal * 7` in its weekly water-goal indicator, potentially inconsistent with a partial current week. Data loader: `src/app/hydration/actions.ts` `getWeeklyHydrationData`, weekly Monday-start navigation, normal hydration log CRUD; preserve these existing paths.

**Definition of done**: User opening the Weekly view midweek sees an average across **elapsed calendar days in that displayed week, inclusive of today**, NOT all seven; a past fully completed week still divides by seven. Display remains stable with no logs and no future-dated logs. Don't alter historical log values, daily goal, database schema, Telegram, or other modules.

### Concrete acceptance examples (week starts Monday, in the same user-local date frame used by UI)

- **Current Thursday:** Monday 1000 ml, Tuesday 2000 ml, Wednesday 0 ml, Thursday 3000 ml ⇒ total 6000 / **4** = **1500 ml/day**; Fri–Sun are not in the denominator.
- **Current Monday:** 500 ml logged today ⇒ **500 ml/day** (1 day), not 71. No logs ⇒ 0 (not NaN, not divide-by-zero).
- **Current Sunday:** all seven calendar days elapsed ⇒ divide by 7. Previously completed week ⇒ divide by 7.
- **Week entirely in future:** denominator must not become negative or zero-division; avoid showing false average/progress; future nav is normally disabled but function remains safe.
- **User-selected old week:** existing zero-log days DO count in the 7-day denominator. Do **not** divide only by the number of days containing logs.
- **Calendar boundaries:** week crossing month/year, day transitions around midnight and timezone/calendar-day normalization; no mixing UTC milliseconds with local calendar day counts. Use existing date-fns app conventions, do not invent a new timezone service.
- **Drink types:** `totalWater + totalOther` is the current all-drink weekly average contract. Preserve this unless real source/tests prove another intended definition.
- **Related UI consistency:** if partial-week goal/progress indicators refer to elapsed days, use the *same effective day count* rather than keeping a misleading 7-day goal. Keep scope tight; do not redesign the chart/whole screen.

## C. Full implementation path — ONE coordinator turn, ONE builder, ONE QA owner

**Preflight (read-only and quick):** From OpenClaw, inspect `docs/v0.5/OCT22_VERIFIED_STATUS_AND_DECISIONS.md`, existing NutriSnap isolated night branch/worktree actual HEAD/status, exact hydration source/tests; ensure the W04 bug still exists. If already fixed, TEST IT and report `W04_ALREADY_PASS`, no fake implementation. No code changes in original dirty checkout. Don't merge or reset prior commits.

**Step 1 — Send one clear AGY-Manickam build task:** Codex High is AI coordinator. AGY-Manickam writes the actual change, ideally extracts a small pure `getElapsedWeekDays`/weekly stats helper within an existing hydration-specific module or a single tiny added module to enable deterministic tests. Choose the smallest edit. No new dependencies, schema, auth or Telegram changes. Preferred allowed files: `src/app/hydration/page.tsx` and ONE hydration-specific helper/test pair if needed. If more files are genuinely required, document exactly why before editing; never change unrelated tracked files.

**Step 2 — Builder runs fast tests, commits locally:** Add deterministic unit/regression tests for all example cases (time frozen or injected `now`, no wall-clock-dependent flaky tests); ensure both current and historical week logic. Keep clean Git diff. Agent returns SHA, files changed, tests run. No push or GitHub update.

**Step 3 — Independent Codex verification:** Codex High **does not author the implementation**; inspect changed diff and challenge edge cases. Re-run new focused tests independently, existing appropriate hydration/related tests, `npm run typecheck`, and `git diff --check`. Run targeted browser UI check of weekly tab on local/test server if already available; no production deployment or live user data modification. Explicitly distinguish `BROWSER_PASS`, `BROWSER_NOT_RUN` (environment missing), and `BROWSER_FAIL`—no invented screenshots. If the UI has a visible weekly average, verify that value matches tested examples and historical weekly behavior.

**Step 4 — Limited repairs:** If test/review FAIL, Codex sends only concrete failing findings to Manickam; at most **two repair + re-test iterations** within the **same task** (at most 3 builder coding prompts total). On fixed PASS, stop—don't optimize extra. On still FAIL/quota/no safe worker, stop with `PARTIAL` and preserve code SHA/evidence; no silent prompt retries after unknown Herdr timeout. **Codex self-testing is independent of AGY author; do not claim full independent review if Codex had to edit production code itself.**

**Step 5 — One owner-ready result:** Write a short local report `docs/v0.5/evidence/W04_HYDRATION_WEEKLY_AVERAGE_RESULT.md` under a *safe* documentation path/worktree (or run-state `morning.md` when local repo split makes that safer). Include actual source SHA(s), exact tests and results, denominator table, model/agent startup/prompt/repair counts, browser check state, screenshot paths if any, changed file list, pending baseline failures, and local review instructions. Code branch clean, unmerged. No re-documenting V0.5 architecture or H1–H5.

**Working mode:** Because V0.5 launcher is proven, don't run any more smoke tests of the launcher for this feature. It's acceptable for today's owner-invoked Codex High turn to coordinate Manickam directly; if using the launcher, it must originate from an existing plain shell after Codex is idle, never prompt Codex's currently occupied pane. One dispatch only, no blind resend.

## D. Stop conditions, quota and autonomy

- One task authorization covers implementation, isolated tests, local commits and up to two repair turns. **Do not ask the owner for another approval merely to run a test or correct a failing assertion.**
- Reserve quota for QA; pragmatic allocation of today's remaining capacity: **up to 15% investigation/prompting, ~60% implementation/repairs, ≥25% independent QA/report**, as *planning proportions of available quota*, not guaranteed usage controls.
- Any new trust/credential/survey/OS privilege prompt, unexpected dirty tracked files in the W04 worktree, model quota exhaustion, unknown dispatch state, changed app requirements, production DB changes or irreversible action: `WAITING_FOR_HUMAN` or `PARTIAL` with exact blocker. No automatic permission acceptance, no duplicate task sends, no extra agents.
- Keep **scope guard**: ship the lamp (correct weekly stats), not a moon generator (new hydration engine, full analytics layer, reminder scheduler rewrite or product redesign).

## E. Acceptance matrix for final reviewer

| Requirement | Exact proof | Must pass? |
|---|---|---|
| Partial current week | Frozen Thursday fixture, 6000/4=1500 | Yes |
| Current Monday / empty | 500/1=500, 0/1=0 | Yes |
| Historical + Sunday | 7-day denominator | Yes |
| Never count future days | Injected current date, future dates ignored/safely handled | Yes |
| Date boundaries | Month/year and local-day scenarios | Yes |
| No cross-module regression | typecheck + relevant existing tests + diff check | Yes |
| UI weekly average | Local browser if available, otherwise report `NOT_RUN` explicitly | Browser expected if test environment supports it |
| Module commits & evidence | Code SHA, clean branch, exact test counts, one report | Yes |
| No forbidden action | No push/merge/deploy/schema/schedule or new framework | Yes |

**Final return fields:** `W04_PASS` or `W04_PARTIAL` or `W04_BLOCKED` · local code SHA · actual command/count summary · UI verification status · clean Git branch · one next owner action. Stop. Do NOT propose another H-phase.

## F. One user-visible next action (copy 2 lines, not this file)

Select **GPT-6.1-Sol (High)** in the Codex model picker, within existing `agent-orchestration-lab` project. Then say:

> Execute W04 from `docs/v0.5/W04_HYDRATION_COMPLETE_RUN_PLAN_2026-10-22.md` on `origin/planning/v0.5-p0-handoff-20261019`. One bounded Codex→AGY-Manickam implementation + independent QA + at most two repairs; finish the module and local report in this run. Follow actual local status, protect original checkout, no push/merge/deploy/scheduling. Return `W04_PASS` with commit and tests or one specific blocker.

Fetching the instruction file is permitted; remote instruction Git is not authority to overwrite live unpushed code.

## G. Questions tracked instead of interrupting execution

1. Should W04 include a revised weekly water-goal progress widget? **Default yes, only if the existing widget explicitly measures current-week progress and the mismatch is reproduced; same denominator, no redesign.**
2. Should a future week be navigable? **Default no change; preserve current navigation controls, merely avoid divide-by-zero in helper.**
3. Should the average count only days with logs? **No—count elapsed calendar days; missing days are zero.**
4. Should W04 go into main? **No. Owner must review the unmerged branch and approve promotion separately.**
