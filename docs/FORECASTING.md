# Forecasts, odds and event-market rules

The `forecasting` pack owns probability-analyst and `/team-forecast`. It depends
on science-data/core: 19 profiles and 11 workflows. It supports recorded event
forecasts and conditional betting/prediction-market analysis without a betting
or account runtime. The full catalog has 35 profiles, 20 workflows and 7 packs.

## Responsibilities and methods

[Probability analyst](../agents/probability-analyst/instructions.md) owns event,
quote, score/calibration and settlement analysis. Data-analyst inspects inputs,
mathematician supports numerical review, and evidence-validator checks completed
claims. Financial trading backtests belong to quant-researcher; chain/protocol
records belong to onchain-analyst when that optional pack is available.

| Skill | Scope and resource |
| --- | --- |
| [odds-analysis](https://github.com/powerpuff-kitty/ai-skills/tree/main/odds-analysis) | Quote formats, complete-market overround, named margin assumptions and conditional fee-adjusted payoffs. |
| [forecast-calibration](https://github.com/powerpuff-kitty/ai-skills/tree/main/forecast-calibration) | Recorded probabilities/labels, proper scores, calibration counts, dependence and fit/evaluation separation. |
| [settlement-rule-review](https://github.com/powerpuff-kitty/ai-skills/tree/main/settlement-rule-review) | Exact event definitions, rule/source versions, time boundaries, void/refund and proposal/dispute/final status. |

Each includes a focused reference, worked examples, a report template and 6
unrun acceptance cases. Skills are installed separately with their [installation
prompt](https://github.com/powerpuff-kitty/ai-skills/blob/main/INSTALL.md); missing
skills permit bounded direct work and explicit limits.

## Select the pack

```sh
python3 scripts/validate.py --pack forecasting
python3 scripts/build.py --adapter portable --pack forecasting
python3 scripts/build.py --adapter opencode --pack forecasting
python3 scripts/install.py --pack forecasting --dry-run
python3 scripts/install.py --pack forecasting
```

Use reviewed destinations and preserve customizations per [INSTALL.md](../INSTALL.md).
These are installation instructions, not a record of personal-host changes.

## Worked requests and expected evidence

All examples are synthetic and conditional, not observed task/model outcomes.

### Quotes and conditional payoff

For a comparable exhaustive 2-outcome market, decimal back odds 1.80 and 2.20
imply 5/9 and 5/11. Their sum is 100/99, so overround is 1/99, approximately
1.010101%. Proportional margin removal gives .55/.45; the method does not establish
true probabilities. A 3-way market missing the draw cannot use that 2-way
normalization as a complete market.

With an independently ASSUMED probability .60 and decimal odds1.80, expected unit
net P&L is .08 before costs. Under an isolated-bet assumption of 5% commission on
positive winnings, it becomes .056. A real exchange may net winnings per market;
use its actual fee contract. This illustrates arithmetic, not validated edge,
liquidity, a personal stake recommendation or executed profit.

### Forecast evaluation

Recorded p=[.8,.6,.2,.4] and resolved y=[1,0,0,1] have mean binary Brier .20;
a predeclared constant .5 baseline has .25. In bins [0,.5) and [.5,1], mean
predictions .3/.7 each have observed rate .5 and n=2. Improvement on 4 records
does not prove calibration or significance. Unresolved outcomes remain excluded
with counts/status; they are not losses. A zero probability for an observed event
has infinite natural-log loss unless a separately declared clipped metric is used.

A calibrator fitted on the final evaluation labels has not been validated on an
untouched test. Repeated updates to the same event and overlapping horizons need
appropriate evaluation units, weights and dependence-aware uncertainty.

### Settlement comparison

A regulation-time Team X win and an extra-time-inclusive win are different events.
If the game is drawn at90 minutes and X wins extra time, the declared definitions
differ; actual payout still needs the full rules. Strictly above100 and at least100
also differ at100. A closed market or proposed outcome is not final settlement.
Missing timezone, rule precedence or source policy keeps the conclusion conditional.

## Workflow and evidence limits

`/team-forecast <question>` frames the event/as-of, gathers necessary approved
external rule/source evidence BEFORE dependent analysis, checks data/definitions,
then evaluates relevant quotes, forecasts or terms. Independent checks follow
completed claims. Probability-analyst writes only requested saved artifacts;
actual output is verified after the sole writer finishes.

The pack does not create/access gambling accounts, choose personal stakes, bypass
eligibility/limits, place bets/orders, sign, post resolution bonds, propose/dispute
outcomes or claim funds. Forecast accuracy, calibration, conditional utility and
actual profit remain distinct evidence. Native loading and broad reasoning
reliability are not established by source checks; cases remain not_run.

1 [retained independent synthetic skill review](../evals/observed/crypto-forecast-review-2026-10-14/manifest.json)
checks chain/finality, contract counterevidence, DeFi scenarios, odds/fees, proper
scores and settlement boundaries. Reports and exact arithmetic are retained; this
is not a profile/host-loading evaluation or broad outcome benchmark.
