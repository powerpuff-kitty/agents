from pathlib import Path
import hashlib, importlib.util, json, os, re, subprocess, sys
from datetime import datetime, timedelta
from collections import Counter
from math import erfc, sqrt

OUT=Path('/private/tmp/product-methods-independent-review-2026-10-14')
SKILLS=Path('/Users/tcsntcsn/TCSN/skills')
AGENTS=Path('/Users/tcsntcsn/TCSN/agents')
NEW=['product-instrumentation','product-analytics','product-experimentation','competitor-monitoring','native-app-delivery','user-research','market-opportunity-research']
ROLES=['data-analyst','feature-developer','performance-engineer','quality-engineer','release-engineer','researcher','scientist','user-researcher']
files=[]
for name in NEW:
    files.extend(p for p in (SKILLS/name).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
files.extend(SKILLS/x for x in ['README.md','product-design/SKILL.md','competitive-research/SKILL.md','test-engineering/SKILL.md','test-engineering/references/browser-recovery.md','test-engineering/tests/cases.json','test-engineering/tests/fixtures/browser-recovery.json','performance-audit/SKILL.md','performance-audit/references/recovery-evidence.md'])
files.extend(AGENTS/'agents'/x/'instructions.md' for x in ROLES)
files=sorted(set(files))
def hashes():
    return [{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files]
before=hashes(); (OUT/'inspected-files.json').write_text(json.dumps(before,indent=2)+'\n')
commands=[]
def run(argv,cwd=None):
    env=os.environ.copy();env.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(OUT))
    r=subprocess.run(argv,cwd=cwd,env=env,text=True,capture_output=True)
    commands.append({'argv':argv,'cwd':str(cwd) if cwd else None,'environment_overrides':{'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(OUT)},'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    return r
r=run(['python3','--version'])
r=run(['python3','-B','-m','unittest','discover','-s','competitor-monitoring/tests','-v'],SKILLS)
helper=SKILLS/'competitor-monitoring/scripts/compare_snapshots.py'
r=run(['python3','-B',str(helper),str(SKILLS/'competitor-monitoring/tests/fixtures/baseline.json'),str(SKILLS/'competitor-monitoring/tests/fixtures/current.json')])
# Independent edge probes; all inputs and subprocess temporaries stay in OUT.
probe=OUT/'probes';probe.mkdir(exist_ok=True)
snapshot={'format_version':1,'captured_at':'2026-10-14T12:00:00Z','sources':[]}
for label,sources in [('empty-inventory',[]),('empty-facts',[{'id':'pricing','locator':'https://vendor.example/pricing','status':'ok','observed_at':'2026-10-14T11:00:00Z','facts':[]}])]:
    a={**snapshot,'sources':sources};b={**a,'captured_at':'2026-10-15T12:00:00Z'}
    pa=probe/(label+'-baseline.json');pb=probe/(label+'-current.json')
    pa.write_text(json.dumps(a));pb.write_text(json.dumps(b))
    run(['python3','-B',str(helper),str(pa),str(pb)])
json_results=[];links=[]
for p in files:
    if p.suffix=='.json':
        v=json.loads(p.read_text());json_results.append({'file':str(p),'parsed':True})
    if p.suffix=='.md':
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'): continue
            path=target.split('#',1)[0]
            links.append({'file':str(p),'target':target,'exists':(p.parent/path).exists()})
(OUT/'source-checks.json').write_text(json.dumps({'json_parse':json_results,'relative_links':links,'external_links':'not fetched; network out of scope'},indent=2)+'\n')

def load(skill):return json.loads((SKILLS/skill/'tests/fixtures/input.json').read_text())
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
inst=load('product-instrumentation');allowed=set(inst['contract']['allowed']);required=set(inst['contract']['required']);seen=set();qa=[]
for n,e in enumerate(inst['events'],1):
    qa.append({'row':n,'duplicate_event_id':e.get('event_id') in seen,'missing_fields':sorted(required-e.keys()),'unexpected_property_names':sorted(e.keys()-allowed)})
    seen.add(e.get('event_id'))
a=load('product-analytics');unique={};replays=0
for e in a['events']:
    if e['event_id'] in unique: replays+=1
    else:unique[e['event_id']]=e
cutoff=dt(a['observation_end']);window=timedelta(hours=a['window_hours']);units=[]
for u in sorted({e['unit_id'] for e in unique.values()}):
    rows=[e for e in unique.values() if e['unit_id']==u]
    starts=[dt(e['at']) for e in rows if e['event']==a['entry_event'] and dt(e['at'])<=cutoff]
    if not starts: units.append({'unit':u,'classification':'no_entry'});continue
    start=min(starts);mature=start+window<=cutoff
    outcomes=[e for e in rows if e['event']==a['conversion_event'] and start<=dt(e['at'])<=start+window and dt(e['at'])<=cutoff]
    units.append({'unit':u,'mature':mature,'valid_conversion':bool(outcomes)})
exp=load('product-experimentation');counts=exp['counts'];total=sum(c['assigned'] for c in counts.values());chi=sum((counts[k]['assigned']-total*p)**2/(total*p) for k,p in exp['planned_allocation'].items())
market=load('market-opportunity-research');segments=market['segments'];prices=[s['list_price']*(12 if s['price_period']=='month' else 1) for s in segments];overlap=market['overlap']['buying_units_in_both'];base=sum((s['buying_units']-overlap)*price for s,price in zip(segments,prices))
calculations={'scope':'Local synthetic fixture arithmetic and source-informed walkthrough, not blinded model-evaluation outcomes, actual collector/browser/device/participant/production evidence, or externally verified market facts. Acceptance case files unchanged.',
'instrumentation':{'raw_rows':len(inst['events']),'rows':qa,'sensitive_values':'not copied'},
'analytics':{'raw_rows':len(a['events']),'deduplicated_rows':len(unique),'replays':replays,'unit_reconciliation':units,'mature_denominator':sum(x.get('mature',False) for x in units),'mature_converters':sum(x.get('mature',False) and x.get('valid_conversion',False) for x in units)},
'experimentation':{'descriptive_rates':{k:c['converted']/c['assigned'] for k,c in counts.items()},'assignment_chi_square_df1':chi,'assignment_srm_p_df1':erfc(sqrt(chi/2)),'limits':'Assignment mechanism, exposures, guardrails and concrete outcome window not supplied; rates descriptive, causal interpretation blocked.'},
'market':{'distinct_hypothetical_buying_units':sum(s['buying_units'] for s in segments)-overlap,'annual_list_prices':prices,'illustrative_revenue_bounds':[base+overlap*min(prices),base+overlap*max(prices)],'assumption':'Each overlapping buying unit buys exactly one of the two listed packages; no demand, reach, transaction-price or revenue validation.'}}
(OUT/'fixture-arithmetic.json').write_text(json.dumps(calculations,indent=2)+'\n')
(OUT/'commands-results.json').write_text(json.dumps(commands,indent=2)+'\n')
after=hashes();(OUT/'source-stability.json').write_text(json.dumps({'unchanged':before==after,'file_count':len(files)},indent=2)+'\n')
print(json.dumps({'reviewed_files':len(files),'commands':[{'argv':x['argv'],'exit_code':x['exit_code']} for x in commands],'json_files':len(json_results),'broken_links':[x for x in links if not x['exists']],'source_stable':before==after,'calculations':calculations},indent=2))
