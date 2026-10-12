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
| `/team-feature <feature>` | Implement the described feature | Applicable architecture/design framing, one feature-developer source writer, then independent quality and relevant conditional reviews |
| `/team-ui <screens or journey>` | Review only | Designer establishes representative coverage, followed by quality/evidence checks and performance review when relevant |
| `/team-release <target>` | Readiness review | Release-engineer establishes gates, specialists assess applicable evidence, and release-engineer reconciles the readiness matrix |
| `/team-product <scope>` | Product definition/review | Product-manager frames the problem, evidence/feasibility roles assess it, then requirements/flows and acceptance checks follow |
| `/team-science <question>` | Derived from the request | Scientist frames the question, methods are reviewed, the protocol is finalized, requested implementation/execution is serialized, then results are interpreted and independently checked |
| `/team-data <question>` | Derived from the request | Data-analyst checks scope/provenance, relevant methods are reviewed, approved data is analyzed, requested artifacts are saved, and results are independently checked |
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
game design, 3D assets, and technical art. Team-lead selects those only when relevant
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

The installer writes twenty-five profiles and fifteen commands by default.
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
The 83 behavioral scenarios remain unrun until evaluated sessions and artifacts
are retained. Parallel limits and review-only rules are prompt contracts rather
than runtime-enforced semaphores or read-only permissions.
