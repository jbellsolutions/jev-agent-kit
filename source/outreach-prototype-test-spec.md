# Browser outreach prototype: agreed test configuration

Updated September 18, 2026. This records the current design. The offline foundation is implemented; model and browser integration are still pending. No live test messages have been sent. This supersedes earlier model and pilot-budget choices in the broader research brief.

## Test scope

- Build a small working prototype before packaging the full engine, MCP server, and portable plugin.
- Keep research/enrichment, message preparation, and email execution independently runnable, with shared durable job state and evidence. Preserve separate lead-discovery capability in the later engine; it is not the 5,000-row benchmark.
- First live test: 10 authenticated sending accounts, 20 distinct prospect emails per account, 200 total. Send through the actual email browser interface. Use isolated persistent account profiles and reconcile uncertain sends before any retry.
- Second test: enrich a supplied 5,000-row list. Recover missing business contact details, social links, and useful company context, preserving sources and original row identity. This test does not generate or send a 5,000-email campaign.
- The campaign's business/offer and target prospect remain unspecified. The 10 sender accounts and recipient/list inputs have not yet been supplied for this test. These are live-run inputs; independent prototype development can proceed.

## Model routing

| Role | Model | Behavior |
|---|---|---|
| Routine choices and browser decisions | TypeSafe Jev, pinned to the reviewed version | Choose among observed actions/candidates; preserve explicit unknown/blocked outcomes. |
| Primary difficult reasoning and writing | `z-ai/glm-5.3-flash` through OpenRouter | Analyze ambiguous evidence, handle difficult browser states, and produce grounded message drafts. |
| Explicit fallback reasoning and writing | GPT-5.6 Luna Batch through OpenRouter; catalog ID `openai/gpt-5.6-luna:batch` | Process queued tasks when GLM is unavailable after bounded retry or a task fails its evidence/output checks after one repair. A fallback result must pass the same checks. |

Luna Batch is a second attempt with another model, not an assumed quality upgrade. Measure acceptance rate, latency, and cost by model and fallback reason. Do not invoke it automatically for every lead.

Batch work is asynchronous. Save an evidence snapshot and stable job identity, release the browser slot, and continue independent leads while waiting. Reobserve any live page before acting on a completed result. The discount does not apply to ordinary synchronous Luna calls; such a route is not added silently. Confirm the OpenRouter batch submission contract and account availability during implementation rather than passing a batch catalog slug into the existing synchronous client.

The existing synchronous model client is not a batch adapter. A batch adapter needs durable submission/result IDs, individual request/result matching, usage accounting, and reconciliation after interrupted submissions without blindly creating another batch. Neither model may independently authorize a send or change frozen recipient/message content during email execution.

## Budget

- Combined model-spend target: **$10** across both tests and all three models.
- Authorized stretch ceiling: **$20 total**, not an additional $20. At $10, record/report that the target was crossed; work may continue within the ceiling.
- Count input, output, billable reasoning, failed attempts where billed, and retries. Reserve estimated maximum costs before dispatch, including queued batch requests, so parallel work cannot overcommit the remaining ceiling.
- Preserve stricter existing account controls, including the shared TypeSafe $5 monthly cap. Do not bypass that cap through the standalone demo.
- Record existing computer/mailbox costs separately. This is a model budget, not a claim that the complete operation has zero infrastructure cost.

## Evidence required from the tests

- Sending: exact sender/recipient/content verification, matching Sent evidence, no duplicates or cross-account leakage, and recovery from interruptions. Report sent, bounced, replied, and confirmed recipient receipt separately; Sent alone is not delivery or inbox-placement proof.
- Enrichment: check an initial 100-row sample before continuing. Report fields recovered, unsupported/conflicting findings, unresolved rows, audited accuracy, wall time, active browser capacity, model usage, and cost per successfully enriched row. Do not treat merely processing a row as successful enrichment.
- Budget exhaustion must preserve completed results and resumable jobs and identify the unprocessed remainder. Missing fields remain explicitly unknown.

## Verified pricing and current state

OpenRouter currently lists Luna Batch at **$0.10 per million input tokens and $0.60 per million output tokens**. Rates and access must be checked at execution time. [OpenRouter Luna Batch](https://openrouter.ai/openai/gpt-5.6-luna:batch)

Batch processing is asynchronous. [OpenAI Batch documentation](https://developers.openai.com/api/docs/guides/batch)

GLM-5.3-Flash has an OpenRouter listing. [OpenRouter GLM-5.3-Flash](https://openrouter.ai/z-ai/glm-5.3-flash)

The inspected local Jev installation reports configured TypeSafe and text-model credentials. That does not establish live model entitlement or successful Gmail automation. The current demo shares one Chrome profile; the prototype needs actual sender isolation. The hosted Jev gateway currently accepts routing/evidence judgments, so browser-action selection requires a guarded extension. No paid model or send test has been performed to establish these capabilities.

The [offline foundation](../outreach-prototype/README.md) passed 17 tests on Python 3.12. Its [simulation report](outreach-prototype-offline-report.json) records 5,000 synthetic rows imported, 200 simulated message records reconciled, duplicate-attempt prevention, and spending-ceiling enforcement. Actual emails sent, rows researched, and paid model calls were all zero. These checks validate the local bookkeeping behavior, not live browser capacity or model quality.

The implementation order and remaining live inputs are recorded in [the next-steps runbook](outreach-prototype-next-steps.md).
