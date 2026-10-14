# Retained actions and evidence

All verification below is actual execution in this pilot. Project source stayed read-only; writes were pilot scripts/logs, generated `project/dist`, source-archive extraction and disposable installation/test targets. No network, personal configuration, other repositories, publication, tracker action, source commit, tag or third-party installation was used. Supplied evaluation `initial.json`, sibling evaluator runs, author conversation and reviewer reports were not used as evidence. Project unit tests create/read their own synthetic fixture metadata under `scratch`.

## Selected instructions

Read `task.md`, `/private/tmp/standalone-pilot-2026-10-14/shared-contract.md`, relevant metadata from `/private/tmp/standalone-pilot-2026-10-14/catalog.md`, then `project/AGENTS.md`.

| Selected installed instruction | Reason | SHA-256 |
| --- | --- | --- |
| `/private/tmp/standalone-pilot-2026-10-14/pilot/installed/agents/release-engineer.md` | Candidate identity, release gates, consumer artifacts and recovery limits | `335c5017d266346032e0d641dcb7051799f786c71754f2f024496edc5e56bcf4` |
| `/private/tmp/standalone-pilot-2026-10-14/pilot/installed/agents/quality-engineer.md` | Installer correctness, negative cases and test evidence | `95a6febc6a6475665fbac7ebe03a3c9dfbf6907cb501f274b4c744ad3acc402e` |
| `/private/tmp/standalone-pilot-2026-10-14/installed-skills/release-review/SKILL.md` | Requested readiness assessment, not release execution | `7a81e9be233d684dc7906f5463ab1798debb0e1af419bc2eedaab09ab10dd9f6` |

These instructions were manually selected and read; no claim is made that the host automatically activated profiles or triggered skills. No team/delegation, broad audit, release-execution or unrelated domain procedure was selected. No meaningful failed attempt required structured reflection. Exact model/usage unavailable: recorded as unknown.

[Instruction hashes](logs/instruction-sha256.json) also retain exact paths/hashes for task, catalog, shared contract and project AGENTS. [Initial source identity](logs/source-before.json) retains revision `73b241f5eb9240034d78f531abd8ace804ed0890`, initially empty Git status, full tracked-file hashes, Python version and platform. [Final source check](logs/source-final.json) confirms every tracked file unchanged, same revision and empty Git status.

## Inspection commands and scope

Used `cat`, `rg --files`, `rg -n`, `sed -n`, `nl -ba`, `wc -l` and local Git commands; command results were successful. Relevant source read: `README.md`, `INSTALL.md`, `CONTRIBUTING.md`, `docs/{ARCHITECTURE,DISTRIBUTION,PACKS}.md`; `scripts/{build,install,validate,check_docs,behavior_eval,opencode_probe}.py`, `scripts/opencode-host.json`; both adapter renderers/configs; all six test modules; `.github/workflows/validate.yml`. Catalogue listing was limited to permitted pilot paths and supplied metadata. Project documentation checker and archive/hash checks mechanically process source files; retained reviewer-report prose was not used to support findings.

Identity commands: `git rev-parse --show-toplevel`, `git status --short`, `git rev-parse HEAD`, `python3 --version`. `git tag --list` returned no tags. `git cat-file -t 18584173054bb7d16c2448e5892da923cd68370e` returned `commit`. `git diff --name-only 18584173054bb7d16c2448e5892da923cd68370e HEAD` returned only `INSTALL.md`; the inspected diff changes only the copyable prompt's SHA.

## Gates actually run

From the pilot: `python3 -B run_gates.py`, exit 0. [Runner](run_gates.py) retains subprocess argv/cwd/exit/log in [gate-results.json](logs/gate-results.json). It sets `PYTHONDONTWRITEBYTECODE=1` and `TMPDIR` to this pilot's `scratch`; all project subprocesses use the recorded Python 3.14 executable.

From `project`, all exit 0:

```sh
python3 scripts/validate.py
python3 scripts/check_docs.py
python3 scripts/build.py --adapter portable
python3 scripts/build.py --adapter opencode
python3 scripts/build.py --adapter portable --check
python3 scripts/build.py --adapter opencode --check
python3 -m unittest discover -s tests -p test_workflows.py -v
python3 -m unittest discover -s tests -p test_selection.py -v
python3 -m unittest discover -s tests -p test_audit_regressions.py -v
python3 -m unittest discover -s tests -p test_native_probe.py -v
python3 -m unittest discover -s tests -p test_docs.py -v
```

Raw stdout/stderr: `logs/gate-01.log` through `logs/gate-11.log`. Tests: 24 + 5 + 4 + 3 + 1 = 37 passed. Tests include expected rejection of drift, unknown selections, invalid pack graphs/state, symlink collisions, command conflicts before profile writes, local edits and explicit backup replacement. The host download test mocks its network response; no actual download was performed.

From `project/tests`, with the same environment, also ran:

```sh
python3 -B -m unittest -v test_behavior_eval.BehaviorEval.test_no_overwrite_of_an_existing_evaluation test_behavior_eval.BehaviorEval.test_new_cases_route_both_modes_and_keep_reasoning_ungraded
```

Exit 0, 2 tests passed: [raw log](logs/behavior-safe.log), [exact argv and exclusions](logs/behavior-safe.json). Total 39 of 42 tests executed. The boundary, read-only-fixture and discovery-fixture behavior tests were excluded because they invoke synthetic commits. No full-suite pass is claimed.

## Installation and source-consumer reproduction

From the pilot:

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/private/tmp/standalone-pilot-2026-10-14/pilot/scratch python3 -B installer_probe.py
python3 -B archive_probe.py
```

Both exit 0. [Installer probe](installer_probe.py) ran 8 grouped checks against the actual imported installer; [retained results](logs/installer-probe.json) include exact target/backup paths. Initial installs use actual compiled source; the update uses an in-memory compiler wrapper appending synthetic v2 content. It checks exact old profile/state backups, updated digest, private mode, repeat byte/mtime stability, prior team selection retention, unrelated bytes and local-edit refusal without writes. It does not claim a historical release upgrade or native host loading.

[Archive probe](archive_probe.py) invokes `git archive --format=tar --prefix=ai-agents-candidate/ HEAD` twice and compares SHA-256. It checks regular safe paths, LICENSE, no `.git`/`dist` archive members, then extracts under `scratch/archive-consumer`. The extracted source runs validation, docs, both builds/checks and these CLI installation operations with explicit isolated targets:

```sh
python3 scripts/install.py --target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/agents --commands-target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/commands --pack core --dry-run
python3 scripts/install.py --target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/agents --commands-target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/commands --pack core
python3 scripts/install.py --target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/agents --commands-target /private/tmp/standalone-pilot-2026-10-14/pilot/scratch/archive-install/commands --pack core
```

All 9 archive-consumer commands exit 0; logs `archive-01.log` through `archive-09.log` and [archive-probe.json](logs/archive-probe.json) retain exact cwd/argv/results. Core installs 16 profiles, 8 commands and 2 license notices; repeat reports 26 unchanged. Both extracted exports match checkout exports byte-for-byte, including manifests. Full output per adapter is 56 hashed outputs plus the build manifest.

Archive: `scratch/ai-agents-0.1.0-beta.1-candidate.tar`, SHA-256 `6f4f6f64d550e33f4c0e44ef2e45026d0c76d8eab002460793319e0aa5110cdf`. Portable build-manifest SHA-256 `c30f93e229cf102dcbd497a29928ed755480f4fcce001e76806e56558c47f73a`; OpenCode manifest SHA-256 `e8fa1def7d583c2d283727f7e25e50d09ded8a471b3d1ef10220833051d1a201`.

The reproduction probes intentionally refuse existing target fixtures. To repeat, retain these results and choose fresh disposable `scratch` destination names in copies of the scripts; do not erase retained evidence or user content. The build/test gate runner can rerun directly. Native-host fetch/probe, full suite, minimum Python/platform matrix, remote release and backup restoration remain explicit handoff checks. No additional reviewer ran.
