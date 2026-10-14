# Narrow source recheck 2

Initial records are preserved separately in `review-initial.md`, `temporal-drift.json`, and `review-recheck-1.md`. This recheck inspects only the requested fixes against current scoped source, not other reviewers' results. Input identity is `source-hashes-recheck-2.json`; evaluator SHA-256 is `8f81be97ecfeb1bbae7467284e353f048fd98d7af78a7094d783e7fb47fd6683`. Eight files changed since first hash capture: evaluator, evaluator tests, the three case-spec files and three templates. End hashes are in `source-hashes-recheck-2-end.json`; no scoped source changed during this recheck.

## Results

**F1 remains fixed.** All three new discovery tasks still point to `instructions/catalog.md`; explicit mode still stages the assigned role/procedure.

**F2 resolved in source and local preparation probes.** `agents/scripts/behavior_eval.py:40` now puts “Read operating-contract.md first” in the catalog. Line 102 directs the task to read `instructions/operating-contract.md` before optional selection. The file is staged in discovery as before; explicit mode continues appending it to role.md. Independent local synthetic staging confirmed that each of the three discovery cases contains both required paths/instructions. This establishes routing, not that a future model actually reads or follows the contract.

**G1 resolved as a specification and unit-coverage gap.** All twelve cases now have distinct prompts and discriminating criteria, with explicit fixture use/transformation instructions where a variant is needed. Structured reflection separates observed failure, architecture violation, absent evidence and routine success; memory specifies exact stale/superseded/invalidated exclusions, conflict handling, local-only filtering and c1/c2/c3 rejection; agent security specifies indirect injection, forged approval, stored-memory injection and a benign control. Fixture-referenced memory IDs were checked against the supplied fixture. All twelve remain accurately marked `not_run`. These are improved acceptance specifications; this recheck did not execute the twelve model scenarios or validate a materializing runner for all variants.

`agents/tests/test_behavior_eval.py:46-71` now exercises all three new cases in explicit and discovery modes, checks discovery catalog/shared-contract references, asserts the reasoning verdict stays unverified, checks invariant baselines and detects workspace mutations. The full scoped file passed: **5 tests, exit 0**, including six new-case/mode combinations in the added test. The test fixture uses synthetic catalog instructions, so it verifies evaluator mechanics rather than real-skill behavior.

The three report templates now carry appropriate domain evidence: attempt/trigger/correction for reflection, query/include/exclude/curation for memory, and source/sink/control/attack/benign results for agent security. The prior optional usability suggestion is addressed.

## Checks and limits

- Scoped unittest command and captured output: `unit-recheck-2-command.json`, `unit-recheck-2.log` (5 tests passed in 0.957s).
- Independent preparation probe source: `probe-recheck-2.py`; captured evaluator and JSON results under `probe-recheck-2/`. Six current-source combinations passed baseline workspace/instruction invariants; all six deliberately changed fixture inputs were detected. All three discovery outputs reference the catalog and shared contract, and instruct reading the shared contract first.
- Source/spec inventory: `case-spec-recheck-2.json`. No cases were reclassified from not-run to pass.

No remaining actionable defect was found in these narrow corrections. No repository source was written by this reviewer. No package, network, provider, live tool, persistent-memory, production or model/end-to-end action was performed. Source/spec routing and deterministic hash checks do not establish model instruction selection, response quality, privacy/backend enforcement or production reliability. Earlier canonical comparison was not repeated because canonical and main-procedure bytes are unchanged.
