# P0.2 ADR output contract — quick checker

P0.2 is **one bounded documentation step**. Treat `prompts/V0.5_P02_ADR_MASTER_PROMPT.md` as the operational instruction and this file as the review checklist.

## Evidence to save in Git

1. `ADR_0001_SINGLE_CONTROL_PLANE.md`: stated alternatives and one recommended authority model, including why not to run two dispatchers simultaneously.
2. `evidence/P0.2_ADR_REVIEW_2026-10-19.md`: source refs, tested/NOT_RUN, risk table, any FAILED/BLOCKED outcomes, suggested owner decision.
3. `STATUS_AND_DECISIONS.md`: exact phase result and one next proposed step; never mark the owner's decision APPROVED without their instruction.
4. Git commit SHA (and remote branch URL only if push was safe); report if `PUSH_HOLD`.

## Required negative checks

- Zero changes under `scripts/`, `config/`, `systemd/`, NutriSnap or original dirty orchestration checkout.
- Zero new Herdr panes, cbds tasks, Codex/AGY execution workers, deployments, merges or timer changes.
- Zero unverified claim that named `agy --agent` equals an authenticated profile.
- No claim that unattended Nightshift works merely because 4 historical fixture tasks passed.
- No next-step execution without approval.

## Status rubric

- **PASS_FOR_OWNER_REVIEW:** ADR complete, sources/unknowns explicit, documentation-only scope verified and committed.
- **BLOCKED:** Important authority/merge fact cannot be safely investigated; document as unresolved and stop.
- **FAIL:** Scope violation or internal inconsistency; record evidence and do not advance.

After P0.2, the owner decides whether to approve **P0.3 context correction planning only**. There is no automatic progression.
