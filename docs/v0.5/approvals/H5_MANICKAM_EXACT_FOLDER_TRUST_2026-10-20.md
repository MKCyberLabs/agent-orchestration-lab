# H5 owner approval — Manickam existing seat, one exact folder trust

**Date:** 2026-10-20 (Asia/Kolkata)
**Status:** Explicit owner approval received; **not yet executed or verified**.

## Owner's exact authorization

> Yes, I authorize selecting 'Yes, I trust this folder' exactly once for the existing AGY-Manickam/default-profile seat in Herdr pane wD:p2, only for /home/openclaw/worktrees/agent-orch-v05-p0. Then verify readiness and update H5 local Git evidence. No new agent, coding prompt, automatic approvals for other folders, push or scheduling. Stop for review.

## Scope and idempotent execution

- Target: **currently existing** AGY-Manickam/default-profile interactive session **wD:p2**, with the **exact** folder `/home/openclaw/worktrees/agent-orch-v05-p0` on its visible AGY trust dialog.
- Once: in that pane **only if the dialog is still present and matches the exact folder**, select `Yes, I trust this folder` **one time**. This grants that profile read/edit/execute access to that specified worktree. Do not send the response into a different agent/pane/session, a different folder, or a different approval dialog.
- If the dialog is already gone and Manickam is interactive/ready, **do not reopen it, click again or start a replacement agent**; only verify and report. If the displayed folder/permission differs, leave it blocked and ask a new exact question.
- Use the existing Herdr session; no second agent startup, pane creation, profile/account change, credential inspection or repeated full inventory.
- After that one decision, read `herdr agent get wD:p2`, `herdr agent explain wD:p2 --json` and a nonsecret detector/visible screen snapshot. Record matched explicit safe idle vs `default_known_agent_idle_fallback`/blocked state. **No agent prompt** or model coding task.
- Document actual pane/process, trust outcome, profile selector evidence **without secrets**, ready/blocked classification, and that AGY-Rohit historical `wD:p4` is currently **shell-only**. Distinct account identity remains **owner-attested**, not independently confirmed from account credentials. Do not invent verification.
- Update only local `docs/v0.5/evidence/H5_HERDR_ROLE_SEATS.md` and local `STATUS_AND_DECISIONS.md` / roadmap status as actually observed; commit **locally**, and STOP with short result and SHA. Preserve local H5 evidence commit `36e1b9b2dd87095813204487e897b333ac59b43a`.

**Explicitly not authorized:** accepting other trust/permission/survey dialogs, auto-Yes script, another AGY startup, login, manifest hot reload, Herdr restart, coding task, second prompt, push, merge, deployment, cron/systemd or any Nightshift scheduled task. `PUSH_HOLD` persists.

**Reported starting condition:** Codex High active `wD:p1`; Manickam/default-profile AGY trust-blocked `wD:p2`; Rohit `wD:p4` is shell-only; status shell `wD:p5`; zero H5 startups and zero coding prompts.

**Outcome allowed:** `H5_SEAT2_READY` only for a verified live Manickam interactive seat; `H5_PRESENT_NEEDS_INSPECTION` if ambiguous fallback, `H5_WAITING_FOR_HUMAN` if a different approval appears. This Git record alone is not evidence that the permission was accepted.
