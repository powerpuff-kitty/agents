# Final bounded v3 runner recheck

**The v2 initial-identity finding is resolved in v3 for the requested case.** An initially deleted tracked file now produces a retained initial identity, explicit unavailable hashes and nonzero refusal before any gate command executes. Clean success/failure behavior remains correct. No new concern was established within these three bounded probes.

Reviewed script: `../pilot-tooling-correction/run_gates.v3.py`, SHA-256 `c17c839155847f5d59ab3560fab1658c54753a96d97aa865178b739addaf6d82`.

| Independent probe | Observed result |
|---|---|
| Clean source; `/usr/bin/true` | Runner 0; source identity and one successful command log/result retained |
| Clean source; `/usr/bin/false` | Runner 1; source identity and one failed command log/result retained |
| Initially deleted tracked fixture file; configured gate writes a sentinel | Runner 1; source-before.json records the actual synthetic fixture revision and `D fixture.txt`; `tracked_sha256` is null and `hash_status` is `not_collected_dirty_source`. No command log/results or gate sentinel exists; deleted-file state remains unchanged. |

The dirty-input record represents unavailable hashes explicitly rather than inventing bytes or a successful collection. It is written before the refusal. The recorded revision is verified against the actual synthetic test repository and is not candidate-source provenance.

Reproduction driver: `correction_v3_probe.py`. Raw copies, stdout/stderr, identity and command logs are under `correction-v3-artifacts/{clean-success,clean-failure,initially-deleted-tracked}/`; `results.json` retains exact outcomes/identities/script hashes. Only command-list AST configuration was changed in probe copies; comparison confirms all identity/preflight/execution/aggregation logic matches v3. Each probe runs in its own disposable synthetic Git fixture under review/, with explicit fixture identity and global/system Git config disabled.

`inputs.json` pins v3 and every earlier report; all hashes still match. Earlier reports, candidate snapshots and v1/v2 scripts were not changed. No full-suite or unrelated check was repeated: the separate 45-test source-archive result remains in correction-recheck.md. No network, installations, personal configuration, actual-repository commit, publication, tracker or production operation occurred. This is a scoped gate-runner check, not a sandbox or exhaustive action-history certification.
