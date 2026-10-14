#!/usr/bin/env python3
"""Offline exact-arithmetic review. Reads only listed sources and the fixture."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

ROOT = Path('/private/tmp/crypto-forecast-forward')
INPUT = ROOT / 'input.json'
SKILLS = Path('/Users/tcsntcsn/TCSN/skills')
NAMES = ['onchain-data-analysis', 'smart-contract-review', 'defi-risk-analysis',
         'odds-analysis', 'forecast-calibration', 'settlement-rule-review']
raw = INPUT.read_bytes()
before = hashlib.sha256(raw).hexdigest()
data = json.loads(raw, parse_float=Decimal)
f = lambda v: F(v)
show = lambda v: {'exact': str(v), 'decimal': str(Decimal(v.numerator) / Decimal(v.denominator))}
records = data['chain_data']['records']
eligible = [r for r in records if r['chain_id'] == data['chain_data']['chain_id']
            and r['canonical'] and r['receipt_status'] == 1]
unique = {(r['chain_id'], r['block_hash'], r['tx_hash'], r['log_index']): r for r in eligible}
c = data['defi']
hf = f(c['collateral_value']) * f(c['threshold']) / f(c['debt_value'])
shocked_collateral = f(c['collateral_value']) * (1 + f(c['collateral_only_price_shock']))
r = f(c['relative_price_ratio'])
# This fixture's ratio has the exact square root 3.
assert r == 9
lp_ratio = 2 * F(3) / (1 + r)
o = data['odds']
quotes = list(map(f, o['decimal_quotes']))
implied = [1 / q for q in quotes]
total = sum(implied)
p, commission = f(o['independent_probability_assumption_first_outcome']), f(o['commission_rate'])
win_net = (quotes[0] - 1) * (1 - commission)
forecasts = data['forecasts']
resolved = [v for v in forecasts['records'] if v['status'] == 'resolved' and v['outcome'] is not None]
excluded = [v['id'] for v in forecasts['records'] if v not in resolved]
errors = [(f(v['p']) - v['outcome']) ** 2 for v in resolved]
brier = sum(errors) / len(errors)
baseline = sum((f(forecasts['baseline_probability']) - v['outcome']) ** 2 for v in resolved) / len(resolved)
bins = []
for low, high, closed in [(F(0), F(1, 2), False), (F(1, 2), F(1), True)]:
    rows = [v for v in resolved if f(v['p']) >= low and (f(v['p']) <= high if closed else f(v['p']) < high)]
    bins.append({'range': '[0,.5)' if not closed else '[.5,1]', 'n': len(rows),
                 'mean_p': show(sum(f(v['p']) for v in rows) / len(rows)),
                 'event_rate': show(F(sum(v['outcome'] for v in rows), len(rows)))})
paths = [Path('/Users/tcsntcsn/TCSN/tcsn.io/.agentic/README.md'),
         Path('/Users/tcsntcsn/TCSN/tcsn.io/.agentic/manifest.yaml'), INPUT]
paths += [SKILLS / name / suffix for name in NAMES
          for suffix in ['SKILL.md', 'references/method.md', 'assets/report-template.md']]
hashes = [{'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths]
after = hashlib.sha256(INPUT.read_bytes()).hexdigest()
assert before == after, 'Fixture changed while calculating'
output = {
    'python_version': platform.python_version(), 'review_time_utc': datetime.now(timezone.utc).isoformat(),
    'input_sha256_before': before, 'input_sha256_after': after, 'input_unchanged': before == after,
    'source_inventory': hashes,
    'chain': {'scaled_amount': show(F(data['chain_data']['raw_amount'], 10 ** data['chain_data']['declared_verified_decimals'])),
              'eligible_rows': len(eligible), 'unique_eligible_events': len(unique),
              'unique_finalized_eligible_events': sum(r['finalized'] for r in unique.values())},
    'defi': {'initial_hf': show(hf), 'shocked_collateral': show(shocked_collateral),
             'shocked_hf': show(shocked_collateral * f(c['threshold']) / f(c['debt_value'])),
             'collateral_at_hf_one': show(f(c['debt_value']) / f(c['threshold'])),
             'shock_at_hf_one': show(f(c['debt_value']) / f(c['threshold']) / f(c['collateral_value']) - 1),
             'lp_relative_value': show(lp_ratio), 'lp_relative_return': show(lp_ratio - 1)},
    'odds': {'raw_implied': list(map(show, implied)), 'sum_raw': show(total),
             'overround': show(total - 1), 'proportional_normalization': [show(v / total) for v in implied],
             'gross_ev': show(p * quotes[0] - 1), 'winning_net_profit': show(win_net),
             'fee_adjusted_ev': show(p * win_net - (1 - p)), 'break_even_p': show(1 / (1 + win_net))},
    'forecast': {'resolved_n': len(resolved), 'excluded_ids': excluded,
                 'squared_errors': list(map(show, errors)), 'brier': show(brier), 'baseline': show(baseline),
                 'brier_skill': show(1 - brier / baseline), 'bins_descriptive_only': bins,
                 'brier_if_unresolved_wrongly_zero': show(sum((f(v['p']) - (v['outcome'] or 0)) ** 2
                                                             for v in forecasts['records']) / len(forecasts['records']))},
    'settlement': {'value': data['settlement']['official_value_at_cutoff'],
                   'A_threshold_satisfied': data['settlement']['official_value_at_cutoff'] >= 150,
                   'B_threshold_satisfied': data['settlement']['official_value_at_cutoff'] > 150,
                   'trading_status': data['settlement']['trading_status'],
                   'resolution_status': data['settlement']['resolution_status'],
                   'final_status': data['settlement']['dispute_and_final_status']}
}
print(json.dumps(output, indent=2))
