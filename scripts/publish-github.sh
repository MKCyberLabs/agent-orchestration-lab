#!/usr/bin/env bash
set -euo pipefail

REPO="${1:-MKCyberLabs/agent-orchestration-lab}"

if ! command -v gh >/dev/null 2>&1; then
  echo 'GitHub CLI (gh) is required.' >&2
  exit 2
fi

gh auth status >/dev/null

if git remote get-url origin >/dev/null 2>&1; then
  echo "origin already exists: $(git remote get-url origin)"
  echo 'Refusing to create another remote automatically.' >&2
  exit 3
fi

echo "Creating private repository: $REPO"
gh repo create "$REPO" --private --source=. --remote=origin --push

echo
echo 'Published. Clone elsewhere with:'
echo "  gh repo clone $REPO"
