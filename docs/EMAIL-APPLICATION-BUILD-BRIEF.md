# Email Research Enrichment and Browser Outreach Application Build Brief

This is the authoritative handoff for the application discussed in the source project. It consolidates the agreed product design, test scope, implementation state, next steps, and operating constraints. The source documents are preserved verbatim below for full context.

## Intended outcome

Build a small, evidence-first application that accepts a supplied lead list and produces normalized records, public-source company evidence, recovered business contact details, explicit conflicts and unknowns, qualified lead scores, individualized drafts, safe campaign review, authorized browser-based email execution, send reconciliation, reply/opt-out suppression, and transparent cost/result reporting.

The first useful product is research plus contact evidence plus a useful individual message for each qualified lead. Gmail execution and reply handling are the next capability. Jev is a general typed-decision component throughout the application, while Super Browser supplies routed data/browser/computer execution and durable operations.

## Current agreed tests

- Enrichment: audit the first 100 supplied rows, then continue toward 5,000 only if accuracy, time, and cost are acceptable.
- Sending: 10 isolated authorized sender accounts, 20 distinct prospect emails per account, 200 total, beginning with one first-touch per account.
- Models: pinned reviewed Jev for routine typed decisions; `z-ai/glm-5.3-flash` for difficult reasoning/writing; `openai/gpt-5.6-luna:batch` only as the durable fallback after bounded failure or failed evidence checks.
- Model budget: report at $10 combined usage and block new reservations at the $20 total ceiling. Preserve the stricter shared TypeSafe $5 monthly cap.
- No live inputs, account permissions, audience legality, deliverability, or inbox placement should be inferred from the documentation.

## Source documents

The following documents are copied in full in this repository and remain the detailed specification:

- `source/outreach-prototype-test-spec.md`
- `source/outreach-prototype-next-steps.md`
- `source/researched-outreach-plan.md`
- `source/outreach-prototype-README.md`
- `source/implementation-status.md`
- `source/jev-pilot-acceptance.md`
- `source/jev-comparison-pilot.md`

Read the test specification first, then the researched plan for rationale and the next-steps runbook for sequencing. The implementation status prevents simulations and partial infrastructure from being mistaken for live readiness.
