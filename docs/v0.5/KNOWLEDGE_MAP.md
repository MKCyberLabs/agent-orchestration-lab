# Project and operations knowledge map — V0.5

**This is an address book, not proof that each linked source is the current authoritative version.** P0 must verify host paths, branches, SHAs and runtime configuration.

## Orchestration lab

| Concept | Initial address | Grounding / warning |
|---|---|---|
| Repo | \`MKCyberLabs/agent-orchestration-lab\` | Local host previously \`/home/openclaw/agent-orchestration-lab\`; verify |
| V0.4 Nightshift | \`scripts/nightshift.py\` | One configured worker, sequential, JSON state |
| V0.4 operating notes | \`docs/NIGHTSHIFT_V0.4_PILOT.md\` | Says no timer is auto-installed |
| Disposable smoke | \`scripts/openclaw-v04-smoke.sh\` | Requires actual headless Codex/AGY CLI on host |
| Offline contracts | \`tests/test_nightshift.py\`, \`tests/test_openclaw_smoke.py\` | Mock CLIs; cannot establish real account identity |
| Backlog examples | \`config/backlog.example.json\`, \`config/nightshift.example.json\` | Examples, not live approved tasks |
| Scheduled service | \`systemd/mk-nightshift@.service\`, \`systemd/mk-nightshift@.timer\` | Source exists; installed/enabled state unknown |
| Earlier multi-agent design | \`docs/ARCHITECTURE.md\`, \`docs/V0.2_TICKET_REVIEW_LOOP.md\` | Herdr/cbds experiments; do not dual-dispatch |
| Existing agent rules | \`AGENTS.md\` | Generic shared rules; contextualize for V0.5 |
| This pilot | \`docs/v0.5/START_HERE.md\` | Planning document only |

## NutriSnap product (source must be pinned during P0)

| Concept | Likely code/document address | Status and caution |
|---|---|---|
| Product repo | \`MKCyberLabs/NutriSnap\` | Confirm local source and branch |
| Shared agent context | \`AGENTS.md\` | On \`main\`, older v0.1 instructions were observed; **stale-pointer risk** |
| Product overview | \`README.md\` | Describes Next.js UI, Telegram and separate Python API |
| Next.js frontend | \`src/app/\`, \`src/components/\` | Verify precise feature routes against pinned SHA |
| Domain/business logic | \`src/lib/\` | Validate ownership and dependencies |
| Shared reminders | \`src/lib/scheduler.ts\`, \`src/instrumentation.ts\` | Avoid creating second scheduler; runtime/build distinction |
| Finance and accounting | \`src/lib/finance/\` | Money/tenant isolation/idempotency are high-risk |
| Database | \`prisma/schema.prisma\` | No production migrations or \`prisma db push\` |
| Python analysis API | Separate deployed service; NutriSnap \`README.md\` describes it | Treat observed production host path as **not** an approved testing target |
| Telegram integration | Relevant route/service files under \`src/\` | Locate exact source and mock before tests |
| Existing development baseline | \`docs/DEVELOPMENT_BASELINE.md\` | Inspect actual test DB and authorization before using |
| Current workflow evidence | Relevant \`versions/\`, \`docs/\`, Git issues and branch-specific reports | Identify current rather than carrying forward 13 v0.1 reads |

## What agents should read at startup

1. \`docs/v0.5/START_HERE.md\` for orchestration intent.
2. \`docs/v0.5/STATUS_AND_DECISIONS.md\` for the latest approved step.
3. Specific \`P0_CHECKLIST.md\` subsection or approved issue and **only** its directly relevant project files.

Do **not** inject all legacy logs, all \`versions/\` docs or entire transcripts into the agent context.

## Who knows what — proposed seats, not yet registered processes

- **Owner:** product behavior, permissions, deadlines, release decision.
- **Python dispatcher (future verified registry):** executable selection, authenticated profile verification, worktree, approved task, timeout and status.
- **AGY-Manickam:** implementation OR coordination when explicitly assigned; not a magical authenticated identity conveyed by role text.
- **AGY-Rohit:** bounded implementation/test work when explicitly assigned.
- **Codex:** architecture and independent review when asked; review must not silently become implementation.

## OpenRig concepts we borrow, without copying framework

- Addresses and maps, not mandatory giant context dumps.
- Durable named responsibility, not vague invocation through another model.
- Differentiate observation, verified evidence, approved rules.
- Short incident lessons, attached to relevant failure paths.
- Refocus after compaction/restart **later**, only after V0.5 has a useful and trustworthy handoff.
- Keep the owner's goal central; "search before build."

References: \`https://github.com/mvschwarz/openrig\`, \`https://openrig.dev/\` and creator's context / architecture writeups. These are learning references, **not runtime dependencies**.
