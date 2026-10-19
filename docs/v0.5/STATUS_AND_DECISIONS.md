# V0.5 status, decisions and lessons

Date: 2026-10-19. **Planning documents committed only on `planning/v0.5-p0-handoff-20261019`.**

| Step | State | Evidence / next gate |
|---|---|---|
| P0.1 host inventory | **PASS_FOR_P0_PLANNING — OWNER ACCEPTED** | [Preserved evidence](evidence/P0.1_INVENTORY_2026-10-19.md); operational readiness still HOLD |
| P0.2 authority ADR | **AUTHORIZED — DOCUMENTATION ONLY / IN PROGRESS** | [Codex master prompt](../../prompts/V0.5_P02_ADR_MASTER_PROMPT.md); [output contract](P02_ADR_OUTPUT_CONTRACT.md). ADR requires separate owner decision |
| P0.3 NutriSnap context correction | PROPOSED | Separate owner approval and pinned NutriSnap branch |
| P0.4 project source map | PROPOSED | Actual source/paths must be verified |
| P0.5 trust and evidence | PROPOSED | Show worker vs host verification distinction |
| P0.6 readiness and blockers | PROPOSED | No live CLI smoke without authorization |
| P1 seat registry and negative tests | NOT_STARTED | Requires P0 gate |
| P2 issue/skill/knowledge contract | NOT_STARTED | Requires P1 gate |
| P3 real night pilot | NOT_STARTED | Requires P2 gate and separate approval |

## Decisions established as planning constraints

- **D-01: No OpenRig installation.** Borrow navigable knowledge, seats, refocus, maturity concepts.
- **D-02: One active dispatcher per experiment.** V0.5 uses the existing sequential Python runner as planned authority; Herdr/cbds is not silently layered onto it. P0.2 confirms or revises with owner approval.
- **D-03: Real identity != agent name.** `agy --agent`, Herdr pane title and model self-report do not prove authenticated CLI account or execution.
- **D-04: Every step is gated.** Codex may inspect P0.1 and recommend P0.2; may not advance without approval.
- **D-05: No auto promotion.** No merge, deployment, production database actions, live Telegram sends, new scheduler or automatic hardware flash.
- **D-06: Truth stays traceable.** Git source SHA, actual tests, host receipts and owner decisions outweigh prose/status.
- **D-07: No unbounded work.** Preserve doghouse goal; avoid new dashboards/frameworks, unauthorized subtasks and unlimited reviews.

## Known pitfalls to re-check, not assumptions of current host state

1. A user asked AGY-Rohit to call AGY-Manickam, and observed it creating an internal agent. **Outcome:** add externally verifiable launch receipt; never accept nested substitution.
2. NutriSnap `main:AGENTS.md` contains historical v0.1 workflow pointers despite later branches existing. **Outcome:** validate current branch and create a small map, not another giant startup prompt.
3. P0.1 checked **four historical `VERIFIED_COMMITTED` fixture task receipts** (two Codex, two AGY). They support the historical fixture outcome **only**, not headless profile selection, 24×7 readiness, unattended recovery or release.
4. Earlier coordination spent tokens polling terminals and expanding the control plane. **Outcome:** deterministic waits and scarce model wake-ups, without switching frameworks mid-milestone.
5. Verification paperwork can outgrow delivery. **Outcome:** acceptance evidence matters only if it protects useful completion.

## Decision/update protocol

- One actor records the owner-approved decision and its reason; pending questions remain marked pending.
- For operational claims write full branch/SHA, tool command, date, redacted evidence location, verification status.
- If an old decision becomes false, mark `SUPERSEDED` and link the replacement; do not erase the reason.
- Keep this file short. Archive later historical checkpoints as separate evidence after owner approves documentation updates.

## First handoff

P0.1 is complete and its report is preserved at `docs/v0.5/evidence/P0.1_INVENTORY_2026-10-19.md`. The owner authorized **P0.2 only** as a docs/ADR inspection and Git evidence task. Codex High should read `prompts/V0.5_P02_ADR_MASTER_PROMPT.md`, write/commit planning documents in a separate isolated branch, and STOP for owner approval before P0.3.
