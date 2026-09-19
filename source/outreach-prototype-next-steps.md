# Running the outreach prototype

## Completed: local foundation

The foundation passed 17 offline tests on Python 3.12. It imported 5,000 synthetic lead rows and reconciled 200 simulated message records across ten profile identifiers. Tests covered concurrent spending reservations, the $10 target and $20 ceiling, suppression, sender/content matching, interrupted send attempts, duplicate imports, and expired worker claims.

**No emails were sent, no rows were actually researched, and no paid model calls were made.** Actual browser isolation and model access remain unverified. [Raw simulation report](outreach-prototype-offline-report.json) · [Implementation](../outreach-prototype/README.md)

## Next: connect the models and one browser

The agent will extend the hosted Jev connection for bounded action selection while preserving its existing monthly budget. It will add GLM as the primary reasoning/writing client and a durable Luna Batch fallback adapter, with every call counted against the same pilot ledger. It will then connect a single isolated Gmail profile and independently check its signed-in identity, compose controls, exact draft content, and Sent evidence.

Credentials already being present does not prove endpoint access or account readiness. Connection checks and any paid model smoke tests will be reported separately and counted in the agreed $10 target / $20 maximum. The standalone Jev demo will not be used to bypass the hosted budget.

## Then: run the 200-message test

The live campaign needs a defined business/offer, target audience and recipient records, plus ten verified sender identities. The agent will prepare the researched messages, check their evidence and campaign rules, and bind each message to its sender. These inputs are not inferred from unrelated project datasets or default browser logins.

After draft checks, the run starts with one first-touch message per account. Those ten count toward the total of 200. Continue with the remaining 190 only while account identity, content checks, account limits, and reconciliation are passing. Each sender has at most 20 messages for this pilot. Replies and opt-outs feed suppression before further sends. Provider limits may spread the run across days.

Success means matching Sent evidence for the intended messages, no duplicate sends or account mix-ups, and an honest record of failures or unresolved outcomes. Sent evidence alone does not establish delivery or inbox placement. Uncertain attempts are held for reconciliation.

## Then: benchmark 5,000 supplied rows

Build the independent enrichment worker to investigate company websites, search results, and relevant public directories/social pages. Preserve original rows and attach evidence to recovered emails, phone numbers, social links, and company context. Keep conflicting or unavailable information explicit.

Run 100 supplied rows first, audit the recovered fields, and report cost and time before continuing. The 100 rows count toward 5,000. Continue within the model budget; retain partial results and the unprocessed remainder if the ceiling is reached. This larger test enriches the list without producing or sending a 5,000-message campaign.

The report separates rows processed from rows successfully enriched and includes per-field recovery, audited accuracy, failures, elapsed time, active browser capacity, model/fallback usage, and model cost. It also lists infrastructure costs separately.

## Productization follows evidence

Use the observed failure rate, recovery rate, and cost to decide what needs fixing before increasing concurrency. Package the proven workers behind the dedicated engine/MCP and portable plugin, with Super Browser integration, after the live workflow works. The current foundation does not certify hundreds of simultaneous browsers, deliverability, or the final enrichment cost target.
