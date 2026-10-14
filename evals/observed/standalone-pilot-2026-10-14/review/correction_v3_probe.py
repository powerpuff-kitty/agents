from pathlib import Path
import ast,hashlib,json,os,subprocess,sys
B=Path('/private/tmp/standalone-pilot-2026-10-14/review');O=B/'correction-v3-artifacts';O.mkdir();S=Path('/private/tmp/standalone-pilot-2026-10-14/pilot-tooling-correction/run_gates.v3.py');source=S.read_text()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inputs={str(S):sha(S)}
for name in ['report.md','actions.md','pilot-review.md','pilot-actions.md','correction-recheck.md','correction-v2-recheck.md']:
 inputs[str(B/name)]=sha(B/name)
(O/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
def configuration(n):return isinstance(n,(ast.Assign,ast.AugAssign)) and ((isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='commands' for t in n.targets)) or (isinstance(n,ast.AugAssign) and isinstance(n.target,ast.Name) and n.target.id=='commands'))
def stripped(text):
 tree=ast.parse(text);tree.body=[n for n in tree.body if not configuration(n)];return ast.dump(tree,include_attributes=False)
results=[]
for label,command in [('clean-success',['/usr/bin/true']),('clean-failure',['/usr/bin/false']),('initially-deleted-tracked',[sys.executable,'-B','-c',"from pathlib import Path;Path('gate-executed.txt').write_text('must not run')"])]:
 root=O/label;project=root/'project';project.mkdir(parents=True);(project/'fixture.txt').write_text('Synthetic source.\n')
 def git(*args):return subprocess.check_output(['git',*args],cwd=project,env=env,text=True).strip()
 git('init','-q');git('add','fixture.txt');git('-c','user.name=Review Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic v3 fixture');revision=git('rev-parse','HEAD')
 if label=='initially-deleted-tracked':(project/'fixture.txt').unlink()
 tree=ast.parse(source);first=next(i for i,n in enumerate(tree.body) if configuration(n));tree.body=[n for n in tree.body if not configuration(n)];tree.body.insert(first,ast.parse('commands = '+repr([command])).body[0]);ast.fix_missing_locations(tree)
 script=root/'run_gates.py';script.write_text(ast.unparse(tree)+'\n');assert stripped(source)==stripped(script.read_text())
 r=subprocess.run([sys.executable,'-B',str(script)],cwd=root,env=env,capture_output=True,text=True,timeout=30)
 (root/'stdout.txt').write_text(r.stdout);(root/'stderr.txt').write_text(r.stderr)
 initial=json.loads((root/'logs/source-before.json').read_text());assert initial['revision']==revision
 gates=root/'logs/gate-results.json';log_count=len(list((root/'logs').glob('gate-*.log')))
 if label=='initially-deleted-tracked':
  assert r.returncode==1 and initial['status_before']=='D fixture.txt'
  assert initial['tracked_sha256'] is None and initial['hash_status']=='not_collected_dirty_source'
  assert not (project/'gate-executed.txt').exists() and not (project/'fixture.txt').exists()
  assert not gates.exists() and log_count==0
 else:
  assert r.returncode==(0 if label=='clean-success' else 1)
  assert initial['status_before']=='' and initial['tracked_sha256']['fixture.txt']==sha(project/'fixture.txt')
  assert log_count==1
  assert json.loads(gates.read_text())[0]['exit']==r.returncode
 results.append({'case':label,'runner_exit':r.returncode,'initial_identity':initial,'command_log_count':log_count,'gate_results_recorded':gates.exists(),'gate_sentinel_present':(project/'gate-executed.txt').exists(),'script_sha256':sha(script)})
 print(json.dumps({k:v for k,v in results[-1].items() if k!='initial_identity'}),flush=True)
assert all(sha(Path(p))==h for p,h in inputs.items())
(O/'results.json').write_text(json.dumps({'reviewed_v3_sha256':sha(S),'probes':results,'inputs_and_earlier_reports_unchanged':True},indent=2)+'\n')
