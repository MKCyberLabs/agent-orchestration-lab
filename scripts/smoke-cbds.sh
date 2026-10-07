#!/usr/bin/env bash
set -euo pipefail

if ! command -v cbds >/dev/null 2>&1; then
  echo 'cbds is not installed. See README.md.' >&2
  exit 2
fi

printf 'cbds status:\n'
cbds status

printf '\nWorker skill status:\n'
cbds skill status || true

cat <<'MSG'

Smoke check complete.
Next: give prompts/MASTER_PROMPT.md to the orchestrator and execute T001.
Do not start a transcript-polling loop if a worker does not report.
MSG
