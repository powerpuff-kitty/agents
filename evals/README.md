# Behavior evaluations

[144 canonical scenarios](behavior-cases.json) specify at least 2 cases per role
and team, plus shared/procedure boundaries. Specification objects retain
`execution_status: not_run`; observed outcomes live separately and never rewrite
a scenario into a claimed pass.

## Observed canonical cases

The [current follow-up index](observed/native-followup-2026-10-15/index.json)
records **13 observed cases and 131 unobserved cases** across 144 specifications.
It adds project-context, tenant-security, sanitized-secret-evidence, proposed-
architecture and unavailable-delegation executions. Acceptance failures remain
observations, not passes. The [follow-up report](observed/native-followup-2026-10-15/README.md)
keeps the initial 10 trials, 2 corrections, installation exercise and project pilot
separate, with independent decisions and explicit unresolved findings.

The earlier [standalone-pilot index](observed/standalone-pilot-2026-10-14/index.json)
retains its 8-case scope, including unavailable-compiler and false-recovery cases.
The [native OpenCode trials](observed/native-routing-2026-10-14/README.md) repeat 3
of those cases using built-in build without skill/subagent calls or custom profile
selection. Registration alone does not prove automatic catalog selection. The earlier
[reliability index](observed/reliability-2026-10-14/index.json) retains its 6-case scope.
Statistical reliability remains unverified.

The earlier [smoke suite](observed/behavior-smoke-2026-10-14/index.json) contains
these 3 historical cases; its source counts remain historical:

| Case | Observable outcome | Remaining limit |
| --- | --- | --- |
| implementation-dirty-worktree | Boundary fix passed 5 tests; owner edit and tests preserved | 1 fixture; supplemental checks are self-checks |
| focused-review-with-skills | Staged/unstaged defects and new caller reviewed; source/selection unchanged | Review action log is not an authenticated complete trace |
| geo-specialist-sampled-visibility-not-causality | Counts, sampling mismatch and unsupported certification distinguished | Supplied observations; no live provider or causal measurement |

Each case retains task, instruction/input identities, final workspace, actual
response/action log, deterministic checks and parent-review rationale. Exact model
identity was unavailable. These runs test explicit instruction use, not automatic
routing, host delegation, repeated reliability or general domain expertise.

## Repeated catalog selection

[8 catalog-selection trials](observed/reliability-2026-10-14/README.md) repeat 2
synthetic tasks before and after the shared-contract routing fix. Fresh sessions
choose from metadata; native automatic-trigger behavior, exact model/usage and
statistical reliability remain unverified. The record retains a reporting error,
a broad mechanical-read limitation and a false test-byte invariant for legitimate
added tests. Artifact checks never silently become reasoning verdicts.

## Fresh independent repository audits

The [2026-10-14 repository audits](observed/fresh-repository-audits-2026-10-14/README.md)
retain 2 original reports, briefs, source identities and dispositions for 8 confirmed
findings. Use [the fresh-review method](../docs/FRESH-REVIEWS.md) for independent audits.
The coordinator must establish a new reviewer session without inherited author
conversation where supported. Pass accepted requirements and raw snapshot evidence,
not author conclusions or intended answers. Preserve actual invocation/isolation
provenance and the original report before triage. Explicit isolation does not prove
coverage or automatic routing. The 4 fresh-review acceptance specifications are
unexecuted until separately evaluated; repository audits are distinct observations.
The earlier smoke index retains its historical 124-case source count.

## Reproduce a scoped fixture

```sh
python3 scripts/behavior_eval.py prepare --case implementation-dirty-worktree --skills-source /path/to/skills --output /path/to/new/evaluation
# Give task.md, instructions/ and workspace/ to a fresh authorized session.
# Retain its actual result.md and action log outside workspace/.
python3 scripts/behavior_eval.py grade --output /path/to/new/evaluation
```

The harness makes no model calls. Grade checks original tests/preserved files or
read-only workspace invariants; it does not grade reasoning or authenticate all
actions. Review each acceptance criterion against the actual response and available
artifacts, recording pass/fail/unverified and limits. Do not show expected answers
or reviewer conclusions to the evaluator. Use local fixtures/stubs only and retain
failed/missing checks. Never upload private data or run a provider/budget implicitly.
Missing-compiler and false-recovery fixtures are also available as
`implementation-unavailable-check` and `browser-recovery-false-pass`. A preserved
workspace does not establish compilation or recovery success. From a source archive
without Git metadata, the harness records a null source revision and retains input
and preparer hashes; it never substitutes an unrelated parent repository's commit.

Current focused-review fixtures also retain a semantic staging hash (modes, blobs,
stages and NUL-delimited paths). Grading compares it separately from porcelain
status, so a changed staged blob cannot hide behind identical status text.
Stat-cache byte refreshes do not change that identity. Legacy inputs without the
hash report a null preservation check; they do not produce a truthy pass.

## Design extraction exercises

The [source-only and DTCG exercises](observed/design-extraction-2026-10-14/README.md)
retain reports, candidate artifacts, source identities and independent reviews.
They are explicit-instruction observations, not canonical role-case executions,
automatic routing proof, live app/browser capture or full DTCG certification.
Public exports withhold unrelated project context and disclose separate-copy changes.

## Product-method exercises

[Measurement and research/app exercises](observed/product-methods-2026-10-14/README.md)
retain 8 explicit-procedure synthetic tasks, reproducible calculations and independent
review records. They do not count as canonical role-case executions, live studies,
automatic routing or production/app/browser verification.

## Other observations

[Finance](observed/finance-skill-review-2026-10-14/manifest.json),
[crypto/forecasting](observed/crypto-forecast-review-2026-10-14/manifest.json)
and [content/GEO](observed/content-geo-review-2026-10-14/manifest.json) retain
separate explicit-skill exercises. They do not count as canonical role-case runs.
[Installation verification](../docs/INSTALLATION-VERIFICATION.md) covers registry
loading, which is separate from model behavior. Preserve raw records as historical
evidence even when current instructions or counts change.

## Matched native comparisons and project pilot

The [2026-10-15 comparison](observed/native-comparison-2026-10-15/README.md) retains
18 planned DeepSeek runs across 3 fixtures, 3 usage modes and 2 repetitions, plus
a separately recorded startup retry, 2 context candidates and a real AI Agents
project pilot. Built-in controls, explicit skill-body attachments and named primary
profiles are distinguished. Failures/timeouts remain in the roster, and task
acceptance comes from independent review rather than host completion.

The pilot's incomplete native change is separate from the coordinator's tested,
independently reviewed staging-identity correction. The shorter debugging skill
retains scoped before/after outcomes; source bytes and provider measurements remain
distinct. That comparison repeats already observed cases and retains its 8/144
coverage baseline; the later follow-up index records the additional 5 executions.
Use [the native evaluation guide](../docs/NATIVE-EVALUATIONS.md) to prepare offline,
run only explicitly authorized inference, and produce result-bound review reports.

The required offline `python3 scripts/check_evidence.py` gate verifies registered
artifact manifests, exact review bindings and in-memory measurement regeneration.
It preserves failed/missing outcomes and uses no host executable, credentials,
AI Skills checkout or paid inference. See [the native guide](../docs/NATIVE-EVALUATIONS.md).
