# MK Nightshift × Herdr — Agent Operations & Recovery Runbook

**Purpose:** A dedicated instruction file for the existing OpenClaw **development** setup. Prove one Python → Herdr → AGY-Rohit task, handle red human-attention prompts, verify tests and local Git, and **stop without endless troubleshooting**. Not a general Herdr manual.

**Authorization:** Reading this runbook does **not** authorize another detector reload, model prompt, folder trust, new seat, Git push or timer. A previous one-refresh/one-override authorization was exhausted.

## 1. Exact project status — keep checkmarks

| Milestone | Actual state |
|---|---|
| Real Python → Codex CLI → tests → local Git (P1A and W02) | ✅ PASS |
| W02 isolated Chromium + PostgreSQL UAT | ✅ 26 PASS / 0 FAIL / 1 optional build NOT_RUN |
| Herdr operator `wD:p1`, AGY-Rohit `wD:p4`, status shell `wD:p5` | ✅ H1/H2 READY |
| Python → Herdr H3 adapter | ✅ 38 offline tests PASS, local code `ab4917a2c3368e5c80a5d92ac208be731fb1903e` |
| H3 live agent work | ⏸ 0 prompts; fallback idle; no task acceptance/commit |
| One upstream refresh + one override/reload | ⏸ override rejected for **nonnumeric version**, rejected file removed |
| Latest local evidence | `28039ed9848cccf91ab0dbe56fc54e4ec2ed339b`; `docs/v0.5/evidence/H3_HERDR_DETECTOR_RECOVERY.md` |

Local commits are not independently visible in the remote instruction branch while `PUSH_HOLD` remains; these are owner-reported host facts.

## 2. Roles and ownership: one control plane

- **Owner:** approves one task and each new folder/permission grant, decides rollout.
- **Python Nightshift:** the **sole dispatcher and state writer**. Selects task and seat, enforces one prompt/timeout/allowlist, runs host tests, commits locally, writes morning report.
- **Herdr:** visible workspace, pane, process and agent **lifecycle** (not Git/test authority).
- **AGY-Rohit:** the existing **real interactive builder** in `wD:p4`. It is already trusted for `/home/openclaw/worktrees/agent-orch-v05-p0`; a NEW task worktree could request separate trust and must stop.
- **Codex High:** preserved owner/operator `wD:p1`. **Status pane** `wD:p5` is a plain shell, not an agent.
- **Future seats:** AGY-Manickam/reviewer not part of H3.

**Layout rule:** One persistent Herdr workspace; reuse existing panes; **one Git worktree and report per task, not one new window per task**. Python may ensure/create missing approved panes on a *future bootstrap* and store returned IDs. Do **not** build seat provisioning during this H3 recovery.

## 3. Relevant Herdr commands and semantics (use installed --help)

| Need | Command |
|---|---|
| Current seat | `herdr agent list`; `herdr agent get wD:p4` |
| Why idle/blocked? | `herdr agent explain wD:p4 --json` (or `--verbose`) |
| Exact screen detector sees | `herdr agent read wD:p4 --source detection --lines 60` |
| Actual permission dialog | `herdr agent read wD:p4 --source visible --lines 60` |
| Active manifest source/version/warning | `herdr server agent-manifests --json` |
| Test a saved UI snapshot locally | `herdr agent explain --file /ABS/screen.txt --agent ACTUAL_KIND --json` |
| Fetch latest manifest once | `herdr server update-agent-manifests --json` — **already tried; don't repeat** |
| Load a corrected local override | `herdr server reload-agent-manifests` — **only with NEW owner permission** |
| One task, after all gates pass | `herdr agent prompt wD:p4 "ONE_APPROVED_TASK" --wait --until idle --until done --until blocked --timeout 900000` |
| Wait without submitting | `herdr agent wait wD:p4 --until idle --until done --until blocked --timeout 900000` |

Commands prefixed `herdr agent` address a *recognized agent*. `pane` is raw terminal control. **Never use raw keys or automatic Yes/Enter to respond to a trust/permission dialog.**

Caveats: `idle` can be `default_known_agent_idle_fallback` without any matched rule. `agent prompt --wait` can return `agent_prompt_stalled` **after sending input**; timeout is NOT proof of zero delivery. Both waits can hang indefinitely if `--timeout` is omitted. A `done`/`idle` only marks an apparent settled turn; Python tests and local Git decide task PASS. If AGY internally launches background work, idle need not mean all work finished.

## 4. Detection manifests — why the last attempt failed

Herdr recognizes the foreground process and evaluates the **live bottom-screen buffer** using the active agent-kind manifest. A screen with no matching rule can look falsely `idle`. Local overrides at `~/.config/herdr/agent-detection/<actual-agent-kind>.toml` outrank remote/bundled manifests when **valid**. A malformed override is **ignored with a warning**, so fallback remains unchanged. Herdr can hot-reload rules without restarting the agent.

**Manifest header example** (grounded in official Herdr Cursor manifest, **not** a ready-to-use AGY config):

```toml
id = "cursor"
version = "2026.08.03.1"
min_engine_version = 1

[[rules]]
id = "example_rule"
state = "blocked"
priority = 320
region = "bottom_non_empty_lines(8)"
visible_blocker = true
contains = ["write to this file?"]
```

**Do not copy that manifest to AGY.** Read the **actual AGY KIND/id and installed compatible header** first. `version` is a *quoted dotted numeric string*; NOT `"h3-fix"`, `"v1"` or an arbitrary label. `min_engine_version` is an integer. The exact compatible version number, matcher fields, regex syntax, precedence and engine requirement must come from working **installed** manifests and parser. Avoid universal rules like `contains = [""]`, generic blank-screen idle or broad prompt text. A blocked trust rule must beat a safe-idle composer rule; otherwise fail closed.

### Mandatory offline precheck — before any reload

Build a single candidate against the actual active/bundled agent-kind manifest and real saved AGY prompt and blocked snapshots. Confirm TOML syntax AND basic schema with Python `tomllib`:

```bash
python3 - <<'PY'
import pathlib, re, tomllib
p = pathlib.Path("/ABS/PATH/TO/AGY_CANDIDATE.toml")
d = tomllib.loads(p.read_text())
v = d.get("version")
assert isinstance(d.get("id"), str) and d["id"]
assert isinstance(v, str) and re.fullmatch(r"[0-9]+(?:\.[0-9]+)+", v), "numeric dotted quoted version"
assert isinstance(d.get("min_engine_version"), int)
assert isinstance(d.get("rules"), list) and len(d["rules"]) > 0
print("HEADER_PREFLIGHT_PASS", d["id"], v, len(d["rules"]))
PY
```

**This is NOT complete manifest validation.** Also use installed Herdr local explain with a saved **real idle** screen and **real trust/approval** screen if available. Ensure the proposed rule matches the first and cannot misclassify the second as safe idle. If an earlier blocked snapshot does not exist, call that test `NOT_RUN`, keep Python's conservative on-screen approval guard, and do not claim all blockers are recognizable.

The active server's `agent explain` and `server agent-manifests` after a hot reload must show the **actual loaded local override version, explicit matched rule, no warning, and no idle fallback**. Just parsing TOML or seeing `idle` is NOT success.

## 5. H3 corrected happy flow — one precise controlled attempt

The last owner approval was exhausted. **Wait for a NEW explicit owner approval** for **one corrected numeric-version override + one hot reload** before modifying the live Herdr manifest. The owner can optionally authorize continuation of the *still unused* one H3 AGY-Rohit prompt after a trustworthy matched state appears.

1. **REUSE:** Existing `wD:p1`, `wD:p4`, `wD:p5` only. Verify local commit `28039ed9848cccf91ab0dbe56fc54e4ec2ed339b` or clean descendant. Read saved H3 recovery evidence. Do not repeat previous upstream refresh or another model/login check.
2. **PIN THE FAILING LAYER:** Use installed Herdr help, `agent explain`, bottom screen and manifest status; identify actual agent-kind/id and precise rejected `version` error. Do not modify Python adapter for a Herdr schema failure.
3. **OFFLINE FIRST:** Backup original local override if present; construct **one** narrowly scoped candidate with supported numeric version and safe idle/blocked rules. TOML/header checks, saved-screen Herdr explain and existing 38 adapter tests. Fix syntax **offline**, not through live reload cycles. After **two** offline failures on same schema, STOP and request actual installed schema/output rather than invent version numbers.
4. **APPLY ONCE after new owner approval:** Put validated candidate at canonical **actual-kind** override path; perform **one** `herdr server reload-agent-manifests`. No restart, new panes, manifest upstream update or account changes.
5. **VERIFY:** Active rule source/version and specific **matched safe idle**; no `default_known_agent_idle_fallback`, no visible trust prompt. If invalid, undo new override and restore original (a reload may be necessary solely to restore previous state); STOP `DETECTOR_NOT_VERIFIED`. No prompt.
6. **DISPATCH AT MOST ONCE:** If confirmed ready, Python sends original previously approved H3 task to **wD:p4**. Track `prompts_sent` and do not submit a second time after stall/timeout. If new worktree trust screen appears, mark `WAITING_FOR_HUMAN`; ask the owner for **exact pane and directory**, never auto-accept. If task completes, run allowlisted diff audit and host acceptance and local Git commit. Only then mark `VERIFIED_COMMITTED` and report.
7. **STOP:** Outcome, matched rule/fallback, live 0/1 reloads, 0/1 prompts, tests PASS/FAIL/NOT_RUN, code/evidence SHA and one concrete next owner action.

## 6. State mapping: red flag is human attention

| Evidence | Python state | Required action |
|---|---|---|
| Explicit matched safe idle, no visible approval, approved task unsent | `READY_TO_DISPATCH` | One send |
| Active turn observed | `WORKER_RUNNING` | Bounded wait |
| `blocked` OR trust/permission/question on screen even when Herdr says `idle` | `WAITING_FOR_HUMAN` | RED; preserve details, STOP, ask owner |
| `idle/done` after task activity | `TEST_RUNNING` | Host tests + allowed paths, not instant success |
| Tests + audit PASS, local commit obtained | `VERIFIED_COMMITTED` → `REVIEW_REQUIRED` | Keep seat, report |
| `default_known_agent_idle_fallback` or ambiguous `unknown` | `NEEDS_INSPECTION` | STOP before dispatch |
| CLI timeout, `agent_prompt_stalled`, bad JSON, disconnect | `NEEDS_INSPECTION` | Prompt might already be sent; **NO RETRY** |
| Test fail, disallowed file change | `FAILED` or `REVIEW_REQUIRED` | Preserve changes; don't reset |

## 7. Lessons from our ACTUAL failures

| Failure | Root cause | Permanent prevention |
|---|---|---|
| H1 AGY trust dialog showed red | Interactive folder trust required | Approve exact AGY pane + exact directory once; never auto-Yes. |
| H3 says idle via `default_known_agent_idle_fallback` | No explicit screen detection rule matched | Check `explain` matched rule and visible bottom screen before any prompt. |
| H3 override rejected | Manifest `version` was not numeric-dotted | Read working installed manifest; offline TOML+schema+real snapshot validation **before** consuming live reload. |
| Rejected override deleted; fallback unchanged | Invalid local override does not become active | Verify **server active source/version and rule**, not file existence. |
| Attempt allowance exhausted with zero task prompts | Used live attempt to discover avoidable schema constraint | Separate offline candidate preparation from live mutation; one new owner authorization per live correction. |
| Earlier repeated architecture/security loops | Fixed adjacent layers instead of actual blocker | One failing layer, one hypothesis, one minimal change, one proof, one report. |
| W02 initially partial | Code commit was not browser/database acceptance | Complete isolated UAT; keep 26 PASS milestone checked, do not revisit without regression. |

### How to think when stuck — six questions

1. **Where is the failure?** Manifest parse, screen detection, task dispatch, agent, host tests, Git, or owner approval? Name ONE.
2. **What is the exact evidence?** Short CLI error, Herdr `explain` reason, actual file/version; no invented assumptions.
3. **What authoritative schema applies?** Local `--help`, valid installed AGY manifest, Herdr's current running server—not guessed docs from a different version.
4. **Can I reproduce WITHOUT quota/live impact?** TOML+version precheck, saved-screen explain, mocked Python tests.
5. **What specifically proves success?** Active matched rule, safe/blocked distinction, exactly one task prompt, host test and Git SHA. **An idle badge alone does not.**
6. **What stays untouched?** Existing panes/profiles, worktrees/commits, old login, NutriSnap, production/owner data, Git push and cron.

**Bounded troubleshooting:** **one diagnosis → one root-cause hypothesis → up to two offline candidate corrections → one separately authorized live action → one verification → PASS or STOP.** No silent unlimited loops, extra workers, shell-polling or new framework.

## 8. Required SHORT reporting contract

```text
RESULT: H3_PASS | H3_WAITING_FOR_HUMAN | DETECTOR_NOT_VERIFIED | BLOCKED
Layer / exact error:
Herdr: wD:p4 | actual agent-kind | source/version | matched rule OR fallback
Attempts: previous refresh=1; previous rejected override=1; this new approved reload=0/1; AGY prompts=0/1
Offline: TOML/header PASS/FAIL; real idle test PASS/FAIL; blocked test PASS/FAIL/NOT_RUN; adapter tests PASS/FAIL
Live: matched safe idle | approval dialog (exact path/action) | unknown
Host acceptance: PASS/FAIL/NOT_RUN; task code SHA or none
Local evidence commit: <SHA>; worktrees clean/dirty as observed
One next owner action: <exact decision or none>
```

Do not commit emails, API keys, cookies, real environment values, screenshots containing credentials, production database URLs or raw private transcripts. Local execution evidence remains local while `PUSH_HOLD` persists.

## 9. Official references — relevant to this project, not a general manual

- [Herdr Agents: status fallback, precedence and manifests](https://herdr.dev/docs/agents/)
- [Herdr agent automation: pane vs agent, one prompt and stall semantics](https://herdr.dev/docs/agent-automation/)
- [Herdr CLI reference: explain, server reload and flags](https://herdr.dev/docs/cli-reference/)
- [Herdr official Cursor detection manifest: numeric dotted version example](https://github.com/herdrdev/herdr/blob/master/website/agent-detection/cursor.toml)
- [Herdr agent skill: operator workflow](https://herdr.dev/docs/agent-skill/)
