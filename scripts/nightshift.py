#!/usr/bin/env python3
"""Fail-closed, single-task cbds night-shift pilot. No deployments or merges."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, time, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

ID = re.compile(r"^[a-z][a-z0-9_-]{1,47}$")
CBDS_ID = re.compile(r"^(run|tsk|dsp)_[A-Za-z0-9_-]+$")
STATES = {"RUN_CREATING", "RUN_CREATED", "TASK_CREATING", "TASK_CREATED", "DISPATCHING", "WAITING", "REVIEW_REQUIRED", "BLOCKED", "NEEDS_RECONCILIATION"}
AMBIGUOUS = {"RUN_CREATING", "TASK_CREATING", "DISPATCHING"}


class Hold(Exception):
    pass


def require(condition: bool, message: str):
    if not condition:
        raise Hold(message)


def load_config(path: Path) -> dict:
    c = json.loads(path.read_text(encoding="utf-8"))
    require(c.get("schema_version") == 1, "unsupported config schema")
    require(isinstance(c.get("project_id"), str) and ID.fullmatch(c["project_id"]), "invalid project_id")
    for k in ("worktree", "task_file", "state_dir", "quota_file"):
        require(isinstance(c.get(k), str) and Path(c[k]).is_absolute(), f"{k} must be an absolute path")
    require(isinstance(c.get("approved"), bool), "approved must be explicit boolean")
    require(c.get("timezone") == "Asia/Kolkata", "pilot requires Asia/Kolkata")
    require(isinstance(c.get("agent"), str) and ID.fullmatch(c["agent"]), "invalid Herdr agent kind")
    require(type(c.get("min_quota_percent")) in (int, float) and 0 <= c["min_quota_percent"] <= 100, "invalid minimum quota")
    require(type(c.get("quota_max_age_minutes")) is int and 1 <= c["quota_max_age_minutes"] <= 1440, "invalid quota max age")
    for k in ("start", "stop"):
        require(re.fullmatch(r"(?:[01][0-9]|2[0-3]):[0-5][0-9]", c.get(k, "")), f"invalid {k} clock")
    require(c["start"] != c["stop"], "empty schedule window")
    return c


def now_local():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


def active_window(c: dict, instant: datetime):
    local = instant.astimezone(ZoneInfo(c["timezone"]))
    s = time.fromisoformat(c["start"])
    e = time.fromisoformat(c["stop"])
    # Cross-midnight windows are tied to the preceding calendar date.
    if s < e:
        if not s <= local.timetz().replace(tzinfo=None) < e:
            return None
        return local.date().isoformat()
    clock = local.timetz().replace(tzinfo=None)
    if clock >= s:
        return local.date().isoformat()
    if clock < e:
        return (local.date() - timedelta(days=1)).isoformat()
    return None


def ensure_preflight(c: dict, *, check_quota=True):
    repo = Path(c["worktree"])
    require(repo.is_dir() and Path(c["task_file"]).is_file(), "worktree or approved task file missing")
    require(shutil.which("cbds") is not None and shutil.which("git") is not None, "cbds/git missing")
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, timeout=15)
    require(result.returncode == 0 and not result.stdout.strip(), "worktree not clean")
    branch = subprocess.run(["git", "-C", str(repo), "branch", "--show-current"], capture_output=True, text=True, timeout=15)
    require(branch.returncode == 0 and branch.stdout.strip() not in ("", "main", "master"), "not an isolated feature branch")
    # Do not allow an unattended worker to receive unrestricted or very large instructions.
    require(Path(c["task_file"]).stat().st_size <= 12000, "task file exceeds 12 KB")
    if check_quota:
        quota_check(c)


def quota_check(c: dict, *, instant=None):
    path = Path(c["quota_file"])
    require(path.is_file(), "quota snapshot missing: fail closed")
    data = json.loads(path.read_text(encoding="utf-8"))
    stamp = datetime.fromisoformat(data["checked_at"])
    require(stamp.tzinfo is not None, "quota timestamp missing timezone")
    now = instant or datetime.now(timezone.utc)
    age = (now - stamp).total_seconds() / 60
    require(0 <= age <= c["quota_max_age_minutes"], "quota snapshot stale or in future")
    agent = data.get("agents", {}).get(c["agent"], {})
    require(agent.get("authenticated") is True, "agent not authenticated")
    value = agent.get("remaining_percent")
    require(type(value) in (int, float) and 0 <= value <= 100, "agent quota is unknown")
    require(value >= c["min_quota_percent"], "insufficient agent quota")
    return value


def atomic_write(path: Path, value: dict):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp." + str(os.getpid()))
    with tmp.open("x", encoding="utf-8") as file:
        os.chmod(tmp, 0o600)
        json.dump(value, file, indent=2, sort_keys=True)
        file.write("\n")
        file.flush()
        os.fsync(file.fileno())
    os.replace(tmp, path)
    fd = os.open(str(path.parent), os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


@contextmanager
def locked_state(c: dict):
    directory = Path(c["state_dir"]) / c["project_id"]
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(directory, 0o700)
    lockpath = directory / "controller.lock"
    with lockpath.open("a+") as lock:
        os.chmod(lockpath, 0o600)
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Hold("another controller holds project lock")
        yield directory / "state.json"


def cbds(c: dict, *args, timeout=90):
    # Scope all calls to the durable cbds run. Never silently select a different open run.
    p = subprocess.run(["cbds", *args, "--json"], cwd=c["worktree"], capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise Hold(f"cbds {args[0]} returned exit {p.returncode}; inspect host logs, do not redispatch")
    try:
        obj = json.loads(p.stdout)
    except json.JSONDecodeError as err:
        raise Hold(f"cbds {args[0]} did not return valid JSON: {err}") from err
    require(isinstance(obj, dict) and isinstance(obj.get("data"), dict), "unexpected cbds envelope")
    return obj["data"]


def id_from(data: dict, kind: str):
    field = {"run": "run_id", "tsk": "task_id", "dsp": "dispatch_id"}[kind]
    value = data.get(field)
    require(isinstance(value, str) and CBDS_ID.fullmatch(value) and value.startswith(kind + "_"), f"missing validated {field}")
    return value


def mark(path: Path, state: dict, phase: str, **extra):
    require(phase in STATES, f"invalid state: {phase}")
    state.update(extra)
    state["phase"] = phase
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write(path, state)


def main_run(c: dict, path: Path, instant: datetime):
    existing = json.loads(path.read_text()) if path.exists() else None
    if existing:
        phase = existing.get("phase")
        if phase in AMBIGUOUS:
            mark(path, existing, "NEEDS_RECONCILIATION", reason="interrupted during non-idempotent cbds operation")
            return existing
        if phase == "WAITING":
            # A worker can finish during a coordinator restart. Only an authoritative cbds report may settle.
            try:
                reports = cbds(c, "report", "list", "--run", existing["run_id"], "--task", existing["task_id"])
                accepted = reports.get("reports")
                require(isinstance(accepted, list), "cbds report list schema unknown")
                matching = [r for r in accepted if isinstance(r, dict) and r.get("task_id") == existing["task_id"] and r.get("accepted") is True and r.get("outcome") in ("succeeded", "failed", "blocked")]
                if len(matching) == 1:
                    mark(path, existing, "REVIEW_REQUIRED" if matching[0]["outcome"] == "succeeded" else "BLOCKED", report_id=matching[0].get("report_id"), outcome=matching[0]["outcome"])
                elif len(matching) > 1:
                    mark(path, existing, "NEEDS_RECONCILIATION", reason="multiple accepted reports")
                # Without a proven report, preserve WAITING. Do not relaunch.
            except (Hold, KeyError) as exc:
                mark(path, existing, "NEEDS_RECONCILIATION", reason=str(exc))
            return existing
        return existing  # One task per approval/window, never implicitly reset.

    require(active_window(c, instant) is not None, "outside approved night window")
    require(c["approved"] is True, "dispatch not approved in config")
    ensure_preflight(c)
    state = {"schema_version": 1, "project_id": c["project_id"], "window_id": active_window(c, instant), "agent": c["agent"]}
    mark(path, state, "RUN_CREATING")  # write-ahead ambiguity checkpoint
    try:
        run_id = id_from(cbds(c, "run", "create", "--objective", f"Nightshift {c['project_id']} {state['window_id']}"), "run")
    except (Hold, subprocess.TimeoutExpired) as exc:
        mark(path, state, "NEEDS_RECONCILIATION", reason=f"uncertain run creation: {exc}")
        return state
    mark(path, state, "RUN_CREATED", run_id=run_id)
    mark(path, state, "TASK_CREATING")
    try:
        spec = Path(c["task_file"]).read_text(encoding="utf-8")
        task_id = id_from(cbds(c, "task", "create", "--run", run_id, "--spec", spec, "--max-attempts", "1"), "tsk")
    except (Hold, subprocess.TimeoutExpired) as exc:
        mark(path, state, "NEEDS_RECONCILIATION", reason=f"uncertain task creation: {exc}")
        return state
    mark(path, state, "TASK_CREATED", task_id=task_id)
    mark(path, state, "DISPATCHING")
    try:
        dispatch_id = id_from(cbds(c, "dispatch", "start", "--run", run_id, "--task", task_id, "--agent", c["agent"], "--cwd", c["worktree"], timeout=120), "dsp")
    except (Hold, subprocess.TimeoutExpired) as exc:
        mark(path, state, "NEEDS_RECONCILIATION", reason=f"uncertain dispatch: {exc}")
        return state
    mark(path, state, "WAITING", dispatch_id=dispatch_id)
    return state


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("doctor", "run", "status"))
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        c = load_config(args.config)
        with locked_state(c) as path:
            if args.action == "status":
                output = json.loads(path.read_text()) if path.exists() else {"phase": "NOT_STARTED"}
            elif args.action == "doctor":
                ensure_preflight(c)
                output = {"status": "PASS", "approved": c["approved"], "project_id": c["project_id"], "within_window": active_window(c, now_local()) is not None}
            else:
                output = main_run(c, path, now_local())
        print(json.dumps(output, indent=2, sort_keys=True))
        return 2 if output.get("phase") in ("NEEDS_RECONCILIATION", "BLOCKED") else 0
    except (Hold, ValueError, KeyError, OSError, subprocess.SubprocessError, json.JSONDecodeError) as exc:
        print(f"HOLD: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(cli())
