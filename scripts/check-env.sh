#!/usr/bin/env bash
set -u

check() {
  local name="$1"
  local cmd="$2"
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '[OK]   %-16s %s\n' "$name" "$(command -v "$cmd")"
  else
    printf '[MISS] %-16s not found\n' "$name"
  fi
}

printf 'Agent Orchestration Lab environment\n'
printf '%s\n' '-----------------------------------'
check git git
check python python
check herdr herdr
check cbds cbds
check codex codex
check agy agy
check jq jq

printf '\nVersions (when available)\n'
printf '%s\n' '-------------------------'
git --version 2>/dev/null || true
python --version 2>/dev/null || true
herdr --version 2>/dev/null || true
cbds --version 2>/dev/null || true
codex --version 2>/dev/null || true
agy --version 2>/dev/null || true
