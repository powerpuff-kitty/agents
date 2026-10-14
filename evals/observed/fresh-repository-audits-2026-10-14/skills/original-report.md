# Independent Skills snapshot audit

Source: `/private/tmp/independent-audit-skills`, detached HEAD `4eb646c4700698fe297f04cadcd2737bc0717cdd`. Initial and final `git status --short` / `git status --porcelain=v1` were empty; `git diff --stat` was empty. No source edits, package installation, host/account configuration, commits, pushes, publication, model calls or live financial/account operations occurred.

This review was performed from the snapshot, repository documentation and focused reproductions, without author conversation, prior audit findings or another agent's conclusions. Evidence is retained under `/private/tmp/fresh-skills-audit-evidence/`.

## Confirmed findings, ranked

### F1 — P2 / medium / high confidence: valid logs can make self-referential byte accounting oscillate and abort

**Location:** `agentic-improvement/scripts/compact_log.py:129–141`, reached from `compact()` at lines 161–162.

`measured()` puts the serialized size, size reduction and budget flag inside the JSON whose size it is calculating. It assumes repeated serialization reaches a fixed point. Some valid inputs have no fixed point: crossing a decimal-digit boundary changes the number of digits in `reduction_bytes`; crossing the budget boundary changes the JSON length of `false` versus `true`. The loop alternates until its 16-iteration limit and raises `LogError`. `main()` then reports `invalid-input` with exit 2 and no compacted record. Increasing the iteration limit does not solve a two-state cycle.

**Reproduction (actual CLI):** retained file `/private/tmp/fresh-skills-audit-evidence/repeated.log` contains `b'x\n' * 344` (688 bytes). Run:

```sh
python3 -B /private/tmp/independent-audit-skills/agentic-improvement/scripts/compact_log.py /private/tmp/fresh-skills-audit-evidence/repeated.log
```

Observed exit **2**, empty stdout and `{"kind":"log-compaction-error","code":"invalid-input"}` on stderr, despite no budget and valid ordinary UTF-8 input. The independent direct API call `compact(b'x\n' * 324, 'synthetic.log')` also raises `output accounting did not converge` (reference length affects the triggering size).

A separate six-byte `hello\n` file at `/private/tmp/fresh-skills-audit-evidence/synthetic.log` fails the actual CLI with either `--budget-bytes 576` or `--budget-bytes 589`. Evidence: `compact-default-repro.json` and `compact-budget-repro.json` in the evidence directory.

**Impact:** otherwise supported logs cannot be compacted. This violates the documented exit contract in `agentic-improvement/references/log-compaction.md:15–17`: valid logs should produce the whole record, with exit 1 for advisory budget overflow rather than an input error. Both literal and packed candidates are measured before selection, so an accounting failure in either candidate aborts the operation.

**Counterevidence:** ordinary inputs and all existing compaction tests pass with a canonical temporary root. This is a boundary-case correctness defect, not data execution or a general losslessness failure.

**Repair/verification:** remove the assumption that variable-width self-accounting always has a fixed point. Choose a representation/accounting convention with guaranteed stable serialized length, or explicitly define accounting outside the measured envelope. Add regressions for a no-budget decimal-boundary cycle and the boolean budget-boundary cycle; verify the full returned record and round-trip data, rather than only that the exception disappears.

### F2 — P2 / medium / high confidence: local tests fail on macOS's default linked temporary-directory path

**Locations:** representative setup `agentic-improvement/tests/test_source_excerpts.py:29–34`; the same pattern appears in Python-outline, required-span and TypeScript-guard tests. `decision-intelligence/tests/test_decision_graph_review.py:235–245` and `251–258` also pass raw `TemporaryDirectory()` paths into the helpers.

The tests use `Path(temp.name)` without canonicalizing the automatically chosen parent. On this macOS host, Python's default temp directory is `/var/folders/k9/0mqqtyn90j31qcqvltrlmww00000gn/T`, whose physical path starts `/private/var/`. The helpers intentionally reject any observed linked ancestor. Thus normal successful-path test fixtures fail with `unsafe-root` / `linked-parent` before the behavior under test is reached.

**Actual checks, from the snapshot root:**

```sh
python3 -B -m unittest discover -s agentic-improvement/tests -p 'test_*.py' -v
python3 -B -m unittest discover -s decision-intelligence/tests -p 'test_*.py' -v
```

Observed: first suite exits **1**, 154 tests, **13 failures / 33 errors / 1 skipped class**; second exits **1**, 34 tests, **2 failures**. Retained logs: `check-1.log`, `check-2.log`.

Rerunning the same commands with `TMPDIR=/private/tmp` gives **exit 0**, 154 tests with the real-compiler class skipped, and **exit 0**, all 34 decision tests. Retained logs: `canonical-check-1.log`, `canonical-check-2.log`.

**Impact:** the ordinary skill-local test invocation is red on a common supported desktop platform and cannot distinguish regressions from temporary-path rejection. This is a test portability defect; it does **not** imply the readers should accept symlink paths.

**Repair/verification:** resolve only normal test-owned fixture paths to their physical locations (`Path(temp.name).resolve()` or a canonical fixture parent). Keep deliberate symlink-refusal tests intact. Run with the host default temp directory as well as an explicitly linked temp-directory alias and confirm success-path tests exercise their intended behavior.

### F3 — P3 / low / high confidence: adapter repository validation cannot detect unlisted files on disk

**Locations:** `adapter-sync/tests/validate_adapter_assets.py:111–116` (`load_bundle`), contrasted with the check at lines 76–78 and `adapter-sync/tests/test_adapter_assets.py:56–58`.

`load_bundle()` constructs the `assets` dictionary exclusively from hard-coded allowlisted filenames. Therefore `validate_bundle()`'s `set(assets) != expected_sources` branch cannot detect an unexpected on-disk asset through the real `validate_repository()` / command-line entrypoint. The unit test injects a dictionary key directly, bypassing the loader, so it does not exercise the shipped path.

**Reproduction:** copy only `adapter-sync/` into a fresh directory under `/private/tmp`, add `assets/unapproved.sh` containing inert synthetic text, and call `validate_repository(copy_root)`. Observed **`[]`**, which the CLI treats as success. Full synthetic inventory and result are retained in `adapter-extra-asset-repro.json`. No original snapshot file was altered and no added file was executed.

**Impact:** an accidentally shipped extra rule/helper/asset can pass a check explicitly advertised as rejecting unexpected shipped assets. Current inspected assets match the intended set; this is a validator coverage defect, not evidence that this snapshot ships an extra or malicious file.

**Repair/verification:** compare the on-disk asset inventory against approved paths (plus the known `assets.json` inventory file), without opening or executing unknown contents. Add an on-disk copied-bundle regression invoking the public repository validator. Preserve the existing rule of never following source paths supplied by an untrusted manifest.

### F4 — P3 / low / high confidence within this snapshot: enrichment documentation claims an evaluator that is not distributed here

**Location:** `design-analysis/references/enrichment.md:34–38`.

The guide says “The repository's synthetic round-trip fixture evaluator rejects altered evidence” and lists other rejection cases. This snapshot contains no design-enrichment evaluator, tests or fixture data. `design-analysis/` contains only `SKILL.md`, its license and two reference files. Repository-wide executable inventory contains four agentic-improvement helpers, one DecisionGraph helper, their tests, and adapter-asset checks; none implements the described enrichment evaluation.

**Trigger/impact:** a user following the standalone copied skill's evaluation instructions cannot locate or run the claimed check and may mistake a documented assertion for available acceptance evidence. This conflicts with the collection's distinction between acceptance specifications and observed outcomes.

**Evidence:** `rg --files design-analysis design-intelligence` and the repository-wide `*.py` / `*.sh` / `*.js` inventory; `rg -n 'evaluat|fixture' design-analysis design-intelligence` locates the unsupported assertion but no implementation. No claim is made that an evaluator does not exist in an external consumer repository.

**Repair/verification:** link the actual owning repository, exact source revision and runnable check if this is external test machinery, or describe these as proposed acceptance cases rather than an existing repository evaluator. Confirm the copied-skill reader can resolve the referenced verification path.

## Scope, sampling and positive evidence

Read the root `README.md` and `INSTALL.md` entrypoints and the local `codebase-audit` procedure/review guides. The snapshot has no root `AGENTS.md` or `.agentic/` router. Reviewed all five executable helper implementations, adapter validation/tests, related routing and helper guides, selected engineering/security/design lifecycle procedures, and the worked financial/crypto/forecast/content methods. This is a broad sampled audit, not certification of every prose instruction or host behavior.

Sampled flows were: selected-evidence capture/compare and unsafe/unavailable input handling; hash-pinned source retrieval and required-span coverage; Python and JS/TS definition navigation; log compaction/restore and budget handling; DecisionGraph dependency grouping and error paths; native adapter bundle loading/validation; skill installation/documentation and standalone resource links.

The standard-library static check validates the presence and simple `name`/`description` shape of frontmatter, matching folder names, per-skill license presence, JSON syntax and local Markdown target existence. It reports **51 skills, 21 JSON files, 125 Markdown files, no issues**. This is a deliberately limited scanner: not full YAML/schema validation, anchor checking, host registration or semantic routing evaluation. Reproducible source and output: `static-check.py`, `static-check.json`.

The adapter suite passes **23 tests** and `python3 -B adapter-sync/tests/validate_adapter_assets.py` exits **0**, printing its explicit host-verification limitation. Retained logs: `check-3.log`, `check-4.log`.

Current primary-reference spot checks corroborated the documented native OpenCode folder discovery model and the DecisionGraph v1 node/reducer shape. They did not reproduce historical host-loading or CLI claims: [OpenCode V2 skills](https://opencode.ai/v2/docs/skills/), [canonical DecisionGraph schema](https://raw.githubusercontent.com/powerpuff-kitty/agentic-harness/main/catalog/schema/decision-graph.v1.schema.json), accessed 2026-10-14. No defect is asserted from those spot checks.

## Actual commands, environment and retained results

All source commands ran from `/private/tmp/independent-audit-skills` unless a full outside-source path is given. Python **3.14.7**, Node **v25.5.0**, macOS. Test subprocesses inherited `PYTHONDONTWRITEBYTECODE=1`; the canonical rerun changed `TMPDIR` only for those processes. No host configuration was changed.

| Command/check | Result | Evidence |
|---|---|---|
| `git rev-parse HEAD` | `4eb646c4700698fe297f04cadcd2737bc0717cdd` | This report |
| `git status --short`, `git diff --stat`, final `git status --porcelain=v1` | Empty | Tool output; source unchanged |
| `python3 -B -m unittest discover -s agentic-improvement/tests -p 'test_*.py' -v` | Exit 1; 13 failures, 33 errors, real-parser class skipped | `check-1.log` |
| Same with `TMPDIR=/private/tmp` | Exit 0; 154 tests, 1 skipped class | `canonical-check-1.log` |
| `python3 -B -m unittest discover -s decision-intelligence/tests -p 'test_*.py' -v` | Exit 1; 34 tests, 2 failures | `check-2.log` |
| Same with `TMPDIR=/private/tmp` | Exit 0; 34 tests | `canonical-check-2.log` |
| `python3 -B -m unittest discover -s adapter-sync/tests -p 'test_*.py' -v` | Exit 0; 23 tests | `check-3.log` |
| `python3 -B adapter-sync/tests/validate_adapter_assets.py` | Exit 0 | `check-4.log` |
| `python3 -B /private/tmp/fresh-skills-audit-evidence/static-check.py` | Exit 0; no sampled structural issues | `static-check.json` |
| Focused compactor CLI repro, default options | Exit 2 for valid 688-byte repeated log | `compact-default-repro.json` |
| Focused compactor CLI repro, budget boundary | Exit 2 at budgets 576 and 589 for valid six-byte log | `compact-budget-repro.json` |
| Copied-bundle adapter extra-asset reproduction | `validate_repository()` returns `[]` | `adapter-extra-asset-repro.json` |

Additional safe source reads used `rg --files`, `rg -n`, `cat`, `sed -n`, `nl -ba`, `wc -l`, `ls -la` and ancestor-entrypoint discovery. Tool output was sometimes truncated during broad concatenated reads; targeted subsequent reads were used for cited locations. No finding depends on the omitted portion of a truncated output. The real-compiler lookup used the test suite's existing `require.resolve("typescript")` probe; it found no compiler in its supported lookup and installed nothing.

## Preferences and unverified areas

No stylistic preferences are promoted to defects. Lack of an independent collection CI workflow is documented and is not itself listed as a defect. No claim is made that trigger overlap, absent optional providers or canonical external contracts are inherently wrong.

Not checked: actual OpenCode/Claude/Cursor/Codex loading, model skill selection/adherence, external CLI lifecycle installation/update/rollback, historical 51-skill loading evidence, real TypeScript compiler integration, minimum Python 3.10 and other operating systems, all external URLs, current financial/legal/security recommendations or comprehensive package vulnerability advisories. JSON `tests/cases.json` files are acceptance specifications, not observed model outcomes. No production, wallet, betting, cloud or account behavior was exercised.

Recommended repair order: F1 accounting correctness, F2 default-environment test portability, then F3's on-disk inventory regression and F4's evaluation provenance. Re-run the affected local checks and the new boundary/loader regressions after fixes; passing current tests alone does not refute the focused reproductions above.
