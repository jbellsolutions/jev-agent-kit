# Jev Agent Kit

This repository is a self-contained handoff for building software with Jev, TypeSafe's System One model. It deliberately treats Jev as a general typed-decision layer, not as a browser-only model.

Give this repository to Codex and say: **Read `AGENTS.md`, then use `docs/EMAIL-APPLICATION-BUILD-BRIEF.md` as the product specification. Read only the TypeSafe references needed for the feature you are implementing.**

For a one-file hosted Super Browser handoff, give the agent [`SUPER-BROWSER-LLM-BOOTSTRAP.txt`](SUPER-BROWSER-LLM-BOOTSTRAP.txt) plus a named Super Browser connection token through its secret manager.

## What is included

- The complete maintained `typesafe-ai` Codex skill.
- A complete offline snapshot of the official TypeSafe documentation, including HTTP API, JavaScript SDK, Python SDK, models, primitives, confidence guidance, patterns, cookbooks, changelogs, and Jev 1.13 jaggedness notes.
- The hosted Super Browser Jev gateway contract and its bounded shared-budget behavior.
- The full email research, enrichment, drafting, browser execution, reconciliation, and pilot specification discussed for the application.
- Provenance and SHA-256 manifests so another agent can verify what it received.

## Start here

1. Read [`AGENTS.md`](AGENTS.md).
2. Read [`docs/EMAIL-APPLICATION-BUILD-BRIEF.md`](docs/EMAIL-APPLICATION-BUILD-BRIEF.md).
3. Read [`skill/typesafe-ai/SKILL.md`](skill/typesafe-ai/SKILL.md).
4. Use [`skill/typesafe-ai/references/docs/INDEX.md`](skill/typesafe-ai/references/docs/INDEX.md) to open only the API, SDK, primitive, confidence, pattern, or cookbook references relevant to the current implementation task.
5. Treat live schemas and current service responses as authoritative when they differ from this dated snapshot.

## Important boundary

Jev returns typed judgments and probabilities. It should choose, rank, score, classify, check evidence, or select a bounded next action. Ordinary code must retain exact calculations, quotas, permissions, idempotency, durable job state, and external-write authorization. A generative model should write prose when prose is needed.

No credentials or provider secrets are included. The hosted Super Browser gateway requires a separately issued Super Browser connection token supplied through the receiving machine's secret manager.

Related repository: [Super Browser with Jev Agent Kit](https://github.com/jbellsolutions/super-browser-jev-agent-kit)
