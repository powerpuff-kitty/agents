# Team workflows

A team preset supplies ordered assignments to team-lead. OpenCode commands load
the preset as a user prompt and select that coordinator in the current session.
The coordinator delegates to specialists using the host's available capabilities.
These are reusable workflow instructions, not a new runtime or a multi-select UI.

| Command | Default intent | Workflow |
| --- | --- | --- |
| `/team <task>` | Derived from the request | Select the smallest useful set of available specialists, with conditional research/review, serialized implementation, verification, and explicitly authorized actions |
| `/team-research <question>` | Research/review only | Researcher gathers cited evidence, then evidence-validator and applicable domain specialists assess it; team-lead reconciles the answer |
| `/team-audit <scope>` | Review only | Project-auditor scopes accepted work, researcher gathers references when needed, then eight core specialists review bounded domains; team-lead consolidates results |
| `/team-feature <feature>` | Implement the described feature | Establish accepted Definition of Done, frame relevant domains, implement with one writer, independently verify, check applicable artifact evidence, then assess integrated readiness |
| `/team-ui <screens or journey>` | Review only | Designer establishes coverage, UX-designer maps relevant journeys, then quality, usability, accessibility, evidence, and applicable performance reviews follow |
| `/team-ux <task or journey>` | Derived from the request | Frame task scope, use available user evidence, assess/design journeys, align UI/copy/access, implement only requested changes, then independently check and reconcile |
| `/team-release <target>` | Readiness review | Release-engineer establishes gates, specialists assess applicable evidence, and release-engineer reconciles the readiness matrix |
| `/team-iteration <increment or target>` | Derived from the request | Establish accepted gates and snapshot, gather relevant context, apply only requested fixes, complete specialist/artifact checks, then report ready, blocked, or unverified |
| `/team-product <scope>` | Product definition/review | Product-manager frames the problem, evidence/feasibility roles assess it, then requirements/flows and acceptance checks follow |
| `/team-science <question>` | Derived from the request | Scientist frames the question, methods are reviewed, the protocol is finalized, requested implementation/execution is serialized, then results are interpreted and independently checked |
| `/team-data <question>` | Derived from the request | Data-analyst checks scope/provenance, relevant methods are reviewed, approved data is analyzed, requested artifacts are saved, and results are independently checked |
| `/team-finance <question>` | Financial analysis/review | Frame source/as-of scope, check data, conditionally analyze models/strategies/portfolio risk, independently verify, reconcile and save only requested artifacts |
| `/team-crypto-review <scope>` | Onchain/protocol review | Check chain/source/finality before applicable contract/economic analysis, independently verify and save only requested artifacts |
| `/team-forecast <question>` | Forecast/odds/rules review | Gather required sources before data/definition checks and analysis, independently verify and save only requested artifacts |
| `/team-launch <product>` | GTM planning/review | Gather evidence, define positioning, create requested plan/drafts, and reconcile commercial/technical readiness without launching |
| `/team-growth <goal>` | Derived from the request | Establish actual baselines, diagnose hypotheses, implement only requested changes, run only authorized experiments, and assess actual outcomes |
| `/team-seo <scope>` | Derived from the request | Audit search eligibility/content, gather relevant support, apply requested fixes, then verify completed outputs and evidence |
| `/team-geo <scope>` | Derived from the request | Establish observed/provided AI visibility, assess source/representation gaps, apply requested improvements, then reassess and validate claims |
| `/team-game <scope>` | Derived from the request | Define mechanics/experience, assess balance/feasibility, implement a requested prototype, then check actual design/quality/playtest evidence |
| `/team-3d <brief>` | Derived from the request | Establish the brief/runtime constraints, create requested assets, integrate requested completed assets sequentially, then check actual visual/runtime evidence |

The audit preset is the broad core-specialist entry point. Every applicable assignment
must produce an actual result or an explicit failed/blocked state. Other presets
explain conditional inclusions and skips instead of invoking every role for every
small task. New domain workflows belong to their [packs](PACKS.md); the core audit
does not automatically invoke every marketing or art role. If scope is empty, a clear current task can supply it; otherwise the
coordinator asks only for the missing critical input.

## General and research teams

Use `/team` when the work does not fit a fixed preset. Team-lead inspects available
role descriptions and project context, selects relevant specialists, and explains
the brief plan. It can use additional registered project specialists within the
same scope and limits; it cannot invent roles or recursively invoke other teams.
A small task can use one specialist or feasible coordinator checks.

The general preset's roster is conditional. Research goes to researcher, claim
checking to evidence-validator, structural decisions to system-architect, UI work
to designer, implementation to feature-developer, correctness to quality-engineer,
security to security-auditor, profiling to performance-engineer, scope/progress to
project-auditor, and release work to release-engineer. Irrelevant assignments and
empty stages are skipped. The [full catalog](CATALOG.md) adds science, mathematics,
data analysis, product/user research, copy, marketing/GTM, SEO/GEO, localization,
game design, 3D assets, technical art and financial/model/portfolio research. Team-lead selects those only when relevant
and available. This is model-interpreted routing, not a classifier.

For requested specialist artifacts, a capable domain role may replace the general
developer as the exclusive writer. A copywriter can own saved content, data-analyst
analysis artifacts, artist-3d assets, and technical-artist integration. Asset creation
and integration run sequentially. Review-only stages return findings or drafts;
source mutations require the requested scope and an explicit serialized owner.

Plans are not executed studies; draft assets are not publications; simulated results
are not observed real-world outcomes; visuals are not valid 3D exports; unavailable
search/AI metrics are not measured visibility. Each workflow preserves those limits.

The request determines whether source changes are authorized. A research or audit
question does not become an implementation task merely because a writer is listed.
Requested changes run with one source writer at a time, then applicable checks.
Requested release preparation has a separate serialized writer stage; explicitly
authorized commit/push, release operations, and tracker updates occur sequentially
after their prerequisites pass. Existing authorization persists.

Use `/team-research` for technical comparisons, product/market questions, data
research, or decision evidence. It first gathers an evidence packet, then checks
citations, freshness, calculations, uncertainty, and relevant domain implications.
Domain review is conditional. Researcher is one broad role, complemented by existing
specialists rather than duplicated into narrow research profiles. Browsing and
source access depend on the host; unavailable evidence stays explicit. Research
answers distinguish facts, vendor assertions, observations, and inference, and
do not authorize implementation or vendor contact by default.

## UX, usability, and accessibility

`/team-ux` focuses on complete user tasks rather than visual consistency alone.
UX-designer maps entry points, prerequisites, transitions, completion, alternatives,
context preservation, and recovery. Designer aligns visual/components, copywriter
supports requested wording when installed, and independent usability-auditor checks
recognition, feedback, confusion, repeated work, dead ends, and guardrails.
Accessibility-specialist checks relevant semantics, keyboard/focus, assistive use,
and declared criteria with actual evidence.

All three specialist roles and the workflow belong to core. User-researcher,
data-analyst, and copywriter are conditional candidates from other packs; filtered
exports skip absent roles and empty evidence stages. Available evidence precedes
journey conclusions, completed flow specifications precede UI/copy alignment, and
requested writing completes before dependent independent checks. Review/design
in a response does not authorize source edits, recruitment, or live experiments.

Usability findings distinguish reproduced barriers, source-supported risks,
heuristics, visual preferences, and actual participant observations. Accessibility
reports distinguish source checks, interpreted automation, actual keyboard/assistive
checks, and unavailable coverage. No task-success rates or screen-reader passes
are invented. [WAI evaluation guidance](https://www.w3.org/WAI/test-evaluate/) explains
why automated tools alone cannot establish complete accessibility.

`/team-ui` and `/team-feature` also use the focused roles when relevant; product
requirements route complete flow design to UX-designer and visual alignment to
designer. Numeric usability or accessibility scores require a disclosed rubric
and actual evidence rather than an aggregate guess.

## Releasability and iteration closure

Iteration-reviewer owns integrated-product Definition of Done assessment;
release-engineer owns technical artifact/consumer evidence and authorized delivery.
`/team-iteration` assesses a named increment and target, with conditional remediation
through one writer followed by applicable independent and artifact checks. It works
in core-only exports and omits the optional product-manager candidate when absent.

`/team-feature` establishes applicable gates before writing and closes with a
readiness assessment after verification/artifact evidence. `/team` reviews product
increments after applicable checks and before dependent release actions. Other
coordinated product implementations use the same closure guidance; solo developers
report feasible self-checks without inventing an independent review.

Every required applicable gate needs current supporting evidence for ready.
A confirmed required failure means blocked; required unknowns without an established
failure mean unverified. Keep baseline failures, accepted exceptions, and stale
results explicit. Requested corrections invalidate affected results and require
rechecks. Implementation completion may coexist with blocked or unverified product
readiness and must be reported separately.

These prompts do not automatically run after changes or enforce CI/merge protection.
Use the actual product's checks and completion process for enforcement. See
[iteration readiness](ITERATION-READINESS.md) for the evidence contract and practical
integration sequence. Review alone authorizes neither fixes nor publication.

## Coordination rules

The coordinator provides isolated children with scope, accepted requirements,
relevant paths, source identity, permitted actions, and evidence expectations.
It owns a stage/member status record and the final result. Specialists do not
recursively launch other coordinators or additional unassigned workers.

Independent reviews of a stable snapshot may run concurrently, with a requested
maximum of three active assignments and any lower host/user limit respected.
Writers complete before dependent reviews. Corrections return to the implementation
owner, then affected checks run against the changed snapshot. Review assignments
do not mutate source or shared trackers merely because a fix was identified.

Findings are deduplicated by root cause, disagreements are reconciled against
source/reproduction, and stale findings are rechecked or labeled stale. Failed
children and unverified checks remain explicit. An average of incompatible
specialist ratings is not a team readiness score.

Review presets do not authorize tags, pushes, publication, deployment, rollback,
intrusive tests, or new large benchmark programs. Existing explicit authorization
persists, and an explicit remediation request can add a serialized fix/verify
stage without redundant permission questions.

## Installation and host mapping

```sh
python3 scripts/install.py --tool opencode
~/.opencode/bin/opencode reload
python3 scripts/validate.py --opencode ~/.opencode/bin/opencode
```

The installer writes twenty-nine profiles and seventeen commands by default.
Use repeatable `--pack` options for a smaller dependency-complete set. Team-lead is a
primary profile, while specialists retain both primary and child eligibility.
Command frontmatter selects team-lead and uses `subagent: false`, keeping the
coordinator in the parent session so specialists can be its children. No selected
model or global permission setting is changed.

For another destination, use `--target <agents-directory>` and optionally
`--commands-target <commands-directory>`. Omitting the latter uses the sibling
`commands/` directory. `--agents-only` installs profiles without commands.
Profile and command directories must not overlap; nesting commands inside an
agent directory could make the host discover command templates as agent profiles.
Conflict protection, backups, and idempotence apply to both destinations.

Portable exports include complete coordinator/specialist bundles in
`dist/portable/agents/` and neutral briefs in `dist/portable/teams/`. Supply the
applicable bundles to another host; the brief does not provision a team by itself.
If named delegation is unavailable, the coordinator can apply feasible role checks
serially and must label them coordinator-performed rather than independent runs.

## Evidence limits

The command registry verifies that the host discovers the slash commands; source
and rendering tests verify their coordinator, scope placeholder, and parent-session
mapping. No actual end-to-end model team run is established by these checks.
The 124 behavioral scenarios remain unrun until evaluated sessions and artifacts
are retained. Parallel limits and review-only rules are prompt contracts rather
than runtime-enforced semaphores or read-only permissions.

## Financial research and risk

[Finance](FINANCE.md) documents `/team-finance`, the three role boundaries,
worked synthetic calculations and pack installation. Data/provenance review
precedes dependent domain analysis; independent checks follow completed results.
Only a requested saved artifact uses the sole writer, followed by artifact review.
Missing inputs remain explicit. Selecting the team does not execute trades,
activate bots, connect wallets or place bets.

## Crypto and event forecasts

[Crypto](CRYPTO.md) and [forecasting](FORECASTING.md) document the two optional
teams, role boundaries and examples. The forecast team gathers needed external
rule evidence before dependent analysis. Both teams check data/definitions first,
independently check completed conclusions, serialize the requested artifact writer
and inspect saved output afterward. Data access, finality, rules and missing labels
remain explicit. No wallet/betting/resolution action is implied by team selection.
