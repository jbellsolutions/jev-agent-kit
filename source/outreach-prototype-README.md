# Outreach prototype — milestone 1

Local, offline foundation for the agreed 200-message / 5,000-row pilot. This is not yet a connected browser sender or enrichment agent.

Implemented: durable row imports and work queues, explicit Jev/GLM/Luna Batch routing, atomic model-spend reservations, ten-profile message assignment, suppression, and reconciliation of interrupted send attempts. All money uses integer nanodollars. Model choices do not grant permission to send.

No external packages, secrets, model calls, or browser connections are needed for this milestone. Existing Super Browser checkouts and production services are unchanged.

## Agent commands

From this directory:

```sh
python3 -m unittest discover -s tests -v
python3 pilot.py verify --report ../deliverables/outreach-prototype-offline-report.json
```

`verify` creates a temporary database, imports 5,000 synthetic records, assigns 200 synthetic messages across ten isolated-profile identifiers, and simulates an interrupted send. Its output distinguishes simulation from live activity. It sends zero emails and makes zero paid calls. The stored profile identifiers are bookkeeping, not proof of actual browser isolation.

## Next implementation milestones

1. Extend the existing hosted Jev gateway to accept bounded browser-action choices while retaining its shared $5 monthly ledger. The current gateway only accepts routing/evidence purposes. Never connect the standalone demo directly to avoid that ledger.
2. Connect OpenRouter GLM requests and Luna Batch submissions/results to the local reservation ledger. Use provider usage to settle charges; retain reservations after unknown outcomes. Verify actual batch access and response contracts before enabling it. The current code routes jobs but does not call these services.
3. Add browser observation/action adapters with separate persistent profiles. Prove the signed-in identity, exact draft fields, and matching Sent result on one Gmail account before expanding. Treat all page content as untrusted data. Reconcile ambiguous sends; do not replay them.
4. Implement enrichment over company sites, search results, and relevant public social/directory pages, recording per-field evidence. Keep missing or conflicting data explicit. Run 100 supplied rows before continuing the 5,000-row benchmark.
5. Prepare campaign evidence and messages once the business/offer and prospect audience are identified. Check each sender and exact approved audience/content, then run one first-touch per account followed by the remainder of the 200 total. Provider limits may spread this across days.

The shared $10 target / $20 ceiling applies to model usage across both tests. Reaching $10 is a reportable milestone; $20 blocks new reservations. Existing stricter account limits remain in force. Computer and mailbox costs are recorded separately. Creating another database does not grant a new spending allowance: the live adapter must use one canonical pilot ledger for both tests.

## Boundaries

- The local queue is for enrichment and draft jobs only. Sending uses a separate state machine.
- A send attempt is recorded before browser execution. An interrupted or uncertain attempt consumes its slot until independently reconciled. Reconciliation can establish it was sent; automatic resend is never provided.
- The send ledger is an internal accounting control, not a Gmail connector, authorization service, or delivery verifier. Live adapters must supply independently observed identity/content evidence and enforce the approved campaign scope.
- The local model ledger does not replace Super Browser's hosted monthly Jev budget.
- Source data stays in original rows. Fields are not guessed, validated, researched, or enriched by importing them.

See [the agreed specification](../deliverables/outreach-prototype-test-spec.md) for model roles and test scope.
