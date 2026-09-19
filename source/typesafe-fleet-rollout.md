# Hermes and Orgo TypeSafe rollout proposal

Observed 2026-09-17. **Proposal only: this release does not install, update, restart, or change profiles on these computers.** The Super Browser owner service remains the only holder of the TypeSafe key and the only service allowed to charge its shared $5 monthly ledger.

## Deployment matrix

| Computer | ID | Observed Hermes runtime | Workspace/source relationship | Later canary |
|---|---|---|---|---|
| Revenue Partner | 9262e760-6069-4dcf-a96f-6a92321ad352 | 0.19.0 (installed metadata; source commit unavailable) | unified-studio-38560b2549f49391; revenue-partner-studio candidate, export hash not proven | tester after verifying its effective skill inventory |
| AI Guy Go To Market | eed51fbb-8f2e-4b78-8d8f-8aa672b11df5 | 0.21.0 · 63279301bcbd | unified-studio-2c9caa6; revenue-partner-studio candidate; ai-guy-go-to-market is its memory vault | studio-qa-email, then team-gtm and team-support |
| AI Guy Operator Co-Founder — Live | 9100ac09-4e00-4de0-be3f-99ea203a1f8e | 0.16.0 · a46462ec6577 | unified-studio-2c9caa6 plus legacy hermes-orgo-studio db9f60d70517; the-operator explicitly binds this computer | QA profile first; distinguish active fieldday profiles from imports |
| Content Studio Agent | afdb8c8d-345a-4d52-ad45-e0f60e7ca9ea | 0.21.3 · a4f8f91e50ca | unified-studio-2c9caa6 plus Content Studio 0.4.0-rc.1; video-editor-content-ops-orgo candidate | studio-qa-content before production content profiles |

The four computers contain 39 named profile directories plus four default homes. Directories and processes inheriting HERMES_HOME are evidence of configuration/use, not proof of active model work. Operator also has processes with HERMES_HOME=/opt/data, separate from the visible profile collection; reconcile that container before touching it. No credentials, model prompts, contact data, or full process environments were collected.

[Machine-readable inventory](typesafe-fleet-inventory.json) records individual paths, skill counts, observed process homes and available source revisions. Version labels are from installed metadata or source fields; exported studio directory names alone do not establish a Git commit.

## Individual profile candidates

Skill counts are local SKILL.md files, not the effective merged catalog. Zero may inherit shared skills. The pilot must read actual skill names/descriptions through the installed Hermes discovery API before ranking suggestions.

| Computer | Profile | Local skill files | Process using this home observed |
|---|---|---:|---|
| Revenue Partner | default | 150 | Yes |
| Revenue Partner | team-revenue | 83 | No |
| Revenue Partner | tester | 0 | No |
| AI Guy Go To Market | default | 259 | Yes |
| AI Guy Go To Market | assistant | 58 | No |
| AI Guy Go To Market | gtm-assistant | 226 | No |
| AI Guy Go To Market | revenue-agent | 58 | No |
| AI Guy Go To Market | studio-qa-email | 0 | No |
| AI Guy Go To Market | team-gtm | 59 | No |
| AI Guy Go To Market | team-support | 59 | Yes |
| AI Guy Operator Co-Founder — Live | default | 93 | Yes |
| AI Guy Operator Co-Founder — Live | fieldday-builder | 0 | Yes |
| AI Guy Operator Co-Founder — Live | fieldday-researcher | 0 | No |
| AI Guy Operator Co-Founder — Live | fieldday-reviewer | 0 | No |
| AI Guy Operator Co-Founder — Live | fieldday-writer | 0 | No |
| AI Guy Operator Co-Founder — Live | imported-ai-guy-go-to-market-065e53ec89 | 233 | No |
| AI Guy Operator Co-Founder — Live | imported-assistant-a07eb7c81b | 83 | No |
| AI Guy Operator Co-Founder — Live | imported-buzz-d7d8298e15 | 197 | No |
| AI Guy Operator Co-Founder — Live | imported-coder-ac30662888 | 94 | No |
| AI Guy Operator Co-Founder — Live | imported-cold-email-agent-1243d7e0ab | 203 | No |
| AI Guy Operator Co-Founder — Live | imported-default-f5250388bd | 204 | No |
| AI Guy Operator Co-Founder — Live | imported-design-5ed70b1b4a | 198 | No |
| AI Guy Operator Co-Founder — Live | imported-hermes_mastery-7cf5c271be | 150 | No |
| AI Guy Operator Co-Founder — Live | imported-local-lead-mining-revenue-agen-e5015eaad8 | 199 | No |
| AI Guy Operator Co-Founder — Live | imported-moltsets-d947a6d5be | 275 | No |
| AI Guy Operator Co-Founder — Live | imported-multica-orgo-6a7a0c744d | 196 | No |
| AI Guy Operator Co-Founder — Live | imported-orchestrator-010672e290 | 93 | No |
| AI Guy Operator Co-Founder — Live | imported-orgo-193edc17a2 | 200 | No |
| AI Guy Operator Co-Founder — Live | imported-reasoner-0fe1ae61a4 | 93 | No |
| AI Guy Operator Co-Founder — Live | imported-rev-ops-agent-7855c756f5 | 200 | No |
| AI Guy Operator Co-Founder — Live | imported-sda-c1a13f5388 | 127 | No |
| AI Guy Operator Co-Founder — Live | imported-speakeragent-799b9cbabb | 113 | No |
| AI Guy Operator Co-Founder — Live | imported-superbrowser-5598b06e53 | 159 | No |
| AI Guy Operator Co-Founder — Live | imported-team-builder-6031a7e126 | 195 | No |
| AI Guy Operator Co-Founder — Live | imported-vps-agent-copy-c8da4eeac8 | 154 | No |
| AI Guy Operator Co-Founder — Live | studio-qa-email | 0 | No |
| AI Guy Operator Co-Founder — Live | studio-qa-files | 0 | No |
| AI Guy Operator Co-Founder — Live | studio-qa-screen | 0 | Yes |
| AI Guy Operator Co-Founder — Live | studio-qa-witness | 0 | Yes |
| Content Studio Agent | default | 86 | Yes |
| Content Studio Agent | imported-assistant-e2d0bb2633 | 83 | No |
| Content Studio Agent | studio-qa-content | 1 | Yes |
| Content Studio Agent | tester | 1 | No |

Imported profiles on Operator and Content Studio remain excluded from the first deployment wave until their owner, use and origin are reconciled. “No” above is a point-in-time observation, not a declaration that a profile is inactive.

## Classify the 28 GitHub search matches

Classification uses each default-branch README plus read-only runtime observations. Repository names are candidates, not 28 confirmed agents.

| Repository | Classification | Treatment |
|---|---|---|
| [hermes-super-agent](https://github.com/jbellsolutions/hermes-super-agent) | Deployment template | Public multi-host fabric distribution; update release template after pilot. |
| [ai-guy-go-to-market](https://github.com/jbellsolutions/ai-guy-go-to-market) | Supporting project | Shared memory vault, not a Hermes executable. |
| [hermes-crm-super-agent](https://github.com/jbellsolutions/hermes-crm-super-agent) | Deployment template | Per-client Salesforce/Slack alpha; preserve inherited fabric pin. |
| [super-duper-agent](https://github.com/jbellsolutions/super-duper-agent) | Deployment template | Desktop/workforce distribution; test packaged extension hooks separately. |
| [hermes-instance-backup](https://github.com/jbellsolutions/hermes-instance-backup) | Backup | Restore artifact; refresh through the normal backup process after approved upgrades. |
| [hermes-super-agent-private](https://github.com/jbellsolutions/hermes-super-agent-private) | Deployment template | Private bootstrap overlay; never place the TypeSafe key in its bundle. |
| [Open-Orgo-Bot](https://github.com/jbellsolutions/Open-Orgo-Bot) | Deployment template | Desktop client fork; match installer/runtime compatibility before release. |
| [ai-guy-on-demand](https://github.com/jbellsolutions/ai-guy-on-demand) | Runtime candidate | README describes deployed extension/gateway; machine and runtime binding unverified. |
| [brightdata-agent](https://github.com/jbellsolutions/brightdata-agent) | Supporting project | CLI toolkit/catalog/skills; source skills may be indexed, not independently upgraded as agents. |
| [event-lead-ops-agent](https://github.com/jbellsolutions/event-lead-ops-agent) | Deployment template | Implementation handoff blueprint, not evidence of a running agent. |
| [hermes-workforce-router](https://github.com/jbellsolutions/hermes-workforce-router) | Supporting project | Preferred shared plugin hook, including pre_llm_call advice and existing workforce routing. |
| [hermes-orgo-studio](https://github.com/jbellsolutions/hermes-orgo-studio) | Archive | GitHub archived; legacy local checkout exists on Operator. Do not upgrade archive in place. |
| [hermes-mastery-hub](https://github.com/jbellsolutions/hermes-mastery-hub) | Supporting project | Training/reference role library. |
| [orgo-ai-guy-bot](https://github.com/jbellsolutions/orgo-ai-guy-bot) | Deployment template | Korgo desktop distribution with compatibility-pinned Hermes; no blanket hermes update. |
| [hermes-desktop-os1](https://github.com/jbellsolutions/hermes-desktop-os1) | Deployment template | OS1 desktop installer; update template only after client compatibility tests. |
| [cold-email-infrastructure](https://github.com/jbellsolutions/cold-email-infrastructure) | Supporting project | Email operations scaffold; no sending or campaign changes in this integration. |
| [hermes-super-agent-internal](https://github.com/jbellsolutions/hermes-super-agent-internal) | Deployment template | Internal fabric distribution; update pinned plugin package rather than Hermes core. |
| [agent-os](https://github.com/jbellsolutions/agent-os) | Deployment template | Agent fabric and vault bundle; no confirmed machine binding. |
| [revenue-partner-studio](https://github.com/jbellsolutions/revenue-partner-studio) | Runtime candidate | Current workspace/control-plane source; exported unified-studio folders need artifact-to-commit attestation. |
| [affiliate-manager](https://github.com/jbellsolutions/affiliate-manager) | Runtime candidate | README identifies separate Docker host 167.71.89.17 and pinned image; not inspected or modified. |
| [peptide-operator-orgo](https://github.com/jbellsolutions/peptide-operator-orgo) | Deployment template | Isolated client operations team template. |
| [ai-cofounder-orgo](https://github.com/jbellsolutions/ai-cofounder-orgo) | Deployment template | Managed leadership team template. |
| [video-editor-content-ops-orgo](https://github.com/jbellsolutions/video-editor-content-ops-orgo) | Runtime candidate | Content Studio candidate; reconcile installed 0.4.0-rc.1 artifact before rollout. |
| [super-browser](https://github.com/jbellsolutions/super-browser) | Confirmed runtime | DigitalOcean owner service; this implementation only, Hermes pin retained. |
| [the-operator](https://github.com/jbellsolutions/the-operator) | Confirmed deployment configuration | README explicitly binds Operator computer 9100ac09-4e00-4de0-be3f-99ea203a1f8e. |
| [hermes-agent](https://github.com/jbellsolutions/hermes-agent) | Supporting project | Framework fork, not an inventory of installations. No blanket core upgrade. |
| [super-agent-sales-director](https://github.com/jbellsolutions/super-agent-sales-director) | Deployment template | Sales vertical fabric template. |
| [sovereign-trades-method](https://github.com/jbellsolutions/sovereign-trades-method) | Deployment template | Vertical skill/fabric kit; validate installation mode before packaging. |

## Shared extension design

Use one small, versioned Hermes plugin with the official TypeSafe skill and the separately identified Super Browser specialist guide. Reuse hermes-workforce-router's extension hooks where present. Add ephemeral advice at the supported pre_llm_call hook and preserve each runtime's current system prompt, permissions, tools, context budget, core version and profile configuration. If a pin lacks a compatible hook, keep that installation unchanged until a tested adapter exists.

The plugin authenticates to the owner Super Browser service with a scoped per-profile credential, stable request identifiers and an explicit timeout. The TypeSafe key never leaves that service. The present release supports only browser route advice and evidence judgments; fleet skill ranking needs a separately reviewed server-side purpose/schema before deployment. Do not expose arbitrary TypeSafe questions or direct SDK access to remote agents.

Follow the [official Hermes skill-suggestion cookbook](https://docs.typesafe.ai/cookbooks/skill_suggestion): build choices from the profile's real, current skill inventory, use a two-stage shortlist and selection when necessary, and allow no-match. No synthesized or cross-profile skill names. Treat a recommendation as optional context; the current Hermes tool/approval rules decide execution. Calls for skill ranking and validation must reserve from the same central monthly ledger.

## Pilot, acceptance and rollback

1. **QA pilot:** start with Revenue Partner's existing tester profile after a read-only check of its inherited skills. Snapshot only that profile and record Hermes version, plugin hash, skill inventory hash and existing extension hooks. Install the plugin disabled, then enable advice for synthetic, read-only cases. Keep production profiles unchanged.
2. **Offline acceptance:** at least 20 labeled routing/skill tasks and 10 evidence cases, including no-match, unrelated inventory, unsupported and contradicted claims, source prompt injection and private-profile boundaries. Require no out-of-catalog suggestions, no permission/scope expansion, no secret output and no duplicate execution. Record accuracy by profile, p50/p95 latency and cost; require at least 90% agreed labels before enabling routine advice.
3. **Metered pilot:** capped sample of 10 synthetic live calls using the central ledger, with a $0.50 pilot suballocation inside the shared $5 ceiling. Compare with the unchanged Hermes baseline. No external messages, campaigns, content publishing or purchases. Missing/timeout/budget failures must leave the ordinary workflow usable.
4. **Staged deployment:** GTM QA → GTM/support profiles; Operator QA → confirmed active profiles; Content Studio QA → approved production content profiles; remaining Revenue profiles. Observe each wave for 24 hours or 20 representative tasks, whichever takes longer. One profile at a time; preserve mixed core versions.
5. **Rollback per profile:** disable the plugin hook first, restore its prior plugin/skill/config snapshot, restart only that profile if required, and rerun the baseline. Never reset the central ledger or retry uncertain remote work. Stop the wave on regression.
6. **Distribution after acceptance:** update active runtime deployment sources, then templates and packaged desktop installers. Refresh backups through their own normal backup process. Leave archives unchanged.

Before each wave, bind the intended profile to its current executable, computer, source artifact and effective skill catalog. README claims or imported directory names alone cannot authorize upgrading a runtime. This proposal deliberately preserves the unresolved export-to-source links instead of assigning a guessed repository or version.
