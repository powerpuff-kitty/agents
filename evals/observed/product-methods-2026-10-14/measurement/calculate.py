"""Offline synthetic measurement exercise; Python standard library only.
Rerun: python3 /private/tmp/measurement-methods-forward-2026-10-14/calculate.py
Source allowlist deliberately excludes cases, reviewer notes, and product sources.
"""
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
from math import sqrt, erfc, comb
import hashlib, json, platform, shutil, sys

OUT = Path(__file__).resolve().parent
SKILLS = Path('/Users/tcsntcsn/TCSN/skills')
AGENTS = Path('/Users/tcsntcsn/TCSN/agents')
NAMES = ('product-instrumentation', 'product-analytics', 'product-experimentation')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(name, obj): (OUT/name).write_text(json.dumps(obj, indent=2)+'\n')
def iso(s): return datetime.fromisoformat(s.replace('Z', '+00:00'))
paths=[]
for name in NAMES:
    for rel in ('SKILL.md', 'references/method.md', 'assets/report-template.md', 'tests/fixtures/input.json'):
        paths.append((SKILLS/name/rel, OUT/'sources'/'skills'/name/rel))
for rel in ('agents/data-analyst/instructions.md', 'agents/scientist/instructions.md', 'shared/operating-contract.md'):
    paths.append((AGENTS/rel, OUT/'sources'/'roles'/rel))
manifest=[]
for src,dst in paths:
    if dst.exists():
        if sha(src)!=sha(dst): raise RuntimeError(f'Source changed since retained snapshot: {src}')
    else:
        dst.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(src,dst)
    manifest.append({'source':str(src),'copy':str(dst.relative_to(OUT)),'sha256':sha(src),'bytes':src.stat().st_size})
write_json('source-manifest.json',manifest)
write_json('runtime.json',{'python':sys.version,'platform':platform.platform(),'packages':'standard library only','source_file_allowlist_entries':len(paths)})
inputs={n:json.loads((OUT/'sources'/'skills'/n/'tests/fixtures/input.json').read_text()) for n in NAMES}

# Tracking: the supplied contract names required and allowed keys, event and revision.
# Type checks below are explicit local QA assumptions, not a supplied type schema.
x=inputs[NAMES[0]]; c=x['contract']; seen={}; rows=[]
for number,e in enumerate(x['events'],1):
    missing=sorted(set(c['required'])-set(e)); extra=sorted(set(e)-set(c['allowed']))
    issues=[]
    if missing: issues.append('missing_required')
    if extra: issues.append('unexpected_field')
    if e.get('event')!=c['event']: issues.append('event_mismatch')
    if e.get('schema_version')!=c['version']: issues.append('version_mismatch')
    for k in c['required']:
        if k in e and (not isinstance(e[k],str) or not e[k]): issues.append('proposed_string_type_or_empty:'+k)
    if 'occurred_at' in e:
        try:
            if iso(e['occurred_at']).tzinfo is None: issues.append('timezone_missing')
        except (ValueError,TypeError): issues.append('timestamp_parse')
    key=e.get('event_id'); duplicate=key in seen
    conflict=duplicate and seen[key]!=e
    if not duplicate: seen[key]=e
    rows.append({'row':number,'event_id':key,'missing_fields':missing,'unexpected_field_names':extra,'issues':issues,'schema_accept':not issues,'duplicate_of_previous':duplicate,'conflicting_duplicate':conflict,'accepted_under_local_strict_policy':not issues and not duplicate})
t={'raw_rows':len(rows),'distinct_event_ids':len(seen),'schema_pass_rows':sum(r['schema_accept'] for r in rows),'schema_rejected_rows':sum(not r['schema_accept'] for r in rows),'duplicate_rows':sum(r['duplicate_of_previous'] for r in rows),'accepted_unique_rows':sum(r['accepted_under_local_strict_policy'] for r in rows),'rows':rows,'policy':'Reject missing/disallowed fields; keep first exact event_id once within this fixture. Local batch policy only; no deployed retention/deduplication window claimed.'}
assert (t['raw_rows'],t['schema_pass_rows'],t['schema_rejected_rows'],t['duplicate_rows'],t['accepted_unique_rows'])==(4,2,2,1,1)
write_json('instrumentation-calculations.json',t)

# Funnel: earliest eligible entry per supplied explicit unit_id; closed 0..48h
# interval, timestamps <= observation_end, no other identity links.
x=inputs[NAMES[1]]; cutoff=iso(x['observation_end']); window=timedelta(hours=x['window_hours'])
unique={}; invalid=[]; duplicate_rows=[]; future=[]
for i,e in enumerate(x['events'],1):
    if not all(k in e for k in ('event_id','unit_id','event','at')): invalid.append(i); continue
    at=iso(e['at'])
    if at>cutoff: future.append(i); continue
    if e['event_id'] in unique:
        if unique[e['event_id']]!=e: raise RuntimeError('Conflicting event ID')
        duplicate_rows.append(i)
    else: unique[e['event_id']]=e
units=defaultdict(list)
for e in unique.values(): units[e['unit_id']].append(e)
ledger=[]
for unit,events in sorted(units.items()):
    entries=[e for e in events if e['event']==x['entry_event']]
    if not entries:
        ledger.append({'unit':unit,'entrant':False,'mature':None,'converted_in_window':None,'reason':'conversion without observed entry; excluded from funnel'})
        continue
    entry=min(iso(e['at']) for e in entries)
    outcomes=[iso(e['at']) for e in events if e['event']==x['conversion_event']]
    eligible=[d for d in outcomes if entry<=d<=entry+window]
    mature=entry+window<=cutoff
    ledger.append({'unit':unit,'entrant':True,'entry':entry.isoformat(),'window_end':(entry+window).isoformat(),'observed_hours':min((cutoff-entry).total_seconds()/3600,x['window_hours']),'mature':mature,'converted_in_window':bool(eligible),'out_of_window_conversion_count':sum(d>entry+window for d in outcomes),'conversion_before_entry_count':sum(d<entry for d in outcomes)})
entrants=[r for r in ledger if r['entrant']]; mature=[r for r in entrants if r['mature']]; immature=[r for r in entrants if not r['mature']]
numerator=sum(r['converted_in_window'] for r in mature); denominator=len(mature)
a={'raw_rows':len(x['events']),'valid_rows':len(x['events'])-len(invalid),'after_deduplication':len(unique),'duplicate_rows':duplicate_rows,'invalid_rows':invalid,'after_cutoff_rows':future,'distinct_units':len(units),'eligible_entrants':len(entrants),'excluded_nonentrant_units':len(units)-len(entrants),'mature_entrants':denominator,'immature_entrants':len(immature),'mature_converters':numerator,'mature_conversion_rate':numerator/denominator if denominator else None,'observed_all_entrant_rate_incomplete':sum(r['converted_in_window'] for r in entrants)/len(entrants),'eventual_current_entrant_rate_lower_bound':numerator/len(entrants),'eventual_current_entrant_rate_upper_bound':(numerator+len(immature))/len(entrants),'ledger':ledger}
assert a['raw_rows']==8 and a['after_deduplication']==7 and (len(entrants),denominator,len(immature),numerator)==(4,3,1,1)
write_json('analytics-calculations.json',a)

# Experiment: Pearson goodness-of-fit at assigned account grain, df=1.
# p=erfc(sqrt(chi_square/2)); exact binomial two-sided corroboration for 50:50.
x=inputs[NAMES[2]]; counts=x['counts']; assert all(isinstance(v,int) and v>=0 for arm in counts.values() for v in arm.values()); assert all(arm['converted']<=arm['assigned'] for arm in counts.values()); n0=counts['control']['assigned']; n1=counts['treatment']['assigned']; total=n0+n1
expected0=total*x['planned_allocation']['control']; expected1=total*x['planned_allocation']['treatment']
chi=(n0-expected0)**2/expected0+(n1-expected1)**2/expected1
p_srm=erfc(sqrt(chi/2)); p_exact=2*sum(comb(total,k) for k in range(min(n0,n1)+1))/(2**total)
c0=counts['control']['converted']; c1=counts['treatment']['converted']; r0=c0/n0; r1=c1/n1; diff=r1-r0
se=sqrt(r0*(1-r0)/n0+r1*(1-r1)/n1)
e={'assigned':{'control':n0,'treatment':n1,'total':total},'expected_assigned':{'control':expected0,'treatment':expected1},'allocation_observed':{'control':n0/total,'treatment':n1/total},'srm':{'method':'Pearson goodness-of-fit, df=1, asymptotic chi-square tail','chi_square':chi,'df':1,'p_value':p_srm,'exact_binomial_two_sided_p':p_exact,'alpha':'not predeclared in supplied input; diagnostic p-values only'},'rates':{'control':r0,'treatment':r1},'effect':{'absolute_difference':diff,'relative_change':diff/r0,'standard_error_unpooled_independent_binomial':se,'exploratory_95pct_normal_interval':[diff-1.959963984540054*se,diff+1.959963984540054*se],'interval_caveat':'Unplanned illustrative precision only, assumes independent fully observed binary accounts and valid measurement. Unresolved SRM blocks causal interpretation; no confirmatory primary outcome test performed.'},'exposure_counts':None,'analysis_account_rows_available':False,'guardrail_results':None,'decision':'Do not infer causal lift or approve rollout. Investigate unresolved allocation discrepancy and measurement/exposure validity first.'}
assert chi==20 and r0==.05 and r1==.06 and 0<p_srm<.00001
write_json('experiment-calculations.json',e)
# Source identity verification after all calculations.
assert all(sha(Path(m['source']))==m['sha256']==sha(OUT/m['copy']) for m in manifest)
print(json.dumps({'instrumentation':{k:v for k,v in t.items() if k not in ('rows','policy')},'analytics':{k:v for k,v in a.items() if k!='ledger'},'experiment':e,'source_checks':'15 retained source/copy SHA-256 matches; self-check assertions passed'},indent=2))
