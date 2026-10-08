# Strict Sol QA Ticket Output Contract

Perform a comprehensive review sweep: all changed files, interacting unchanged code,
UI -> server action -> service -> database, security, financial invariants,
concurrency/idempotency, dates/timezones, reminder lifecycle, regression tests and build.
Do NOT stop after the first issue. Report ALL substantiated findings together.
Do not invent evidence or claim a test passed unless actually executed.
Preserve IDs of previously reported issues and verify every claimed fix on the pinned SHA.

After human-readable findings, emit exactly one valid fenced JSON packet (the opening fence
is three backticks immediately followed by json, the closing fence is three backticks):

  schema_version: "1.0"
  reviewed_commit: exact full HEAD SHA
  verdict: same PASS | FAIL | BLOCKED value as first line
  coverage: one item for EACH of:
    authorization, money_math, loan_lifecycle, credit_card_lifecycle,
    concurrency_idempotency, recurrence_timezone, reminder_delivery,
    ui_backend_boundary, tests_build.
  Each coverage item: {"area": string, "status": "EXAMINED"|"NOT_EXAMINED", "evidence": detailed specific path/check}.
  findings: all unresolved issue ticket objects with:
    id (stable uppercase token e.g. SOL-R001-001), severity (P0/P1/P2/P3),
    status (OPEN/REGRESSED/DISPUTED), title,
    file (relative path that exists), line (positive 1-based line number),
    observed (exact actual behavior), expected (correct behavior),
    reproduction (repeatable steps and data), root_cause (call path/reason),
    impact (security/financial/customer consequences),
    fix_strategy (bounded suggested change), acceptance_criteria (nonempty array),
    regression_tests (nonempty array with deterministic tests).
  prior_ticket_dispositions: [{"id":ticket ID, "status":"OPEN"|"REGRESSED"|"VERIFIED_FIXED"|"DISPUTED", "evidence": concrete behavior/test}].
  tests_run: [{"command": exact command really executed, "result":"PASS"|"FAIL"}].
  not_run: string array describing any missing test/build/browser gates.
  release_risks: string array for uncertainty and decisions.

JSON must use real key/value syntax and valid string quoting. Do not emit
a pseudo-JSON outline; construct a valid JSON object with all required keys.

PASS rules:
- No actionable open findings in findings[].
- ALL required review areas marked EXAMINED with evidence.
- Every previously open P0/P1 ticket independently VERIFIED_FIXED.
- A code-review PASS is NOT a release gate PASS: skipped database/build/browser
  tests must be disclosed in not_run.
- Never tailor the verdict to satisfy a quota or retry counter.

FAIL rules:
- One or more actionable issues, all represented as complete tickets.
- Include prior issue disposition (OPEN, REGRESSED, VERIFIED_FIXED, DISPUTED).
- Don't arbitrarily cap count or omit findings to shorten output; group only
  true duplicates, and describe their call sites.

BLOCKED rules:
- If repository, prior tickets, required review areas or evidence cannot be
  inspected, explain why; do not manufacture PASS. Add reason to release_risks.

The first two lines of the complete response must remain:
VERDICT: PASS|FAIL|BLOCKED (one exact value)
Reviewed commit: <exact full HEAD SHA>

A deterministic local validator verifies the packet; invalid responses result
in BLOCKED instead of an accepted PASS. Model completeness is not guaranteed.
