# TypeSafe / Jev assistance

Super Browser exposes optional `typesafe_evaluate` routing and evidence judgments
through its hosted MCP and the Hermes action gateway. The existing main model,
permissions, browser selection and execution checks remain authoritative.

The TypeSafe connection page stores the owner key encrypted. The server runs
`typesafe-sdk==0.6.0` against `jev-1.13.0`. Set `SB_TYPESAFE_ENABLED=1` on the owner
service only after live validation. The SDK receives `TYPESAFE_API_KEY` at runtime;
the key is not passed to the browser, Hermes subprocess, or exported skills.
Global agents use the hosted MCP connection and need no separate TypeSafe key.
The portable skill's `scripts/evaluate.py` is also a thin authenticated MCP
client for agents without loaded MCP tools. It reuses `~/.super-browser.env`
or `SUPER_BROWSER_URL`/`SUPER_BROWSER_TOKEN`; `--status` reads the shared ledger,
and otherwise it accepts the JSON evaluation request on standard input.

## Interface

```json
{"purpose":"evidence","state":{"claim":"The plan includes 10 seats.","source":"The plan includes 10 seats."},"request_id":"seats-check-1"}
```

```json
{"purpose":"routing","state":{"goal":"Fetch the public JSON API endpoint","url":"https://example.com/data.json","providers_allowed":["decodo-http"],"max_cost_usd":0.01},"request_id":"route-check-1"}
```

Direct MCP clients can set `scope` to narrow candidates. Hermes gateway calls use
the actual conversation scope. Only the owner can consume this integration.
Use `advisor_manage {operation:typesafe_status,arguments:{}}` for current status.
No-match, missing connection, disabled service, budget exhaustion, and service
errors are explicit outcomes. Advice never updates the approved execution route.

## Billing and recovery

A SQLite ledger uses integer nanodollars and atomic reservations for all callers.
The immutable $5 limit resets by calendar month in America/New_York. Each request
has one Choice question and <=32 KB of serialized input. Each attempt reserves a
conservative one million input tokens ($0.042 at the pinned model's published
price), then settles from actual input usage. Output tokens are free. Unknown
outcomes retain the full reservation in their original month. Reusing the same
request ID cannot create another request. Rate-limit/overload responses allow one
retry after a one-second delay, with a separate reservation. Other errors do not
retry. Calls time out after eight seconds plus a one-second cancellation allowance.
Price/model changes require an explicit reviewed release.

The monthly TypeSafe cap is distinct from existing conversation model/provider
budgets. Tests and other agents do not receive additional independent allowances.
Concurrent requests, restarts and uncertain outcomes all use the same owner DB.

## Documentation maintenance

The portable TypeSafe skill contains original Markdown, readable copies and a
manifest with source URLs, retrieval time, upstream skill revision and hashes.
The index and sitemap must match before a snapshot is published. The full corpus
is available offline and through `super-browser://typesafe/docs` MCP resources.

The existing advisor documentation monitor checks the whole corpus every seven
days. Changed snapshots are staged under the advisor state's `typesafe-updates`
directory and appear in Profile's documentation proposals. Failed or incomplete
refreshes leave the approved bundle unchanged. Review staged changes, regenerate
the bundle and its global/project skill copies, run tests, then deploy as a normal
release. Upstream skill instructions and license remain separately archived.

Run `python -m super_browser.typesafe_docs DESTINATION` to stage a fresh corpus;
use `--validate` to verify an existing corpus. These operations fetch public docs
only and never execute downloaded code. `scripts/sync-typesafe-skill` validates
the approved archive and copies the maintained skill to a specified agent skill
root. The canonical maintained package is `skills/typesafe-ai`; project/global
installations and wheels are distribution copies of that version.

Roll back through the normal release activator or set `SB_TYPESAFE_ENABLED=0`.
Keep the ledger and connection vault intact so a rollback cannot reset spending.
