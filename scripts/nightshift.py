#!/usr/bin/env python3
"""Single-process, zero-orchestrator-token night shift. Explicit approval required.

No Herdr, cbds, agent polling, automatic merge, deploy, or destructive cleanup.
Never run in a worktree containing personal or production data.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, time, timezone
import fcntl
import fnmatch
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
from zoneinfo import ZoneInfo

ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{1,55}$")
TZ = ZoneInfo("Asia/Kolkata")
DENY = (".env", ".env.*", "**/.env", "**/.env.*", ".github/**",
        "**/secrets/**", "**/*credential*", "**/*private_key*",
        "**/deploy*", "**/flash*", "**/esptool*", "**/*.pem", "**/*.key")
TERMINAL = {"VERIFIED_COMMITTED", "FAILED", "QUOTA_PAUSED"}


class Hold(Exception):
    pass


def require(ok, why):
    if not ok:
        raise Hold(why)


def clock():
    return datetime.now(TZ)


def atomic_write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    tmp = path.with_name(path.name + ".tmp." + str(os.getpid()))
    with tmp.open("x", encoding="utf-8") as f:
        os.chmod(tmp, 0o600)
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_commands(cmds):
    require(isinstance(cmds, list), "verification commands must be a list")
    for cmd in cmds:
        require(isinstance(cmd, list) and 1 <= len(cmd) <= 12 and
                all(isinstance(a, str) and a and "\x00" not in a for a in cmd),
                "verification must use argv arrays, not shell")
        require(Path(cmd[0]).name in ("python", "python3", "pytest", "npm", "npx", "node", "arduino-cli"),
                "unsupported verification executable: " + cmd[0])


def load_config(path):
    c = read_json(path)
    require(c.get("schema_version") == 2, "expected V0.4 sequential schema_version=2")
    require(isinstance(c.get("project_id"), str) and ID.fullmatch(c["project_id"]), "invalid project ID")
    require(c.get("timezone") == "Asia/Kolkata", "timezone must be Asia/Kolkata")
    require(type(c.get("approved")) is bool, "approved must be a boolean")
    for field in ("worktree", "backlog_file", "state_dir"):
        require(isinstance(c.get(field), str) and Path(c[field]).is_absolute(), field + " must be absolute")
    require(c.get("worker") in ("codex", "agy"), "worker must be codex or agy")
    require(re.fullmatch(r"nightshift/[A-Za-z0-9/_-]+", c.get("branch", "")), "require explicit nightshift/ branch")
    require(type(c.get("max_minutes")) is int and 5 <= c["max_minutes"] <= 120, "invalid campaign minutes")
    require(type(c.get("task_minutes")) is int and 1 <= c["task_minutes"] <= 60, "invalid task minutes")
    require(type(c.get("max_tasks")) is int and 1 <= c["max_tasks"] <= 8, "invalid task count")
    for field in ("start", "stop"):
        require(isinstance(c.get(field), str) and re.fullmatch(r"(?:[01]\d|2[0-3]):[0-5]\d", c[field]), "invalid " + field)
    require(time.fromisoformat(c["start"]) < time.fromisoformat(c["stop"]),
            "pilot requires a same-day clock window")
    validate_commands(c.get("verify_commands"))
    require(c["verify_commands"], "at least one host verification command is required")
    return c


def load_backlog(path, project):
    obj = read_json(path)
    require(obj.get("schema_version") == 1 and obj.get("project_id") == project, "backlog project/schema mismatch")
    tasks = obj.get("tasks")
    require(isinstance(tasks, list) and len(tasks) <= 30, "invalid backlog size")
    seen = set()
    for task in tasks:
        tid = task.get("task_id")
        require(isinstance(tid, str) and ID.fullmatch(tid) and tid not in seen, "duplicate or invalid task ID")
        seen.add(tid)
        require(type(task.get("approved")) is bool, "task needs explicit approval")
        require(isinstance(task.get("objective"), str) and 20 <= len(task["objective"]) <= 3000, "task objective missing/broad")
        require(isinstance(task.get("context_files"), list) and len(task["context_files"]) <= 12, "invalid context")
        require(isinstance(task.get("allowed_paths"), list) and 1 <= len(task["allowed_paths"]) <= 12, "invalid allowed paths")
        for name in task["context_files"] + task["allowed_paths"]:
            require(isinstance(name, str) and name and not name.startswith("/") and
                    ".." not in Path(name).parts and "\\" not in name and
                    not name.startswith(".git") and name not in ("*", "**", "**/*"),
                    "unsafe or broad relative path")
        require(isinstance(task.get("depends_on", []), list), "invalid task dependencies")
        require(type(task.get("max_diff_lines", 250)) is int and
                1 <= task.get("max_diff_lines", 250) <= 500, "invalid diff budget")
        validate_commands(task.get("acceptance_commands"))
        require(task["acceptance_commands"], "task needs host acceptance command")
    for task in tasks:
        require(all(d in seen and d != task["task_id"] for d in task.get("depends_on", [])),
                "invalid dependency reference")
    return tasks


def window(c, when):
    local = when.astimezone(TZ)
    start, stop = time.fromisoformat(c["start"]), time.fromisoformat(c["stop"])
    if start <= local.time().replace(tzinfo=None) < stop:
        return local.date().isoformat()
    return None


def seconds_left(c, started, now):
    local = now.astimezone(TZ)
    end_clock = datetime.combine(local.date(), time.fromisoformat(c["stop"]), TZ)
    return min((end_clock - local).total_seconds(),
               c["max_minutes"] * 60 - (now - started).total_seconds())


def git(repo, *args, timeout=25):
    p = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, timeout=timeout)
    require(p.returncode == 0, "git " + " ".join(args[:3]) + " failed")
    return p.stdout.decode("utf-8", errors="replace").strip()


def preflight(c):
    repo = Path(c["worktree"]).resolve(strict=True)
    require((repo / ".git").is_file(), "require a dedicated linked Git worktree")
    require(git(repo, "rev-parse", "--show-toplevel") == str(repo), "repository path mismatch")
    require(git(repo, "branch", "--show-current") == c["branch"], "wrong/nightshift branch")
    require(not git(repo, "status", "--porcelain=v1", "--untracked-files=all"), "worktree is dirty")
    require(not (Path(c["state_dir"]).resolve() == repo or repo in Path(c["state_dir"]).resolve().parents),
            "state must live outside repository")
    require(shutil.which(c["worker"]) is not None and shutil.which("git") is not None,
            "coding CLI or git unavailable")
    return repo


@contextmanager
def lock(c):
    parent = Path(c["state_dir"])
    parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(parent, 0o700)
    root = parent / c["project_id"]
    root.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(root, 0o700)
    # Global capacity lock prevents two projects consuming the same model quota.
    with (parent / "global.lock").open("a+") as global_file, \
         (root / "runner.lock").open("a+") as project_file:
        for f in (global_file, project_file):
            os.chmod(f.name, 0o600)
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Hold("another night-shift process already owns model/project capacity")
        yield root


def persist(root, state):
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write(root / "state.json", state)


def paths_changed(repo):
    raw = subprocess.run(["git", "-C", str(repo), "status", "--porcelain=v1",
                          "-z", "--untracked-files=all"], capture_output=True, check=True).stdout
    names = raw.decode("utf-8", "surrogateescape").split("\0")
    names = [n for n in names if n]
    result = []
    i = 0
    while i < len(names):
        item = names[i]
        require(len(item) >= 4, "unexpected git status entry")
        code, name = item[:2], item[3:]
        result.append((code, name))
        if "R" in code or "C" in code:
            i += 1
            require(i < len(names), "malformed rename entry")
            result.append((code, names[i]))
        i += 1
    return result


def audit(repo, task, base):
    require(git(repo, "rev-parse", "HEAD") == base, "worker modified Git history")
    changed = paths_changed(repo)
    require(changed, "agent produced no file changes")
    allowed = task["allowed_paths"]
    for code, name in changed:
        pure = Path(name)
        require(not pure.is_absolute() and ".." not in pure.parts and
                not (repo / pure).is_symlink(), "unsafe or symlink path")
        require(not any(fnmatch.fnmatchcase(name, pat) for pat in DENY), "forbidden path " + name)
        require(any(fnmatch.fnmatchcase(name, pat) for pat in allowed), "out-of-scope path " + name)
        require("D" not in code and "R" not in code and "C" not in code,
                "file deletion/rename is not auto-approved")
    patch = subprocess.run(["git", "-C", str(repo), "diff", "HEAD", "--unified=0", "--"],
                           capture_output=True, check=True).stdout.decode("utf-8", "replace")
    # Reject weakening existing regression assertions without manual review.
    require(not any(line.startswith("-") and not line.startswith("---") and
                    re.search(r"\b(assert|expect\s*\(|it\s*\(|test\s*\()", line)
                    for line in patch.splitlines()), "potential test weakening requires review")
    count = sum(1 for line in patch.splitlines() if line[:1] in ("+", "-") and
                not line.startswith(("+++", "---")))
    for code, name in changed:
        if code == "??":
            p = repo / name
            require(p.is_file() and p.stat().st_size < 300000, "untracked file too large/nonregular")
            count += len(p.read_bytes().splitlines())
    require(count <= task.get("max_diff_lines", 250), "diff exceeds task budget")
    return sorted({name for _, name in changed})


def process(argv, repo, logbase, timeout, stdin=None):
    logbase.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (logbase.with_suffix(".stdout")).open("wb") as out, \
            (logbase.with_suffix(".stderr")).open("wb") as err:
        os.chmod(out.name, 0o600)
        os.chmod(err.name, 0o600)
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"  # host tests must not dirty fixture with pyc files
        p = subprocess.Popen(argv, cwd=repo, stdin=subprocess.PIPE if stdin is not None else subprocess.DEVNULL,
                             stdout=out, stderr=err, start_new_session=True, env=env)
        timed_out = False
        try:
            p.communicate(stdin.encode("utf-8") if stdin is not None else None, timeout=max(1, int(timeout)))
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(p.pid, signal.SIGTERM)
            try:
                p.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
                p.communicate()
    return p.returncode, timed_out


def worker(c, repo, task, root, timeout):
    context = "\n".join(task["context_files"])
    prompt = ("Work ONLY inside this isolated worktree. Read AGENTS.md and listed context files first. "
              "Do not commit, push, merge, deploy, flash hardware, edit credentials, or run git reset/clean. "
              "Do not weaken tests. If ambiguous, report BLOCKED and do not edit. "
              "Modify only the allowed paths. Host verification is authoritative.\n"
              "TASK: " + task["task_id"] + "\nOBJECTIVE: " + task["objective"] +
              "\nCONTEXT FILES:\n" + context + "\nALLOWED PATHS:\n" +
              "\n".join(task["allowed_paths"]) + "\n")
    logfile = root / "logs" / (task["task_id"] + "-" + str(int(datetime.now().timestamp())))
    if c["worker"] == "codex":
        argv = ["codex", "exec", "--sandbox", "workspace-write", "--ephemeral", "--json", "-"]
        rc, timed = process(argv, repo, logfile, timeout, stdin=prompt)
        result = False
        tokens = None
        with logfile.with_suffix(".stdout").open(encoding="utf-8", errors="replace") as f:
            for line in f:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "turn.completed":
                    result = True
                    usage = event.get("usage", {})
                    tokens = usage.get("total_tokens") if isinstance(usage, dict) else None
                if event.get("type") in ("turn.failed", "error"):
                    result = False
        return rc == 0 and not timed and result, tokens, logfile, timed
    argv = ["agy", "-p", prompt, "--output-format", "json",
            "--print-timeout", str(max(1, int(timeout / 60))) + "m"]
    rc, timed = process(argv, repo, logfile, timeout)
    try:
        obj = json.loads(logfile.with_suffix(".stdout").read_text(encoding="utf-8"))
        usage = obj.get("usage", {})
        return rc == 0 and not timed and obj.get("status") == "SUCCESS", \
               usage.get("total_tokens"), logfile, timed
    except (OSError, ValueError, AttributeError):
        return False, None, logfile, timed


def verify(c, repo, task, root, seconds):
    commands = task["acceptance_commands"] + c["verify_commands"]
    for index, cmd in enumerate(commands):
        rc, timed = process(cmd, repo, root / "logs" / (task["task_id"] + "-test-" + str(index)),
                            min(180, seconds))
        require(rc == 0 and not timed, "host verification failed: " + " ".join(cmd))
    return len(commands)


def report(root, c, state, tasks):
    lines = ["# Night Shift — " + c["project_id"], "",
             "Campaign: " + str(state.get("window_id", "none")), "",
             "Branch: " + c["branch"], "",
             "Status: " + state.get("phase", "NOT_STARTED"), "",
             "| Task | Result | Commit |", "|---|---|---|"]
    results = state.get("tasks", {})
    for task in tasks:
        r = results.get(task["task_id"], {})
        lines.append("| " + task["task_id"] + " | " + r.get("phase", "QUEUED") +
                     " | " + r.get("sha", "-") + " |")
    lines += ["", "## Next approved tasks", ""]
    for task in tasks:
        if task["approved"] and task["task_id"] not in results:
            lines.append("- " + task["task_id"] + ": " + task["objective"][:180].replace("\n", " "))
    if state.get("blocker"):
        lines += ["", "## Blocker", "", state["blocker"]]
    output = root / "reports" / (str(state.get("window_id", "undated")) + "-morning.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(output, 0o600)
    return output


def campaign(c, root, tasks, now=None):
    now = now or clock()
    win = window(c, now)
    require(c["approved"] and win is not None, "not approved or outside scheduled window")
    repo = preflight(c)
    state_file = root / "state.json"
    state = read_json(state_file) if state_file.exists() else {"tasks": {}, "phase": "READY"}
    require(state.get("phase") not in ("WORKER_RUNNING", "TEST_RUNNING", "BLOCKED"),
            "interrupted or blocked prior task needs manual reconciliation")
    if state.get("window_id") != win:
        state["window_id"] = win
        state["window_completed"] = 0
    started = now
    state["phase"] = "RUNNING"
    persist(root, state)
    try:
        for task in tasks:
            if state["window_completed"] >= c["max_tasks"] or seconds_left(c, started, clock()) < 60:
                break
            tid = task["task_id"]
            if not task["approved"] or tid in state["tasks"]:
                continue
            if not all(state["tasks"].get(dep, {}).get("phase") == "VERIFIED_COMMITTED"
                       for dep in task.get("depends_on", [])):
                continue
            base = git(repo, "rev-parse", "HEAD")
            state["phase"] = "WORKER_RUNNING"
            state["tasks"][tid] = {"phase": "WORKER_RUNNING", "base_sha": base}
            persist(root, state)
            budget = min(c["task_minutes"] * 60, int(seconds_left(c, started, clock())) - 30)
            ok, tokens, log, timed = worker(c, repo, task, root, budget)
            state["tasks"][tid]["tokens"] = tokens
            state["tasks"][tid]["log"] = str(log)
            require(ok, "worker failed/timeout; retained isolated changes for manual inspection: " + tid)
            state["phase"] = "TEST_RUNNING"
            state["tasks"][tid]["phase"] = "TEST_RUNNING"
            persist(root, state)
            files = audit(repo, task, base)
            verify(c, repo, task, root, int(seconds_left(c, started, clock())))
            require(audit(repo, task, base) == files, "verification changed the audited file set")
            require(git(repo, "rev-parse", "HEAD") == base, "verification unexpectedly committed")
            git(repo, "add", "--", *files)
            git(repo, "commit", "-m", "nightshift(" + tid + "): verified implementation")
            sha = git(repo, "rev-parse", "HEAD")
            require(not git(repo, "status", "--porcelain=v1", "--untracked-files=all"),
                    "post-commit worktree dirty")
            state["tasks"][tid].update({"phase": "VERIFIED_COMMITTED", "sha": sha, "files": files})
            state["window_completed"] += 1
            state["phase"] = "RUNNING"
            persist(root, state)
        state["phase"] = "REVIEW_REQUIRED"
    except Hold as exc:
        state["phase"] = "BLOCKED"
        state["blocker"] = str(exc)
        persist(root, state)
    persist(root, state)
    return state


def cli(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=("doctor", "run", "status", "report"))
    p.add_argument("--config", type=Path, required=True)
    a = p.parse_args(argv)
    try:
        c = load_config(a.config)
        with lock(c) as root:
            tasks = load_backlog(c["backlog_file"], c["project_id"])
            if a.action == "doctor":
                repo = preflight(c)
                value = {"status": "PASS", "repo": str(repo), "approved": c["approved"],
                         "eligible_now": window(c, clock()) is not None, "queued": len(tasks)}
            elif a.action == "run":
                value = campaign(c, root, tasks)
            else:
                value = read_json(root / "state.json") if (root / "state.json").exists() else {"phase": "NOT_STARTED", "tasks": {}}
            if a.action in ("run", "report"):
                value["morning_report"] = str(report(root, c, value, tasks))
        print(json.dumps(value, indent=2, sort_keys=True))
        return 2 if value.get("phase") == "BLOCKED" else 0
    except (Hold, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print("HOLD: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(cli())
