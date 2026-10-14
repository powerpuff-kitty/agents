# Standalone project pilot and failure cases

This record adds **2 observed canonical cases**, bringing coverage to **8 observed
and 136 unobserved** of the 144 specifications. All specification objects retain
`not_run`; the [index](index.json) records observations separately. Four reflection
branch exercises and the real-project pilot do not inflate that canonical count.

## Real project and handoff

A fresh evaluator used a direct-install snapshot of this actual Agents repository
at `73b241f5eb9240034d78f531abd8ace804ed0890`, choosing release-engineer, quality-engineer
and release-review from metadata. Its [original result](pilot/result.initial.md)
and [actions](pilot/actions.md) cover validation, exports, 39 of 42 tests, partial
installation, repeats, simulated managed updates, conflicts and source-archive
consumption. Three synthetic-commit tests were excluded under that pilot's task
constraint; they were never labeled passing. The later independent
[pilot review](review/pilot-review.md) reproduced the supported checks.

Root handed the frozen result to a separate reviewer session. This is actual
coordinator-orchestrated review using installed instructions, not native team-command
execution or automatic host triggering. Profile/skill installation was direct and
used no Harness CLI. The pilot did not implement or exercise a browser/app product.

## New observed cases

- [Unavailable compiler](cases/implementation-unavailable-check/result.md): a scoped
  input-validation fix preserved the owner's note. The required compiler actually
  failed with exit 127. The retained 52-case JavaScript logic check and independent
  finite contract checks support logic only; TypeScript compilation remains unverified.
- [False recovery pass](cases/browser-recovery-false-pass/result.md): wrong route,
  viewport/theme, unapproved baseline, failed retries and process-local state do not
  establish the claimed visual/recovery success. No browser or production fault ran.
- Reflection branches: [failed test](cases/reflection-failed-test/result.md),
  [architecture finding](cases/reflection-architecture-finding/result.md),
  [insufficient evidence](cases/reflection-insufficient-evidence/result.md) and
  [routine success](cases/reflection-no-reflection-needed/result.md). Evidence references,
  fact/inference separation and appropriate abstention were independently reviewed.

The [six-case review](review/report.md) found no actionable output defect in that
finite scope. These 6 tasks share 1 evaluator session; they are not 6 independent
trials. Actual model/provider identity and token/cost usage are unknown.

## Findings and corrections

The pilot-only runner recorded each command's exit but returned zero even when a
subcommand failed. All original gate records were zero and independently reproduced;
the defect does not turn them into failures. The original script/report remain intact.
Separate [initial correction](pilot-tooling-correction/correction.md) and
[owner-work follow-up](pilot-tooling-correction/correction-v2.md) preserve v1/v2.
The [v3 identity follow-up](pilot-tooling-correction/correction-v3.md) records initial
dirty-source identity before hashing and refuses checks while preserving owner work.
Controlled passing/failing probes and separate reviewer rechecks retain each stage.
The [final v3 recheck](review/correction-v3-recheck.md) supports the corrected
preflight and clean-source success/failure behavior; earlier findings remain intact.

Both root and independent review observed that the archived evaluation helper
assumed `.git` existed. The [retained failure and correction](archive-correction.md)
led to a permanent regression and null source revision when Git metadata is absent.
The pilot's permanent managed-update/downgrade regression now changes actual source
in a disposable copy, checks byte-exact backups, protects local edits and restores
the earlier managed version. Final release checks apply to their recorded commit,
not retroactively to the older pilot snapshot.

The pilot review's archive count describes 1,268 members as regular files. The raw
archive contains 860 regular files and 408 directories; retain its [separate reviewer
correction](review/correction-recheck.md) alongside the original report. No functional artifact result changes.

[Protocol checks](protocol-checks.json) separately validate a root-authored synthetic
reflection example against the pinned canonical schema and supplied evidence/IDs,
and all 12 memory fixture records against their schema. They are deterministic
format checks, not model serialization, cloud memory operations or executed corrections.

## Provenance and reproduction

[Public export](public-export.json) identifies byte-preserved selected files and
omitted duplicate repositories, installation trees and archives. No text redactions
were made. Original sandbox paths remain in scripts/logs; reconstruct the recorded
source revisions and restage explicit locations before replay. Selected complete
skill folders and profile bodies are under `instructions/`; discovery metadata and
original full-input hashes are retained. [Manifest](manifest.json) hashes the public
record. No runtime export includes this evidence directory.

The initial sessions used `fork_turns: none`; reviewer correction rechecks reuse
its context. The reviewer disclosed an initial filename listing that exposed excluded
pilot path metadata before that scope was allowed, without reading those bodies.
This is not perfect isolation or an authenticated exhaustive action trace. Native
automatic routing, all 144 model cases, repeated statistical reliability, minimum
Python/platform coverage and live production outcomes remain unverified.
