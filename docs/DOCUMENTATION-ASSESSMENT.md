# Documentation assessment and recommended standard

Assessment date: 2026-10-14. Scope: 38 skill entrypoints and their reference-file
inventory, 29 agent identities/instruction structures, existing catalogs,
installation guides and selected security/creative/engineering output contracts.
This is a source/documentation assessment, not an observed model-behavior or
professional-domain certification. Recommendations below are not implemented
examples or newly accepted quality gates.

## Recommendation

Every skill and agent needs precise, usable documentation. A long handbook for
every entry would add duplication and context cost. Use a concise entrypoint,
then add detailed references where the workflow, tools, stakes or evidence require
them. The [Agent Skills specification](https://agentskills.io/specification)
recommends progressive disclosure: short discovery metadata, focused instructions
and resources loaded as needed. It recommends keeping SKILL.md below 500 lines.
[Anthropic's explanation](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
also treats skills as composable, task-specific onboarding material.

Original assessment source evidence: all 38 skills contain Objective, Inputs, Context,
Procedure, Output and Completion sections. Their entrypoints are 34–59 lines;
22 have Markdown reference guides. All 29 roles have identity/description and
instruction sources. A missing references directory is not automatically a defect:
small procedures may already be adequately documented inline. File/heading counts
do not measure instruction effectiveness or completeness.

## Recommended documentation tiers

| Tier | Applies to | Required useful detail |
| --- | --- | --- |
| Baseline | Every skill and agent | Purpose, trigger and exclusions, required inputs, responsibility/procedure, deliverable, evidence/completion criteria, dependencies/tool assumptions, permission limits and relevant handoffs. One small invocation/output illustration when ambiguity warrants it. |
| Workflow | Multi-stage or tool-dependent tasks | A representative input/output, artifact schema/template, failure/uncertainty handling, tool/version examples, recovery and a repeatable check. Load detailed material on demand. |
| Specialist | Security, cryptography, finance, hardware, aviation and comparable consequential work | Dated authoritative references, scope/units/assumptions, exact tool/data provenance, realistic negative cases, validation limits and domain review. Keep simulated, tested, deployed and certified states separate. |

For a skill, SKILL.md owns routing and procedure. Put substantial examples,
stack-specific guidance and report templates in that skill's local references or
assets, linked from the entrypoint. Keep executable helpers and their dependencies
explicit. A second README is optional only when it serves a different audience;
do not duplicate SKILL.md by default.

For an agent, agent.json owns discovery identity and instructions.md owns role
responsibility, method selection, handoffs and completion. Keep reusable detailed
procedures in Skills. Explain adjacent-role boundaries in the catalog and use
existing team docs for coordination examples. Do not add a handbook or a new role
merely to repeat a skill.

Document validation in four separate states: source checks, isolated helper tests,
actual host loading and observed task/model outcomes. The original snapshot included
100 agent acceptance specifications, not 100 observed successes. OpenCode skill
loading remains unverified in the isolated v2.0.27 probe described in
[SKILLS.md](SKILLS.md#local-verification-boundary).

## Skill-by-skill assessment

The guide column counts Markdown files directly in references/, not all supporting
assets, helper tests or deeper resources. The last column identifies the next useful
example/reference to review or add; it does not assert that every subject is absent
from all existing resources. Prioritize actual ambiguity and user failures.

| Skill | Reference guides | Recommended next documentation |
| --- | --- | --- |
| [accessibility-audit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/accessibility-audit/SKILL.md) | 1 | Add a keyboard/focus finding and manual-versus-automated coverage example; extend the existing guide. |
| [adapter-sync](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/adapter-sync/SKILL.md) | 6 | Keep host-specific references current; add a conflict/idempotence example without duplicating templates. |
| [adr-management](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/adr-management/SKILL.md) | 0 | A short supersession/index example is sufficient; no separate handbook needed. |
| [agentic-app](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/agentic-app/SKILL.md) | 2 | Document a minimal install and a conflict recovery using the existing guides. |
| [agentic-improvement](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/agentic-improvement/SKILL.md) | 8 | Retain measured evidence-reuse examples; consolidate before adding more reference pages. |
| [agentic-structure-audit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/agentic-structure-audit/SKILL.md) | 0 | Priority: expose the authoritative scoring rubric, one evidence-backed report and unknown/partial-coverage treatment. |
| [api-design](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/api-design/SKILL.md) | 0 | Add one request/error/idempotency contract and a backward-compatibility example. |
| [change-review](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/change-review/SKILL.md) | 1 | Add one grounded finding and one refuted suspicion to the existing method guide. |
| [ci-triage](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/ci-triage/SKILL.md) | 1 | Add a run/attempt evidence example distinguishing failed tests, access blockers and pending checks. |
| [code-quality](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/code-quality/SKILL.md) | 1 | Keep native diagnostic/accepted-rule examples current; avoid another generic checklist. |
| [codebase-audit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/codebase-audit/SKILL.md) | 3 | Use the existing report template; add a sampled-flow/coverage-limit example. |
| [competitive-research](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/competitive-research/SKILL.md) | 0 | Add a dated comparison example that separates supply, adoption proxies and validated demand. |
| [component-resolution](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/component-resolution/SKILL.md) | 1 | Add a provider compatibility/license decision and a rejected candidate. |
| [database-design](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/database-design/SKILL.md) | 0 | Priority: add a schema invariant, migration/backfill and rollback/verification example. |
| [decision-intelligence](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/decision-intelligence/SKILL.md) | 3 | Keep finite outcomes, abstention and recorded-results examples distinct from provider execution. |
| [dependency-upgrade](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/dependency-upgrade/SKILL.md) | 0 | Add a versioned breaking-change source, adaptation and failed-upgrade recovery example. |
| [design-analysis](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/design-analysis/SKILL.md) | 2 | Add an evidence-to-finding example with observed/inferred/unknown classifications. |
| [design-intelligence](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/design-intelligence/SKILL.md) | 2 | Add one lifecycle/artifact handoff with explicit missing-tool fallback; reuse current references. |
| [design-research](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/design-research/SKILL.md) | 1 | Add provenance, licensing and observation-versus-requirement examples. |
| [design-system](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/design-system/SKILL.md) | 1 | Add a token/component/state contract with ownership and proof requirements. |
| [design-system-compliance](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/design-system-compliance/SKILL.md) | 3 | Use the existing report template; add accepted exception versus actual violation evidence. |
| [documentation](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/documentation/SKILL.md) | 0 | A small canonical-truth/router correction example is enough; avoid duplicating the project docs. |
| [identity-design](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/identity-design/SKILL.md) | 1 | Add an approved direction, rejected reference and constraints/rights example. |
| [implementation-plan](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/implementation-plan/SKILL.md) | 0 | Add a compact dependency/gate/rollback example; keep it separate from accepted architecture. |
| [incident-review](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/incident-review/SKILL.md) | 0 | Priority: add a redacted timeline and corrective-action template; explicitly separate retrospective from active response. |
| [marketing](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/marketing/SKILL.md) | 0 | Add a brief, channel/voice constraints, supported-claim draft and editorial acceptance example. |
| [migration](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/migration/SKILL.md) | 1 | Extend the existing guide with duplicate-source conflict and recovery evidence, not another layout description. |
| [model-fit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/model-fit/SKILL.md) | 0 | Priority: identify the authoritative registry/rubric and show insufficient-evidence handling; do not invent rankings. |
| [performance-audit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/performance-audit/SKILL.md) | 0 | Priority: add a reproducible benchmark with environment, warmup, variability and comparable before/after results. |
| [product-design](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/product-design/SKILL.md) | 1 | Add one complete flow, edge-state and acceptance-criteria example using the existing reference. |
| [release](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/release/SKILL.md) | 0 | Priority: document a versioned artifact/provenance checklist and failed-publication/recovery example. |
| [release-review](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/release-review/SKILL.md) | 0 | Priority: add a candidate-specific gate table with pending, skipped and blocking checks. |
| [repository-maintenance](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/repository-maintenance/SKILL.md) | 1 | Extend the existing guide with exact-head/squash evidence and a preserved changed branch. |
| [security-review](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/security-review/SKILL.md) | 2 | Maintain the existing review/report guides; add language/framework-specific references only for supported stacks. |
| [seo-audit](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/seo-audit/SKILL.md) | 0 | Priority: add a route-level example distinguishing source, built output, HTTP response and search-provider evidence. |
| [systematic-debugging](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/systematic-debugging/SKILL.md) | 1 | Add a minimal reproduction, rejected hypothesis and regression example to the existing guide. |
| [test-engineering](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/test-engineering/SKILL.md) | 1 | Add a behavior/risk matrix, meaningful assertion and flaky-test counterexample. |
| [threat-model](https://github.com/powerpuff-kitty/skills/blob/9bb9c319b7371627e2dbc17fc696d1ee812d5218/threat-model/SKILL.md) | 0 | Priority: add one trust-boundary diagram, threat record and mitigations/validation template. |

## Agent-by-agent assessment

All roles have source instructions and share the operating contract. The table
identifies a useful role-specific illustration or handoff to review/add, rather
than proposing 29 separate manuals. Keep authority and procedure definitions in
their current canonical sources.

| Agent | Recommended next documentation |
| --- | --- |
| [accessibility-specialist](../agents/accessibility-specialist/instructions.md) | A manual keyboard/assistive-technology evidence example and incomplete-coverage handoff. |
| [artist-3d](../agents/artist-3d/instructions.md) | A source/export manifest, render/geometry validation and explicit missing-tool fallback. |
| [copywriter](../agents/copywriter/instructions.md) | A brief-to-draft example with audience, voice, channel, claims and an editor acceptance rubric. |
| [data-analyst](../agents/data-analyst/instructions.md) | A dataset grain/quality contract, reproducible calculation and uncertainty example. |
| [designer](../agents/designer/instructions.md) | A visual/component/state artifact handoff that preserves the approved design authority. |
| [evidence-validator](../agents/evidence-validator/instructions.md) | An independent claim-check example including contrary evidence and unresolved provenance. |
| [feature-developer](../agents/feature-developer/instructions.md) | A scoped implementation handoff and optional-skill fallback; reuse development skills for methods. |
| [game-designer](../agents/game-designer/instructions.md) | A mechanics/balance hypothesis and playtest evidence; separate simulated balance from player outcomes. |
| [geo-specialist](../agents/geo-specialist/instructions.md) | A dated prompt/provider/region sample with observed citations and limits on attribution. |
| [gtm-strategist](../agents/gtm-strategist/instructions.md) | A channel/launch experiment with explicit pricing assumptions and measurable decision criteria. |
| [iteration-reviewer](../agents/iteration-reviewer/instructions.md) | A compact ready/blocked/unverified example linking the existing iteration-readiness contract. |
| [localization-specialist](../agents/localization-specialist/instructions.md) | Locale glossary, plural/format/context examples and actual linguistic/layout review boundaries. |
| [marketing-strategist](../agents/marketing-strategist/instructions.md) | Audience/positioning brief, evidence-backed claims and a testable campaign hypothesis. |
| [mathematician](../agents/mathematician/instructions.md) | Assumptions, derivation/numerical checks and a proof-versus-heuristic example. |
| [performance-engineer](../agents/performance-engineer/instructions.md) | Environment-specific measurement/handoff with uncertainty; reuse performance-audit procedure. |
| [product-manager](../agents/product-manager/instructions.md) | A requirement/non-goal/acceptance example with unresolved decisions and outcome ownership. |
| [project-auditor](../agents/project-auditor/instructions.md) | An acceptance-to-evidence status table; distinguish sampled readiness from complete verification. |
| [quality-engineer](../agents/quality-engineer/instructions.md) | A risk/behavior test matrix and independent review handoff; reuse test-engineering/change-review. |
| [release-engineer](../agents/release-engineer/instructions.md) | A candidate/artifact/provenance/recovery handoff with actual publication state. |
| [researcher](../agents/researcher/instructions.md) | A dated source comparison with contradictory evidence and an explicit stopping criterion. |
| [scientist](../agents/scientist/instructions.md) | An experiment/control/analysis example separating planned protocol from observed results. |
| [security-auditor](../agents/security-auditor/instructions.md) | Priority: one reachable finding and false-positive rebuttal; route threat design, implementation review and active response distinctly. |
| [seo-specialist](../agents/seo-specialist/instructions.md) | A URL-level evidence/handoff example separating eligibility from measured search performance. |
| [system-architect](../agents/system-architect/instructions.md) | A boundary/contract decision example with migration consequences and ADR ownership. |
| [team-lead](../agents/team-lead/instructions.md) | One end-to-end team brief, serialized writer ownership and evidence reconciliation; reuse teams docs. |
| [technical-artist](../agents/technical-artist/instructions.md) | A versioned asset/runtime integration contract with actual shader/import/render checks. |
| [usability-auditor](../agents/usability-auditor/instructions.md) | A task walkthrough finding; distinguish heuristic inspection from a participant study. |
| [user-researcher](../agents/user-researcher/instructions.md) | A consent-aware study plan, anonymized evidence and observation-versus-interpretation handoff. |
| [ux-designer](../agents/ux-designer/instructions.md) | A complete journey/state/recovery specification with acceptance and design-system dependencies. |

## Priority and verification

First improve threat-model, incident-review, release/release-review, database-design,
performance-audit and model-fit/audit rubric references where real tasks expose
ambiguity. For content expansion, a clear brief/voice/claims contract and an editor
rubric come before another general-purpose writer profile. New cryptography,
finance, hardware and aviation workflows need specialist-tier references from the
start; the [domain assessment](DOMAIN-OPPORTUNITIES.md) defines candidate artifacts.

Before adding detail, inspect the existing guide and choose a real failure or
ambiguous outcome. Add the smallest useful example or template, then exercise it
on a fixed task with a matching negative/uncertainty case. Record the source/host/
model/tool versions, input identity, actual result and limits. Link checks and
render/build freshness should pass, but cannot stand in for task-outcome evidence.
The existing [evaluation backlog](https://github.com/powerpuff-kitty/skills/issues/26)
remains the right place for reproducible routing/outcome work.

No bulk examples, new skills or agent roles were created in the original assessment.
The owner later authorized the focused finance implementation described below.

## Finance implementation follow-up

The finance milestone added three skills and three agents, bringing that snapshot
to 41 skills and 32 profiles. The original 67-entry table remains a historical baseline;
these six entries complete the current documentation inventory.

| Entry | Documentation delivered | Verification boundary |
| --- | --- | --- |
| [market-data-validation](https://github.com/powerpuff-kitty/skills/tree/main/market-data-validation) | Timing/instrument/action/universe reference, split/publication examples and report template. | Source checks and arithmetic are distinct from dataset quality and host/model outcomes. |
| [financial-model-review](https://github.com/powerpuff-kitty/skills/tree/main/financial-model-review) | Accounting/cash/valuation/risk methods, worked calculations and report template. | No accounting certification, blanket recalculation or future-value guarantee. |
| [backtest-validation](https://github.com/powerpuff-kitty/skills/tree/main/backtest-validation) | Causality/fill/ledger/selection reference, cost/compounding cases and report template. | No live execution or model-performance claim from a source check. |
| [financial-analyst](../agents/financial-analyst/instructions.md) | Role procedure, handoffs and worked examples in [FINANCE.md](FINANCE.md). | Historical records, assumptions and scenarios remain distinct. |
| [quant-researcher](../agents/quant-researcher/instructions.md) | Research validity procedure and causal/ledger examples in [FINANCE.md](FINANCE.md). | Simulations and paper/live execution have separate evidence. |
| [portfolio-risk-analyst](../agents/portfolio-risk-analyst/instructions.md) | Snapshot/exposure/stress procedure and leverage example in [FINANCE.md](FINANCE.md). | Limited scenarios and statistical estimates do not establish safety. |

These examples and references implement the specialist documentation tier without
creating duplicate per-entry handbooks. Eighteen skill cases and twelve role/team
cases are new acceptance specifications and remain not_run until evaluated.

## Crypto and forecasting implementation follow-up

The owner authorized continuation after the finance foundation. Optional
[crypto](CRYPTO.md) and [forecasting](FORECASTING.md) packs now add onchain-analyst,
probability-analyst, `/team-crypto-review` and `/team-forecast`. The current catalogs
contain 47 skills, 34 profiles, 20 workflows and seven packs. Contract-security
review remains with security-auditor. No wallet/account or execution runtime is
introduced. Other domain candidates remain recommendations.

Six new skills have local methods, worked examples, report templates and six
acceptance specifications each: onchain-data-analysis, smart-contract-review,
defi-risk-analysis, odds-analysis, forecast-calibration and settlement-rule-review.
Their guides cover identity/finality/units, source/deployment and economic controls,
quote/margin/fees, proper scores/calibration and exact settlement definitions.
The two new roles have self-contained procedures and linked pack walkthroughs.
These eight additions extend the per-entry documentation inventory to all 81
current entries (47 skills plus 34 roles). Twelve new role/team specifications
bring the canonical case count to 124; none is promoted to an observed outcome.
