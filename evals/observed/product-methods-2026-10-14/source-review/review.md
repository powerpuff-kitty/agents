# Independent public catalog source review

Reviewed 2026-10-14. Scope: seven proposed product/mobile/research skills; the changed test-engineering browser/recovery guide, fixture and acceptance cases; performance-audit recovery guide and hook; the eight changed focused-procedure hooks in Agents. Adjacent product-design/competitive-research routing and Skills README were inspected for context. Repositories remained read-only. No other reviewer reports or authoring scripts were read. No network, accounts, packages, SDKs, real participants, live collection, production operations, or personal configuration were used.

The review request is retained in `request.md`. `inspected-files.json` contains absolute paths, SHA-256 hashes and byte sizes for 65 source files. `source-stability.json` confirms those files were unchanged during the retained check run. The reviewer is a separate delegated session; this is a source-informed review, not a blinded model evaluation. Acceptance specifications were inspected as source and were not relabeled as observed model outcomes.

## Actionable findings

### F1 — P2: Empty evidence receives the helper's successful unchanged exit

Locations: `/Users/tcsntcsn/TCSN/skills/competitor-monitoring/scripts/compare_snapshots.py:33`, `:40`, `:73`, `:90`, `:141`; documented contract `/Users/tcsntcsn/TCSN/skills/competitor-monitoring/references/method.md:23`.

Both source and fact inventories allow zero entries. Comparing two empty source inventories, or the same `ok` source with empty fact inventories on both sides, produces `items: []` and exit 0 because the final `any(...)` evaluates false. The guide defines exit 0 as structurally unchanged **comparable observations**. These inputs supply no comparable observations. An extraction failure or uninitialized baseline can therefore look like a clean unchanged run when a caller follows the documented exit contract. The JSON explicitly disclaims factual verification, but it does not flag this absence of evidence.

Actual reproduction: the independent CLI probes retained under `probes/empty-inventory-*` and `probes/empty-facts-*` both exited 0 with an empty item list. Exact argv/stdout/stderr are in `commands-results.json`. This is an observed local helper result, not an inference about a running monitoring service.

Suggested fix: return an explicit `insufficient_evidence`/`coverage_gap` item and exit 1 when there are no comparable facts, or reject empty observation inventories as invalid with exit 2. Decide and document the intended semantics of an intentionally empty watchlist separately. Add both CLI regressions; ensure a nonempty unchanged comparison still exits 0.

### F2 — P2: Recovery extension is absent from the skill's selection contract

Locations: `/Users/tcsntcsn/TCSN/skills/performance-audit/SKILL.md:3`, `:9`, `:13`, `:19`, `:25`, `:35`, `:39`; related hook `/Users/tcsntcsn/TCSN/agents/agents/performance-engineer/instructions.md:60`.

The new context hook explicitly supports requested reliability/restoration/recovery measurements, and the agent hook routes reliability questions there. However, the public description still selects only performance bottlenecks, latency, throughput and resource concerns; the required input is still a performance concern. Objective, main procedure, output and completion also remain exclusively about bottlenecks and demonstrating improvements. A standalone request to assess durable recovery/restore readiness therefore does not match the advertised skill trigger, and loading the skill introduces an unrelated optimization/comparable-improvement requirement alongside the recovery guide.

This is a source/spec routing finding. No host selection or model-adherence run was performed, so an actual missed invocation is not claimed.

Suggested fix: include requested reliability/recovery measurement in the frontmatter and inputs, and explicitly branch the procedure/output/completion for a scoped recovery assessment or unexecuted plan. Keep generic incident postmortems with incident-review. Add a recovery-only acceptance scenario that does not require optimization or an invented owner target. Verify host selection separately if that is a release claim.

## Lower-priority usability observations

- `/Users/tcsntcsn/TCSN/agents/agents/feature-developer/instructions.md:57` and `:66`, and `/Users/tcsntcsn/TCSN/agents/agents/quality-engineer/instructions.md:77` and `:86`, each contain two consecutive sections named `Focused procedures`. Merge the appended hook into the existing section. The content is compatible; this is avoidable navigation/repetition, not a behavior blocker.
- `/Users/tcsntcsn/TCSN/skills/product-experimentation/SKILL.md:38` unconditionally says `Scientist owns design`, although this is a portable standalone procedure and the rest of the role dependencies are conditional. Prefer the task's assigned experiment/design owner, mentioning scientist only when such a role exists. This avoids implying a mandatory installed role for solo skill users.
- The competitor-monitoring `missing-page` acceptance case describes an omitted fact, but the bundled baseline/current snapshots only demonstrate a changed price, cosmetic text and an unavailable source. The helper unit suite does exercise an omitted fact. Either point that case at an explicit omitted-fact fixture or add one to the public example so its manual exercise is complete. This does not invalidate the passing unit test.

## Source and specification assessment

The seven core skills are reasonably compact (about 300–375 words each, with focused method references) and divide responsibilities coherently: collection contracts, descriptive metrics and causal experiments; initial landscapes, repeated evidence comparison and opportunity sizing; participant evidence and native delivery. Their shared scope/evidence language is useful for independently installed procedures rather than excessive boilerplate. No broad trimming is warranted.

Instrumentation covers identity scope, replay versus genuine repeat activity, event/ingestion time, collection eligibility, unauthorized SDK/vendor changes and transport reconciliation. Analytics explicitly covers window maturity, invalid denominators, retention definitions and noncausal interpretation. Experimentation covers assignment/exposure/analysis distinctions, clustering, SRM, peeking, multiplicity, guardrails and practical thresholds. User research preserves said/did distinctions, quote restrictions, negative cases, sample limits and planned versus executed sessions. Market research preserves buying units, overlap, period/currency assumptions, reach and demand uncertainty. Native delivery distinguishes process state from durable intent and simulator/device/distribution evidence, and does not fabricate server idempotency guarantees. Browser/recovery guidance correctly binds visual evidence to route/state/readiness, baseline review, retry artifacts and actual durable restoration.

All eight agent additions preserve task scope, available-method fallbacks and the distinction between a handoff and a real scheduler, real participant access, production collection or distribution. Apart from F2 and the low-priority formatting/role observations, no additional routing or scope defect was identified. The public helper is standard-library-only, bounded by input size/inventory limits, treats input text as inert, validates duplicate keys/nonfinite values/dated source order, and has no network/write/notification operations.

## Actual local executions

Full commands, environment overrides, exit codes, stdout and stderr are retained in `commands-results.json`; the reproducible review runner is `run_checks.py`.

- `python3 --version`: exit 0; Python version is retained in the command log.
- From Skills, `python3 -B -m unittest discover -s competitor-monitoring/tests -v`: exit 0, eight tests passed. `PYTHONDONTWRITEBYTECODE=1` avoided repository bytecode writes and `TMPDIR` pointed inside this review directory.
- Helper CLI on supplied baseline/current snapshots: exit 1 as expected for the observed price change and unavailable source; cosmetic plan-name text was unchanged. No retrieval or alerts were claimed.
- Independent empty-inventory and empty-facts CLI probes: both exit 0, reproducing F1.
- Review-runner JSON parse and relative Markdown-link check: 18 JSON files parsed; no missing relative file targets in the 65-file scope. These are source checks only; URLs were not fetched.
- Review-runner synthetic fixture arithmetic: instrumentation finds a duplicate replay, missing `occurred_at`, and unexpected `email` property without copying its value. Funnel data has eight rows, seven unique events, three mature entrants and one mature converter; D is immature and E has no entry. Experiment fixture has descriptive rates 5% and 6%, assignment chi-square 20 (one degree of freedom; approximately 7.74e-6 diagnostic p), with mechanism/exposure/guardrails and concrete outcome window unverified. Market fixture has 3,500 distinct hypothetical buying units and illustrative annual list-price revenue of USD 3.6–3.7 million only under the explicit one-package-per-overlap assumption. These calculations are retained in `fixture-arithmetic.json`.

The synthetic research, browser/recovery and native scenarios were reviewed as data. They support findings/plans, not executed participant sessions, browser traces, durable restores or device results. Acceptance-case statuses remain `not_run`. No general catalog validator, host registration, model-adherence evaluation, full browser/build check, external-source freshness check or production verification was run. This review makes no certification claim for those layers.
