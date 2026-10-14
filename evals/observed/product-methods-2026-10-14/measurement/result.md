# Offline measurement methods exercise

Completed three fresh synthetic-data procedure runs. Source repositories and fixtures remained unchanged; outputs are confined to this new temporary directory.

| Procedure | Supported result | Detailed evidence |
| --- | --- | --- |
| Tracking contract / payload QA | 4 rows: 2 schema rejections, 1 exact replay; 1 unique locally admissible payload. Real emission/business success unverified. | [Tracking report](instrumentation-report.md), [calculations](instrumentation-calculations.json) |
| Product funnel | 8 raw rows → 7 unique events → 4 entrants → 3 mature users → 1 mature conversion: **33.33%**. One immature user is separately reported. | [Funnel report](analytics-report.md), [unit ledger](analytics-calculations.json) |
| Experiment | 5% vs 6% conversion (+1 percentage point); 900/1,100 assignment split versus planned 50:50 gives χ²=20, diagnostic p≈7.74×10⁻⁶. **Hold causal/rollout decision** pending validity investigation; exposure and guardrails unavailable. | [Experiment report](experiment-report.md), [calculations](experiment-calculations.json) |

Reproduce: `python3 /private/tmp/measurement-methods-forward-2026-10-14/calculate.py`. Standard-library execution exited 0; source/copy SHA-256 comparisons and local assertions passed. [Repeat-run checks](verification.json), [artifact hashes](artifact-hashes.json), [actual output](run-output.json), [runtime](runtime.json), [exact source hashes/copies](source-manifest.json), [verbatim task](task.md), and [actions and unavailable checks](actions.md) are retained.

Only relevant public skill/method/template instructions, the two role instructions/shared contract, and the three raw synthetic inputs are copied. No cases, author/reviewer notes, network, installed packages, accounts, production actions, commits or publication were used. Independent review, full behavior-case evaluation and live collection/experiment validation were not performed. These are bounded supplied-data results and author self-checks.
