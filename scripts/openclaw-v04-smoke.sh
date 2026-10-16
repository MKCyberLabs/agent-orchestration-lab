#!/usr/bin/env bash
# MKCyberLabs V0.4 manual daytime live smoke on OpenClaw.
# Creates a NEW disposable repository; never touches existing project worktrees.
set -Eeuo pipefail
IFS=$'\n\t'
WORKER="${1:-codex}"
case "$WORKER" in codex|agy) ;; *) echo "Usage: bash scripts/openclaw-v04-smoke.sh [codex|agy]" >&2; exit 2;; esac
RUNNER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
command -v git >/dev/null || { echo "git is required" >&2; exit 2; }
command -v python3 >/dev/null || { echo "python3 is required" >&2; exit 2; }
command -v "$WORKER" >/dev/null || { echo "$WORKER CLI is missing; authenticate before testing" >&2; exit 2; }
STATE_HOME="${XDG_STATE_HOME:-$HOME/.local/state}"
TEST_PARENT="$STATE_HOME/mk-nightshift-smoke"
mkdir -p "$TEST_PARENT"
chmod 700 "$TEST_PARENT"
TEST_ROOT="$(mktemp -d "$TEST_PARENT/fixture.XXXXXXXX")"
chmod 700 "$TEST_ROOT"
BASE="$TEST_ROOT/source"
WT="$TEST_ROOT/worktree"
CFG="$TEST_ROOT/config.json"
REPORT="$TEST_ROOT/state/fixture/reports"
echo "Fixture: $TEST_ROOT"
echo "This pilot consumes a small amount of authenticated $WORKER quota."
echo "No cron/systemd job will be installed. No existing project is modified."

mkdir -p "$BASE"
git init -q -b main "$BASE"
git -C "$BASE" config user.name "Nightshift Fixture"
git -C "$BASE" config user.email "fixture@mkcyberlabs.invalid"
cat > "$BASE/AGENTS.md" <<'EOF'
# Disposable nightshift smoke fixture
Implement ONLY the tiny approved Python functions specified in the current task.
No Git operations, external commands, network requests, installs or file edits
outside the exact task's allowed_paths. The host Python runner executes tests.
EOF
cat > "$BASE/math_ops.py" <<'EOF'
def add(a: int, b: int) -> int:
    """Return the arithmetic sum of two integers."""
    raise NotImplementedError("Implement this simple function")
EOF
cat > "$BASE/text_ops.py" <<'EOF'
def normalize_label(value: str) -> str:
    """Trim and collapse internal whitespace into one space; preserve case."""
    raise NotImplementedError("Implement this simple function")
EOF
git -C "$BASE" add -- AGENTS.md math_ops.py text_ops.py
git -C "$BASE" commit -qm "test: create disposable V0.4 fixture"
git -C "$BASE" worktree add -q -b nightshift/fixture "$WT"

# Config and approval exist ONLY in a private temporary fixture directory.
python3 - "$TEST_ROOT" "$WORKER" <<'PY'
import json
from pathlib import Path
import sys
root, worker = Path(sys.argv[1]), sys.argv[2]
config = {
  "schema_version": 2, "project_id": "fixture",
  "worktree": str(root / "worktree"),
  "backlog_file": str(root / "backlog.json"),
  "state_dir": str(root / "state"),
  "timezone": "Asia/Kolkata", "start": "00:00", "stop": "23:59",
  "approved": True, "worker": worker, "branch": "nightshift/fixture",
  "max_minutes": 35, "task_minutes": 12, "max_tasks": 2,
  "verify_commands": [["python3", "-c",
    "import ast, pathlib; [ast.parse(pathlib.Path(f).read_text()) for f in ('math_ops.py','text_ops.py')]"]]
}
tasks = [
  {"task_id": "TEST_ADD", "approved": True,
   "objective": "Implement ONLY math_ops.add(a,b) so it returns a+b for integers, including zero and negatives. Do not modify any other file. Host acceptance asserts add(2,3)==5, add(-7,3)==-4 and add(0,0)==0.",
   "context_files": ["AGENTS.md","math_ops.py"],"allowed_paths":["math_ops.py"],"depends_on":[],
   "max_diff_lines": 50,
   "acceptance_commands": [["python3","-c",
     "from math_ops import add; assert add(2,3)==5; assert add(-7,3)==-4; assert add(0,0)==0"]]},
  {"task_id": "TEST_LABEL", "approved": True,
   "objective": "Implement ONLY text_ops.normalize_label(value) by trimming leading/trailing whitespace and collapsing each interior whitespace run to one ASCII space while preserving letter case. Host acceptance checks spaces/tabs/newlines and empty input.",
   "context_files": ["AGENTS.md","text_ops.py"],"allowed_paths":["text_ops.py"],
   "depends_on":["TEST_ADD"],"max_diff_lines": 50,
   "acceptance_commands": [["python3","-c",
     "from text_ops import normalize_label as n; assert n('  Hello   World  ')=='Hello World'; assert n('  A\\tB\\nC ')=='A B C'; assert n('   ')==''"]]}
]
(root/"config.json").write_text(json.dumps(config,indent=2)+"\n")
(root/"backlog.json").write_text(json.dumps({"schema_version":1,"project_id":"fixture","tasks":tasks},indent=2)+"\n")
for filename in ("config.json","backlog.json"):
    (root/filename).chmod(0o600)
PY

echo
echo "=== PRE-FLIGHT ==="
python3 "$RUNNER_DIR/scripts/nightshift.py" doctor --config "$CFG"
echo
echo "=== RUN TWO APPROVED FIXTURE TASKS ==="
set +e
python3 "$RUNNER_DIR/scripts/nightshift.py" run --config "$CFG"
RESULT=$?
set -e
echo
echo "=== FINAL LOCAL GIT LOG ==="
git -C "$WT" log --oneline -4
echo
echo "=== MORNING-STYLE REPORT ==="
if [[ -f "$REPORT/$(TZ=Asia/Kolkata date +%F)-morning.md" ]]; then
  cat "$REPORT/$(TZ=Asia/Kolkata date +%F)-morning.md"
else
  echo "Report missing; inspect state.json and logs."
fi
echo
echo "=== ARTIFACTS (PRESERVED) ==="
echo "$TEST_ROOT"
echo "Logs and source are deliberately preserved; do not run git clean/reset."
if [[ "$RESULT" -ne 0 ]]; then
    echo "Smoke test BLOCKED or FAILED; no Night Shift timer has been enabled." >&2
    exit "$RESULT"
fi
echo "Smoke command completed. Verify BOTH tasks show VERIFIED_COMMITTED before declaring PASS."
