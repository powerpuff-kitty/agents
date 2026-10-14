# Agent catalog

The suite contains 33 specialists and 1 coordinator. Portable identity and
procedure live in each linked source directory; generated outputs combine them
with the shared operating contract. Profiles depend on actual host tools, data,
permissions, and project instructions. See [packs](PACKS.md) for installation and
[teams](TEAMS.md) for coordinated workflows.

| Agent | Responsibility | Owning pack |
| --- | --- | --- |
| [team-lead](../agents/team-lead/instructions.md) | Select available roles, brief delegates, serialize writers, reconcile actual evidence | core |
| [feature-developer](../agents/feature-developer/instructions.md) | Implement, debug, refactor, and verify scoped software | core |
| [system-architect](../agents/system-architect/instructions.md) | Architecture, ownership, contracts, and structural trade-offs | core |
| [project-auditor](../agents/project-auditor/instructions.md) | Accepted scope, implementation status, progress, and readiness evidence | core |
| [iteration-reviewer](../agents/iteration-reviewer/instructions.md) | Integrated increment releasability against accepted Definition of Done and current snapshot evidence | core |
| [quality-engineer](../agents/quality-engineer/instructions.md) | Correctness, meaningful tests, regressions, and reliability | core |
| [security-auditor](../agents/security-auditor/instructions.md) | Reachable weaknesses, privacy, and trust boundaries | core |
| [designer](../agents/designer/instructions.md) | Visual UI, design systems, components, states, and responsive consistency | core |
| [ux-designer](../agents/ux-designer/instructions.md) | Complete journeys, task sequence, hierarchy, continuity, and recovery | core |
| [usability-auditor](../agents/usability-auditor/instructions.md) | Independent task walkthroughs, confusion, friction, and evidence-linked repairs | core |
| [accessibility-specialist](../agents/accessibility-specialist/instructions.md) | Deep semantics, keyboard/focus, assistive checks, and declared accessibility criteria | core |
| [performance-engineer](../agents/performance-engineer/instructions.md) | Measured bottlenecks, resource budgets, and comparable optimizations | core |
| [release-engineer](../agents/release-engineer/instructions.md) | Artifacts, readiness, authorized release operations, and recovery | core |
| [researcher](../agents/researcher/instructions.md) | Current cited sources and decision comparisons | core |
| [evidence-validator](../agents/evidence-validator/instructions.md) | Independent provenance, calculation, uncertainty, and claim checks | core |
| [financial-analyst](../agents/financial-analyst/instructions.md) | Reconciled statements, budgets, forecasts and valuation models | finance |
| [quant-researcher](../agents/quant-researcher/instructions.md) | Point-in-time strategy research, realistic backtests and out-of-sample evidence | finance |
| [portfolio-risk-analyst](../agents/portfolio-risk-analyst/instructions.md) | Holdings/NAV, net/gross exposures, liquidity and stress/model assumptions | finance |
| [onchain-analyst](../agents/onchain-analyst/instructions.md) | Chain/block/finality evidence, token/protocol activity and DeFi research | crypto |
| [probability-analyst](../agents/probability-analyst/instructions.md) | Recorded forecasts, odds/payoffs, proper scoring and settlement definitions | forecasting |
| [scientist](../agents/scientist/instructions.md) | Hypotheses, controls, experiments, sampling, and empirical interpretation | science-data |
| [mathematician](../agents/mathematician/instructions.md) | Models, derivations, proofs, numerical stability, and error bounds | science-data |
| [data-analyst](../agents/data-analyst/instructions.md) | Actual data quality, grain, metrics, cohorts, funnels, and interpretation | science-data |
| [product-manager](../agents/product-manager/instructions.md) | Requirements, priorities, outcomes, and acceptance criteria | product-growth |
| [user-researcher](../agents/user-researcher/instructions.md) | Actual user evidence and bounded study plans/synthesis | product-growth |
| [copywriter](../agents/copywriter/instructions.md) | Supported product, UX, campaign, and onboarding wording | product-growth |
| [marketing-strategist](../agents/marketing-strategist/instructions.md) | Audiences, positioning, messaging, and campaign hypotheses | product-growth |
| [gtm-strategist](../agents/gtm-strategist/instructions.md) | Distribution, launch sequencing, pricing hypotheses, and sales motion | product-growth |
| [seo-specialist](../agents/seo-specialist/instructions.md) | Search eligibility, intent, content, structure, and measured performance | product-growth |
| [geo-specialist](../agents/geo-specialist/instructions.md) | Observed AI-answer mentions, citations, and factual representation | product-growth |
| [localization-specialist](../agents/localization-specialist/instructions.md) | Specified locales, terminology, formats, pluralization, and international UI | product-growth |
| [game-designer](../agents/game-designer/instructions.md) | Mechanics, progression, balance, economies, and player experience | game-3d |
| [artist-3d](../agents/artist-3d/instructions.md) | Actual 3D asset creation/review or an explicit tooling fallback | game-3d |
| [technical-artist](../agents/technical-artist/instructions.md) | Shaders, rendering, import/export pipelines, and art/runtime integration | game-3d |

Researcher gathers existing knowledge; scientist designs or evaluates empirical
tests; mathematician checks formal/numerical reasoning; data-analyst interprets
actual datasets; evidence-validator independently checks completed claims. None
can certify its own work merely by adopting another role name.

Marketing-strategist owns positioning, GTM-strategist the commercial launch plan,
and copywriter the wording. SEO and GEO share discoverability and factual content
foundations while measuring different surfaces. Localization adapts approved meaning.
Artist-3d owns assets and technical-artist integration, with separate serialized
writing when both are requested. Modeling/rendering access is not provisioned by
the profile and missing tools remain explicit.

UX-designer owns the flow specification, designer visual/system alignment,
usability-auditor independent task assessment, accessibility-specialist deep access
checks, and user-researcher actual user evidence. Copywriter supports labels and
recovery wording. A heuristic walkthrough or automated scan is not a participant
study or proof of complete accessibility. Optional information-architecture and
interaction-design roles are not separate profiles in this catalog.

Iteration-reviewer reconciles the accepted Definition of Done across the integrated
increment, release-engineer supplies technical artifact/deployment evidence, and
project-auditor tracks delivered work against scope. Ready, blocked, or unverified
is target/snapshot-specific; no role turns missing required evidence into a pass.
See [iteration readiness](ITERATION-READINESS.md) for the closure contract and
project-specific CI integration boundary.

There is no generic engineer or optimizer profile. Team-lead chooses the owner
and method for the actual objective: software behavior, resource cost, game balance,
conversion, or mathematical optimization.

Financial-analyst owns financial reporting/model conclusions, quant-researcher
strategy-research validity, and portfolio-risk-analyst current holdings/exposure
and stress assumptions. They share available validation skills and use actual
independent evidence checks. These analytical profiles do not supply a broker,
wallet or gambling runtime. See [finance examples and scope](FINANCE.md).

Onchain-analyst owns chain/protocol evidence, while security-auditor assesses
contract exploitability and portfolio-risk-analyst economic exposure. Probability-
analyst owns event definitions, odds and recorded forecast evaluation. These roles
do not provide wallets, betting accounts or transaction execution. See
[crypto](CRYPTO.md) and [forecasting](FORECASTING.md) for worked methods and scope.
