#!/usr/bin/env bash
# Invoke with: bash scripts/install-sol-review-profile.sh
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
profile_src="$root/config/codex/sol-review-profile.toml"
codex_home="${CODEX_HOME:-$HOME/.codex}"
config="$codex_home/config.toml"
mkdir -p "$codex_home"

if [[ -f "$config" ]] && grep -Eq '^[[:space:]]*\[profiles\.sol-review\][[:space:]]*$' "$config"; then
  echo "BLOCKED: [profiles.sol-review] already exists in $config; inspect it manually. No changes made."
  exit 3
fi

tmp="$(mktemp "$codex_home/.config.toml.XXXXXX")"
trap 'rm -f "$tmp"' EXIT
if [[ -f "$config" ]]; then
  cat "$config" > "$tmp"
fi
printf '\n' >> "$tmp"
cat "$profile_src" >> "$tmp"

# Fail closed on malformed TOML or profile override collisions.
python3 - "$tmp" <<'PY'
import sys, tomllib
with open(sys.argv[1], "rb") as stream:
    config = tomllib.load(stream)
p = config.get("profiles", {}).get("sol-review", {})
expected = {
    "model": "gpt-6.1-sol",
    "model_reasoning_effort": "high",
    "sandbox_mode": "read-only",
    "approval_policy": "never",
    "web_search": "disabled",
}
for key, value in expected.items():
    if p.get(key) != value:
        raise SystemExit(f"Invalid sol-review profile key: {key}")
print("TOML verified")
PY

if [[ -f "$config" ]]; then
  backup="$config.backup.$(date +%Y%m%d-%H%M%S)"
  cp -p "$config" "$backup"
  echo "Previous configuration backed up: $backup"
fi
chmod 600 "$tmp"
mv -f "$tmp" "$config"
trap - EXIT
echo "Profile installed safely: $config"
echo "Next: bash scripts/preflight-codex-reviewer.sh"
