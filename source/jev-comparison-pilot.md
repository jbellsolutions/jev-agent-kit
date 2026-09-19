# Jev comparison pilot

The owner dashboard records Jev's alternative interpretation of the **first
`browser_route` call in each main-advisor run**. Hermes and the existing router
remain in charge. The pilot neither changes a route nor bypasses a connection,
scope, approval, or spending check. Other Hermes profiles and Orgo workers are
outside this release.

## Question and comparison

The four choices are `planning`, `api`, `browser`, and `needs_context`. The private
preset in `advisor/typesafe_pilot.py` classifies the immediate request, using its
redacted prompt, explicit browser selection, and currently verified API operations.
It does not see Hermes's answer. Missing conversation context and mixed tasks may
produce `needs_context`. Prompts larger than 6 KB are excluded rather than truncated.
Only the owner’s `orchestrator` conversations participate. Specialist conversations
and guests are excluded. The existing public TypeSafe tool retains its two purposes.

The baseline reflects the router's precedence: planning; explicitly selected or
required signed-in browser; API suitability; a selected unattended browser; or
needs-context/provider selection. This compares **intent categories**, not provider
names or browser device identifiers. It observes only runs where Hermes invokes
`browser_route`; it cannot measure requests that never reach that action.

The exact original route, paired judgments, probabilities, confidence, option
order, model, usage, elapsed time and cost are retained on the owner service.
No pilot result appears in Hermes's tool response. Capture uses a local durable
queue after the original result is saved. Network calls run in a separate worker.
Ordinary work continues on capture or model failures. The report exposes a count
of internal capture/processing errors without storing sensitive exception bodies.

## Bounds and recovery

The campaign is `browser-intent-v1`. An explicit, idempotent start fixes its end
seven days later. It admits at most 100 samples, including synthetic validation,
and has a $0.50 lifetime sublimit **inside the existing $5/month TypeSafe limit**.
Both limits use the same atomic reservations; the sublimit survives month rollover.
Uncertain billing retains its reservation. A $0.042 reservation is required before
each attempt, so the campaign may stop below $0.50 when the next reservation would
not fit. Existing eight-second timeouts and bounded retries still apply.

Only one sample per run is captured. Already admitted samples may finish after the
sample admission limit. Unstarted samples expire after 15 minutes or at campaign
expiry. Pause prevents new samples and jobs; a call already in progress can finish
its bounded attempts. Restart recovers completed results and marks interrupted
jobs uncertain without replay. Deployment draining includes the worker's live
calls. Rollback keeps the ledger and experiment tables intact; the previous
release continues to read the original ledger schema.

## Dashboard and management

Open **TypeSafe / Jev → Manage connection → Jev comparison pilot** for status,
spending, pause/resume, and paginated comparisons. The existing authenticated
management interface also supports:

- `typesafe_pilot_report {offset:0,limit:20}` (0–20 samples; default summary only).
- `typesafe_pilot_control {action:start|pause|resume}`. Start cannot reset a campaign.
- `typesafe_pilot_label {sid,label,note}` for an independent review with evidence.

These operations require the workspace owner through either dashboard or MCP.
Reports and labels stay on the owner service. No new provider credentials are
installed globally or distributed in bundles.

## Evaluation and promotion

Traffic and synthetic validation have separate metrics. Fixture baselines are
explicitly identified as reference labels, not Hermes output. Agreement with
Hermes is not accuracy; a completed workflow is not an accuracy label. Accuracy
uses only samples with an independent evidence note. Review disagreements and a
representative sample of agreements, including confident wrong agreements. Report
sample counts, unavailable/expired samples, category coverage, and option-order
sensitivity; do not select a confidence threshold from a tiny success-only set.

`scripts/validate-jev-pilot` previews eight frozen synthetic cases without paid
calls. On the owner service, `--live` evaluates both option orders under the shared
ledger (16 idempotent cases). It requires the existing owner database and encrypted
vault. CI never invokes live mode. Run this with the candidate release's Python and
`SB_TYPESAFE_ENABLED=1` before enabling traffic collection.

This experiment adds Jev calls and does **not** establish cost savings. Its report
leaves savings unknown and promotion marked `review_required`. After the campaign,
assess independently labeled traffic per category and propose a separate release
for any proven fast path. There is no automatic promotion or Hermes upgrade.

The design follows TypeSafe's [confidence guidance](https://docs.typesafe.ai/confidence)
and [typed Choice primitive](https://docs.typesafe.ai/primitives/choice). Thresholds
must be measured for the task; confidence is not permission or proof of correctness.
