# Releasability after each increment

Iteration-reviewer assesses whether the integrated product meets its accepted
Definition of Done for a named target. Release-engineer supplies technical artifact,
consumer, configuration, and recovery evidence. Project-auditor traces accepted work
and progress. Team-lead coordinates applicable specialists and owns corrections/status.

The profile and `/team-iteration` belong to core. They can assess a feature, a group
of work items, or the current increment without requiring Scrum ceremonies, a named
sprint, or a particular tracker.

```text
/team-iteration assess the current increment for our staging target
/team-iteration fix the scoped readiness defects and verify the increment
/team-feature implement the accepted feature and assess integrated releasability
/team check whether these changes leave the product ready to ship
```

## Definition of Done and evidence

Use the project's existing accepted requirements and policies. If it has no named
Definition of Done document, reconstruct applicable gates from accepted behavior,
test/release commands, and operational constraints; label genuinely new criteria
as proposals rather than silently imposing or approving them. Missing policy does
not justify abandoning feasible checks or fabricating a ready verdict.

For each criterion record:

| Field | Required content |
| --- | --- |
| Criterion and basis | Accepted requirement/policy and its exact reference |
| Applicability | Required gate, justified not-applicable condition, or advisory concern |
| Expected evidence | Observable acceptance, command/result, artifact, or supported check |
| Observed status | passed, failed, unverified, or not-applicable with a reason |
| Identity and coverage | Source revision/dirty snapshot, artifact hash, environment, date, covered behavior |
| Exception | Existing explicit policy/authorization basis and bounded scope; no invented waiver |
| Next action | Specific repair, verification, or unresolved input and owner when known |

Assess applicable accepted behavior and existing critical journeys, regressions,
security/privacy, UX/accessibility, documented performance budgets, build/package
integrity, consumer installation/startup, configuration, compatibility, migrations,
documentation, and recovery. Select proportionately; do not turn every text change
into a full security audit or benchmark program. A known unaffected gate can reuse
evidence only with a stated applicability basis.

Incomplete functionality must be genuinely isolated if it is outside the release
scope. Check feature-flag defaults/exposure and dependencies; a label saying disabled
does not prove isolation. Documented accepted debt differs from a required-gate
failure. Neither an issue closure nor new unit-test success establishes complete
integrated behavior or artifact startup.

## Verdict contract

- **ready**: all required applicable gates pass with current evidence for the
  named target and snapshot.
- **blocked**: a required gate has a confirmed failure; retain other unknowns too.
- **unverified**: no required failure is established, but required evidence,
  criteria, target identity, or applicability remains unresolved.

The gate statuses and verdict are reviewed evidence contracts, not a computed
percentage. A high pass count cannot hide one required failure or missing gate.
After relevant source/artifact/configuration changes, identify stale results and
rerun affected and dependent checks before issuing a fresh verdict. Preserve baseline
failures even when the requested feature itself is implemented; fix only authorized
scope, and report out-of-scope blockers separately.

Readiness is separate from publication authorization and from live deployment state.
A local artifact check cannot establish a published or deployed revision. The
requested assessment is complete when the verdict and every required gate's evidence
or gap are clear; scoped remediation is complete after applicable rechecks.

## Workflow and project integration

`/team-iteration` frames the accepted gates, gathers relevant context, applies fixes
only when requested through one writer, performs applicable independent reviews,
checks artifact/consumer evidence, and reconciles the final verdict. Core-only
exports omit the optional product-manager assignment while retaining the readiness
reviewer, quality and release roles. `/team-feature` establishes gates before
implementation and adds artifact/readiness closure after independent verification.
`/team` assesses product increments after checks and before dependent release actions.
Solo developer sessions perform feasible self-checks and label their lack of an
independent review rather than inventing a delegated result.

These are prompt workflows. Installation does not add a watcher, run after every
commit, invoke a model in CI, change branch protection, or modify product repositories.
To enforce repeatable product gates, integrate that project's actual existing checks
with its CI and completion process, for example:

1. Establish the accepted increment, Definition of Done, target, and baseline.
2. Run repository-native required checks on the candidate and retain actual logs,
   artifact hashes, environment, and source identity.
3. Verify built-artifact installation/startup and critical journey smoke checks in
   the approved isolated environment where required.
4. Review the current evidence with `/team-iteration` and retain the gate verdict.
5. After fixes, rerun affected checks and refresh the verdict before any authorized
   dependent delivery. Required failure or unknown prevents a ready claim.

This package supplies no universal CI workflow or deterministic verdict executor;
the correct commands, credentials, checks, and enforcement depend on the product.
All model behavior specifications remain unrun until retained evaluated sessions
establish actual dispatch, review quality, and completion behavior.
