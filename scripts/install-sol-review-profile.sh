#!/usr/bin/env bash
# Codex CLI 0.134+ uses ~/.codex/<profile>.config.toml, not [profiles.<name>] tables.
set -euo pipefail
root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$root/scripts/install-sol-review-profile.py"
