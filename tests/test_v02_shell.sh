#!/usr/bin/env bash
# Offline self-test for V0.2 scripts. Does not call a real LLM.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash -n "$root/scripts/install-sol-review-profile.sh"
bash -n "$root/scripts/preflight-codex-reviewer.sh"
bash -n "$root/scripts/run-sol-review.sh"
echo "PASS: Bash syntax"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/bin" "$tmp/repo" "$tmp/state" "$tmp/codex-home"

git init -q "$tmp/repo"
git -C "$tmp/repo" config user.name "Lab CI"
git -C "$tmp/repo" config user.email "lab@example.test"
printf 'def add(a,b): return a+b\n' > "$tmp/repo/calculator.py"
git -C "$tmp/repo" add .
git -C "$tmp/repo" commit -qm "fixture baseline"
git -C "$tmp/repo" branch -M main
sha="$(git -C "$tmp/repo" rev-parse HEAD)"

cat > "$tmp/bin/bwrap" <<'SH'
#!/usr/bin/env bash
exit 0
SH
cat > "$tmp/bin/codex" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
case "${1:-}" in
  --version) echo "mock-codex 0.0.0"; exit 0;;
  sandbox) [[ "${MOCK_SANDBOX_FAIL:-0}" == 1 ]] && exit 23 || exit 0;;
  --profile)
    report=""
    while [[ $# -gt 0 ]]; do
      if [[ "$1" == "--output-last-message" ]]; then report="$2"; shift 2; continue; fi
      shift
    done
    [[ -n "$report" ]] || exit 2
    if [[ "${MOCK_CODEX_VERDICT:-PASS}" == EXEC_ERROR ]]; then exit 29; fi
    if [[ "${MOCK_CODEX_VERDICT:-PASS}" == NO_REPORT ]]; then exit 0; fi
    verdict="${MOCK_CODEX_VERDICT:-PASS}"
    if [[ "$verdict" == MISMATCH ]]; then verdict=PASS; ref="0000000000000000000000000000000000000000"; else ref="$(git rev-parse HEAD)"; fi
    printf 'VERDICT: %s\nReviewed commit: %s\nNo findings\n' "$verdict" "$ref" > "$report"
    exit 0;;
esac
echo "Unexpected mock Codex arguments" >&2; exit 2
SH
cat > "$tmp/bin/cbds" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$CBDS_TEST_LOG"
SH
chmod +x "$tmp/bin/"*
export PATH="$tmp/bin:$PATH"
export XDG_STATE_HOME="$tmp/state"

python3 "$root/tests/test_profile_install.py"
echo "PASS: current Codex profile install, migration and conflict protection"

bash "$root/scripts/preflight-codex-reviewer.sh" >/dev/null
echo "PASS: token-free preflight"

export CBDS_TEST_LOG="$tmp/cbds.log"
CBDS_TASK_ID=tsk_test CBDS_DISPATCH_ID=dsp_test MOCK_CODEX_VERDICT=PASS \
  bash "$root/scripts/run-sol-review.sh" "$tmp/repo" main > "$tmp/pass.log"
grep -q 'VERDICT: PASS' "$tmp/pass.log"
grep -q -- '--outcome succeeded' "$CBDS_TEST_LOG"
grep -q 'VERDICT=PASS' "$CBDS_TEST_LOG"
echo "PASS: accepted PASS report"

: > "$CBDS_TEST_LOG"
set +e
CBDS_TASK_ID=tsk_test CBDS_DISPATCH_ID=dsp_test MOCK_CODEX_VERDICT=FAIL \
  bash "$root/scripts/run-sol-review.sh" "$tmp/repo" main > "$tmp/fail.log"
status=$?
set -e
[[ "$status" -eq 27 ]]
grep -q 'VERDICT=FAIL' "$CBDS_TEST_LOG"
grep -q -- '--outcome succeeded' "$CBDS_TEST_LOG"
echo "PASS: code FAIL is a delivered review, not crashed transport"

: > "$CBDS_TEST_LOG"
set +e
CBDS_TASK_ID=tsk_test CBDS_DISPATCH_ID=dsp_test MOCK_SANDBOX_FAIL=1 \
  bash "$root/scripts/run-sol-review.sh" "$tmp/repo" main > "$tmp/blocked.log" 2>&1
status=$?
set -e
[[ "$status" -eq 22 ]]
grep -q -- '--outcome blocked' "$CBDS_TEST_LOG"
echo "PASS: failed sandbox becomes BLOCKED without a model call"

: > "$CBDS_TEST_LOG"
set +e
CBDS_TASK_ID=tsk_test CBDS_DISPATCH_ID=dsp_test MOCK_CODEX_VERDICT=MISMATCH \
  bash "$root/scripts/run-sol-review.sh" "$tmp/repo" main > "$tmp/mismatch.log"
status=$?
set -e
[[ "$status" -eq 24 ]]
grep -q -- '--outcome blocked' "$CBDS_TEST_LOG"
echo "PASS: wrong reviewed SHA rejected"

[[ "$(git -C "$tmp/repo" rev-parse HEAD)" == "$sha" ]]
[[ -z "$(git -C "$tmp/repo" status --porcelain)" ]]
echo "PASS: source repo unchanged"
echo "ALL OFFLINE V0.2 SCRIPT TESTS PASSED"
