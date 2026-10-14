# Separate v2 runner recheck

**The v1 dirty-start/owner-draft finding is resolved in v2.** The clean-source preflight refuses the deletion command before it runs, records the initial identity and preserves the synthetic owner draft's exact bytes, mode and mtime. Failed commands, changed tracked source and final dirty status produce nonzero exits in the tested paths. One lower-priority initial-identity recording gap remains for an already deleted tracked file.

Reviewed entrypoint: `../pilot-tooling-correction/run_gates.v2.py`, SHA-256 `578b32e2ea22836e2856b649ab562d1370f9e0c8c4d6b8ec767707776fcbe9e4`. Historical v1 and its recheck remain unchanged. This assessment uses the supplied clean-source gate-runner contract; it makes no sandbox or comprehensive action-authentication claim.

## Independent probes

Only command-list AST configuration was changed in disposable copies. AST comparison verifies the preflight, identity capture, execution/logging and aggregation match v2 exactly. Each project is a synthetic test-only Git repository under `correction-v2-artifacts/`; no reviewed source or actual repository was committed or changed.

| Input | Runner result | Evidence |
|---|---|---|
| Clean source, successful command | 0 | Initial/final identity, command log and result JSON retained |
| Failed command followed by successful command | 1 | Both command logs retained, exit records `[1,0]`; source unchanged |
| Successful command changes tracked source | 1 | Changed tracked hash and dirty after-status retained |
| Initially dirty tracked file | 1 before test commands | Initial identity recorded, zero command logs, bytes/mode/mtime unchanged |
| Successful command leaves untracked content | 1 | Final dirty status and command log retained |
| Initially untracked owner draft; configured command deletes it | **1 before test command** | Initial identity recorded, zero command logs, draft preserved exactly |
| Initially deleted tracked file | 1 before test commands | Source preserved and no commands run, but initial identity record missing; see finding below |

Raw scripts, stdout/stderr, identity JSON and command logs are kept in each named probe directory; `results.json` indexes actual statuses and copied-script hashes. The supplied three v2 positive/negative/owner-draft raw probe sets were also inspected and their aggregation/preflight AST matched the current v2 source. They support the stated controls; the independent probes add tracked-change/final-dirty and missing-tracked-file coverage.

## P3: a deleted tracked file prevents initial identity retention

Location: `run_gates.v2.py:23` hashes every `git ls-files` path before building/writing initial identity or reaching the dirty preflight. If a tracked file is already deleted, `read_bytes()` raises `FileNotFoundError`. The runner returns 1 without running commands and preserves the existing work, but `logs/source-before.json` is absent. This leaves the explicit “record initial identity” requirement incomplete for this ordinary dirty-source state.

Reproduction: `correction-v2-artifacts/dirty-deleted-tracked-before/` commits a synthetic fixture file, deletes it before the runner starts, then configures `/usr/bin/true`. The complete traceback is in `stderr.txt`; no gate logs/results or initial identity are produced. The fixture remains unchanged by the runner.

Correction direction: capture revision/status and record missing/unreadable tracked paths explicitly before refusing dirty source; unavailable bytes should not receive fabricated hashes. Alternatively, write a minimal initial identity before attempting tracked-file hashing. Add this negative case alongside the owner-draft regression. This is an evidence-retention issue, not a renewed failure to refuse dirty work or evidence that an unsafe command ran.

## Preservation and limits

`inputs.json` pins the exact v2 source/checks/note and original v1 correction report/evidence manifest; all still match. Original case/pilot review retention hashes also match. `correction_v2_probe.py` is the exact reproduction driver. Git fixtures use explicit test identity with global/system config disabled. No network, accounts, personal configuration, installations, publication, trackers, production operations or extra reviewer/model session occurred.

The 45-test source-archive pass and 16 null-revision preparation checks remain the separate results in `correction-recheck.md`; they were not rerun for this runner-only change. Native host/platform/minimum-Python/release/restoration limits from the earlier review remain unchanged. No original report or finding was rewritten.
