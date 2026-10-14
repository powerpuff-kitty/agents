from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,importlib.util
BASE=Path('/private/tmp/standalone-pilot-2026-10-14/review');SOURCE=BASE/'candidate-source';OUT=BASE/'correction-recheck-artifacts'
OUT.mkdir(exist_ok=False);(OUT/'logs').mkdir();(OUT/'scratch').mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((BASE/'candidate-source-sha256.json').read_text())
assert all(sha(SOURCE/name)==digest for name,digest in manifest.items())
assert {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*') if p.is_file()}==set(manifest)
assert not any(p.is_symlink() for p in SOURCE.rglob('*'))
(ROOT:=OUT/'source').mkdir()
for name in manifest:
 dest=ROOT/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/name,dest)
assert not (ROOT/'.git').exists()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(OUT/'scratch'),GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
commands=[['scripts/validate.py'],['scripts/check_docs.py'],['scripts/build.py','--adapter','portable'],['scripts/build.py','--adapter','opencode'],['scripts/build.py','--adapter','portable','--check'],['scripts/build.py','--adapter','opencode','--check'],['-m','unittest','discover','-s','tests','-v']]
records=[]
for i,command in enumerate(commands,1):
 argv=[sys.executable,'-B',*command]
 result=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True,text=True,timeout=180)
 log=OUT/'logs'/f'gate-{i:02d}.log';log.write_text(result.stdout+result.stderr)
 records.append({'argv':argv,'cwd':str(ROOT),'exit':result.returncode,'log':str(log.relative_to(OUT))})
 (OUT/'gates.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(records[-1]),flush=True)
 assert result.returncode==0,log
# Make a source copy nested inside a synthetic parent repository. It has no own .git.
parent=OUT/'parent-repository';parent.mkdir()
(parent/'marker.txt').write_text('Synthetic parent identity, never candidate provenance.\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=parent,env=env,text=True).strip()
git('init','-q');git('add','marker.txt');git('-c','user.name=Review Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic parent fixture')
parent_revision=git('rev-parse','HEAD')
nested=parent/'extracted-source';shutil.copytree(SOURCE,nested)
assert not (nested/'.git').exists()
spec=importlib.util.spec_from_file_location('archive_behavior_eval',nested/'scripts/behavior_eval.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
skills=OUT/'synthetic-skills'
for name in sorted({skill for role,skill in module.CASES.values()}):
 folder=skills/name;(folder/'tests/fixtures').mkdir(parents=True)
 (folder/'SKILL.md').write_text('---\nname: '+name+'\ndescription: Synthetic local preparation test.\n---\n')
 (folder/'tests/fixtures/input.json').write_text('{"synthetic":true}\n')
 (folder/'tests/fixtures/gateway.py').write_text('def authorize(*args): return False\n')
# module.prepare fixture Git commits are explicitly allowed and remain below OUT.
original_env={k:os.environ.get(k) for k in ['TMPDIR','GIT_CONFIG_NOSYSTEM','GIT_CONFIG_GLOBAL']}
os.environ.update({k:env[k] for k in original_env})
prepared=[]
try:
 for case in module.CASES:
  for discovery in [False,True]:
   initial=module.prepare(case,OUT/'prepared'/(case+('-discovery' if discovery else '-explicit')),skills,discovery)
   assert initial['source_revision'] is None,(case,initial['source_revision'],parent_revision)
   assert initial['skills_revision'] is None
   assert initial['preparer_sha256']==sha(nested/'scripts/behavior_eval.py')
   assert initial['workspace_sha256'] and initial['instruction_sha256'] and initial['task_sha256']
   prepared.append({'case':case,'discovery':discovery,'source_revision':initial['source_revision'],'preparer_sha256':initial['preparer_sha256'],'workspace_files':len(initial['workspace_sha256']),'instruction_files':len(initial['instruction_sha256'])})
finally:
 for k,value in original_env.items():
  if value is None:os.environ.pop(k,None)
  else:os.environ[k]=value
(OUT/'preparation.json').write_text(json.dumps({'synthetic_parent_revision':parent_revision,'preparations':prepared,'no_parent_revision_guessed':True},indent=2)+'\n')
print(json.dumps({'gate_commands':len(records),'all_exit_zero':True,'archive_preparations':len(prepared),'source_revision_null':True,'parent_revision_not_used':True}))
