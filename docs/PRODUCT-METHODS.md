# Product methods

Use the existing roles with optional focused procedures from
[Skills](https://github.com/powerpuff-kitty/ai-skills). The catalog remains 35 profiles;
these methods add depth without duplicating ownership. Installation and updates
remain separate for [profiles](../INSTALL.md) and
[skills](https://github.com/powerpuff-kitty/ai-skills/blob/main/INSTALL.md).

| Request | Method | Existing owner | Required output |
| --- | --- | --- | --- |
| Define or verify product events | product-instrumentation | data-analyst defines; feature-developer implements; quality-engineer verifies | Versioned event contract, collection scope, identity/dedupe rules and payload QA |
| Explain conversion or retention | product-analytics | data-analyst | Reproducible unit/window/eligibility definitions, mature denominators and descriptive results |
| Plan or interpret an experiment | product-experimentation | scientist, with data-analyst | Assignment/exposure checks, estimand, guardrails, stopping policy and validity-qualified readout |
| Track competitor changes | competitor-monitoring | researcher | Dated comparable snapshots, material changes, coverage gaps and explicit repeat-run handoff |
| Build or assess an iOS/Android flow | native-app-delivery | feature-developer; quality/release reviewers | Lifecycle/offline/permission behavior and separate source, simulator, device and distribution evidence |
| Plan or synthesize participant research | user-research | user-researcher | Study/evidence scope, consent/use limits, coded observations, contradictions and sampling limits |
| Assess an addressable opportunity | market-opportunity-research | researcher; product/marketing interpret | Buyer/segment definitions, overlap-adjusted ranges and separately supported demand/WTP claims |
| Verify browser visuals and recovery | test-engineering; performance-audit recovery guidance | quality-engineer; performance-engineer | Reviewed visual baseline plus journey/state checks; measured restoration/loss only when actually exercised |

Read only relevant method references; the skill owns its procedure and report
template. Profiles continue with feasible native methods if the skill is absent,
and identify unavailable tools or evidence. They never silently install skills.
Install only the desired skill folders directly from the Skills repository.
The optional CLI also offers domain presets; its embedded revision can lag the
source. See [installation channels](DISTRIBUTION.md) before choosing a manager.

## Use

Request `/team-data` for a supplied event export, `/team-growth` for a product
experiment, `/team-research` for a market assessment or competitor comparison,
`/team-ux` for participant evidence and `/team-feature` for an accepted native flow.
Name the desired procedure when precision helps. Commands request host-dependent
coordination; they do not enforce scheduling or tool permissions.

A monitoring report includes cadence, sources, freshness policy, owner and next
run. A recurring watch exists only after an authorized scheduler is actually
configured and checked. A tracking plan does not authorize collection in a project
that excludes tracking. Studies, live experiments, SDK/device work and deployment
need their actual task inputs and execution scope.

[Retained offline exercises](../evals/observed/product-methods-2026-10-14/README.md)
separate synthetic calculations and source reviews from real participant, browser,
device, production or model-team execution. Canonical case specifications remain
separate; [the evaluation index](../evals/README.md) owns their status.
