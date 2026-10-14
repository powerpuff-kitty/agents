# Independent measurement-output review

No material substantive error was identified in the three retained reports. Independent calculations from their retained synthetic fixtures reproduce their headline results and decision limits. This conclusion applies to the reviewed snapshot and bounded exercises; it does not certify a live collector, population funnel or experiment.

| Output reviewed | Independent result | Disposition |
| --- | --- | --- |
| `instrumentation-report.md` and `instrumentation-calculations.json` | 4 raw payloads; 3 event IDs; 2 shape-valid rows sharing e1; 1 valid unique event. Fixture index 2 lacks `occurred_at`; index 3 contains a field outside the allowed list. | Supported. The report labels its stricter equality/type checks and batch deduplication as local assumptions, separates unique events from people, and does not claim actual signup completion or collection. |
| `analytics-report.md` and `analytics-calculations.json` | 8 rows → 7 unique events → 4 entrant units → 3 mature and 1 immature → 1 mature converter, or 1/3. A converts at +24h; B's +72h is outside the window; C has no recorded conversion; D has only 24h follow-up; E has no entry. | Supported. The report retains D's censoring, excludes E without inventing entry, labels 1/4 incomplete and the 25%–50% eventual bound conditional, and avoids causal/population claims. |
| `experiment-report.md` and `experiment-calculations.json` | Expected 1,000/1,000 vs observed 900/1,100; Pearson χ²=20, df=1, upper-tail p≈7.744216431×10⁻⁶. Exact two-sided binomial p≈8.457089536×10⁻⁶. Rates 5% and 6%; +1 percentage point, +20% relative. | Supported. Unresolved allocation discrepancy, absent exposure/assignment details, outcome-window detail and guardrails justify holding causal/rollout conclusions. Neither statistic identifies the cause. |

Thirty-seven numeric/row/ledger comparisons matched. Independent effect arithmetic used exact fractions, the chi-square tail used `erfc`, and the exact binomial check summed integer combinations under n=2,000 and planned p=0.5. The illustrative independent normal interval uses z=1.959963984540054; the author's endpoints are consistent with z rounded to 1.96. Their sub-0.0001-percentage-point difference is harmless and does not affect the reported conclusion. Both analyses label this unplanned independent-binomial precision calculation as unable to establish valid causal lift or equivalence.

## Finding R1: mutable-source coupling limits later replay

Severity: low; reproducibility/portability limitation, not an arithmetic or original-snapshot defect. The reports direct readers to `python3 calculate.py`; the review request states that script checks current mutable role sources. This review did not read or execute it, because authoring scripts were excluded and a target-directory execution might rewrite reviewed artifacts. The reported guarded-command failure was therefore not reproduced.

Source drift itself is confirmed by independently hashing current original paths against the retained manifest. These three originals now differ from their retained copies:

| Source | Retained SHA-256 | Current SHA-256 |
| --- | --- | --- |
| `product-experimentation/SKILL.md` | See the exact pair in `reviewed-hashes.json` | Changed |
| `agents/agents/data-analyst/instructions.md` | See the exact pair in `reviewed-hashes.json` | Changed |
| `agents/agents/scientist/instructions.md` | See the exact pair in `reviewed-hashes.json` | Changed |

All 15 retained source copies still match the declared historical hashes. Thus the original successful source checks remain historical evidence for that pinned snapshot; current drift does not disprove them. A future maintainer should separate historical-copy replay from live-source drift detection so the retained computation remains reproducible after legitimate instruction changes. No author artifact or original source was rewritten. This review supplies its own `replay.py` using retained input copies and records drift separately.

## Evidence and scope

`independent-calculations.json` contains the independently derived payload decisions, per-unit funnel ledger, formula results and missing-evidence fields. `comparison.json` records the 37 successful checks, verifies 28 retained artifacts against the author's hash inventory, and confirms that all 29 selected reviewed originals remained unchanged during review. `reviewed-hashes.json` identifies every reviewed file and all current-versus-retained source pairs. The excluded authoring script was neither read, copied, hashed independently nor executed; its string entry in the author's hash inventory was incidental provenance, not code review.

No expected answers, behavior-case files or author/reviewer notes were read. Inputs and public procedure/role instructions were inspected before the report bodies, and independent replay output was written before reading those bodies. The reviewer did not author these three measurement outputs. This is an independently executed cross-output review; clean history-free host isolation is not asserted. No further reviewer was spawned, and lack of additional findings is not exhaustive coverage proof.
