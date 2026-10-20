# H4 — integrated Herdr path, offline acceptance

**Review date:** 2026-10-20 (Asia/Kolkata)
**Disposition:** **H4_INTEGRATED_PASS — owner-reported offline scope; READY FOR NEXT SEAT MILESTONE.** This is not evidence of current live Herdr readiness or unattended execution.

## Reported receipts

- Integrated previously tested H3 Python↔Herdr helper into the maintained Nightshift runner, including explicit survey/trust **WAITING_FOR_HUMAN**, fallback/unknown **NEEDS_INSPECTION**, and existing-seat configuration.
- **49 integration tests PASS + 11 detector cases PASS**, no reported failures; code commit **`005b596581128925d11c0ab53e20fda6e1f44d5b`**.
- Evidence commit **`43964c3179a1951353929d563b403497917ebcb5`**; local `docs/v0.5/evidence/H4_HERDR_INTEGRATION.md`.
- Source and H3 worktrees reported clean. **No new AGY prompt, manifest reload, push, merge, deployment or scheduling**.
- Important qualification: **historical Herdr PIDs were absent in the inspection context, so live seat readiness was NOT VERIFIED.** Do not assume old pane IDs `wD:p1/p4/p5` or old process PID are still alive/attached. Re-discover the current running Herdr server and agent state when authorized before routing another task.
- This GitHub instruction branch cannot fetch the owner's OpenClaw-local source SHA/evidence due to `PUSH_HOLD`. The review **accepts the reported test milestone**, not an independently inspected diff. No more agent launches or repetition of H3/H4 are justified by that limitation alone.

## Decisions

**Close H4 offline integration checkmark.** Keep separate:
- H3 = proven once *manual* AGY-Rohit coding handoff with host verification after a survey hold.
- H4 = offline integrated adapter and regressions.
- H5 = **not started**: live current Herdr seat inventory and AGY-Manickam's actual distinct CLI profile mapping.
- N1 unattended timer/human-attention behavior = **not started**.
- `PUSH_HOLD`, release/merge/deploy controls remain.

## Next narrow work

`prompts/V0.5_H5_SECOND_SEAT_ROLE_PARITY.md` stages one bounded H5 step: first discover the **current** Herdr server/panes (don't recreate previously known panes blindly), verify whether existing AGY-Rohit is live, check a real *distinct* AGY-Manickam account/profile through supported nonsecret status/owner attestation, and only after owner authorizes, start **at most one second AGY seat** if it is truly absent. No coding prompts/tasks, no retries or auto folder-trust. Keep Python the sole state authority. Existing Codex High operator can remain reviewer; no second Codex process needed merely to show a review seat.

**After H5:** one owner-gated unattended no-push run with current-seats reconciliation, capped timeout, honest report and STOP; not a recurring timer yet. Avoid a new layout subsystem.
