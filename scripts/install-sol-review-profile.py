#!/usr/bin/env python3
"""Install/migrate a Codex 0.134+ named profile safely.

Never overwrite unrelated user settings; preserve a backup if config.toml changes.
Requires Python 3.11+ for tomllib.
"""
import datetime as dt
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "config" / "codex" / "sol-review.config.toml"
CODEX_HOME = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
CONFIG = CODEX_HOME / "config.toml"
PROFILE = CODEX_HOME / "sol-review.config.toml"
LEGACY_HEADING = re.compile(r'^\s*\[profiles\.sol-review\]\s*(?:#.*)?$')
NESTED_LEGACY = re.compile(r'^\s*\[+profiles\.sol-review(?:\.|\])')
ANY_HEADING = re.compile(r'^\s*\[')
ROOT_SELECTOR = re.compile(r'''^\s*profile\s*=\s*(?:"sol-review"|'sol-review')\s*(?:#.*)?$''')

def load_toml(s: str, origin: Path) -> dict:
    try:
        return tomllib.loads(s)
    except tomllib.TOMLDecodeError as exc:
        raise RuntimeError(f"Cannot parse {origin}: {exc}") from exc

def atomic_write(path: Path, data: str, mode: int = 0o600) -> None:
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(data)
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def migrate_config(text: str) -> str:
    # Only remove the exact legacy table and exact legacy top-level selector.
    # Never touch other user tables, hook definitions or agent profiles.
    out: list[str] = []
    skipping = False
    inside_root = True
    for line in text.splitlines(keepends=True):
        if NESTED_LEGACY.match(line) and not LEGACY_HEADING.match(line):
            raise RuntimeError("Nested legacy profile table found; manual migration required")
        if LEGACY_HEADING.match(line):
            skipping = True
            inside_root = False
            continue
        if ANY_HEADING.match(line):
            skipping = False
            inside_root = False
        if skipping:
            continue
        if inside_root and ROOT_SELECTOR.match(line):
            continue
        out.append(line)
    return "".join(out)

def run() -> None:
    desired_text = SOURCE.read_text(encoding="utf-8")
    desired = load_toml(desired_text, SOURCE)
    CODEX_HOME.mkdir(mode=0o700, parents=True, exist_ok=True)

    existing = PROFILE.read_text(encoding="utf-8") if PROFILE.exists() else None
    if existing is not None and load_toml(existing, PROFILE) != desired:
        raise RuntimeError(
            f"BLOCKED: {PROFILE} already exists with different values. "
            "Review it manually; installer will not overwrite."
        )

    raw = CONFIG.read_text(encoding="utf-8") if CONFIG.exists() else ""
    parsed = load_toml(raw, CONFIG)
    legacy = parsed.get("profiles", {}).get("sol-review", None)
    if legacy is not None and legacy != desired:
        raise RuntimeError(
            "BLOCKED: legacy [profiles.sol-review] has custom values. "
            "Review settings and migrate manually; nothing changed."
        )
    if "profile" in parsed and parsed["profile"] != "sol-review":
        raise RuntimeError(
            "BLOCKED: another legacy top-level profile selector exists; "
            "migrate it manually before using --profile."
        )

    migrated = migrate_config(raw)
    parsed_after = load_toml(migrated, CONFIG)
    if parsed_after.get("profiles", {}).get("sol-review") is not None:
        raise RuntimeError("Legacy profile table remained after migration")
    if "profile" in parsed_after:
        raise RuntimeError("Legacy profile selector remained after migration")

    if existing is None:
        atomic_write(PROFILE, desired_text)
        print(f"Installed current-format profile: {PROFILE}")
    else:
        print(f"Profile already correct: {PROFILE}")

    if migrated != raw:
        stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = CONFIG.with_name(f"config.toml.backup.v02.{stamp}")
        shutil.copy2(CONFIG, backup)
        atomic_write(CONFIG, migrated, CONFIG.stat().st_mode & 0o777)
        print(f"Removed legacy selector/table; original backed up: {backup}")
    else:
        print("Base user config unchanged (no legacy selector/table)")

    print("PASS: Codex modern profile is installed; no model call made")

if __name__ == "__main__":
    try:
        run()
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        sys.exit(3)
