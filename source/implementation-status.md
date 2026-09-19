# Super Browser implementation — September 13, 2026

Release `421473e` is deployed. The existing Railway dashboard now uses actual Hermes on DigitalOcean and an isolated Super Browser worker on the Revenue Partner Orgo computer. Browser selection defaults to Auto. The existing Revenue Partner agent retains its own display and profile.

## Delivered

- Chat, Tools, Workflows and Templates navigation; shared 70/30 chat and guide pages for all 15 registered integrations.
- Persistent conversations, sequenced streaming events, visible tool activity, editable plans through conversation, run steering, stop and eligible continuation, source-backed results and downloadable artifacts.
- Integration scopes, explicit browser routing, required-session disconnection handling, a serial desktop queue, atomic run/workspace budgets and delayed provider billing reconciliation.
- Maintained authenticated MCP transport with 27 tools, preserving the legacy interfaces.
- Transactional token storage, bounded requests, authenticated listings, expired advisor-run recovery, pinned release dependencies, checksum manifests and automatic rollback.
- Encrypted off-server backup on Revenue Partner. The final snapshot restored 801 files and passed integrity checks for 14 SQLite databases; its encrypted off-server checksums also matched. The private recovery key remains on this Mac.
- Redundant Railway advisor stopped; its configuration and volume preserved. The old uncontrolled DigitalOcean self-update timer is disabled.

## Verification

448 tests and the complete repository verification script passed with local fixture-server access. Public MCP initialization, tool discovery and unauthenticated-request rejection passed. A deliberately broken release was rejected and the healthy release restored automatically. Live checks covered real Hermes, Steel, Composio, public HTTP, Apify, Revenue Partner open/read/screenshot, steering, event reconnects, and stopped-run continuation. Browser screenshot artifacts loaded at their actual 1280 × 900 dimensions.

GitHub Actions cannot start because GitHub reports an account billing restriction. No billing settings were changed. Draft review: https://github.com/jbellsolutions/super-browser/pull/42

## Collection

The 25-record pilot and final 1,000-business collection are complete. The final export contains distinct public business contact groups with explicit Florida state evidence and source URLs. Shared phones, websites and place IDs group related listings; these are not verified legal entities. It has 308 missing websites and 38 missing public phones. No verified emails or named decision-makers are claimed. No lead messages were sent.

Recorded workspace variable usage, including verification: **$4.929518 of the $10 ceiling**, with no outstanding reservations. Fixed subscriptions are separate; their current totals have not been verified.

Files: `final-florida-1000/florida-1000-businesses.csv`, `final-florida-1000/florida-1000-businesses.json`, and `final-florida-1000/quality-and-cost.json`.

## Outstanding acceptance limits

- Chrome extension installation is authorized and the extension is prepared, but browser controls were unavailable and a subsequent attempt was interrupted by a change in Chrome. It is not installed or paired. Live “this browser” access and signed-in account reuse are therefore not certified. Opening Railway alone does not grant access to tabs or logins.
- Connected account identity still needs an end-to-end verification flow. Account-routing unit tests do not establish real account discovery.
- Retriever's remote MCP adapter, Decodo's paid proxy/scraping route, and several other provider-specific paid execution paths remain unverified or unconnected. Their vendor guides do not imply these actions are ready. The application labels readiness explicitly.
- The isolated worker currently exposes tab listing, opening, reading and screenshots. General desktop clicks, typing, uploads and messaging require additional execution adapters and, for messaging, separate authorization.
- Bulk API collection is bounded and budgeted. This release does not certify 100 or 1,000 simultaneous browser sessions.
- Claimed desktop work with an uncertain outcome requires inspection rather than automatic replay. Backups on Revenue Partner are off-server but are not an immutable independent object-storage archive; retention and a third recovery location remain operational improvements.

The source reference folders and synced project sources were preserved.

## File upload addition

The chat composer now includes Attach, and every conversation has a Files panel with uploaded documents and created reports, datasets and screenshots. Files persist across refreshes and are included in the encrypted backups. Document text extraction supports text PDFs, DOCX, XLSX and common text formats; unsupported files remain downloadable. Image understanding and OCR are not connected. Uploads allow 10 MB per file. The advisor can read conversation-owned documents and create TXT, Markdown, CSV and JSON downloads.

Validation: 456 tests and the full verification suite passed. Browser checks covered attachment selection, upload, preview, saved history and mobile layout. Through the live Railway URL, a synthetic DOCX was uploaded, read by real Hermes and turned into a saved Markdown report. A 1.1 MB upload downloaded byte-for-byte unchanged. The model check cost $0.002578.
