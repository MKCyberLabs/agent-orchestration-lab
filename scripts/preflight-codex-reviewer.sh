#!/usr/bin/env bash
# Offline Codex/Linux sandbox preflight: NO LLM invocation, NO sudo, NO host changes.
set -euo pipefail
echo "Codex reviewer preflight (no tokens)"

if ! command -v codex >/dev/null 2>&1; then
  echo "BLOCKED: codex not found in PATH" >&2
  exit 10
fi
codex --version
if ! command -v bwrap >/dev/null 2>&1; then
  echo "BLOCKED: system bubblewrap missing. Install distro bubblewrap; see docs/CODEX_REVIEWER_RUNBOOK.md" >&2
  exit 11
fi
echo "bwrap: $(command -v bwrap)"
if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  echo "OS: ${PRETTY_NAME:-unknown}"
fi
if command -v sysctl >/dev/null 2>&1; then
  sysctl kernel.unprivileged_userns_clone kernel.apparmor_restrict_unprivileged_userns 2>/dev/null || true
fi
echo "Testing Linux sandbox, no model call: codex sandbox linux /bin/true"
if ! timeout 45s codex sandbox linux /bin/true; then
  echo "BLOCKED: Codex Linux sandbox could not run /bin/true. Inspect AppArmor/userns policy; do not disable security globally." >&2
  exit 12
fi
echo "PASS: system bwrap and Codex sandbox execute a shell command"
