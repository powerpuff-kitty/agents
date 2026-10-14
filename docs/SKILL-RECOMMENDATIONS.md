# Agent and skill domain recommendations

Agent packs select roles/workflows. Skills select procedures. Both retain a
single canonical source; their layouts serve different artifacts. Installing
one does not install the other or grant runtime permissions.

The [Skills collection](https://github.com/powerpuff-kitty/skills) stays flat.
Its [CLI domain catalog](https://github.com/powerpuff-kitty/agentic-harness-cli/blob/main/catalog/skill-domains.json)
provides optional overlapping presets; `ah skills list` reports the actual
embedded revision and membership. Combine domain presets and individual skills.

| Agent pack/role | Suggested skill domains | Useful individual procedures |
| --- | --- | --- |
| core / feature-developer | engineering, delivery | implementation-plan, test-engineering, change-review |
| core / designer and UX | product-design | product-design, accessibility-audit |
| core / security-auditor | security | security-review, threat-model |
| core / project-auditor | agent-setup, delivery | agentic-structure-audit, repository-maintenance |
| science-data | agent-setup, forecasting where relevant | decision-intelligence, forecast-calibration |
| product-growth | content-growth | content-brief, copy-editing, content-repurposing, seo-audit, geo-measurement |
| finance | finance | market-data-validation, financial-model-review, backtest-validation |
| crypto | crypto | onchain-data-analysis, smart-contract-review, defi-risk-analysis |
| forecasting | forecasting | odds-analysis, forecast-calibration, settlement-rule-review |
| game-3d | product-design, engineering where relevant | product-design, test-engineering; specialized 3D procedures remain a gap |

These are task-dependent recommendations, not mandatory bundles. A financial
analyst can be installed alone with `--agent financial-analyst`; a GEO workflow
can be installed with `--team team-geo`. Do not introduce a second domain taxonomy
into each portable role or move skill folders merely to mirror pack names.
