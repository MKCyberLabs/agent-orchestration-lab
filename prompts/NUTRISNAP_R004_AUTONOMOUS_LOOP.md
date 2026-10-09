# NUTRISNAP R004 — AUTONOMOUS TICKET-TO-PASS CAMPAIGN

**User authorization (2026-10-09):** The owner explicitly authorizes unattended R004 repair, test, and independent Codex GPT-6.1 Sol High cycles, up to **5 NEW distinct integrated-code-SHA reviews** in this separately authorized campaign (normally stop after 3 if satisfactory). There is no per-review user-approval requirement within this campaign. Preserve ALL earlier R001/R002/R003 rounds and findings; never relabel previous failure as PASS. This specific owner authorization overrides the earlier V0.2 master prompt's `stop after any Sol FAIL pending owner authorization` for R004 only. All other safety, evidence and acceptance gates remain mandatory. A five-review limit is not a target to exhaust. Model-token availability is finite; rate limits, cost ceilings and account restrictions are real STOP/BLOCKED conditions, not excuses for fabricated PASS.

You are the EXISTING Gemini coordinator in Herdr pane wB:p1 using **real Herdr + cbds**, not a simulated worker framework. Read and respect:
- `~/agent-orchestration-lab/skills/cbds-orchestrator/SKILL.md`
- `~/agent-orchestration-lab/docs/CODEX_REVIEWER_RUNBOOK.md`
- `~/agent-orchestration-lab/docs/V0.2_TICKET_REVIEW_LOOP.md`
- `~/agent-orchestration-lab/scripts/review-loop-gate.py`
- `~/agent-orchestration-lab/scripts/run-sol-review.sh`
- `~/agent-orchestration-lab/prompts/SOL_TICKET_REVIEW_APPENDIX.md`
- the NutriSnap repository's `AGENTS.md` and test scripts.
If any file is unavailable, disclose it and use installed verified command help rather than inventing CLI subcommands.

## A. Fixed baseline and immutable evidence

The last genuinely completed and validated independent FAIL review was:
- Repository: `MKCyberLabs/NutriSnap`
- Reviewed `main` SHA: `f0c914de9ed0c30d3d4ef3754fda967f9f9b64e5`
- Previous comparison base: `f39cd020c0248eac9d2190607747f4313eb3e82f`
- Result: `FAIL`, exit 27, **14 open** (8 P1, 6 P2): seven carried-forward tickets plus seven R003 tickets.
- Do NOT re-review unchanged `f0c914d`, re-run a previously accepted Sol review, or silently reclassify any finding.

Find the actual latest read-only review evidence under:
`/home/openclaw/.profiles/rohit-kumar/.local/state/agent-orchestration-lab/reviews/f0c914de9ed0c30d3d4ef3754fda967f9f9b64e5/`
Resolve the ACTUAL timestamped folder by checking `review.md`, `tickets.json`, `ticket-issues/INDEX.md`, exact reviewed SHA and validator result. Never guess a timestamped path. Copy or link immutable evidence into the campaign ledger without altering the original files.

Initial OPEN ticket IDs, precisely these fourteen:
- P1: `SOL-R001-004`, `SOL-R001-007`, `SOL-R001-008`, `SOL-R003-001`, `SOL-R003-002`, `SOL-R003-003`, `SOL-R003-004`, `SOL-R003-007`
- P2: `SOL-R001-011`, `SOL-R002-006`, `SOL-R002-007`, `SOL-R002-008`, `SOL-R003-005`, `SOL-R003-006`

Keep a **single authoritative ledger** recording every old and new ticket as OPEN, REGRESSED, DISPUTED or VERIFIED_FIXED, including precise source reference, root cause, acceptance tests and evidence. Historical 9 verified fixes and original R001-P1 tickets remain tracked for regressions.

## B. Critical 6 AM automatic-merge safety gate — BEFORE ANY work branch push

The owner operates a local 6 AM IST script that merges sub-branches into `main`. Read the REAL script/scheduler configuration and its branch-selection behavior; do not guess which branches are included. Treat any branch automatically merged before approval as a safety violation.

- Prepare an isolated R004 worktree/branch rooted at exact `f0c914d`, suggested: `/home/openclaw/Projects/NutriSnap-r004-auto`, `orchestration/finance-r004-autoloop`.
- Keep this branch excluded from ALL automated promotion/merge mechanisms; preferably it is local-only during repair and review.
- If the scheduled merge also scans local branches, put a narrow explicit exclusion for `orchestration/finance-r004-autoloop` in the actual script. First back up the original, inspect/dry-run or test the selector, and verify the exclusion. Do not change behavior for unrelated branches, disable all scheduled jobs, force-push, or rewrite main.
- If exclusion cannot be proved, report `BLOCKED_AUTOMERGE_SAFETY` and STOP BEFORE creating/pushing code repairs or beginning expensive model work.
- No production database writes, deployment, payments, migrations, live credentials, force pushes or merges to `main`. All DB tests must point exclusively to isolated test PostgreSQL (typically port 5433); prove connection target before mutation.
- Refresh `origin/main` and verify it is still exactly `f0c914de9ed0c30d3d4ef3754fda967f9f9b64e5` before starting. If not, STOP and report divergence rather than silently shifting scope.

## C. Durable cbds state and round initialization

1. `cbds status`, `herdr pane list`; rehydrate the existing R001 run `run_m4b5hrvfwv4xw`, its reports/dispatches, and confirm no orphaned live workers/review processes. Preserve its history. If R001 is still open, settle it using actual accepted reports and documented commands; do not lose audit evidence or duplicate existing tasks. Use a fresh named cbds R004 run ONLY if permitted by current installed cbds semantics; otherwise continue the existing valid run with distinct R004 tasks.
2. One coordinator, maximum two simultaneous source-editing AGY workers, nonoverlapping file allowlists, one active Codex reviewer at a time. Each worker must use genuine cbds dispatch/task/report lifecycle and stable checkpoint IDs.
3. Read `review-loop-gate.py --help`. For the R004 repository create a NEW state file scoped only to this campaign. Initialize with `--max-rounds 5 --completed-rounds 0 --last-reviewed-sha f0c914de9ed0c30d3d4ef3754fda967f9f9b64e5 --prior-result FAIL --initial-ticket-ids` containing all fourteen IDs. Use `--branch orchestration/finance-r004-autoloop`, actual `--repo`, and real cbds run ID. Do NOT edit JSON by hand, reset review_count, or overwrite prior state.
4. After a crash, read current cbds and gate state and resume from the LAST accepted transition. Never re-dispatch a settled task or repeat a reviewed SHA.

## D. Round 1: repair all 14 existing tickets before invoking Sol

Worker A, ideally `agy-manickam`, exclusive source ownership:
- `src/lib/finance/finance-service.ts`
- `src/lib/scheduler.ts`
- `src/lib/finance/debt-service.ts`
- `src/components/finance/ObligationForm.tsx`
- Tickets: `SOL-R001-004`, `SOL-R001-007`, `SOL-R001-008`, `SOL-R002-008`, `SOL-R003-001`, `SOL-R003-004`, `SOL-R003-007`.

Worker B, ideally `agy-rohit`, exclusive source ownership:
- `src/lib/finance/loan-service.ts`
- `src/lib/finance/credit-card-service.ts`
- `src/components/finance/LoanForm.tsx`
- `src/app/finance/bills/page.tsx`
- Tickets: `SOL-R001-011`, `SOL-R002-006`, `SOL-R002-007`, `SOL-R003-002`, `SOL-R003-003`, `SOL-R003-005`, `SOL-R003-006`.

Assign test files to a single owner each; create distinct new test files as needed. If root causes cross the file boundary, settle ownership BEFORE editing, with coordinator-owned bounded integration fixes only after workers finish. Each repair must address the underlying invariant, not simply patch the demonstrated example. Preserve user-account isolation, idempotency, loan/card/debt accounting conservation, timezone-specific calendar rules, reminder schedule and lease/fencing correctness.

Specific mandatory regressions:
- Concurrent distinct/raw-vs-date-only EMI keys, correct stable occurrence identity under row locks.
- Scheduler claim vs concurrent schedule change, lease expiry, simultaneous claimers and late completion from an old attempt; attempts must be fenced.
- Concurrent debt repayments with actual PostgreSQL transactions and outstanding/idempotency verification.
- Statement membership validation during credit-card reversal under statement lock.
- Custom/malformed note bracket metadata, maximum note length and legacy payment notes.
- Legacy/unlinked scheduled-date fallback without replacing the scheduled due date with the transaction timestamp.
- Explicit configured user timezone across LoanForm, DebtForm and ObligationForm; daylight-saving boundary.
- Statement-managed bills hide generic Paid action and propagate the chosen payment-account ID.

Both workers must provide committed full SHA, exact changed files, test assertions/output, defect disposition and genuine accepted cbds report. No isolated worktree result is trusted until integrated and retested.

## E. Deterministic integration gates — model-free first

Before every Sol review:
1. Verify worker cbds outcomes and accepted report IDs, Git commit lineage, file allowlists, no dirty worktree, no overwriting previously accepted changes.
2. Integrate only accepted commits into isolated R004 branch; record the exact SHA. No full-repo test evidence from a worker is sufficient by itself; rerun on INTEGRATED SHA.
3. Run the repository's verified local gate and relevant tests (finance, loans, payments, reminders/scheduler, real test-DB concurrency, security/auth, life-hub, food, today, UI, analysis contract), `npm run typecheck`, `npm run build`, and `git diff --check`. Capture exact commands, exit codes, totals, postgres target and immutable logs. If not configured, mark browser/UI e2e `NOT_RUN` instead of PASS; try safe isolated browser smoke testing if existing test runner supports it.
4. If deterministic test FAIL, repair locally/through distinct accepted cbds tasks BEFORE spending Sol tokens. No reviewer call while software gates fail.
5. Prepare a concise canonical prior-ticket ledger (all open IDs, statuses, acceptance evidence, historical regression-sensitive areas) within the `SOL_REVIEW_PRIOR_TICKETS_FILE` wrapper's 20,000-byte inclusion limit. Do not silently truncate prior ticket IDs or send huge redundant raw reports.
6. Use `review-loop-gate.py integrate` with genuine accepted cbds report IDs and a real nonempty final test-evidence file. Do not fake IDs or invent passing evidence. The R004 code SHA must differ from last reviewed SHA.

## F. The automatic Sol review cycle (maximum FIVE new valid reviewed SHAs)

Run one independent GPT-6.1 Sol High read-only reviewer on the exact integrated R004 SHA, with `SOL_REVIEW_TICKET_MODE=1` and `SOL_REVIEW_PRIOR_TICKETS_FILE=/actual/concise/ledger`, via:
```bash
SOL_REVIEW_TICKET_MODE=1 \
SOL_REVIEW_PRIOR_TICKETS_FILE="/absolute/path/to/concise-prior-ticket-ledger.md" \
bash /home/openclaw/agent-orchestration-lab/scripts/run-sol-review.sh \
  /home/openclaw/Projects/NutriSnap-r004-auto \
  f0c914de9ed0c30d3d4ef3754fda967f9f9b64e5
```

Interpret `exit 27 + valid validated ticket packet + FAIL` as SUCCESSFUL delivery of a failed CODE review, not an agent crash. `exit 0 + PASS` is a review PASS ONLY if strict packet validation and SHA checks pass. `BLOCKED/invalid JSON/quota/sandbox/network` is NOT a code FAIL or PASS: record evidence and STOP; never fabricate coverage or force a passing disposition. A rate limit may be retried ONLY after a verified reset, with the old process proven terminated and at most one controlled retry; do not spin on the limit.

Use `review-loop-gate.py review --repo ... --report /actual/review.md` for a VALID review result to update durable status, preserving ticket continuity. If `FAIL`:
1. Read the WHOLE tickets.json, previous dispositions and fresh issue-card batch; deduplicate by root cause but retain stable IDs.
2. Assign all substantiated P0/P1/P2 findings as bounded cbds repair tasks with clear file ownership, acceptance criteria and real regression tests; include P3 in ledger, do not silently waive.
3. Continue repairs/integration/testing/review automatically with a NEW code SHA, only if `review_count < max_rounds`, no safety blocker, and there is evidence the next patch fixes concrete findings.
4. Never run another Sol review on the SAME SHA. Never invoke multiple reviewers in parallel. Never treat 5 reviews as an instruction to spend 5 reviews when PASS is already reached.
5. If fifth valid review FAILs, `max_rounds_reached` is a HARD STOP with HOLD, preserved evidence and full remaining tickets. Do not reset state or start a sixth campaign.

If `PASS`, verify all open blocking tickets were explicitly VERIFIED_FIXED in validated dispositions and all 9 required coverage domains were EXAMINED. Independently rerun software gates on the exact same review SHA and check for any changes since review. If SHA changes, invalidate approval and require a new review within the remaining budget.

## G. Exit criteria, remote push and owner-facing report

On PASS and all applicable automated gates, output `REVIEW_PASS_PENDING_RELEASE_GATES`; browser/UI e2e or other NOT_RUN gate must remain explicitly pending. Never equate Sol PASS with production approval.

If safe merge-exclusion is proven, you may push ONLY the isolated R004 feature branch (no main, no force push). Do not automatically merge to main, change prod DB, or deploy; these always require owner approval.

Publish a compact durable report with: campaign run ID, rounds consumed (new and historic separately), each reviewed code SHA, Sol verdict/packet path, open/verified/regressed ticket counts and IDs, all accepted worker cbds report IDs, test output links and evidence, test DB target, UI gate, exact final branch SHA, remote status, cost/quota blockers and clear owner action.

STOP STATUSES (never claim PASS otherwise):
- `REVIEW_PASS_PENDING_RELEASE_GATES` if independent Sol PASS and automated gates pass, but human/product/UI approval remains.
- `BLOCKED_AUTOMERGE_SAFETY` if 6 AM auto-merge exclusion cannot be proved.
- `BLOCKED_ENVIRONMENT` for invalid Sol packet, missing cbds verification, auth, quota, DB or sandbox trouble.
- `HOLD_UNRESOLVED_FINDINGS` on 5th FAIL or any unresolved P0/P1.
- `HOLD_TEST_FAILURES` for failing deterministic gates.
- `HOLD_MAIN_DIVERGED` if starting origin/main differs from the reviewed baseline.

This owner's current message authorizes fully autonomous bounded review ITERATIONS without re-prompting on every genuine Sol FAIL, but no release/main merge/production changes.
