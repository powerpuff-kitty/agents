# Behavior evaluations

[128 canonical scenarios](behavior-cases.json) specify at least 2 cases per role
and team, plus shared/procedure boundaries. Specification objects retain
`execution_status: not_run`; observed outcomes live separately and never rewrite
a scenario into a claimed pass.

## Observed canonical smoke cases

The [2026-10-14 smoke suite](observed/behavior-smoke-2026-10-14/index.json)
records **3 observed cases and 125 unobserved cases**. Each ran in a fresh scoped
session with explicit role/skill instructions and isolated synthetic artifacts.

| Case | Observable outcome | Remaining limit |
| --- | --- | --- |
| implementation-dirty-worktree | Boundary fix passed 5 tests; owner edit and tests preserved | 1 fixture; supplemental checks are self-checks |
| focused-review-with-skills | Staged/unstaged defects and new caller reviewed; source/selection unchanged | Review action log is not an authenticated complete trace |
| geo-specialist-sampled-visibility-not-causality | Counts, sampling mismatch and unsupported certification distinguished | Supplied observations; no live provider or causal measurement |

Each case retains task, instruction/input identities, final workspace, actual
response/action log, deterministic checks and parent-review rationale. Exact model
identity was unavailable. These runs test explicit instruction use, not automatic
routing, host delegation, repeated reliability or general domain expertise.

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

## Other observations

[Finance](observed/finance-skill-review-2026-10-14/manifest.json),
[crypto/forecasting](observed/crypto-forecast-review-2026-10-14/manifest.json)
and [content/GEO](observed/content-geo-review-2026-10-14/manifest.json) retain
separate explicit-skill exercises. They do not count as canonical role-case runs.
[Installation verification](../docs/INSTALLATION-VERIFICATION.md) covers registry
loading, which is separate from model behavior. Preserve raw records as historical
evidence even when current instructions or counts change.
