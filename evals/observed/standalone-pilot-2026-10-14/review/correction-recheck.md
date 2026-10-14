# Correction recheck

The corrected candidate meets the requested source-archive preparation/full-test requirement in the exercised environment. **All 45 declared tests passed** from a disposable copy without `.git`, alongside validation, documentation and both adapter build/check gates. The runner correction fixes failed-subcommand exit propagation and detects changed/finally dirty source, but **one dirty-start gap remains**. Original reports and reviewed inputs are preserved.

## Remaining P2 runner finding: dirty initial source can be hidden by a successful command

Reviewed script: `../pilot-tooling-correction/run_gates.py`, SHA-256 `0eb7db697ba10b945e683a98d44bbd79ca1428caf6811f1b11526a13e078f47e`. It captures `status_before` at line 26 but its exit predicate at line 60 checks only failed subprocesses, tracked-byte changes and `status_after`.

Concrete synthetic reproduction under `correction-recheck-artifacts/runner-probes/dirty-untracked-before-removed`: a committed one-file test repository begins with an untracked `owner-draft.txt`. The selected harmless test command deletes that synthetic untracked file and returns zero. Captured before-status is `?? owner-draft.txt`; after-status is empty; tracked hashes are unchanged; runner incorrectly returns **0**. This violates the supplied requirement that dirty reviewed source cause nonzero exit and could conceal loss of pre-existing untracked work. No user/source file was deleted: the file existed only inside the disposable synthetic test fixture.

Correction direction: include initial dirty status in the failure decision, preferably reject that precondition before running gates. Add this dirty-start/removed-untracked negative case. This is a review finding; no original tooling correction was edited.

Counterevidence and resolved portion: independent probes return the expected results for clean successful command (0), failed subcommand (1), modified tracked source (1), initially dirty tracked source remaining dirty (1), and newly untracked content remaining after checks (1). Provided positive/negative raw logs also match true→0 and false→1; AST comparison confirms their execution/aggregation code matches the corrected script after removing only command-list configuration. The normal retained run records all 11 commands at zero, clean before/after source and unchanged tracked hashes. The residual finding does not turn those actual passing records into failures; it prevents calling the broader dirty-source requirement completely satisfied.

Exact probe commands, before/after identity, process/subcommand exits, copied-script hashes, stdout/stderr and raw result files are retained under `runner-probes/` and indexed by `runner-probes.json`. All runner control copies change only the command-list AST; identity/execution/exit logic remains unchanged.

## Source correction and independent full-suite execution

Candidate identity is the 861-file `candidate-source-sha256.json` manifest, SHA-256 `77677bfad7d16baf096d0e52030d3bee23cedc87d973ff65bc76e9a79dc49315`. No commit identity is inferred for this supplied source snapshot.

`behavior_eval.py` now checks for its source root's own `.git` before resolving HEAD. From a Git-free source tree it retains null revision plus workspace/instruction/task/preparer hashes. This directly fixes the archive-copy failure recorded in the earlier pilot review without guessing a containing repository's revision.

Executed in `correction-recheck-artifacts/source` (a byte-identical disposable copy, no `.git`), Python 3.14.7, bytecode disabled, TMPDIR inside the review artifacts:

| Actual command | Result |
|---|---|
| `python3 -B scripts/validate.py` | Exit 0 |
| `python3 -B scripts/check_docs.py` | Exit 0 |
| `python3 -B scripts/build.py --adapter portable` | Exit 0 |
| `python3 -B scripts/build.py --adapter opencode` | Exit 0 |
| `python3 -B scripts/build.py --adapter portable --check` | Exit 0 |
| `python3 -B scripts/build.py --adapter opencode --check` | Exit 0 |
| `python3 -B -m unittest discover -s tests -v` | Exit 0; **45 tests, OK**, including previously excluded fixture-commit tests and all three new regressions |

Raw logs are `logs/gate-01.log` through `gate-07.log`; exact argv/cwd/exits are in `gates.json`. Synthetic fixture commits were explicitly authorized for this recheck and occurred only inside disposable test directories. No reviewed source or actual repository was committed or changed.

Additional independent preparation check: copied the candidate beneath a synthetic parent repository with a real test-only parent commit, while keeping the extracted source itself `.git`-free. Prepared **all eight supported cases in explicit and discovery modes (16 preparations)** using synthetic local skill fixtures. Every preparation succeeded, source_revision and skills_revision remained null, the preparer hash matched the actual candidate script, and input/instruction/task hashes were present. The synthetic parent commit was never used as source provenance. `preparation.json` and retained per-preparation initial records pin these observations. This tests the parent-revision boundary beyond the new unit test's nonrepository source directory.

## Update/downgrade regression assessment

`candidate-source/tests/test_workflows.py::test_source_update_and_downgrade_preserve_backups_and_local_edits` passed in the full suite. It exercises the actual CLI/compiler against a copied source tree, rather than mocking the rendered update. It checks managed v1→v2 content/state backup bytes, profile/state private modes, unchanged-repeat bytes/mtimes, local-customization refusal with no installation writes, and v2→v1 restoration plus backup/unrelated profile preservation.

The test's deliberate restoration of its own synthetic local customization before downgrade is consistent with the existing install contract: edited content remains a conflict until the owner deliberately resolves it; no automatic overwrite or pruning is introduced. It does not claim host loading, a historical release upgrade, command-update completeness or a full manual recovery rehearsal. No new contract concern was established in this test.

## Separate correction of the initial archive-member wording

The original `pilot-review.md` described 1,268 “regular” members. Inspection of the actual retained `pilot-repro/candidate.tar` shows:

| Member class | Count |
|---|---:|
| Regular files | **860** |
| Directories | **408** |
| Symbolic links | 0 |
| Hard links | 0 |
| Other | 0 |
| Total members | **1,268** |

The regular-file count equals the original 860 tracked-file identities. Archive SHA-256 remains `6f4f6f64d550e33f4c0e44ef2e45026d0c76d8eab002460793319e0aa5110cdf`. This record corrects that wording; the original report and archive remain unchanged. Exact classification is in `archive-member-classes.json`.

## Preservation and limits

All 861 candidate files still match the supplied manifest; copied tracked source bytes are unchanged after execution. All 2,727 supplied tooling files outside `.git` internals match the review-start snapshot. Initial case/pilot report retention hashes still match. `preservation.json` records identities; `correction_recheck.py` and `correction_runner_probe.py` retain exact reproductions. One grouped read used the wrong cwd for RELEASING.md and returned a missing-path error; the correct candidate document was immediately read with the explicit review cwd. No evidence claim depends on that failed read.

This is a correction recheck in the existing independent reviewer session, not a new independent session or authenticated exhaustive action trace. No root narrative, desired verdict, network, personal configuration, installation, account, publication, tracker or production operation was used. Git tests used explicit synthetic identity and disabled global/system Git configuration. Native-host/CI execution, minimum Python/platform coverage, remote publication and manual restoration remain unverified. The earlier full-suite gap is resolved for this candidate/environment; the remaining runner finding and those unrelated limits stay explicit.
