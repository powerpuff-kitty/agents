"""Offline fixture comparison and arithmetic, not executed app/browser/study tests."""
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'sources'
def read(name):
    return json.loads((SRC / name).read_text())

identity = json.loads((ROOT / 'source-identities.json').read_text())
for row in identity['files']:
    actual = hashlib.sha256((ROOT / row['copy_path']).read_bytes()).hexdigest()
    assert actual == row['copy_sha256'], row['copy_path']

command = [sys.executable, str(SRC / 'competitor-monitoring/scripts/compare_snapshots.py'),
           str(SRC / 'competitor-monitoring/tests/fixtures/baseline.json'),
           str(SRC / 'competitor-monitoring/tests/fixtures/current.json')]
proc = subprocess.run(command, capture_output=True, text=True)
(ROOT / 'comparison.stdout.json').write_text(proc.stdout)
(ROOT / 'comparison.stderr.txt').write_text(proc.stderr)
comparison = json.loads(proc.stdout)
assert proc.returncode == 1
actual_classes = {(x['source_id'], x.get('fact_key')): x['classification'] for x in comparison['items']}
assert actual_classes == {('pricing', 'plan-name'): 'unchanged', ('pricing', 'pro-price'): 'changed',
                          ('release-notes', None): 'coverage_gap'}
baseline = read('competitor-monitoring/tests/fixtures/baseline.json')
current = read('competitor-monitoring/tests/fixtures/current.json')
old_price = Decimal(baseline['sources'][0]['facts'][0]['value'])
new_price = Decimal(current['sources'][0]['facts'][0]['value'])
price_delta = new_price - old_price

market = read('market-opportunity-research/tests/fixtures/input.json')
solo, agency = market['segments']
overlap = market['overlap']['buying_units_in_both']
solo_annual = solo['list_price']
agency_annual = agency['list_price'] * 12
solo_only = solo['buying_units'] - overlap
agency_only = agency['buying_units'] - overlap
nonoverlap_value = solo_only * solo_annual + agency_only * agency_annual
low = nonoverlap_value + overlap * min(solo_annual, agency_annual)
high = nonoverlap_value + overlap * max(solo_annual, agency_annual)
naive = solo['buying_units'] * solo_annual + agency['buying_units'] * agency_annual
assert (solo_only, agency_only, low, high, naive) == (2500, 500, 3600000, 3700000, 4200000)

research = read('user-research/tests/fixtures/input.json')
assert all(row['analysis_allowed'] for row in research['records'])
counts = {'permitted_synthetic_records': len(research['records']),
          'interview_said_records': sum(x['observation_type'] == 'said' for x in research['records']),
          'task_did_records': sum(x['observation_type'] == 'did' for x in research['records'])}
browser = read('test-engineering/tests/fixtures/browser-recovery.json')
test, recovery = browser['test_result'], browser['recovery']
checks = {'fixture_route_matches': test['actual_route'] == test['expected_route'],
          'fixture_has_state_assertions': bool(test['state_assertions']),
          'fixture_fonts_ready': test['fonts_ready'],
          'fixture_acknowledged_state_lost_after_restart': recovery['acknowledged_saved'] and recovery['after_restart'] == 'empty',
          'recovery_duration_measured': recovery['measured_recovery_seconds'] is not None,
          'lost_record_count_measured': recovery['measured_lost_record_count'] is not None}
assert checks == {'fixture_route_matches': False, 'fixture_has_state_assertions': False,
                  'fixture_fonts_ready': False, 'fixture_acknowledged_state_lost_after_restart': True,
                  'recovery_duration_measured': False, 'lost_record_count_measured': False}
results = {
    'kind': 'offline-fixture-checks-and-calculations; no product execution',
    'python': sys.version, 'comparison_command': command, 'comparison_exit': proc.returncode,
    'competitor': {'delta_usd_per_seat_month': str(price_delta),
                   'percentage_of_baseline': str(price_delta / old_price * 100),
                   'fixture_current_is_future_dated_relative_to_task_date': current['captured_at'][:10] > '2026-10-14',
                   'retrieval_performed': False},
    'market': {'currency': 'USD', 'period': 'annual', 'agency_annual_list_price': agency_annual,
               'distinct_buying_units': solo['buying_units'] + agency['buying_units'] - overlap,
               'solo_only': solo_only, 'agency_only': agency_only, 'overlap': overlap,
               'nonoverlap_value': nonoverlap_value, 'naive_double_counted_sum': naive,
               'conditional_full_participation_low': low, 'conditional_full_participation_high': high,
               'naive_overstatement_low': naive - high, 'naive_overstatement_high': naive - low,
               'overlap_assignment_sensitivity': '3,600,000 + 200*x USD/year; x is overlap units assigned agency price, 0 <= x <= 500',
               'reach_adoption_wtp_validated': False},
    'research': counts, 'browser_fixture_consistency': checks,
    'unavailable': ['app source/build/SDK/device/backend checks', 'browser runs/traces/recovery measurements',
                    'actual participant sessions', 'live market or competitor retrieval']}
(ROOT / 'checks.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps({'source_copy_hashes_verified': len(identity['files']), 'comparison_exit': proc.returncode,
                  'market_range': [low, high], 'checks_output': 'checks.json', 'product_tests_executed': 0}))
