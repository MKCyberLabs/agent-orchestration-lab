# V0.5 H3 — AGY-Rohit detection fallback disposition

**Date:** 2026-10-19 (Asia/Kolkata)
**Disposition:** **ADAPTER PASS / LIVE H3 BLOCKED SAFELY**. Do not mark H3 done.

## Actual evidence reported from OpenClaw

- H3 Python→Herdr adapter implemented, **38 offline tests PASS**; local adapter code commit `ab4917a2c3368e5c80a5d92ac208be731fb1903e`.
- Local evidence commit `9ead870c1d18d901d0686df30c6fd1ee35bfc1c6`; report `docs/v0.5/evidence/H3_HERDR_PYTHON_HANDOFF.md`.
- Existing AGY-Rohit seat `wD:p4` is preserved. Herdr `agent explain` reported `idle` **via `default_known_agent_idle_fallback`**, no matched rule.
- **Zero** live task prompts sent, so H3 real work, tests and task Git SHA remain **NOT_RUN**.
- Local commits are OpenClaw-local under `PUSH_HOLD`; this Git review assesses user-provided receipts rather than inspecting local result bytes.

## Technical assessment

Herdr's official agent-detection docs explain this exact fallback: a recognized process with no matching screen rule can be labeled `idle` even when an unfamiliar approval screen is visible. The H3 adapter correctly fails closed. Do **not** add a Python shortcut that treats all fallback-idle states as safe to prompt.

The supported resolution path is **one bounded detection reconciliation**, not new sessions/accounts or a rewritten runner:

1. Inspect non-secret `herdr agent explain wD:p4 --json`, live bottom-buffer screen, manifest source/priority/shadow, and available agent detection flags. Confirm the pane is really at the prompt, not a red approval UI.
2. Use the documented `herdr server agent-manifests --json` and, **only with owner approval**, do one `herdr server update-agent-manifests --json` to refresh supported upstream rules **in the running server** (no restart). Re-check live matched rule and blocked screen behavior.
3. If still fallback, optionally repair **one** minimal **actual agent-kind** local detection manifest override. Validate it offline using the current prompt snapshot and an earlier **real** approval/trust snapshot (if available); carefully test blocked outranks idle. Backup original override, load with documented `herdr server reload-agent-manifests` once, recheck live. No global config or generic “force idle” bypass.
4. If correct idle/blocked distinctions cannot be proven, leave H3 `NEEDS_INSPECTION` and stop with one concrete remaining fact. Never auto-click a trust prompt, submit a coding prompt or alter a different agent/session because of a fallback.

**Sources:** https://herdr.dev/docs/agents/ ; https://herdr.dev/docs/cli-reference/ ; https://herdr.dev/docs/agent-automation/ .

## Owner permission and planned continuation

**Do not execute manifest refresh/override from merely reading this review.** Ask owner to explicitly approve the narrow detection reconciliation. Owner can choose to include **continuation of the already-approved but never-dispatched H3 task** if (and only if) safe matched idle is observed after the fix. One task prompt total, no retry.

**No changes to:** AGY-Rohit/Codex identity, worktree trust dialogs, NutriSnap code, another coding agent, push/merge/deploy, unattended scheduler, production data. Record actual diff and test status locally and stop.
