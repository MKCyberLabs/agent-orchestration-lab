#!/usr/bin/env bash
set -euo pipefail

DEST="${CBDS_SRC:-$HOME/.local/src/cbds}"

for cmd in git node npm; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required command: $cmd" >&2
    exit 2
  fi
done

NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "Node.js 18.17+ is required by cbds; found $(node --version)." >&2
  exit 2
fi

mkdir -p "$(dirname "$DEST")"
if [ -d "$DEST/.git" ]; then
  echo "Updating cbds in $DEST"
  git -C "$DEST" pull --ff-only
else
  echo "Cloning cbds into $DEST"
  git clone https://github.com/zqkra/cbds "$DEST"
fi

echo 'Installing cbds CLI...'
npm install -g "$DEST"

echo 'Installing cbds worker skill...'
cbds skill install

if command -v herdr >/dev/null 2>&1; then
  echo 'Linking cbds as a Herdr plugin...'
  herdr plugin link "$DEST" || {
    echo 'Herdr plugin link did not complete; CLI/skill installation is still available.' >&2
  }
else
  echo 'Herdr not found; skipping plugin link.' >&2
fi

echo
echo 'Verification:'
cbds --help >/dev/null
cbds skill status || true
echo 'cbds setup complete.'
