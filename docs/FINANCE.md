# Financial research and risk

The finance pack adds 3 profiles and `/team-finance`. It depends on science-data,
which depends on core, so a finance export contains 21 profiles and 11 workflows.
The full catalog contains 35 profiles, 20 workflows and 7 packs. These counts
refer to rendered sources, not observed model outcomes or live financial services.

## Responsibilities

| Profile | Owns | Adjacent boundary |
| --- | --- | --- |
| [financial-analyst](../agents/financial-analyst/instructions.md) | Statements, budgets, cash-flow/valuation models, financial assumptions and the consolidated research report | Trading simulations belong to quant-researcher; holdings/exposure risk to portfolio-risk-analyst. |
| [quant-researcher](../agents/quant-researcher/instructions.md) | Point-in-time strategy research, backtest assumptions, costs and out-of-sample/trial evidence | Company reporting/valuation and current holdings risk are separate analyses; execution engineering is not provided. |
| [portfolio-risk-analyst](../agents/portfolio-risk-analyst/instructions.md) | Approved holdings snapshots, NAV/exposures, concentration, liquidity and stress/model risk | A risk estimate or limit breach does not execute a portfolio change. |

These roles can analyze relevant stock, fund, crypto-asset or other instrument data
when the actual data/method supports it. A profile name does not supply asset-specific
market data, derivatives pricing, an account connection, cryptography expertise or
betting-model validation by themselves. Optional [crypto](CRYPTO.md) and
[forecasting](FORECASTING.md) packs now supply those focused research methods.

## Reusable procedures

Procedures live independently at the AI Skills repository root. Install them separately using
its [installation guide](https://github.com/powerpuff-kitty/ai-skills/blob/main/INSTALL.md).
The role can perform bounded direct checks if a skill is unavailable; it does not
silently install it or claim host loading.

| Skill | Useful detail |
| --- | --- |
| [market-data-validation](https://github.com/powerpuff-kitty/ai-skills/tree/main/market-data-validation) | Field/time/adjustment contract, point-in-time fundamentals, corporate actions, instrument/universe coverage and a report template. |
| [financial-model-review](https://github.com/powerpuff-kitty/ai-skills/tree/main/financial-model-review) | Formula/source review, statement/cash reconciliation, discounting, valuation bridges, risk assumptions and a report template. |
| [backtest-validation](https://github.com/powerpuff-kitty/ai-skills/tree/main/backtest-validation) | Causal timeline, fills/costs, ledger reconciliation, selection effects, out-of-sample validity and a report template. |

Current source references are reviewed 2026-10-14. Verify current provider, standard,
engine and data versions when applying them. They provide methods, not universal
accounting policy, suitability certification or a future-return claim.

## Build and install a selected pack

From a reviewed checkout, use an isolated destination or the host locations you
actually intend. Existing installer conflict/backup rules remain in force.

```sh
python3 scripts/validate.py --pack finance
python3 scripts/build.py --adapter portable --pack finance
python3 scripts/build.py --adapter opencode --pack finance
python3 scripts/install.py --pack finance --dry-run
python3 scripts/install.py --pack finance
```

These are instructions for a requested installation, not a record of changes to
any personal host. For a project destination, supply the same explicit `--target`
and `--commands-target` to dry-run and apply, as described in [INSTALL.md](../INSTALL.md).
Installing profiles does not connect a broker/wallet, install skills or run a model.

## Example requests and expected evidence

All numerical examples below are synthetic. They illustrate the artifact/acceptance
contract and do not represent observed model behavior.

### Financial model

Request: “Review this USD-thousands cash and project valuation model without editing.”
Inputs: cash begins at 20, operating cash flow 15, investing -5, financing -2,
no FX/other; model displays ending cash 30. Project cash flows are 110 and 121 at
years 1 and 2, with annual end-of-year rate 10% and time-zero outflow 180.

Expected result: cash should be 28, leaving a residual of 2. Future cash-flow PV
is 200 and project NPV is 20, assuming no terminal value. The report cites the
actual input/formula records, timing, units and independent recomputation. It
preserves the model and reports unknown source/policy assumptions instead of
inserting a plug. A missing source or recalculation engine limits the conclusion.

### Strategy/backtest

Request: “Assess this supplied offline backtest; do not start the bot.”
Inputs: a signal needs a close known after the auction but books its fill at that
same auction; the test period was also used to choose the best of many variants.

Expected result: identify unsupported information/fill timing and test-set reuse;
trace other preprocessing, universe, cost and ledger assumptions before concluding.
Do not load a live-capable configuration or treat an engine-specific clean bias
scan as proof of robust performance. Report source review and actual offline checks
separately. A hypothetical next-open fill needs a recomputed result, not a fabricated one.

A separate ledger sanity case starts with capital 2000, buys 10 shares at 100 and
sells at 110, charging 0.1% on each notional. Entry fee 1 leaves cash 999;
exit proceeds net of fee are 1098.9; final equity is 2097.9. Net P&L is 97.9
and return 4.895% before other costs. This arithmetic check does not validate a
strategy or prove that real orders could receive these fills.

### Portfolio risk

Request: “Review these synthetic exposures under a common -10% linear shock.”
Inputs: NAV 100, long notional 150, short notional 50, no other effects.

Expected result: net exposure 100%, gross exposure 200%; long loses 15 and short
gains 5, producing scenario P&L -10. State the shock, as-of snapshot and linear
assumption. This is not maximum loss; nonlinear derivatives, changing volatility,
liquidity, funding and missing positions may require a different method.

## Team sequencing and completion

`/team-finance <question>` frames the task, checks supplied data, selects relevant
financial/quantitative/risk analysis, then independently checks completed claims.
The financial analyst reconciles the answer. Only an explicitly requested persisted
artifact enters the single-writer stage; its actual saved content is checked after
writing. Domain analyses run only when relevant, within the 3-way concurrency
limit. Parallel reviews do not edit shared source.

A review without enough data returns missing inputs and a bounded method. Historical
facts, forecasts, scenarios, backtests, paper fills and live records stay distinct.
No account connection, subscription, order, collateral/fund transfer, wallet action
or bet is supplied or authorized by the pack. Existing authority for a separate
execution task must be handled by its appropriate actual tool/workflow.

Source validation, deterministic exports and isolated installer tests do not prove
host loading or financial decision quality. The new role/team and skill acceptance
cases remain `not_run` until actual evaluated sessions and artifacts are retained.

1 [retained independent synthetic skill review](../evals/observed/finance-skill-review-2026-10-14/manifest.json)
checked different cash/valuation/fee/compounding records and timing/selection
claims. Its report and arithmetic are retained; it is not an evaluation of these
agent profiles, automatic routing, actual host loading or general reliability.
