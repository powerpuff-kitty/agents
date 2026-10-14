# Synthetic experiment decision assessment

**Hold the causal and rollout decision.** The observed treatment conversion fraction is 6% versus 5%, but assigned counts are 900 control / 1,100 treatment against planned 50:50. This allocation discrepancy is a strong diagnostic signal and remains unexplained. Exposure, assignment implementation, guardrails and account-level outcome logs are unavailable. No launch authority is supplied or exercised.

The question is whether this supplied account-level summary supports a favorable experiment decision. The intended hypothesis (treatment improves conversion) is a working interpretation of that question; intervention, target population and practical threshold are unspecified. The supplied primary is converted accounts / assigned accounts within a declared window, but the duration and actual dates are absent. Assignment unit is account. Analysis uses the assigned denominators, resembling intention-to-treat at aggregate level; genuine random assignment, persistent assignment and complete outcomes cannot be verified. Exposure unit/counts are unknown. No exposed-only reanalysis is invented. Exact source revision is SHA-256 pinned in `source-manifest.json`.

| Metric / guardrail | Denominator / window | Practical threshold | Method / uncertainty |
| --- | --- | --- | --- |
| Primary converted-account fraction | Assigned accounts; actual window unspecified | Not supplied | Descriptive aggregate rates; no predeclared outcome method supplied |
| Guardrails | Not supplied | Not supplied | Harm cannot be assessed |
| Assignment balance diagnostic | 2,000 assigned accounts; planned 50:50 | Diagnostic alpha not supplied | Pearson goodness-of-fit; exact binomial corroboration |

Stopping input states fixed horizon with this sample delivered at its scheduled cutoff. That is retained as a fixture assertion; schedule adherence, duration, mature follow-up and repeated looks are not independently verified. Baseline assumptions, sample-size/power/precision plan, exclusions, alpha/tails, multiplicity and outcome test are not supplied. No retrospective confirmatory plan or power estimate is invented.

| Validity check | Actual input / method | Result | Interpretation |
| --- | --- | --- | --- |
| Assignment SRM | Expected 1,000 / 1,000; Pearson sum((observed−expected)^2/expected), df=1 | χ²=20; tail p=0.000007744216431 | Strong discrepancy under planned allocation; unresolved blocker |
| Exact corroboration | Binomial n=2,000, p=0.5; two-sided 2×P(X≤900) | p=0.000008457089536 | Same diagnostic conclusion; not an independent review |
| Aggregate arithmetic | Converted ≤ assigned; counts positive integers | 45≤900 and 66≤1,100 | Arithmetically consistent only |
| Exposure / noncompliance | No logs supplied | Unknown | Cannot establish delivered treatment or ITT/exposure consistency |
| Assignment implementation / identity persistence | Not inspected; no account-level rows | Unknown | Cannot verify randomization, deduplication, repeated accounts or unit isolation |
| Missingness / join loss / timing | Only aggregates; no eligibility ledger or timestamps | Unknown | Cannot establish outcome completeness or mature follow-up |
| Guardrail harms / interference / contamination | No guardrails or relevant records | Unknown | Cannot establish safety, independence or lack of spillovers |
| Fixed horizon / multiplicity | Stopping policy text only | Unverified implementation; multiplicity unknown | No confirmatory interpretation claimed |

SRM formulas: χ²=(900−1000)²/1000+(1100−1000)²/1000=20. For df=1, its asymptotic upper tail is erfc(sqrt(20/2)). Exact binomial uses standard-library integer combinations, so the corroboration does not need a numerical statistics package. Neither p-value determines the root cause. Plausible investigations include bucketing/eligibility, logging, bots, join loss and post-assignment filtering. Do not rebalance, selectively exclude or otherwise repair the assignment sample post hoc merely to improve its ratio.

Assignment → exposure → analysis: control 900 → unknown → supplied assigned denominator 900; treatment 1,100 → unknown → supplied assigned denominator 1,100. These summaries do not independently establish the actual analysis ledger or absence of exclusions. Converted counts are 45 and 66. Rates are 45/900=0.05 and 66/1100=0.06. Absolute difference is **+1 percentage point**; relative difference is **+20%** versus control. These remain descriptive.

An explicitly unplanned illustrative precision calculation uses independent fully observed binomial accounts: SE=sqrt(0.05×0.95/900 + 0.06×0.94/1100)=0.0102005. A normal 95% interval for the rate difference is approximately **−0.999 to +2.999 percentage points**. It assumes valid measurement and independent accounts; the unresolved validity issue means it cannot establish causal lift or practical equivalence. This is not a prespecified outcome analysis, no primary-outcome p-value is claimed, and no favorable-method selection or equivalence claim is made. Without the account-level data, dependence/clustering or missingness sensitivity cannot be calculated. The practical threshold is unknown.

Decision: investigate the assignment discrepancy first, inspect allocation persistence and eligibility joins, reconcile assigned/exposed/analyzed accounts and mature outcomes, and obtain the original metric/window/multiplicity plan and guardrails. Then reassess using the predeclared analysis or transparently designate a future valid test. A corrected ledger or new data could change this answer. Neither a rerun, deployment nor user traffic is authorized by this exercise.

Actual offline methods and outputs are in `calculate.py` and `experiment-calculations.json`. Current online statistical/vendor documentation was not verified because the task explicitly requires offline execution; no vendor runtime semantics or completed live experiment is certified. Generalizability to other accounts/platforms is unmeasured. Own arithmetic corroboration is not independent evidence validation.
