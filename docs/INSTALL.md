# Installation / Lab Host Setup

This lab assumes Linux/Omarchy with Git, Node.js, Herdr, Codex and Antigravity (`agy`) already available.

## 1. Check what is installed

```bash
./scripts/check-env.sh
```

## 2. Install cbds

Recommended lab setup:

```bash
./scripts/install-cbds.sh
```

The script:
- clones/updates `https://github.com/zqkra/cbds`
- installs its CLI globally with npm
- installs the cbds worker skill for supported agents
- links it into Herdr when Herdr is available

Then verify:

```bash
cbds status
cbds skill status
./scripts/smoke-cbds.sh
```

Upstream requirements at the time this lab was created: Node.js >= 18.17 and Herdr >= 0.8.0.

## 3. Do not install Gas City yet

Gas City is intentionally Phase 2. First prove T001/T002 using only Herdr + cbds so there is a clean baseline.

After the baseline succeeds, follow the current upstream Gas City installation guide instead of freezing an install command in this repo:

- https://github.com/gastownhall/gascity
- https://github.com/gastownhall/gascity/tree/main/docs/getting-started

## 4. Start the first experiment

Give the contents of `prompts/MASTER_PROMPT.md` to Codex. It explicitly instructs the orchestrator to run **T001 only** and stop after recording metrics.
