#!/usr/bin/env bash
# Read-only independent Codex review pinned to a Git SHA.
# bash scripts/run-sol-review.sh /absolute/path/to/project [base_ref]
# For cbds integration, this MUST be executed inside a cbds-managed shell with genuine CBDS_* env.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="${1:-}"
base="${2:-origin/main}"
if [[ -z "$repo" ]]; then
  echo "Usage: bash scripts/run-sol-review.sh /path/to/repo [base_ref]" >&2
  exit 2
fi

cbds_context=0
if [[ -n "${CBDS_TASK_ID:-}" || -n "${CBDS_DISPATCH_ID:-}" ]]; then
  if [[ -z "${CBDS_TASK_ID:-}" || -z "${CBDS_DISPATCH_ID:-}" ]]; then
    echo "BLOCKED: incomplete CBDS_* worker identity" >&2
    exit 3
  fi
  cbds_context=1
fi

finish() {
  local verdict="$1" details="$2"
  echo "VERDICT: $verdict"
  echo "$details"
  if [[ "$cbds_context" == 1 ]]; then
    if [[ "$verdict" == BLOCKED ]]; then
      cbds done --outcome blocked --subject "Sol review blocked" \
        --question "Resolve reviewer environment or specification blocker before review approval" \
        --body "$details"
    else
      # A finding FAIL is a successfully completed *review*, never code approval.
      cbds done --outcome succeeded --subject "Sol independent review delivered: $verdict" \
        --body "VERDICT=$verdict; $details"
    fi
  fi
}

if ! git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  finish BLOCKED "Not a valid Git worktree: $repo"
  exit 20
fi
repo="$(git -C "$repo" rev-parse --show-toplevel)"
sha="$(git -C "$repo" rev-parse --verify HEAD)"
if ! git -C "$repo" rev-parse --verify "${base}^{commit}" >/dev/null 2>&1; then
  finish BLOCKED "Base ref $base unavailable in $repo. HEAD=$sha"
  exit 21
fi
if ! bash "$script_dir/preflight-codex-reviewer.sh"; then
  finish BLOCKED "Sandbox preflight failed. HEAD=$sha. No model review started."
  exit 22
fi

state_base="${XDG_STATE_HOME:-$HOME/.local/state}/agent-orchestration-lab/reviews"
work="$state_base/$sha/$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$work"
chmod 700 "$work"
prompt="$work/prompt.md"
result="$work/review.md"
stdout="$work/codex.stdout.log"
stderr="$work/codex.stderr.log"

cat > "$prompt" <<EOF
You are GPT-6.1 Sol High, independent READ-ONLY code and security reviewer.
Project path: $repo
Reviewed commit: $sha
Base ref: $base
Inspect the full Git diff from the merge base through HEAD. Verify security,
user ownership, financial invariants, reminders, idempotency, regression
tests and any prior repair evidence. Do not modify any files, dispatch
workers, access live credentials, initiate payments or run destructive commands.
Only report tests actually executed. If repository access is unavailable,
return BLOCKED, not a fabricated verdict.

The FIRST lines of your response MUST be precisely:
VERDICT: PASS|FAIL|BLOCKED   (select exactly one)
Reviewed commit: $sha

Then include:
- Findings ranked P0/P1/P2 with exact path:line evidence, or "No findings";
- Which tests you actually ran and their results;
- Prior findings coverage;
- Integration recommendation.
Do not claim PASS if you could not read Git files.
EOF

echo "Review target $sha (base $base)"
echo "Evidence directory: $work"
set +e
(
  cd "$repo" &&
  codex --profile sol-review exec \
    --model gpt-6.1-sol \
    --sandbox read-only \
    --output-last-message "$result" \
    - < "$prompt"
) > "$stdout" 2> "$stderr"
rc=$?
set -e

if [[ $rc -ne 0 || ! -s "$result" ]]; then
  finish BLOCKED "Codex process unavailable or no output (exit=$rc); HEAD=$sha; logs=$work"
  exit 23
fi
verdict="$(sed -nE 's/^VERDICT: (PASS|FAIL|BLOCKED)$/\1/p' "$result" | head -n 1)"
if [[ -z "$verdict" ]] || ! grep -Fqx "Reviewed commit: $sha" "$result"; then
  finish BLOCKED "Reviewer verdict/SHA missing or mismatched. Expected HEAD=$sha; report=$result"
  exit 24
fi
if [[ "$verdict" == BLOCKED ]]; then
  finish BLOCKED "Reviewer returned BLOCKED; HEAD=$sha; report=$result"
  exit 25
fi
if [[ "$(git -C "$repo" rev-parse HEAD)" != "$sha" ]]; then
  finish BLOCKED "HEAD changed during review; original=$sha; report=$result"
  exit 26
fi

finish "$verdict" "Reviewed commit=$sha; base=$base; report=$result"
echo "Evidence: $result"
if [[ "$verdict" == FAIL ]]; then
  exit 27
fi
