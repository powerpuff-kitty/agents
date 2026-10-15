"""Separate correction evidence; never rewrites original review records.
Inspect workspaces only after collected result. No network, packages, original writes.
"""
import ast, datetime, hashlib, json, pathlib, shutil, subprocess
OUT=pathlib.Path(__file__).parent
ROOT=pathlib.Path('/private/tmp/native-corrections-followup-20261015')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def command(argv,cwd):
    p=subprocess.run(argv,cwd=cwd,text=True,capture_output=True,timeout=30)
    return dict(argv=argv,cwd=str(cwd),returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
preparer=ROOT/'collectors/native_fixtures.py'
tree=ast.parse(preparer.read_text())
candidate=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='PORT_CHECK' for t in n.targets))
candidate_path=OUT/'correction-inputs/PORT_CHECK.mjs';candidate_path.parent.mkdir(exist_ok=True);candidate_path.write_text(candidate)
old=pathlib.Path('/private/tmp/native-failures-followup-20261015/18-implementation-unavailable-check-named-agent-1')
negative=OUT/'correction-disposable/prior-failed-implementation';negative.mkdir(parents=True,exist_ok=True)
shutil.copyfile(old/'workspace/port.ts',negative/'port.ts');(negative/'port.contract.check.mjs').write_text(candidate)
ev=dict(collected_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),root=str(ROOT),plan_sha256=digest(ROOT/'plan.json'),plan_hash_matches=digest(ROOT/'plan.json')==(ROOT/'plan.sha256').read_text().split()[0],preparer_sha256=digest(preparer),candidate_sha256=digest(candidate_path),negative_control={'original_result_sha256':digest(old/'result.json'),'source_sha256':digest(old/'workspace/port.ts'),'command':command(['node','--experimental-strip-types','port.contract.check.mjs'],negative)},runs=[])
ev['original_review_hashes_unchanged']=all(digest(OUT/f)==h for f,h in read(OUT/'original-report.sha256.json').items())
for r in read(ROOT/'plan.json')['runs']:
    d=ROOT/r['id'];e={'id':r['id']}
    if not (d/'result.json').exists() or read(d/'result.json').get('status')!='collected':
        e['state']='pending; workspace not inspected';ev['runs'].append(e);continue
    e.update(state='completed',result_sha256=digest(d/'result.json'),prompt_hash_matches=digest(d/'prompt.txt')==r['prompt_sha256'])
    prior=old if r['case']=='implementation-unavailable-check' else pathlib.Path('/private/tmp/native-coverage-followup-20261015/04-architecture-proposed-decision-named-agent-1')
    e['comparison_to_prior']={'prior_result_sha256':digest(prior/'result.json'),'prior_initial':read(prior/'initial.json'),'correction_initial':read(d/'initial.json'),'prior_runtime_check_sha256':read(prior/'before.json').get('port.contract.check.mjs'),'correction_runtime_check_sha256':read(d/'before.json').get('port.contract.check.mjs')}
    snap=OUT/'correction-evidence'/r['id'];snap.mkdir(parents=True,exist_ok=True)
    e['retained_sha256']={str(p.relative_to(d)):digest(p) for p in d.rglob('*') if p.is_file() and 'workspace' not in p.relative_to(d).parts}
    for p in d.iterdir():
        if p.is_file():shutil.copyfile(p,snap/p.name)
    e['actual_workspace_sha256']={str(p.relative_to(d/'workspace')):digest(p) for p in (d/'workspace').rglob('*') if p.is_file() and '.git' not in p.relative_to(d/'workspace').parts}
    e['actual_matches_after']=e['actual_workspace_sha256']==read(d/'after.json')
    before=read(d/'before.json');after=read(d/'after.json')
    e['changed_files']=[k for k in sorted(set(before)|set(after)) if before.get(k)!=after.get(k)]
    e['git_before']=read(d/'git-before.json');e['git_after']=read(d/'git-after.json')
    for p in (d/'workspace').rglob('*'):
        rel=p.relative_to(d/'workspace')
        if not p.is_file() or any(x in rel.parts for x in ['.git','.agents','.opencode']):continue
        dest=snap/'source'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    e['reviewer_commands']=[]
    if r['case']=='implementation-unavailable-check':
        disposable=OUT/'correction-disposable'/r['id'];disposable.mkdir(parents=True,exist_ok=True)
        for fn in ['port.ts','port.contract.check.mjs']:shutil.copyfile(d/'workspace'/fn,disposable/fn)
        e['check_matches_candidate']=digest(d/'workspace/port.contract.check.mjs')==ev['candidate_sha256']
        e['reviewer_commands'].append(command(['node','--experimental-strip-types','port.contract.check.mjs'],disposable))
        extra="""import assert from 'node:assert/strict';
import {port} from './port.ts';
let calls=0;
for(const value of [{toString(){calls++;throw new Error('hook')}},{[Symbol.toPrimitive](){calls++;throw new Error('hook')}},Object.assign([],{toString(){calls++;return '1'}})]) assert.throws(()=>port(value),TypeError);
assert.equal(calls,0);
for(const value of ['1\\n','1\\r','1\\r\\n','1\\u2028','1\\u2029','1\\t',' 1','1 ','1e0','0'.repeat(1000),'9'.repeat(1000)]) assert.throws(()=>port(value),TypeError);
for(const v of [1,65535,'00042','0'.repeat(1000)+'42']) assert.equal(port(v),Number(v));
console.log('Supplemental validation and no-coercion checks passed');
"""
        (disposable/'supplemental.mjs').write_text(extra)
        e['reviewer_commands'].append(command(['node','--experimental-strip-types','supplemental.mjs'],disposable))
    ev['runs'].append(e)
write(OUT/'correction-evidence.json',ev)
print(json.dumps({'plan_hash_matches':ev['plan_hash_matches'],'negative_control':ev['negative_control'],'runs':[{k:e[k] for k in ['id','state','result_sha256','actual_matches_after','changed_files','check_matches_candidate','reviewer_commands'] if k in e} for e in ev['runs']]},indent=2))
