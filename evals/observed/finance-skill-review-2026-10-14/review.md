# Independent review of synthetic financial records

Reviewed 2026-10-14 UTC. Source: `/private/tmp/finance-forward-test/input.json`, 1,869 bytes, SHA-256 `45a44debb5a4fdb8b97c2fbc46df4c0c85618cd2268aa9f07c136740c82750e7`. This is an offline synthetic fixture, not a real instrument, account, paper-trading run or observed forward test. Original inputs were preserved. Only the three authorized skill folders and fixture were read; this report is the sole written artifact.

## Conclusions and calculations

| Source path / original claim | Independently checked result | Assessment |
| --- | --- | --- |
| `market_data.claimed_holding_loss_percent`: -80% | Raw close change = 20/100 - 1 = -80%; with the declared 5-for-1 split, one original share becomes five shares worth 5 × 20 = 100, so economic holding price return = 0%, assuming the split applies to the holding and no other distributions/costs. | -80% is supported as an unadjusted per-share price change, not a split-aware holding loss. |
| `financial_model.displayed_ending_cash`: 30 | 20 + 15 - 5 - 2 + 1 = **29 USD thousands**. Displayed minus calculated residual = **1 USD thousand**. | Confirmed reconciliation discrepancy under the supplied complete cash bridge. Include FX; do not force another balance to fit. Missing reconciliation items would require separate evidence. |
| `financial_model.project.reported_npv`: 218.181818 | PV of future receipts = 120/1.10 + 132/1.10² = 218.18181818; NPV = -210 + that PV + zero terminal value = **8.18181818 USD thousands**. | Reported value matches future-inflow PV within rounding, but omits the initial investment from project NPV, overstating NPV by approximately 210 USD thousands. The underlying spreadsheet formula is not supplied, so the exact implementation cause is inferred. |
| `strategy.synthetic_round_trip.reported_return_percent`: 2% | Buy notional 5 × 40 = 200; sell notional 5 × 44 = 220; gross profit = 20. Entry fee = 200 × .002 = .40; exit fee = 220 × .002 = .44. Net profit = **19.16**, return on initial capital 1,000 = **1.916%**. | 2% is supported only as gross return on total starting capital. A net claim must deduct both fees. Currency for this separate round trip is unstated; monetary figures use its common assumed account unit. |
| `strategy.separate_two_period_return_example.reported_compounded_return_percent`: 0% | (1 + .20)(1 - .20) - 1 = **-4%**. | 0% is the arithmetic sum, not the compounded return. The example is separate from the round trip and must not be combined with it. |

Cash ledger reconciliation for the round trip, assuming no external cash flows or other positions: 1,000 - 200 - .40 = **799.60 cash after entry**, plus position marked at the entry price 200 gives equity 999.60. Exit leaves 799.60 + 220 - .44 = **1,019.16 final cash/equity**, zero position. Entry is fully funded. Asset-only gross return is 10%; it is not the 2% return on starting account capital.

## Timing, data and strategy findings

1. **Fundamental unavailable at the stated decision.** `market_data.fundamental.period_end` is June 30, but its `published_at` is August 20, 2026, 18:00 UTC. The decision is August 15, 14:00 UTC: publication is **5 days 4 hours later**. Its value 12 cannot be justified as available for that decision by its period end. Publication is the earliest stated source availability; ingestion/revision latency is unknown. The fixture does not explicitly say the strategy consumes this fundamental, so actual use/leakage of this field is conditional, while its unavailability is directly established.
2. **Noncausal feature construction.** `strategy.feature` divides each close by the maximum over the entire evaluation interval. This construction can use later observations for earlier rows, and is unsuitable as a general point-in-time feature unless the maximum is restricted to information already available or an independently fixed training reference. On the two supplied bars the maximum 100 happens to occur first, giving scores 1 and .2; a running maximum produces the same two values. Thus these rows establish the faulty dependency specification, not a demonstrated numerical change or a measured performance inflation. There is no evidence the round-trip prices 40/44 were generated from those bars.
3. **Unsupported fill chronology.** `strategy.execution` computes the signal after the closing auction but records entry at that same auction. Under the declared timeline the signal cannot generate an order participating in an already completed auction. The supplied fill is not causally justified. Recompute with an actual feasible order/fill mechanism and price; a next-session price is not supplied and must not be invented.
4. **The named test interval was used for selection.** `strategy.selection` chooses the best of **200 variants** on the interval called test. It therefore acts as selection/validation data, not an untouched final holdout. The winner's result is exposed to selection optimism. The extent and statistical significance cannot be estimated without all trials, dependence, strategy identities and an untouched or appropriately designed walk-forward evaluation.
5. **Historical universe unverified.** `market_data.universe_source` is a current constituent snapshot with no membership history. Using it to reconstruct a historical universe risks survivorship and future-membership bias; actual impact is unknown. The review cannot infer historical membership, delisted coverage or missing instruments from SYNTH-X alone.
6. **Limited structural pass.** Both supplied dates are ordered and unique; both closes are finite positive numbers. These checks cover all two provided bars. There are no OHLC/volume fields, venue/session calendar, durable instrument identifier, publication/ingestion timestamps for bars, retrieval/provider version, revision archive or independent source. Missing-session coverage, OHLC constraints, tradeability and source correctness cannot be checked. No weekday/session or zero-return assumptions were added.

Data contract: the bars are labeled dates, with raw unadjusted USD closes from August 13–14, 2026; exact event/close times and timezone are unstated. The split date is August 14; precise effective-session convention is not supplied. Fundamental value units, accounting meaning and revision policy are unstated. Adjustment calculations above are explicit hypothetical holdings transformations, not edits or proof of a total-return history.

## Sensitivity and model boundaries

Project sensitivity uses the same two end-of-year cash flows, initial outflow 210 at t=0 and terminal value zero. Values are USD thousands:

| Annual effective discount rate | Future-receipt PV | Project NPV |
| --- | ---: | ---: |
| 0% | 252.000000 | 42.000000 |
| 5% | 234.013605 | 24.013605 |
| 10% (supplied) | 218.181818 | 8.181818 |
| 15% | 204.158790 | -5.841210 |
| 20% | 191.666667 | -18.333333 |

The NPV sign changes between 10% and 15%; this is an assumption sensitivity, not evidence that any alternative rate is required. Cash-flow certainty, nominal/real and pre/post-tax consistency, financing basis, reporting period/entity, accounting policy and required-return justification are unavailable. The model's USD-thousands convention is applied to the nested project; a different intended unit would need explicit confirmation. No balance sheet, full statements, workbook formulas, hidden sheets or external links were supplied for inspection or engine recalculation.

For the round trip, with symmetric per-notional fee f and additional total costs C, net profit = 20 - 420f - C. At f=.002 and C=0 this gives 19.16; fees reduce account return by .084 percentage points. At zero other costs, the fee-only break-even rate is 20/420 = **4.76190476% per traded notional**; at the supplied fee, extra costs of **19.16** exhaust the profit. These are arithmetic thresholds holding fill prices fixed, not realistic cost or capacity estimates. Other costs zero is a declared scenario assumption, not verified absence of spread, slippage, financing, taxes or market impact. No execution timestamps, quantities available in the market, lot rules, dated trades, full ledger/equity curve, benchmark, annualization convention or external-flow records are supplied. No Sharpe ratio, drawdown, annualized return, confidence interval, capacity or future profitability can be supported.

## Actual verification and reproducibility

All tool calls were local shell commands, with observed exit code **0**. Python version was **3.14.7**. Decimal calculations used the default 28 significant-digit context; six-decimal displays above are rounded. The reported PV is within 0.000001 USD thousand of recomputed PV; the NPV/cash/return discrepancies materially exceed that display tolerance. No external reference links in the skills were fetched and no supplied strategy code was run.

Reads performed:

- `cat` on the three authorized `SKILL.md` files and the fixture, in one command.
- `cat` on each skill's linked reference guide and report template, in one command; the financial-model guide was also read individually to ensure its full contents were inspected.
- A local `python3` here-document loaded the fixture, printed its SHA-256/length and Python version, checked dates/finite prices, recomputed cash, PV/NPV sensitivity, fees/cash balances/return, compounded returns and publication delay. Actual calculation logic was:

```python
import hashlib, json, sys, datetime
from decimal import Decimal as D
from pathlib import Path
p = Path('/private/tmp/finance-forward-test/input.json')
b = p.read_bytes()
d = json.loads(b)
print(sys.version.split()[0], hashlib.sha256(b).hexdigest(), len(b))
x = d['strategy']['synthetic_round_trip']
buy = D(str(x['quantity'])) * D(str(x['buy_price']))
sell = D(str(x['quantity'])) * D(str(x['sell_price']))
fee = D(str(x['fee_per_traded_notional']))
c = D(str(x['initial_capital']))
print(buy, sell, buy*fee, sell*fee, c-buy-buy*fee)
print(c-buy-buy*fee+sell-sell*fee, sell-buy-(sell+buy)*fee)
print((sell-buy-(sell+buy)*fee)/c*100, (sell-buy)/(sell+buy))
f = d['financial_model']
print(sum(D(str(f[k])) for k in ['beginning_cash', 'operating_cash_flow',
          'investing_cash_flow', 'financing_cash_flow', 'fx_effect']))
pj = f['project']
cfs = [D(str(z)) for z in pj['end_of_year_cash_flows']]
for r in [D('0'), D('.05'), D('.1'), D('.15'), D('.2')]:
    pv = sum(cf/(1+r)**i for i, cf in enumerate(cfs, 1))
    print(r, pv, pv-D(str(pj['initial_outflow_at_t0'])))
print(((1+D('.2'))*(1-D('.2'))-1)*100)
print(datetime.datetime.fromisoformat(d['market_data']['fundamental']['published_at'])
      - datetime.datetime.fromisoformat(d['market_data']['strategy_decision_at']))
bars = d['market_data']['bars']
dates = [z['date'] for z in bars]
print(len(dates)==len(set(dates)), dates==sorted(dates),
      all(D(str(z['close'])).is_finite() for z in bars))
```

The code block preserves the executed calculation operations with print formatting condensed; it is not a separate backtest run. Split-aware return, the causality/selection judgments and the linear cost sensitivity were reviewed directly from the supplied records and formulas. The final artifact write and subsequent read/hash check were also local commands; the fixture hash was checked again after writing this report.

## Supported use and remaining work

This fixture supports bounded arithmetic and specification review. Several stated values are gross prices, PV or arithmetic sums mislabeled as economic loss, NPV or compounded/net returns. It does not support a clean historical simulation, a measured forward test, or an economically viable strategy claim. Correct those labels/calculations in a separately authorized derived artifact; obtain point-in-time data/universe records, causal feature/fill implementation, complete costs/ledger and trial history before validating strategy performance. Preserve the reported values alongside corrections.

Skill ambiguity affecting the review was limited: the backtest skill is framed around historical simulations while the assignment calls this a synthetic forward-test review. Its causal, accounting and selection methods apply to the supplied specification, but no forward-test result was inferred. The templates provide overlapping evidence contracts; they were consolidated into one report. Their synthetic worked examples were treated as method guidance, never as fixture answers. No skill required network access or executing a backtest engine; neither occurred.

## Exact local read inventory and arithmetic invocation

Files read (no host-loader files or separate acceptance-case specifications were inspected):

```text
/Users/tcsntcsn/TCSN/skills/market-data-validation/SKILL.md
/Users/tcsntcsn/TCSN/skills/market-data-validation/references/validation-guide.md
/Users/tcsntcsn/TCSN/skills/market-data-validation/assets/report-template.md
/Users/tcsntcsn/TCSN/skills/financial-model-review/SKILL.md
/Users/tcsntcsn/TCSN/skills/financial-model-review/references/model-review.md
/Users/tcsntcsn/TCSN/skills/financial-model-review/assets/report-template.md
/Users/tcsntcsn/TCSN/skills/backtest-validation/SKILL.md
/Users/tcsntcsn/TCSN/skills/backtest-validation/references/backtest-review.md
/Users/tcsntcsn/TCSN/skills/backtest-validation/assets/report-template.md
/private/tmp/finance-forward-test/input.json
/private/tmp/finance-forward-test/review.md (post-write artifact check only)
```

Exact original arithmetic shell command (exit 0; output captured during this review):

```sh
python3 - <<'PY'
import hashlib,json,sys,datetime
from decimal import Decimal as D
from pathlib import Path
p=Path('/private/tmp/finance-forward-test/input.json'); b=p.read_bytes(); d=json.loads(b)
x=d['strategy']['synthetic_round_trip']; buy=D(str(x['quantity']))*D(str(x['buy_price'])); sell=D(str(x['quantity']))*D(str(x['sell_price'])); fee=D(str(x['fee_per_traded_notional'])); c=D(str(x['initial_capital']))
print('Python:',sys.version.split()[0]); print('UTC:',datetime.datetime.now(datetime.timezone.utc).isoformat()); print('sha256:',hashlib.sha256(b).hexdigest()); print('bytes:',len(b)); print('buy_notional:',buy,'sell_notional:',sell,'entry_fee:',buy*fee,'exit_fee:',sell*fee,'entry_cash:',c-buy-buy*fee,'final_cash:',c-buy-buy*fee+sell-sell*fee,'net_pnl:',sell-buy-(sell+buy)*fee,'net_return_pct:',(sell-buy-(sell+buy)*fee)/c*100,'break_even_fee:',(sell-buy)/(sell+buy))
f=d['financial_model']; print('ending_cash:',sum(D(str(f[k])) for k in ['beginning_cash','operating_cash_flow','investing_cash_flow','financing_cash_flow','fx_effect']))
pj=f['project']; cfs=[D(str(z)) for z in pj['end_of_year_cash_flows']]
for r in [D('0'),D('.05'),D('.1'),D('.15'),D('.2')]:
 pv=sum(cf/(1+r)**i for i,cf in enumerate(cfs,1)); print('rate',r,'pv',pv,'npv',pv-D(str(pj['initial_outflow_at_t0'])))
print('compounded_return_pct:',((1+D('.2'))*(1-D('.2'))-1)*100)
print('published_minus_decision:',datetime.datetime.fromisoformat(d['market_data']['fundamental']['published_at'])-datetime.datetime.fromisoformat(d['market_data']['strategy_decision_at']))
bars=d['market_data']['bars']; dates=[z['date'] for z in bars]; print('unique_keys:',len(dates)==len(set(dates)),'ordered_dates:',dates==sorted(dates),'finite_closes:',all(D(str(z['close'])).is_finite() for z in bars))
PY
```

Host loading, automatic skill routing and separate acceptance-case specifications remain **untested**. No conclusion about their behavior follows from this report.
