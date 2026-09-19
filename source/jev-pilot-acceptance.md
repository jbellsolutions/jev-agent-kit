# Jev comparison pilot — live acceptance

The pilot is live in Super Browser revision `b68aca5`. [PR #54](https://github.com/jbellsolutions/super-browser/pull/54) merged as `619274d16850437baa71f6507ad673469e1e8cfe`. Its tree matches the deployed application. The previous frozen release, `f0c544c`, remains the rollback target.

The pilot is collecting comparisons for the first browser-routing decision in each owner main-advisor run. It stops admitting work after 100 total samples, expires **September 25, 2026 at 03:47 PM ET**, and has a **$0.50 sublimit within the existing $5 monthly TypeSafe budget**. Hermes and all execution/approval checks remain authoritative.

## Verified results

- All 542 repository tests, fixture checks, packaging checks and syntax checks passed. GitHub's Python 3.10, Python 3.12 and minimal-install checks passed on the final revision.
- Eight fixed synthetic examples were tested in both option orders. All 16 choices matched their reference labels. Median response time was 487 ms; maximum 775 ms. Confidence shifted by up to nine percentage points despite stable choices.
- A real Hermes request then completed through the deployed service and produced its background Jev comparison. The original route and result remained unchanged. This example is recorded as synthetic validation, not organic traffic.
- Seventeen validation samples now exist; zero real traffic samples were present at acceptance. These checks do not establish production accuracy or cost savings.
- Pilot spending was **$0.000397698**; total September TypeSafe spending was **$0.000521346**. The separate Hermes acceptance request cost **$0.002507**.
- Dashboard API and MCP authentication passed; an unauthenticated report request was rejected. The owner sign-in form and all 111 documentation resources remained available.
- Pause/resume preserved both spending and the campaign dates. Internal pilot errors: zero.
- The encrypted predeployment backup succeeded. The deployment drained work and passed the existing release checks. The Hermes source fingerprint remained unchanged; no other Hermes or Orgo installation was modified.

## Where to inspect it

Open [Super Browser](https://superbrowser.online/tools/typesafe), then **Manage connection → Jev comparison pilot**. It shows status, spending, comparisons and the pause control. Acceptance verified the HTTP/MCP interfaces and served login form; the new panel was not visually inspected.

The app follow-up **Review Jev comparison pilot** is active, checking daily and scheduled for eight checks. It will review the bounded experiment when complete, report insufficient traffic if necessary, and propose any further work without enabling a fast path or extending spending. It stays quiet while the pilot is healthy.

[Full production acceptance](jev-pilot-live-acceptance.json) · [Synthetic results](jev-pilot-validation.json) · [Evaluation and recovery guide](super-browser-jev-pilot/docs/jev-comparison-pilot.md)
