# Domain opportunities and demand review

Assessment date: 2026-10-14. This is a research snapshot and proposed direction,
not an accepted implementation roadmap. It covers the current 38 Skills and 29
Agents, then considers the owner's additional creative, physical-engineering,
security and financial domains. No new roles, skills, integrations or live actions
are introduced by this document.

## What is already covered

- Cybersecurity: `security-auditor`, supported by `security-review` and
  `threat-model`. `incident-review` covers retrospectives, not active incident response.
- Copywriting/content: `copywriter`, `marketing-strategist`, `gtm-strategist`,
  `seo-specialist` and `geo-specialist`; the `marketing`, `competitive-research`
  and `seo-audit` skills provide reusable procedures. There is no dedicated
  editorial production or screenwriting skill.
- Scientific/quantitative foundations: `scientist`, `mathematician`, `data-analyst`,
  `researcher` and `evidence-validator`. These do not establish a specialist
  financial, cryptographic, electronics or aviation workflow by themselves.
- Visual/game work: `designer`, `game-designer`, `artist-3d` and `technical-artist`.
  Film direction, series continuity, physical CAD and flight simulation remain
  distinct gaps. See [the current catalog](CATALOG.md).

## Evidence and interpretation

Install counts below are the directory's reported cumulative installs, rounded at
capture time. They are proxies for attention/adoption, not unique users, paid
demand, successful outcomes or comparative quality. Repository contents demonstrate
supply and scope; they do not establish an underserved market.

| Observed signal | Evidence | What it supports |
| --- | --- | --- |
| Strong practical engineering adoption | [Skills.sh leaderboard](https://www.skills.sh/) reports about 1.1M agent-browser installs and 1.1M TDD installs; [webapp-testing](https://www.skills.sh/anthropics/skills/webapp-testing) reports 177k | Prioritize executable browser/test workflows and verification over another generic developer persona. |
| Substantial content workflow adoption | [Marketing skills directory](https://www.skills.sh/coreyhaines31/marketingskills) reports about 224k copywriting, 156.5k content-strategy and 141.8k copy-editing installs | Content briefing, editing and reuse are credible extensions beyond broad marketing guidance. |
| Explicit security workflow adoption | OpenAI's [security-best-practices](https://www.skills.sh/openai/skills/security-best-practices) reports 10.5k installs and [security-threat-model](https://www.skills.sh/openai/skills/security-threat-model) 7.5k | Improve concrete security procedures and language/framework references. Our threat-model concept already exists; avoid duplicating it. |
| Agent security has a dedicated risk framework | [OWASP Agentic Applications Top 10 for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) addresses autonomous, tool-using systems | A focused AI/agent-security review is a plausible specialization. This is a risk signal, not an install count. |
| Cloud workflows have vendor-backed tooling | [Microsoft Azure Skills](https://github.com/microsoft/azure-skills) combines cloud procedures with MCP configuration | Cloud/IaC review and operational diagnostics are practical collection gaps. Vendor supply does not prove demand for our implementation. |
| Hardware workflows can produce checkable artifacts | [KiCad CLI documentation](https://docs.kicad.org/9.0/en/cli/cli.html) documents ERC/DRC and export operations; [KiCad MCP Pro](https://github.com/oaslananka/kicad-mcp-pro) publishes PCB-specific tools and skills | PCB review, BOM and manufacturing handoff can be more concrete than a generic hardware expert. Tool availability is not evidence that a board is safe to manufacture. |
| Film/series skills already have specialist competitors | [Cinema Skills](https://github.com/DenisHumen/cinema-skills) describes screenwriting, shot planning, editing and series-continuity workflows | These are legitimate task families, but an unserved-market claim would be unjustified. No reliable comparative usage count was established here. |
| Cryptography has changing, authoritative requirements | [NIST's post-quantum cryptography project](https://csrc.nist.gov/projects/post-quantum-cryptography) publishes standards and migration material | Cryptographic inventory, implementation review and migration planning need dated references and test vectors. Cryptography is separate from crypto-asset investing. |
| Finance has real agent tool integrations | [Alpaca Trading API MCP documentation](https://docs.alpaca.markets/us/docs/trading-api-mcp) exposes market research/data and order operations | Research, portfolio analysis and execution are distinct capabilities. A connection is not permission to transact or evidence of profitable strategies. |
| Backtest validity has concrete tooling | [Freqtrade lookahead analysis](https://www.freqtrade.io/en/stable/lookahead-analysis/) documents detection of future-data leakage | A rigorous backtest-review skill has a clear verification target. A clean check does not prove an investment edge. |
| Forecasting has checkable scoring and settlement contracts | [Metaculus scoring documentation](https://www.metaculus.com/help/scores-faq/) explains proper scores; [Polymarket resolution documentation](https://help.polymarket.com/en/articles/13364518-how-are-prediction-markets-resolved) specifies rule-based outcomes | Calibration and settlement-rule analysis are concrete candidates. No reliable comparative adoption or profitability evidence for betting skills was established here. |
| Aviation has mature simulation/design tools | [OpenVSP](https://openvsp.org/) supports aircraft geometry/design analysis; [PX4 simulation](https://docs.px4.io/main/en/simulation/) covers software/hardware-in-the-loop workflows | Simulation and engineering-document support are concrete candidates. This review did not establish marketplace demand for an aviation skill or any certification capability. |

A convenience sample of public issues also reveals delivery/documentation friction:
[agency-agents #888](https://github.com/msitarzewski/agency-agents/issues/888) asks
how to use profiles in VS Code; [#1027](https://github.com/msitarzewski/agency-agents/issues/1027)
reports unresolved runbook role references; [openai/skills #534](https://github.com/openai/skills/issues/534)
reports installer symlink containment concerns. These are contributor reports,
not independently reproduced findings or representative demand measurements.
They support prioritizing clear host support, resolvable routing, safe copying and
real installation checks in our own collection.

## Domain expansion map

All names below are candidates, not existing installable entries. An agent owns a
persistent responsibility and handoffs; a skill owns a repeatable procedure. Start
with a skill under an existing role when responsibility is already covered. Add a
new role only for a distinct recurring workload that benefits from separate scope.

| Domain | Candidate roles if needed | Useful skills/artifacts | Verification and documentation focus |
| --- | --- | --- | --- |
| Copywriting and content creation | Use copywriter/marketing-strategist first; add content-editor for a recurring editorial review role | content-brief, copy-editing, long-form-content, content-repurposing, editorial-calendar, newsletter-production | Approved audience/voice/claims, source-backed facts, complete draft, channel constraints and editor review. Publication is a separate action. |
| Movies and series | screenwriter, story-editor, post-production-engineer | screenplay-development, series-bible, continuity-review, shot-planning, edit-delivery | Story/character canon, episode dependencies, script/timeline formats, frame rates, timecode, color/audio specs, render/export checks and media rights. |
| Electronics and hardware building | electronics-engineer, embedded-engineer | schematic-review, pcb-review, bom-review, embedded-bringup | Datasheet revisions, units/tolerances, electrical limits, ERC/DRC, interfaces and test points. Distinguish planned, simulated, bench-tested and manufacturing-released states. |
| Mechanical/product engineering | mechanical-engineer, manufacturing-engineer | parametric-cad-review, tolerance-analysis, design-for-manufacture | CAD/tool versions, materials, units, fits, loads, geometry/mesh checks and shop/supplier constraints. A render is not a structural result. |
| Robotics and controls | robotics-engineer or controls-engineer | control-simulation, sensor-calibration-review, robot-log-analysis | Coordinate frames, units, timing, model assumptions, stability/performance evidence and simulation-to-hardware limits. |
| Cybersecurity | Retain security-auditor; incident-responder for active response; cloud-security-engineer only for recurring infra scope | ai-agent-security-review, cloud-security-review, supply-chain-review, incident-response-triage | Exact scope, threat paths, evidence/severity, containment/forensics handoffs and isolated validation. Keep incident response distinct from post-incident review. |
| Cryptography | cryptography-engineer when protocol/key-lifecycle work recurs | cryptography-review, cryptographic-inventory, pki-review, pqc-migration-plan | Protocol/library versions, standards, key/nonce lifecycle, interoperability and official test vectors. Mathematical argument, implementation testing and formal proof are different evidence. |
| Aviation/aerospace | aerospace-engineer, simulation-analyst | aerodynamic-analysis-review, flight-simulation-validation, aviation-requirements-traceability | Units/reference frames, envelope/model assumptions, traceable requirements, tool versions, simulation/physical-test evidence and independent engineering review. No airworthiness or operational clearance is established by a profile. |
| Corporate finance/accounting | financial-analyst, fpa-analyst; accounting specialist only when a defined standard/jurisdiction is needed | financial-statement-analysis, financial-model-review, budgeting-forecasting, variance-analysis | Reporting period/currency, authoritative filings, reconciliations, accounting policy, model assumptions and scenario sensitivity. |
| Stocks and investment research | investment-researcher, portfolio-risk-analyst | company-research, valuation-review, portfolio-risk-analysis, market-data-validation | As-of timestamps, source/adjustment provenance, corporate actions, benchmark/currency, scenarios and reproducible calculations. Separate facts, estimates and investment opinions. |
| Quantitative trading | quant-researcher; execution-engineer only for a separate tested execution system | backtest-validation, walk-forward-evaluation, paper-trading-review, execution-risk-review | Point-in-time/universe data, leakage/survivorship bias, out-of-sample tests, multiple testing, fees/slippage/liquidity, latency, limits and reconciliation. Historical/simulated/live records must stay distinct. |
| Crypto assets, DeFi and smart contracts | blockchain-security-engineer or use security-auditor initially; onchain-analyst for repeated chain-data research | smart-contract-review, onchain-data-analysis, defi-risk-analysis, wallet-transaction-review | Chain/block/finality, token decimals, oracle/liquidation/admin risks, contract versions, forks/testnets, allowances and transaction simulation. Cryptographic soundness does not establish economic safety. |
| Betting and prediction markets | probability-analyst or reuse mathematician/data-analyst; settlement-reviewer only if justified | odds-analysis, forecast-calibration, betting-model-validation, settlement-rule-review | Odds conversion and bookmaker margin, timestamps, data leakage, Brier/log-loss calibration, uncertainty, limits and exact settlement rules. Modeling permission does not place a bet or promise positive returns. |
| Education and knowledge work | instructional-designer if course production recurs | lesson-design, assessment-design, source-grounded-explanation | Learner prerequisites, measurable objectives, worked solutions, answer/rubric validation and accessibility. Demand for our version remains unmeasured. |
| Other specialist domains | Domain owner only after concrete task discovery | Candidates include architecture/BIM, climate/energy modeling, logistics, clinical-literature review and legal-document analysis | Define jurisdiction/standard where applicable, data/tools, artifact, expert review and validation before adding a title. No dedicated market study for these domains was performed here. |

## Recommended sequence

1. Finish delivery and outcome evidence: native host discovery, reproducible routing
   and task evaluations. Existing [skills #26](https://github.com/powerpuff-kitty/skills/issues/26)
   already tracks outcome evaluations. More pages or personas do not close that gap.
2. Add a small content set: `content-brief`, `copy-editing`, `content-repurposing`.
   Existing roles can own it; demand proxies and the fit with current coverage are
   stronger than for an entirely new specialist pack.
3. Add `ai-agent-security-review` and `cryptography-review`, with appropriate
   current references and adversarial/negative cases. Expand the existing security
   role before adding a broad collection of overlapping security titles.
4. Pilot one hardware workflow and one film/series workflow against real sample
   artifacts: `pcb-review` and `series-bible`/`continuity-review`. Add only the
   minimum distinct role(s) required by those pilots.
5. If finance is a desired product direction, begin with `market-data-validation`,
   `financial-model-review` and `backtest-validation`, plus a tightly scoped
   financial/quantitative research role. Evaluate on fixed datasets before adding
   live execution integrations. Treat betting/prediction-market workflows separately.
6. Develop aviation/robotics or other specialist packs when an actual toolchain,
   sample task and domain reviewer are available. Their fit is plausible; demand
   and successful outcomes for our collection are still unmeasured.

These priorities are editorial recommendations based on collection fit, available
verification and observed proxies. They are not a numerical market ranking, paid
customer validation or authorization to implement every candidate.

## Repository shape and acceptance

Keep skill folders at the Skills source root. Use searchable names and the README
catalog to group them conceptually. Keep Agents' existing `agents/`, `teams/`,
`packs/`, `shared/` and `adapters/` structure; add optional domain packs only when
there are working members. A shared file layout is less useful than consistent
contracts, installation, provenance and completion evidence.

For each new entry, require a real task, a clear trigger and exclusion, expected
inputs/output, available tool/version assumptions, one representative successful
case, one rejection/uncertainty case and a reproducible validation method. Record
specification, source-test, host-loading and observed-model statuses separately.
See the [documentation assessment](DOCUMENTATION-ASSESSMENT.md) for the per-entry
review and recommended documentation tiers. No automatic brokerage connection,
wallet access, gambling account, physical device control or publication is added.
