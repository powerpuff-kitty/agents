# Synthetic forward-test review

The reported numerical and finality claims require corrections; none establishes deployed exploitability, actual liquidation, calibrated forecasts, realized profitability or final settlement. This is an offline review of `input.json`, classified as synthetic, using the six supplied skills and their method guides/templates. Fixture field paths below identify evidence. All numerical conclusions are conditional on its declared models and metadata.

## Chain records

`chain_data.raw_amount / 10^declared_verified_decimals = 4,500,000 / 10^6 = 4.5` tokens. The reported 4,500,000-token amount confuses raw integer units with tokens. “Verified” decimals are supplied metadata, not independently verified here.

For chain 111, identify an event by `(chain_id, block_hash, tx_hash, log_index)` under the fixture's event-record convention. The two A/T1/0 rows are one duplicate event; B/T2/0 is noncanonical; C/T3/0 failed; the finalized A/T1/0 row on chain 222 is a separate chain and outside the requested count. Thus there is **one unique successful canonical candidate event and zero finalized candidates on chain 111**, contradicting the reported five finalized transfers. The surviving event is explicitly unfinalized. Without ABI/event signatures, token/address fields, block heights, source/query identity, observation time or chain-specific finality policy, these flags do not independently authenticate a real transfer. `starting_balance` and `attribution_source` are null: neither a full balance nor an owner's identity follows from these records. See onchain method, “Snapshot and identity” and “Units, logs and reconciliation.”

## Contract excerpt

`contract.withdraw_sequence` reads the balance, clears it, then makes the external call and requires success. Clearing the balance before interaction is counterevidence to the alleged same-balance repeated withdrawal: callback reentry alone does not restore the cleared entitlement. The external call does **not prove reentrancy vulnerability**. This is not a finding that all reentrancy or other vulnerabilities are absent: alternate entrypoints, dependencies, storage and complete implementation are missing.

`upgradeTo(next) external onlyOwner`, the effective equality check and the accepted architecture describe intentionally authorized owner upgrades. This establishes an administrator trust assumption, not a demonstrated authorization bypass. A compromised or malicious owner could change implementation behavior; reachability/impact beyond that needs actual proxy design and state. There is no proxy address, deployment match, compiler or bytecode, so the claim about a proven vulnerable deployed proxy is unsupported. No compiler, scanner, exploit or execution test ran. See contract method, “Evidence before severity” and “Source-to-state checks.”

## DeFi scenarios

Under `defi.model`, initial HF is `240 × .8 / 120 = 1.6`. A collateral-only 25% fall leaves collateral 180 and HF **1.2**, not .5. Debt and threshold are held constant. HF reaches 1 at collateral 150, a 37.5% fall from 240; below that value the modeled HF falls below 1. The supplied shock does not cross that boundary, and no liquidation transaction or event is supplied. “An actual liquidation occurred” is unsupported even if another scenario crossed a threshold. Close factors, bonuses, oracle/execution conditions and costs are unknown.

For the declared fee-free full-range constant-product LP model, `2√9/(1+9) = .6`: LP value is 60% of the value of holding the initial assets, or **−40% relative to that benchmark**. The numerical −.4 matches relative underperformance, but `reported_lp_usd_return` mislabels it as an absolute USD return. Absolute prices/numeraire and initial portfolio valuation are missing. This does not model concentrated liquidity, fees or executable exit prices. See DeFi method, “Lending example” and “AMM/LP example.”

## Quotes and hypothetical payoff

The fixture declares comparable exhaustive two-outcome decimal back quotes at one time. Raw probabilities are `1/2.4 = 5/12` and `1/1.6 = 5/8`, summing to `25/24`. Overround is `1/24`, or **4.1667%**. The reported probabilities are raw implied values, not margin-free values. Proportional normalization gives **.4 and .6**; this is one margin-removal assumption, not identified true probabilities.

With the independently supplied assumption `p=.45`, precommission unit EV is `.45×2.4−1 = .08`. Under the explicit isolated-bet commission model, winning net profit is `(2.4−1)×.92 = 1.288`, loss is 1, and fee-adjusted unit EV is `.45×1.288−.55 =` **.0296**. The reported .08 omits commission. Break-even probability is `1/2.288 = 125/286 ≈ .437063`; the narrow modeled surplus depends on the unsupported probability assumption. No fills, liquidity, actual bet or realized return is evidenced. See odds method, “Complete-market margin” and “Conditional expectation and commissions.”

## Forecasts

Use the declared unit, one pre-outcome snapshot per distinct question, with equal weights. Q1–Q4 are resolved; Q5 is unresolved and excluded, not scored as zero. Squared errors are `.01, .49, .36, .01`; binary mean Brier is **.87/4 = .2175**. The same-sample constant-.5 baseline is .25, giving Brier skill `1−.2175/.25 = .13`. The reported .302 is reproduced by incorrectly assigning Q5 outcome zero: `(.87+.64)/5=.302`; this is a possible error mechanism, not proof of how the report was produced.

Descriptive bins `[0,.5)` and `[.5,1]` contain two questions each, with mean predictions .25 and .8, versus observed frequency .5 in each. Two observations per bin provide very weak calibration evidence; bin choice is illustrative, and distinct questions do not prove independence. Four resolved questions, unresolved-case selection and no issue/outcome timestamps prevent a general calibration claim or verification of the stated pre-outcome timing. Fitting a calibrator on the same four evaluation labels invalidates an untouched out-of-sample claim. Score improvement establishes no trading profitability; prices, decisions, stakes, costs and realized payouts are absent. See forecast method, “Calibration and uncertainty” and “Fitting and claims.”

## Settlement matrix

| Market | Supplied threshold at 11:00 UTC | Value 150 | Conditional event result |
|---|---|---|---|
| A | At least 150 | Inclusive boundary satisfied | YES |
| B | Strictly above 150 | Exclusive boundary not satisfied | NO |

These contracts differ materially at the supplied boundary. Both are trading-closed with resolution only **proposed**; dispute/final status is null. Neither is evidenced as finally settled YES. Results above apply to the supplied official value and snippets; actual date, market IDs, full rule hierarchy, revisions, void/refund terms, evidence timestamps and finality proof are absent. See settlement method, “Synthetic comparison” and “Resolution versus event truth.”

## Skill assessment and verification boundary

The six skills provide sufficient instructions to challenge these claims without executing financial actions. They explicitly separate source versus deployment evidence, model versus execution, scores versus economic outcomes and proposal versus finality. No substantive conflicting instruction was encountered. Remaining judgment calls are chain-specific event/finality semantics, margin model, calibration bins/uncertainty and complete settlement precedence; the guides require these assumptions to be disclosed rather than supplying universal defaults.

Exact arithmetic, full file inventory/hashes, Python version and results are in `calculate.py` and `calculations.json`; actual commands and preservation checks are in `checks.md`. No network, accounts, keys, installations, transactions, bets or resolution actions were used. Source and fixture preservation were checked by SHA-256. Host loading, automatic routing and separate acceptance-case specifications were not tested; this report does not certify those or any real system.
