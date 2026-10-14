#!/usr/bin/env python3
"""Reproduce fixture arithmetic, not model behavior or backtest performance."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path


def dec(value):
    return Decimal(str(value))


def main():
    raw = (Path(__file__).parent / "input.json").read_bytes()
    data = json.loads(raw)
    cash = data["financial_model"]
    cash_result = sum(dec(cash[key]) for key in (
        "beginning_cash", "operating_cash_flow", "investing_cash_flow",
        "financing_cash_flow", "fx_effect"))
    project = cash["project"]
    rate = dec(project["annual_effective_discount_rate"])
    pv = sum(dec(cf) / (1 + rate) ** time
             for time, cf in enumerate(project["end_of_year_cash_flows"], 1))
    npv = pv - dec(project["initial_outflow_at_t0"])
    trade = data["strategy"]["synthetic_round_trip"]
    entry = dec(trade["quantity"]) * dec(trade["buy_price"])
    exit_value = dec(trade["quantity"]) * dec(trade["sell_price"])
    fees = (entry + exit_value) * dec(trade["fee_per_traded_notional"])
    pnl = exit_value - entry - fees - dec(trade["other_costs"])
    return_pct = pnl / dec(trade["initial_capital"]) * 100
    compound = Decimal(1)
    for value in data["strategy"]["separate_two_period_return_example"]["simple_returns"]:
        compound *= 1 + dec(value)
    compound_pct = (compound - 1) * 100
    bars = data["market_data"]["bars"]
    split_return = (Decimal(5) * dec(bars[1]["close"]) / dec(bars[0]["close"]) - 1) * 100
    assert cash_result == Decimal(29)
    assert abs(npv - Decimal("8.1818181818")) < Decimal("0.000000001")
    assert return_pct == Decimal("1.916")
    assert compound_pct == Decimal(-4)
    assert split_return == Decimal(0)
    print(json.dumps({
        "fixture_sha256": hashlib.sha256(raw).hexdigest(),
        "ending_cash_thousands": str(cash_result),
        "future_receipts_pv_thousands": str(pv),
        "project_npv_thousands": str(npv),
        "round_trip_net_return_percent": str(return_pct),
        "compounded_return_percent": str(compound_pct),
        "split_aware_holding_return_percent": str(split_return),
        "scope": "synthetic arithmetic reproduction only; no model, market or account execution"
    }, indent=2))


if __name__ == "__main__":
    main()
