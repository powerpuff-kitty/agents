"""Independent offline replay from retained fixtures, with privacy-safe output."""
from pathlib import Path
from datetime import datetime, timedelta
from fractions import Fraction
from math import sqrt, erfc, comb
import hashlib
import json
import sys

TARGET = Path('/private/tmp/measurement-methods-forward-2026-10-14')
OUT = Path(__file__).resolve().parent
manifest = json.loads((TARGET/'source-manifest.json').read_text())
hashes = []
for row in manifest:
    path = TARGET/row['copy']
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == row['sha256'], row['copy']
    copied = OUT/'reviewed'/row['copy']
    copied.parent.mkdir(parents=True, exist_ok=True)
    copied.write_bytes(raw)
    current_digest = hashlib.sha256(Path(row['source']).read_bytes()).hexdigest()
    hashes.append({'path':str(path), 'sha256':digest, 'retained_manifest_match':True,
                   'original_source_path':row['source'], 'current_source_sha256':current_digest,
                   'current_matches_retained':current_digest == digest})
for name in ('task.md','source-manifest.json','instrumentation-report.md','analytics-report.md',
             'experiment-report.md','instrumentation-calculations.json','analytics-calculations.json',
             'experiment-calculations.json','result.md','actions.md','runtime.json','run-output.json',
             'verification.json','artifact-hashes.json'):
    path = TARGET/name
    raw = path.read_bytes()
    copied = OUT/'reviewed'/name
    copied.parent.mkdir(parents=True, exist_ok=True)
    copied.write_bytes(raw)
    hashes.append({'path':str(path),'sha256':hashlib.sha256(raw).hexdigest()})
(OUT/'reviewed-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')

def load(skill):
    return json.loads((OUT/'reviewed/sources/skills'/skill/'tests/fixtures/input.json').read_text())

instrument = load('product-instrumentation')
required = set(instrument['contract']['required'])
allowed = set(instrument['contract']['allowed'])
rows, groups = [], {}
for idx, event in enumerate(instrument['events']):
    missing = sorted(required-set(event))
    extras = sorted(set(event)-allowed)
    matching = event.get('event') == instrument['contract']['event'] and event.get('schema_version') == instrument['contract']['version']
    rows.append({'fixture_index':idx,'event_id':event.get('event_id'),'missing_property_names':missing,
                 'extra_property_names':extras,'declared_shape_pass':not missing and not extras and matching})
    groups.setdefault(event['event_id'],[]).append(idx)
instrument_result = {'raw_rows':len(rows),'unique_event_ids':len(groups),
                     'duplicate_groups':{key:value for key,value in groups.items() if len(value)>1},
                     'shape_valid_rows':sum(x['declared_shape_pass'] for x in rows),
                     'deduplicated_shape_valid_events':len({x['event_id'] for x in rows if x['declared_shape_pass']}),
                     'rows':rows,'live_emission_transport_collection_verified':False}

analytics = load('product-analytics')
parse = lambda value: datetime.fromisoformat(value.replace('Z','+00:00'))
end = parse(analytics['observation_end'])
window = timedelta(hours=analytics['window_hours'])
unique = {}
for event in analytics['events']:
    key = event['event_id']
    assert key not in unique or unique[key] == event, 'conflicting duplicate'
    unique.setdefault(key,event)
events = [e for e in unique.values() if parse(e['at']) <= end]
entries = {}
for event in sorted(events,key=lambda e:parse(e['at'])):
    if event['event'] == analytics['entry_event']:
        entries.setdefault(event['unit_id'],parse(event['at']))
ledger = []
for unit,entry in entries.items():
    times = sorted(parse(e['at']) for e in events if e['unit_id']==unit and e['event']==analytics['conversion_event'])
    within = [t for t in times if entry <= t <= entry+window]
    ledger.append({'unit':unit,'entry':entry.isoformat(),'mature':entry+window<=end,
                   'observed_followup_hours':min((end-entry).total_seconds()/3600,analytics['window_hours']),
                   'within_window_conversion':bool(within),
                   'conversion_hours_after_entry':[(t-entry).total_seconds()/3600 for t in times]})
mature = [x for x in ledger if x['mature']]
num = sum(x['within_window_conversion'] for x in mature)
orphan_units = sorted({e['unit_id'] for e in events if e['event']==analytics['conversion_event']} - entries.keys())
analytics_result = {'raw_rows':len(analytics['events']),'deduplicated_events':len(unique),
                    'entrant_units':len(entries),'mature_entrant_units':len(mature),
                    'immature_units':[x['unit'] for x in ledger if not x['mature']],
                    'mature_conversion_numerator':num,'mature_conversion_denominator':len(mature),
                    'mature_conversion_rate':num/len(mature),'observed_all_entrant_rate':sum(x['within_window_conversion'] for x in ledger)/len(ledger),
                    'orphan_conversion_units':orphan_units,'ledger':ledger,
                    'window_boundary_convention':'entry <= conversion <= entry+48h; no boundary-sensitive events in fixture'}

experiment = load('product-experimentation')
c,t = experiment['counts']['control'],experiment['counts']['treatment']
cr,tr = Fraction(c['converted'],c['assigned']),Fraction(t['converted'],t['assigned'])
delta = tr-cr
n = c['assigned']+t['assigned']
expected = {k:n*v for k,v in experiment['planned_allocation'].items()}
chisq = sum((experiment['counts'][k]['assigned']-value)**2/value for k,value in expected.items())
chi_p = erfc(sqrt(chisq/2))
exact_two_sided = 2*sum(comb(n,k) for k in range(min(c['assigned'],t['assigned'])+1))/(2**n)
se = sqrt(float(cr*(1-cr))/c['assigned']+float(tr*(1-tr))/t['assigned'])
ci = [float(delta)-1.959963984540054*se,float(delta)+1.959963984540054*se]
experiment_result = {'analysis_unit':'account','assigned_total':n,'expected_assignment_counts':expected,
                     'assignment_chi_square_df1':chisq,'assignment_chi_square_survival':chi_p,
                     'two_sided_exact_binomial_srm_p':exact_two_sided,
                     'control_rate':float(cr),'treatment_rate':float(tr),
                     'absolute_rate_difference':float(delta),'absolute_percentage_point_difference':float(delta*100),
                     'relative_difference':float(delta/cr),
                     'illustrative_unpooled_normal_difference_95_interval':ci,
                     'interval_limit':'Exploratory iid-binomial normal approximation, not predeclared inference or valid causal evidence; SRM and measurement gaps unresolved.',
                     'missing':['exposure logs','assignment implementation','guardrails','actual declared outcome window','practical threshold','planned inferential method'],
                     'rollout_authorized':False}

result = {'kind':'independent retained-copy-only synthetic replay; not product execution',
          'python':sys.version,'instrumentation':instrument_result,'analytics':analytics_result,'experiment':experiment_result}
(OUT/'independent-calculations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'retained_source_hashes_verified':len(manifest),'current_drifted_sources':[x['original_source_path'] for x in hashes if x.get('current_matches_retained') is False],
                  'instrumentation_valid_unique':instrument_result['deduplicated_shape_valid_events'],
                  'mature_conversion':[num,len(mature)],'srm_chi_square':chisq,
                  'srm_p':chi_p,'exact_binomial_p':exact_two_sided,'effect_pp':float(delta*100),
                  'product_tests':0}))
