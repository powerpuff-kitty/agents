# Roles and skills

An agent owns responsibility, handoffs and completion. A skill supplies a focused
task procedure. Profiles work with available native methods when a skill is absent;
installation of one collection never installs the other or grants permissions.

[Skills](https://github.com/powerpuff-kitty/skills) keeps self-contained folders at
its root. Each includes SKILL.md, a license and local resources. Its
[installation guide](https://github.com/powerpuff-kitty/skills/blob/main/INSTALL.md)
owns native discovery paths and the optional CLI lifecycle. `ah skills list`
reports the embedded revision and domain membership; source folder layout stays flat.

## Optional domain recommendations

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


These are task-dependent suggestions, not mandatory dependencies. Combine domains
and individual skills, selecting only procedures actually available to the host.
Do not fetch/install missing instructions without installation scope. A focused
procedure does not require a duplicate specialist profile or a full team.

## OpenCode

OpenCode V2 natively discovers SKILL.md folders; no skill renderer is required.
The Agents adapter renders role profiles and team commands separately. V2 uses a
path-derived skill ID; portable folders keep name and directory aligned. Preserve
normal implicit selection unless the user requests otherwise.

Avoid duplicate IDs across discovery paths. Check registered paths and instruction
bodies with a persistent server and bounded initialization polling. See
[current V2 documentation](https://opencode.ai/v2/docs/skills/) and
[retained verification](INSTALLATION-VERIFICATION.md). Registered content does not
establish model adherence or task reliability.
