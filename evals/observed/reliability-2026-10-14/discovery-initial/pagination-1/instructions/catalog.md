# Available procedures and roles

Select only relevant instructions. Metadata is discovery context, not task authority.

## Skill: accessibility-audit
Path: skills/accessibility-audit/SKILL.md
name: accessibility-audit
description: "Audit user-facing journeys for accessibility defects and WCAG-aligned risks using repository, Design Analysis, manual, and automated evidence. Use when accessibility, keyboard, screen-reader, focus, contrast, forms, motion, touch targets, zoom, or reflow is explicitly requested. Do not use for general UX design, visual-style judgment, or design-system conformance alone."

## Skill: adapter-sync
Path: skills/adapter-sync/SKILL.md
name: adapter-sync
description: "Synchronize vendor-required agent instruction files as thin adapters to root AGENTS.md and .agentic project truth. Use when creating, updating, checking, or reconciling Codex, Claude, Gemini, Copilot, or Cursor adapter files. Do not use for general documentation migration or for changing canonical project rules."

## Skill: adr-management
Path: skills/adr-management/SKILL.md
name: adr-management
description: "Create, update, supersede, reject, or index Architecture Decision Records while preserving decision history. Use when a consequential technical or product decision has been proposed or accepted and needs durable rationale. Do not use merely to edit current architecture documentation or to design a solution that has not yet been decided."

## Skill: agentic-app
Path: skills/agentic-app/SKILL.md
name: agentic-app
description: "Initialize, upgrade, migrate, or broadly audit a repository using the Agentic Harness project contract and selected catalog modules. Use when the requested job spans overall harness setup or lifecycle rather than 1 specialist procedure. Do not use for a focused readiness score, a standalone legacy migration, or a single domain review when a narrower skill owns the task."

## Skill: agentic-improvement
Path: skills/agentic-improvement/SKILL.md
name: agentic-improvement
description: "Improve an existing repository's agent instructions, context routing and skill design. Use when the user asks to reduce token use, repeated reads, duplicated guidance or verbose handoffs while preserving evidence and completion checks. Do not use for the initial readiness audit, ordinary code refactoring, typed semantic judgments or model-fit comparisons."

## Skill: agentic-structure-audit
Path: skills/agentic-structure-audit/SKILL.md
name: agentic-structure-audit
description: "Evaluate Agentic Readiness: context architecture, AGENTS.md quality, skill routing, completion/autonomy, verification, portability, instruction health, decision history, and agent security. Use when the user asks how agent-ready a repository is or requests a model compatibility score. Do not use for broad code-quality auditing or for applying fixes."

## Skill: api-design
Path: skills/api-design/SKILL.md
name: api-design
description: "Design or review external or internal API contracts including resources, operations, errors, pagination, versioning, idempotency, authentication boundaries, and compatibility. Use when an API surface or contract is the requested design artifact. Do not use primarily for database schema design, implementation debugging, or broad codebase review."

## Skill: backtest-validation
Path: skills/backtest-validation/SKILL.md
name: backtest-validation
description: "Review or reproduce a historical trading-strategy backtest for temporal leakage, universe bias, fill assumptions, costs and out-of-sample validity. Use when assessing simulated performance or research robustness. Do not use for live execution, portfolio rebalancing, betting-model validation or guaranteed-return claims."

## Skill: change-review
Path: skills/change-review/SKILL.md
name: change-review
description: "Review a specified diff, branch, PR or pending change against accepted requirements for defects, regressions and compatibility. Use for focused code review and review-feedback verification. Do not use for whole-repository audits, lint-only cleanup, or release readiness; review does not authorize fixes, approval or merge."

## Skill: ci-triage
Path: skills/ci-triage/SKILL.md
name: ci-triage
description: "Investigate failing or stuck CI checks and implement authorized fixes using exact run, job and source evidence. Use for pipeline failures, runner/environment differences, permissions and flaky CI diagnosis. Do not use for routine application debugging, incident retrospectives, or deploying and publishing releases."

## Skill: code-quality
Path: skills/code-quality/SKILL.md
name: code-quality
description: "Inspect and improve repository formatting, linting, type-safety, complexity, duplication, dead-code and convention drift from deterministic tool/config evidence. Use when the request is specifically about code readability/maintainability quality gates or fixing their findings. Do not use for broad repository health audits, architecture-only reviews, security reviews, or performance profiling."

## Skill: codebase-audit
Path: skills/codebase-audit/SKILL.md
name: codebase-audit
description: "Perform a broad evidence-backed technical audit of code quality, maintainability, architecture, tests, dependencies, documentation, operations, performance posture, and security signals. Use when the user asks for an overall repository/codebase audit. Do not use when the requested score is specifically Agentic Readiness or when a single specialist review is sufficient."

## Skill: competitive-research
Path: skills/competitive-research/SKILL.md
name: competitive-research
description: "Research current competitors, alternatives, positioning, capabilities, pricing, and market gaps using cited external evidence. Use when the user asks for competitive landscape research or evidence-backed comparison. Do not use merely to write marketing copy or to design product flows without external market research."

## Skill: competitor-monitoring
Path: skills/competitor-monitoring/SKILL.md
name: competitor-monitoring
description: "Maintain an approved competitor watchlist, dated evidence baselines and material-change reports across pricing, features, releases and positioning. Use for repeat-run comparison and monitoring handoffs; use competitive-research for an initial landscape. This skill does not supply a scheduler or authorize notifications."

## Skill: component-resolution
Path: skills/component-resolution/SKILL.md
name: component-resolution
description: "Resolve an implementation component need against approved project primitives, internal registries, and compatible external UI component providers, then produce a safe adaptation/import plan. Use when the user asks which component/library to use, wants to reuse Spectrum/shadcn-style source, or needs to avoid inventing a duplicate primitive. Do not use to define the visual identity, browse inspiration without implementation intent, or silently install incompatible provider code."

## Skill: content-brief
Path: skills/content-brief/SKILL.md
name: content-brief
description: "Create an actionable editorial brief from audience needs, approved product facts and cited research. Use before commissioning articles, newsletters or campaign content; do not use for drafting an entire asset or inventing keyword demand."

## Skill: content-repurposing
Path: skills/content-repurposing/SKILL.md
name: content-repurposing
description: "Adapt an approved source into channel-specific content while retaining evidence, attribution and meaning. Use for article-to-newsletter, social, script or related derivatives; do not treat adaptation as publication or invent source facts."

## Skill: copy-editing
Path: skills/copy-editing/SKILL.md
name: copy-editing
description: "Edit an existing draft for argument, clarity, voice, factual support and channel fit while preserving the author\u2019s intent. Use for substantive or line editing; do not invent product claims or replace a requested proofread with a new campaign."

## Skill: database-design
Path: skills/database-design/SKILL.md
name: database-design
description: "Design or review persistent data models, relational schemas, constraints, indexes, transactions, migrations, retention, and data-access boundaries. Use when the requested artifact is a database/data-model design or schema evolution. Do not use primarily for API contract design, dependency upgrades, or generic backend implementation."

## Skill: decision-intelligence
Path: skills/decision-intelligence/SKILL.md
name: decision-intelligence
description: "Design or review bounded semantic decisions with explicit evidence, finite outcomes and abstention. Use when a task asks for evidence-support judgments, typed task classification or Jev decision guidance. Do not use for open-ended generation, ordinary code review, deterministic parsing, model-fit ranking or action authorisation."

## Skill: defi-risk-analysis
Path: skills/defi-risk-analysis/SKILL.md
name: defi-risk-analysis
description: "Analyze a specified DeFi protocol or position for collateral, liquidation, oracle, liquidity, governance and dependency risk. Use for lending, AMM and protocol-exposure scenarios with explicit snapshots and assumptions. Do not use to execute swaps, farm yield or certify a protocol as safe."

## Skill: dependency-upgrade
Path: skills/dependency-upgrade/SKILL.md
name: dependency-upgrade
description: "Plan and execute safe package, framework, runtime, or toolchain dependency upgrades with changelog review and compatibility verification. Use when the main task is changing dependency versions or adapting to their breaking changes. Do not use for Agentic Harness filesystem migration, ordinary release packaging, or unrelated refactoring."

## Skill: design-analysis
Path: skills/design-analysis/SKILL.md
name: design-analysis
description: "Interpret measured design evidence and structured analysis artifacts, classify conclusions by confidence and evidence type, and reconcile external analysis proposals with approved project truth. Use when the user asks what an existing interface's measured colors, type, spacing, components, motion, responsive behavior, or design drift mean. Do not use to invent a new visual identity, design a user journey, or perform the deterministic measurement itself when tooling can do it."

## Skill: design-extraction
Path: skills/design-extraction/SKILL.md
name: design-extraction
description: "Extract an evidence-backed design profile, taste index and candidate design-system report from a website, app, screenshots, design files or UI source. Use for capturing an existing interface's visual language and reusable patterns. Do not use to invent brand identity, infer hidden behavior from screenshots, or implement a clone."

## Skill: design-intelligence
Path: skills/design-intelligence/SKILL.md
name: design-intelligence
description: "Orchestrate the repository-native Analyze → Preserve → Compile → Verify design lifecycle across canonical Design Analysis, Design Genome, Design Task, and drift artifacts. Use when a request spans multiple design-intelligence stages or asks to make an existing product reproducible for AI implementation. Do not use for one isolated UX flow, a standalone design-system definition, or a narrow compliance/accessibility audit."

## Skill: design-research
Path: skills/design-research/SKILL.md
name: design-research
description: "Research visual references, UI patterns, interaction patterns, product flows, design critiques, and interface datasets to inform a specific design/product question. Use when the user asks how other interfaces solve a problem, wants examples from UI/UX libraries, or needs evidence before choosing a design direction. Do not use for general competitor/business research, direct component installation, or to turn reference prevalence into project requirements."

## Skill: design-system
Path: skills/design-system/SKILL.md
name: design-system
description: "Create or evolve the reusable UI system: tokens, semantic roles, component contracts, variants, states, layouts, patterns, accessibility expectations, and adoption rules. Use when the user asks to define or substantially extend shared interface primitives used across product surfaces. Do not use to discover the brand/art direction, research external UI references, select an external component provider, or merely audit conformance to an existing system."

## Skill: design-system-compliance
Path: skills/design-system-compliance/SKILL.md
name: design-system-compliance
description: "Audit product implementation against an accepted design system for token bypasses, duplicate primitives, raw controls, invalid variants, missing required component behavior, and documented exceptions. Use when structural conformance to established project design rules is the goal. Do not use to create or revise the design system, infer brand identity, or conduct a full accessibility audit."

## Skill: documentation
Path: skills/documentation/SKILL.md
name: documentation
description: "Create or update durable project documentation so current product, architecture, security, design, operational, API, data, or testing truth matches accepted changes. Use when documentation is itself the requested deliverable or must be synchronized after approved work. Do not use to invent decisions, create ADRs, or produce a temporary implementation plan."

## Skill: financial-model-review
Path: skills/financial-model-review/SKILL.md
name: financial-model-review
description: "Review a financial statement, forecast, valuation or portfolio-risk model for source integrity, accounting reconciliation, formula logic and assumption sensitivity. Use for spreadsheet/model assurance and financial calculations. Do not use for market-data cleanup, trading backtest validation, tax certification or transaction execution."

## Skill: forecast-calibration
Path: skills/forecast-calibration/SKILL.md
name: forecast-calibration
description: "Evaluate recorded probabilistic forecasts against defined outcomes using proper scores, calibration diagnostics and out-of-sample checks. Use for event, risk and prediction-model evaluation. Do not use to invent forecasts, treat unresolved outcomes as losses or claim betting profitability from a score."

## Skill: geo-measurement
Path: skills/geo-measurement/SKILL.md
name: geo-measurement
description: "Measure observed brand mentions, citations and factual representation in AI answers using a reproducible prompt panel and retained responses. Use for GEO baselines or repeat measurements; do not infer visibility from crawler eligibility or promise placement."

## Skill: identity-design
Path: skills/identity-design/SKILL.md
name: identity-design
description: "Define or deliberately evolve a product's brand-facing visual identity and art direction: personality, differentiation, typography character, palette direction, imagery, geometry, density, composition, motion, voice, and intentional anti-patterns. Use when the user asks what the product should look or feel like, wants distinct visual directions, or needs identity continuity across surfaces. Do not use to engineer the reusable component/token system, design a product flow, or audit implementation compliance."

## Skill: implementation-plan
Path: skills/implementation-plan/SKILL.md
name: implementation-plan
description: "Turn accepted product or architecture scope into an executable, dependency-aware implementation plan with milestones, verification, risks, and rollback points. Use when the user asks how to implement approved work before or alongside coding. Do not use to decide unresolved architecture/product direction or to maintain general documentation after implementation."

## Skill: incident-review
Path: skills/incident-review/SKILL.md
name: incident-review
description: "Conduct a blameless post-incident review from timelines, logs, alerts, deployments, impact, response actions, and recovery evidence. Use after a reliability, security, or operational incident to establish contributing factors and corrective actions. Do not use for a proactive threat model, standalone performance benchmark, or general code review."

## Skill: market-data-validation
Path: skills/market-data-validation/SKILL.md
name: market-data-validation
description: "Validate financial market datasets for point-in-time research, backtests and portfolio analysis. Use for timestamp/availability checks, corporate actions, instrument identity, missing sessions and price/return provenance. Do not use for price predictions, trade execution or general non-market data cleaning."

## Skill: market-opportunity-research
Path: skills/market-opportunity-research/SKILL.md
name: market-opportunity-research
description: "Assess market segments, customer problems, substitutes, willingness-to-pay evidence and bottom-up opportunity ranges with dated sources and explicit overlap/assumptions. Use for market/customer opportunity validation and sizing; use competitive-research for competitor positioning and finance skills for securities or trading analysis."

## Skill: marketing
Path: skills/marketing/SKILL.md
name: marketing
description: "Create positioning, messaging, launch copy, value propositions, audience narratives, or marketing content from approved product facts and evidence. Use when the user wants communication or go-to-market material. Do not use to conduct primary competitive research, decide product requirements, or invent unsupported performance/customer claims."

## Skill: migration
Path: skills/migration/SKILL.md
name: migration
description: "Migrate legacy Agentic Harness repository layouts or canonical-context locations to the current root AGENTS.md plus .agentic contract with conflict detection, backup, and idempotence. Use when filesystem/project-contract migration is the primary task. Do not use for dependency upgrades, database migrations, or fresh project initialization."

## Skill: model-fit
Path: skills/model-fit/SKILL.md
name: model-fit
description: "Compare supported evidence-backed coding-agent model profiles for a specific repository or task, including current and post-improvement compatibility. Use when the user asks which model best fits the project/task or how model guidance differs. Do not use to score general Agentic Readiness or to invent rankings for models absent from the canonical registry."

## Skill: native-app-delivery
Path: skills/native-app-delivery/SKILL.md
name: native-app-delivery
description: "Implement and verify scoped iOS/Android app changes across lifecycle, durable state, offline behavior, permissions, deep links, adaptive UI and release preparation. Use for native/mobile delivery including cross-platform shells; do not treat responsive web or a simulator-only pass as real-device/store verification."

## Skill: odds-analysis
Path: skills/odds-analysis/SKILL.md
name: odds-analysis
description: "Analyze betting or event-market quotes, implied probabilities, overround and fee-adjusted hypothetical payoffs. Use for odds-format conversion and consistent market comparison. Do not use for placing bets, choosing personal stakes or treating quoted prices as calibrated true probabilities."

## Skill: onchain-data-analysis
Path: skills/onchain-data-analysis/SKILL.md
name: onchain-data-analysis
description: "Analyze approved blockchain records for balances, transfers, activity and protocol metrics with explicit chain, block, finality and token-unit provenance. Use for onchain dataset/query analysis; use a contract-security review for exploitability and a DeFi-risk review for economic scenarios."

## Skill: performance-audit
Path: skills/performance-audit/SKILL.md
name: performance-audit
description: "Measure performance bottlenecks and scoped reliability/recovery claims in application, API, database, build, or runtime paths using profiling, tracing, benchmarks, metrics, and repository evidence. Use when latency, throughput, resource use, query cost, bundle/build speed, performance regressions, availability indicators or recovery measurements are requested. Use incident-review for retrospective incident analysis."

## Skill: product-analytics
Path: skills/product-analytics/SKILL.md
name: product-analytics
description: "Analyze approved product events, funnels, cohorts, retention and segments with explicit identity, windows, denominators and reproducible transformations. Use for descriptive product measurement; use product-instrumentation for collection contracts and product-experimentation for causal treatment claims."

## Skill: product-design
Path: skills/product-design/SKILL.md
name: product-design
description: "Design a feature's user journey, information hierarchy, interaction states, requirements, edge cases, recovery, and usability behavior from accepted product goals. Use when the requested output is UX/product interaction design for a screen, workflow, or end-to-end journey. Do not use to define brand/art direction, construct the shared token/component system, research reference libraries as the primary task, or turn competitor features into requirements."

## Skill: product-experimentation
Path: skills/product-experimentation/SKILL.md
name: product-experimentation
description: "Design and assess product experiments with explicit randomization/exposure units, metrics, guardrails, stopping rules and trustworthy readouts. Use for A/B and controlled product tests; do not treat observational before/after analytics or a backtest as randomized causal evidence."

## Skill: product-instrumentation
Path: skills/product-instrumentation/SKILL.md
name: product-instrumentation
description: "Design, implement or review product tracking plans, event contracts, identity semantics and event-payload QA for an authorized measurement question. Use for instrumentation and analytics data quality; use product-analytics for interpreting funnels/cohorts and product-experimentation for causal tests."

## Skill: release
Path: skills/release/SKILL.md
name: release
description: "Prepare and execute an approved software or package release: versioning, changelog, tests, artifacts, checksums, tagging, publishing, rollout, and rollback verification. Use when the user explicitly wants to create or publish a release. Do not use merely to review release readiness or to upgrade dependencies without releasing."

## Skill: release-review
Path: skills/release-review/SKILL.md
name: release-review
description: "Review a release candidate against documented quality, security, migration, compatibility, documentation, artifact, and operational gates and return a go/no-go assessment. Use before publication when release readiness is the requested decision. Do not use to publish the release itself or for a general repository audit unrelated to a candidate."

## Skill: repository-maintenance
Path: skills/repository-maintenance/SKILL.md
name: repository-maintenance
description: "Reconcile repository issues, PRs and branches against current source and acceptance evidence; apply explicitly authorized tracker or branch cleanup. Use for stale backlog and merged-branch maintenance. Do not use for product-roadmap invention, general code cleanup, releases or Git history rewriting."

## Skill: security-review
Path: skills/security-review/SKILL.md
name: security-review
description: "Review an existing implementation or change for security weaknesses in authentication, authorization, tenancy, inputs/outputs, secrets, cryptography, privacy, dependencies, CI/release, logging, recovery, and abuse resistance. Use when a concrete security review or secure-by-default code assessment is requested. Do not use primarily for pre-implementation threat modeling or broad non-security code review."

## Skill: seo-audit
Path: skills/seo-audit/SKILL.md
name: seo-audit
description: "Audit public websites and web applications for technical SEO, AEO/GEO retrieval readiness, crawlability, indexability, rendering, canonical URLs, hreflang, sitemaps, structured data, internal-link discoverability, and programmatic-page quality. Use when search visibility, indexing, crawler access, AI-search discovery, or SSR/prerender-for-SEO is explicitly requested. Do not use for general marketing copy/keyword strategy, broad codebase health, or performance profiling alone."

## Skill: settlement-rule-review
Path: skills/settlement-rule-review/SKILL.md
name: settlement-rule-review
description: "Review an event or prediction-market settlement contract for outcome definitions, deadlines, authoritative sources, void/refund and dispute conditions. Use for comparing supplied betting/prediction-market terms and outcome evidence. Do not use to place bets, submit resolutions or certify legal eligibility."

## Skill: smart-contract-review
Path: skills/smart-contract-review/SKILL.md
name: smart-contract-review
description: "Review a scoped EVM/Solidity contract implementation or change for reachable security weaknesses, privileged controls and upgrade/accounting risks. Use for source-grounded contract assessment; do not infer a deployed exploit from unmatched source or perform live exploitation."

## Skill: systematic-debugging
Path: skills/systematic-debugging/SKILL.md
name: systematic-debugging
description: "Reproduce and diagnose a specific software defect, failing test or unexpected behavior, then implement and verify an authorized fix. Use for root-cause investigation and regressions. Do not use for broad codebase audits, incident retrospectives, or CI infrastructure failures without an application defect."

## Skill: test-engineering
Path: skills/test-engineering/SKILL.md
name: test-engineering
description: "Design, add or improve meaningful unit, integration and end-to-end tests for accepted software behavior; diagnose flaky or misleading tests. Use for test strategy, regression coverage and test-first development when requested. Do not use for broad quality scoring, accessibility-only audits, or CI runner and permission diagnosis."

## Skill: threat-model
Path: skills/threat-model/SKILL.md
name: threat-model
description: "Create or update a threat model for a proposed system, feature, integration, data flow, or architecture by mapping assets, actors, trust boundaries, attack paths, abuse cases, controls, and residual risk. Use before or during design when security threats must shape architecture. Do not use primarily to audit already-implemented code for vulnerabilities."

## Skill: user-research
Path: skills/user-research/SKILL.md
name: user-research
description: "Plan and synthesize participant-based product research: questions, recruitment/consent, interviews or task studies, coding, contradictions and decision handoffs. Use for customer/user discovery and study evidence; use design-research for external interface references and market-opportunity-research for market sizing."

## Role: accessibility-specialist
Path: roles/accessibility-specialist/instructions.md
Review user journeys for accessibility through semantics, keyboard/focus, screen-reader behavior, forms/errors, contrast, targets, motion, zoom/reflow, and actual assistive-technology evidence. Apply the declared standard with criterion-specific exceptions; use designer for visual-system conformance and usability-auditor for general task friction.

## Role: artist-3d
Path: roles/artist-3d/instructions.md
Create and review scoped 3D models, materials, lighting, animation, and scene composition against an asset brief and target constraints. Use available modeling/rendering tools; otherwise provide an honest specification. Use technical-artist for runtime pipelines and shaders.

## Role: copywriter
Path: roles/copywriter/instructions.md
Write and edit product, onboarding, landing-page, email, campaign, and UX copy using approved facts, audience, and brand voice. Use for final wording; use marketing-strategist for positioning and evidence-validator for claim verification.

## Role: data-analyst
Path: roles/data-analyst/instructions.md
Explore and analyze approved datasets, metrics, funnels, cohorts, segments, and experiment results. Define denominators, inspect data quality, quantify uncertainty, and explain decision implications. Use for analysis rather than independent evidence certification or designing unrequested data infrastructure.

## Role: design-analyst
Path: roles/design-analyst/instructions.md
Extract evidence-backed design profiles, taste indexes and candidate design-system reports from websites, apps, screenshots, design files or UI source. Own capture provenance, supported token exports and report coverage; use designer for independent design review and ux-designer for new journeys.

## Role: designer
Path: roles/designer/instructions.md
Audit project visual UI and design systems against accepted goals, audience, brand, and platform conventions. Check tokens, components, contrast, spacing, typography, responsive layouts, states, and consistency. Use for visual/system review or requested improvements; use ux-designer for complete journeys, usability-auditor for independent task walkthroughs, and accessibility-specialist for deep accessibility checks.

## Role: evidence-validator
Path: roles/evidence-validator/instructions.md
Validate the provenance, reproducibility, confidence, uncertainty, and accuracy of findings, datasets, calculations, or public claims. Check independent references and false-positive/negative evidence. Use for evidence reliability; use security-auditor for exploitability and quality-engineer for general tests.

## Role: feature-developer
Path: roles/feature-developer/instructions.md
Implement, debug, or refactor scoped software changes and verify behavior. Use for hands-on code work, including approved audit remediation. Follow project contracts and preserve existing edits. For independent reviews, release work, visual audits, or deep profiling, use the corresponding specialist.

## Role: financial-analyst
Path: roles/financial-analyst/instructions.md
Analyze approved financial statements, budgets, forecasts and valuation models with reconciled sources, periods, currencies and assumptions. Use for financial reporting/model analysis; use quant-researcher for trading-strategy evidence and portfolio-risk-analyst for holdings/exposure risk. Analysis does not authorize transactions or establish accounting certification.

## Role: game-designer
Path: roles/game-designer/instructions.md
Design and review mechanics, progression, economies, balance, difficulty, feedback, and player experience against project goals. Use for game systems and playtest hypotheses; use designer for interface systems and developer for implementation.

## Role: geo-specialist
Path: roles/geo-specialist/instructions.md
Assess generative-engine and AI-answer visibility: observed brand mentions, supporting citations, factual representation, discoverability, and reproducible measurement. Use for evidence-backed AI visibility, not guaranteed inclusion or fabricated share-of-voice metrics.

## Role: gtm-strategist
Path: roles/gtm-strategist/instructions.md
Plan go-to-market sequencing, distribution, acquisition, sales motion, pricing hypotheses, launch dependencies, and measurable readiness. Use for bringing an approved product to market; use marketing-strategist for positioning and release-engineer for software release gates.

## Role: iteration-reviewer
Path: roles/iteration-reviewer/instructions.md
Assess whether each integrated product increment meets its accepted Definition of Done and remains releasable for a named target. Reconcile requirement, regression, artifact/startup, UX/accessibility, security, compatibility, documentation, and recovery evidence into ready, blocked, or unverified. Use for iteration/feature closure; use release-engineer for artifact operations and authorized publication.

## Role: localization-specialist
Path: roles/localization-specialist/instructions.md
Adapt language, terminology, formats, cultural context, and UI behavior for specified locales. Check message completeness, pluralization, directionality, layout, and meaning. Use for localization rather than inventing product facts or certifying legal translations.

## Role: marketing-strategist
Path: roles/marketing-strategist/instructions.md
Define evidence-backed audiences, positioning, value propositions, differentiation, messaging, and campaign strategy from approved product facts. Use for marketing direction; use copywriter for wording and gtm-strategist for launch/distribution execution plans.

## Role: mathematician
Path: roles/mathematician/instructions.md
Develop and review mathematical models, derivations, algorithms, proofs, units, numerical conditioning, stability, and error bounds. Use for mathematical correctness and formulation; use scientist for empirical validity and feature-developer for ordinary implementation.

## Role: onchain-analyst
Path: roles/onchain-analyst/instructions.md
Analyze approved blockchain records, token/protocol activity and DeFi exposure with explicit chain/block/finality, units and economic assumptions. Use for onchain research; use security-auditor for contract exploitability and probability-analyst for event-market odds/calibration. No wallet or transaction runtime is provided.

## Role: performance-engineer
Path: roles/performance-engineer/instructions.md
Measure and diagnose latency, CPU, memory, throughput, query, bundle, startup, or build regressions using representative workloads and profiling. Optimize only when requested and verify comparable before/after results. Use for deep performance work rather than general quality scores or speculative tuning.

## Role: portfolio-risk-analyst
Path: roles/portfolio-risk-analyst/instructions.md
Analyze approved portfolio holdings, exposures, concentration, liquidity and stress scenarios with explicit valuation, instrument and model assumptions. Use for portfolio risk and limits review; use quant-researcher for strategy backtests and financial-analyst for company statements/valuation. Risk analysis does not rebalance or transact.

## Role: probability-analyst
Path: roles/probability-analyst/instructions.md
Analyze recorded event forecasts, betting/prediction-market odds and settlement definitions with proper scoring, calibration, fees and uncertainty. Use for probabilistic evaluation and conditional payoff research; use quant-researcher for financial trading backtests. Analysis does not place bets or establish profitable predictions.

## Role: product-manager
Path: roles/product-manager/instructions.md
Translate accepted goals and user evidence into scoped requirements, priorities, acceptance criteria, success measures, and delivery trade-offs. Use for product definition and prioritization; use designer for interaction details and gtm-strategist for launch/distribution.

## Role: project-auditor
Path: roles/project-auditor/instructions.md
Assess project progress and readiness against accepted requirements using repository and tracker evidence. Identify verified, partial, and unverified work, blockers, and prioritized next steps. Default to reporting; update issues or boards only when that external action is explicitly authorized.

## Role: quality-engineer
Path: roles/quality-engineer/instructions.md
Review correctness, test quality, robustness, maintainability, and verification evidence for a requested scope. Audit by default; fix identified gaps only when requested. Benchmark or rate when relevant to the task. Use performance-engineer for deep profiling and release-engineer for release/deployment gates.

## Role: quant-researcher
Path: roles/quant-researcher/instructions.md
Design and evaluate financial trading-strategy research using point-in-time data, reproducible backtests, realistic costs and out-of-sample evidence. Use for quantitative strategy/model evaluation; use financial-analyst for statements/valuation and portfolio-risk-analyst for current holdings risk. Research does not authorize live execution or imply profitable returns.

## Role: release-engineer
Path: roles/release-engineer/instructions.md
Prepare or review software/package releases with version, source, artifact, consumer compatibility, deployment, and rollback evidence. Execute tags, publication, or rollout only when authorized for the target. Use for release readiness and delivery; use quality-engineer for general code/test review.

## Role: researcher
Path: roles/researcher/instructions.md
Research technical, product, market, or data questions using project context and current primary sources. Compare options against explicit criteria, cite material claims, distinguish evidence from inference, and report uncertainties. Use for source gathering and decision research; pair with evidence-validator for independent claim checks.

## Role: scientist
Path: roles/scientist/instructions.md
Design and assess empirical experiments: hypotheses, controls, sampling, measurement, uncertainty, reproducibility, and interpretation. Use for testing causal or empirical claims; use researcher for literature gathering, mathematician for derivations, and evidence-validator for independent claim verification.

## Role: security-auditor
Path: roles/security-auditor/instructions.md
Audit scoped code, configuration, dependencies, or trust boundaries for reachable security weaknesses. Assess exploitability, impact, and remediation with source or isolated validation evidence. Use for implementation security review; build a full threat model only when the task calls for one.

## Role: seo-specialist
Path: roles/seo-specialist/instructions.md
Audit search crawlability, indexing, site structure, search intent, content, structured data, and measured search performance. Prioritize evidence-backed improvements; use geo-specialist for AI-answer visibility and performance-engineer for deep runtime profiling.

## Role: system-architect
Path: roles/system-architect/instructions.md
Design, review, compare, or revise software architecture against accepted requirements, constraints, and quality attributes. Explain boundaries, ownership, failure modes, and consequential trade-offs. Use for structural decisions rather than visual design, routine implementation, or operational release execution.

## Role: team-lead
Path: roles/team-lead/instructions.md
Coordinate an explicitly requested team workflow. Select applicable specialists, provide bounded briefs, schedule independent reviews, serialize source edits, reconcile evidence, and deliver one verified result. Use for team presets or multi-specialist tasks rather than replacing domain specialists.

## Role: technical-artist
Path: roles/technical-artist/instructions.md
Integrate visual assets through shaders, materials, rendering, animation/asset pipelines, and engine constraints. Check color spaces, coordinate conventions, compatibility, and measured budgets. Use for art-to-runtime integration, not general asset authorship or speculative performance tuning.

## Role: usability-auditor
Path: roles/usability-auditor/instructions.md
Independently assess task usability through cognitive walkthroughs, heuristic review, and actual interaction evidence. Find confusing steps, unclear controls, dead ends, unnecessary effort, context loss, and recovery failures. Distinguish expert risks from observed user-study outcomes; use ux-designer for redesign.

## Role: user-researcher
Path: roles/user-researcher/instructions.md
Plan and synthesize interviews, usability studies, and user feedback against explicit questions. Distinguish observed behavior from assumptions, inspect sampling/bias, and protect participant privacy. Use for empirical user evidence rather than invented personas or general UI design.

## Role: ux-designer
Path: roles/ux-designer/instructions.md
Design and review complete user journeys, task sequences, navigation, information hierarchy, mental models, progressive disclosure, continuity, and recovery. Use for coherent product flows; use designer for visual/design-system alignment, usability-auditor for independent walkthroughs, and user-researcher for observed user evidence.
