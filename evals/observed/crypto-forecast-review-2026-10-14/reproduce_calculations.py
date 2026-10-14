#!/usr/bin/env python3
"""Portable fixture arithmetic; no skill/model/chain/account execution."""
from decimal import Decimal
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def main():
    raw = (Path(__file__).parent / "input.json").read_bytes()
    data = json.loads(raw, parse_float=Decimal)
    chain = data["chain_data"]
    amount = F(chain["raw_amount"], 10 ** chain["declared_verified_decimals"])
    candidates = {
        (r["chain_id"], r["block_hash"], r["tx_hash"], r["log_index"]): r
        for r in chain["records"]
        if r["chain_id"] == chain["chain_id"] and r["canonical"] and r["receipt_status"] == 1
    }
    finalized = sum(r["finalized"] for r in candidates.values())
    defi = data["defi"]
    initial_hf = F(defi["collateral_value"]) * F(defi["threshold"]) / F(defi["debt_value"])
    shocked_hf = initial_hf * (1 + F(defi["collateral_only_price_shock"]))
    ratio = F(defi["relative_price_ratio"])
    assert ratio == 9  # This fixture has exact square root 3; not a generic AMM engine.
    lp_relative = 2 * F(3) / (1 + ratio) - 1
    odds = data["odds"]
    q = [1 / F(v) for v in odds["decimal_quotes"]]
    total = sum(q)
    p = F(odds["independent_probability_assumption_first_outcome"])
    d = F(odds["decimal_quotes"][0])
    ev = p * (d - 1) * (1 - F(odds["commission_rate"])) - (1 - p)
    forecasts = data["forecasts"]
    resolved = [r for r in forecasts["records"] if r["status"] == "resolved" and r["outcome"] is not None]
    brier = sum((F(r["p"]) - r["outcome"]) ** 2 for r in resolved) / len(resolved)
    baseline = sum((F(forecasts["baseline_probability"]) - r["outcome"]) ** 2 for r in resolved) / len(resolved)
    assert amount == F("4.5") and len(candidates) == 1 and finalized == 0
    assert initial_hf == F("1.6") and shocked_hf == F("1.2")
    assert lp_relative == F("-.4") and total - 1 == F(1, 24)
    assert [v / total for v in q] == [F(".4"), F(".6")]
    assert ev == F(".0296") and brier == F(".2175") and baseline == F(".25")
    print(json.dumps({
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "token_amount": str(amount), "canonical_successful_candidates": len(candidates),
        "finalized_candidates": finalized, "initial_hf": str(initial_hf),
        "shocked_hf": str(shocked_hf), "lp_relative_return": str(lp_relative),
        "overround": str(total - 1), "normalized_probabilities": [str(v / total) for v in q],
        "conditional_fee_adjusted_ev": str(ev), "resolved_records": len(resolved),
        "brier": str(brier), "baseline": str(baseline),
        "scope": "synthetic arithmetic only; not real state, calibrated performance or final settlement"
    }, indent=2))


if __name__ == "__main__":
    main()
