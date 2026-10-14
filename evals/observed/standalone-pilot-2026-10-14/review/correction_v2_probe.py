from pathlib import Path
import ast,hashlib,json,os,subprocess,sys
B=Path('/private/tmp/standalone-pilot-2026-10-14/review');O=B/'correction-v2-artifacts';O.mkdir();T=Path('/private/tmp/standalone-pilot-2026-10-14/pilot-tooling-correction');source=(T/'run_gates.v2.py').read_text()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
def configuration(n):return isinstance(n,(ast.Assign,ast.AugAssign)) and ((isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='commands' for t in n.targets)) or (isinstance(n,ast.AugAssign) and isinstance(n.target,ast.Name) and n.target.id=='commands'))
def stripped(text):
 tree=ast.parse(text);tree.body=[n for n in tree.body if not configuration(n)];return ast.dump(tree,include_attributes=False)
inputs={str(p):sha(p) for p in [T/'run_gates.v2.py',T/'checks-v2.json',T/'correction-v2.md',B/'correction-recheck.md',B/'correction-recheck-artifacts/evidence-sha256.json']}
(O/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
results=[]
true=['/usr/bin/true'];false=['/usr/bin/false'];py=lambda code:[sys.executable,'-B','-c',code]
cases=[('clean-success',[true],None),('failed-command-and-retained-later-log',[false,true],None),('tracked-source-changed',[py("from pathlib import Path;Path('fixture.txt').write_text('changed\\n')")],None),('dirty-tracked-before',[true],'tracked'),('dirty-untracked-after',[py("from pathlib import Path;Path('owner-draft.txt').write_text('new\\n')")],None),('owner-draft-delete-command-refused',[py("from pathlib import Path;Path('owner-draft.txt').unlink()")],'untracked'),('dirty-deleted-tracked-before',[true],'deleted')]
for label,commands,dirty in cases:
 root=O/label;project=root/'project';project.mkdir(parents=True);(project/'fixture.txt').write_text('original\n')
 def git(*args):return subprocess.check_output(['git',*args],cwd=project,env=env,text=True)
 git('init','-q');git('add','fixture.txt');git('-c','user.name=Review Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic v2 runner fixture')
 if dirty=='tracked':(project/'fixture.txt').write_text('owner edit\n')
 elif dirty=='untracked':(project/'owner-draft.txt').write_text('Owner draft must survive.\n')
 elif dirty=='deleted':(project/'fixture.txt').unlink()
 before={p.name:(p.read_bytes(),p.stat().st_mode & 0o777,p.stat().st_mtime_ns) for p in project.iterdir() if p.is_file()}
 tree=ast.parse(source);index=next(i for i,n in enumerate(tree.body) if configuration(n));tree.body=[n for n in tree.body if not configuration(n)];tree.body.insert(index,ast.parse('commands = '+repr(commands)).body[0]);ast.fix_missing_locations(tree)
 script=root/'run_gates.py';script.write_text(ast.unparse(tree)+'\n');assert stripped(source)==stripped(script.read_text())
 r=subprocess.run([sys.executable,'-B',str(script)],cwd=root,env=env,capture_output=True,text=True,timeout=30)
 (root/'stdout.txt').write_text(r.stdout);(root/'stderr.txt').write_text(r.stderr)
 identity=root/'logs/source-before.json';gates=root/'logs/gate-results.json';after=root/'logs/source-after.json'
 current={p.name:(p.read_bytes(),p.stat().st_mode & 0o777,p.stat().st_mtime_ns) for p in project.iterdir() if p.is_file()}
 entry={'case':label,'runner_exit':r.returncode,'initial_identity_recorded':identity.exists(),'command_log_count':len(list((root/'logs').glob('gate-*.log'))),'gate_results_recorded':gates.exists(),'project_files_unchanged':current==before,'script_sha256':sha(script)}
 if identity.exists():entry['status_before']=json.loads(identity.read_text())['status_before']
 if gates.exists():entry['subcommand_exits']=[item['exit'] for item in json.loads(gates.read_text())]
 if after.exists():entry['source_after']=json.loads(after.read_text())
 results.append(entry);print(json.dumps(entry),flush=True)
 assert r.returncode==(0 if label=='clean-success' else 1)
 if dirty:assert current==before and entry['command_log_count']==0
 if dirty=='untracked':assert (project/'owner-draft.txt').read_bytes()==b'Owner draft must survive.\n'
# Inspect allowed raw v2 probe evidence without taking its summaries as proof.
provided=[]
for name in ['v2-positive','v2-negative','v2-owner-draft']:
 root=T/name
 if root.exists():
  assert stripped(source)==stripped((root/'run_gates.py').read_text())
  item={'case':name,'script_sha256':sha(root/'run_gates.py'),'stdout':(root/'stdout.txt').read_text(),'stderr':(root/'stderr.txt').read_text()}
  for f in ['source-before.json','source-after.json','gate-results.json']:
   if (root/'logs'/f).exists():item[f]=json.loads((root/'logs'/f).read_text())
  provided.append(item)
(O/'provided-evidence.json').write_text(json.dumps(provided,indent=2)+'\n')
assert all(sha(Path(p))==h for p,h in inputs.items())
summary={'runner_v2_sha256':sha(T/'run_gates.v2.py'),'probes':results,'input_identities_preserved':True}
(O/'results.json').write_text(json.dumps(summary,indent=2)+'\n')
