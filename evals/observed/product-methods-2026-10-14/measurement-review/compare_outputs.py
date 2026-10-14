"""Compare independent replay results with retained authored outputs; no author script."""
from pathlib import Path
import hashlib
import json
from math import isclose

ROOT = Path(__file__).resolve().parent
REVIEWED = ROOT/'reviewed'
own = json.loads((ROOT/'independent-calculations.json').read_text())
instrument = json.loads((REVIEWED/'instrumentation-calculations.json').read_text())
analytics = json.loads((REVIEWED/'analytics-calculations.json').read_text())
experiment = json.loads((REVIEWED/'experiment-calculations.json').read_text())
results = []
def same(name, actual, expected, tolerance=None):
    passed = isclose(actual,expected,rel_tol=0,abs_tol=tolerance) if tolerance is not None else actual==expected
    results.append({'claim':name,'independent':actual,'authored':expected,'match':passed,'absolute_tolerance':tolerance})
same('instrument raw rows',own['instrumentation']['raw_rows'],instrument['raw_rows'])
same('instrument distinct IDs',own['instrumentation']['unique_event_ids'],instrument['distinct_event_ids'])
same('instrument shape passes',own['instrumentation']['shape_valid_rows'],instrument['schema_pass_rows'])
same('instrument valid unique',own['instrumentation']['deduplicated_shape_valid_events'],instrument['accepted_unique_rows'])
for row in own['instrumentation']['rows']:
    author_row = instrument['rows'][row['fixture_index']]
    same(f"instrument row {row['fixture_index']+1} missing names",row['missing_property_names'],author_row['missing_fields'])
    same(f"instrument row {row['fixture_index']+1} extra names",row['extra_property_names'],author_row['unexpected_field_names'])
same('analytics raw rows',own['analytics']['raw_rows'],analytics['raw_rows'])
same('analytics deduplicated events',own['analytics']['deduplicated_events'],analytics['after_deduplication'])
same('analytics entrants',own['analytics']['entrant_units'],analytics['eligible_entrants'])
same('analytics mature entrants',own['analytics']['mature_entrant_units'],analytics['mature_entrants'])
same('analytics mature converters',own['analytics']['mature_conversion_numerator'],analytics['mature_converters'])
same('analytics mature rate',own['analytics']['mature_conversion_rate'],analytics['mature_conversion_rate'])
same('analytics immature units count',len(own['analytics']['immature_units']),analytics['immature_entrants'])
same('analytics orphan units count',len(own['analytics']['orphan_conversion_units']),analytics['excluded_nonentrant_units'])
for row in own['analytics']['ledger']:
    author_row = next(x for x in analytics['ledger'] if x['unit']==row['unit'])
    same(f"analytics {row['unit']} maturity",row['mature'],author_row['mature'])
    same(f"analytics {row['unit']} conversion",row['within_window_conversion'],author_row['converted_in_window'])
same('experiment SRM chi square',own['experiment']['assignment_chi_square_df1'],experiment['srm']['chi_square'])
same('experiment asymptotic SRM p',own['experiment']['assignment_chi_square_survival'],experiment['srm']['p_value'],1e-18)
same('experiment exact SRM p',own['experiment']['two_sided_exact_binomial_srm_p'],experiment['srm']['exact_binomial_two_sided_p'],1e-18)
same('experiment control rate',own['experiment']['control_rate'],experiment['rates']['control'])
same('experiment treatment rate',own['experiment']['treatment_rate'],experiment['rates']['treatment'])
same('experiment absolute difference',own['experiment']['absolute_rate_difference'],experiment['effect']['absolute_difference'],1e-15)
same('experiment relative difference',own['experiment']['relative_difference'],experiment['effect']['relative_change'],1e-15)
for idx,(actual,expected) in enumerate(zip(own['experiment']['illustrative_unpooled_normal_difference_95_interval'],experiment['effect']['exploratory_95pct_normal_interval'])):
    same(f'experiment illustrative CI endpoint {idx}',actual,expected,1e-6)
assert all(x['match'] for x in results)
claimed_hashes = json.loads((REVIEWED/'artifact-hashes.json').read_text())
verified_hashes = []
for path in REVIEWED.rglob('*'):
    if path.is_file() and str(path.relative_to(REVIEWED)) in claimed_hashes:
        name = str(path.relative_to(REVIEWED))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == claimed_hashes[name], name
        verified_hashes.append(name)
source_unchanged = []
for row in json.loads((ROOT/'reviewed-hashes.json').read_text()):
    okay = hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
    assert okay, row['path']
    source_unchanged.append(row['path'])
output = {'comparison_checks':results,'all_match':True,
          'interval_rounding_note':'Independent replay uses 1.959963984540054; authored interval is consistent with rounded 1.96. Maximum allowed discrepancy 1e-6 in rate units; substantive precision unchanged.',
          'authored_artifact_hashes_verified':verified_hashes,
          'reviewed_originals_unchanged':source_unchanged,
          'not_executed':['calculate.py','application','SDK','collector','warehouse','browser','live experiment']}
(ROOT/'comparison.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'numeric_and_ledger_comparisons':len(results),'all_match':True,
                  'authored_hashes_verified':len(verified_hashes),'reviewed_originals_unchanged':len(source_unchanged)}))
