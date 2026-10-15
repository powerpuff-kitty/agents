import hashlib,io,json,subprocess,tarfile
from pathlib import Path
root=Path(__file__).resolve().parent;repo=Path('/Users/tcsntcsn/TCSN/agents');source=root/'source';source.mkdir()
revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git','archive',revision],cwd=repo))) as tar:tar.extractall(source,filter='data')
target=root/'installed/agents';target.mkdir(parents=True);unrelated=target/'unrelated.md';unrelated.write_text('Owner unrelated profile: preserve.\n');unrelated.chmod(0o600)
def snap():
 return {str(p.relative_to(target.parent)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'mode':oct(p.stat().st_mode&0o777)} for p in sorted(target.parent.rglob('*')) if p.is_file()}
records=[];checks={}
def run(name,*flags,exit=0):
 argv=['python3','scripts/install.py','--agent','designer','--target',str(target),*flags]
 result=subprocess.run(argv,cwd=source,text=True,capture_output=True,timeout=30)
 records.append({'step':name,'argv':argv,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
 assert result.returncode==exit,(name,result.stderr)
 return json.loads(result.stdout) if result.returncode==0 else None
before=snap();run('initial dry run','--dry-run');checks['dry_run_no_writes']=snap()==before
run('initial partial install');designer=target/'designer.md';original=designer.read_bytes();designer.chmod(0o640)
upstream=source/'agents/designer/instructions.md';upstream.write_text(upstream.read_text()+'\nSynthetic upstream update for disposable installation exercise.\n')
custom=original+b'\nOwner local customization: preserve unless replacement is explicit.\n';designer.write_bytes(custom)
before=snap();run('local edit conflict',exit=1);checks['conflict_preserves_all_bytes_and_modes']=snap()==before
run('replacement dry run','--replace','--dry-run');checks['replacement_preview_no_writes']=snap()==before
out=run('authorized disposable replacement','--replace');backup=Path(out['backup']);checks['backup_customized_original']= (backup/'designer.md').read_bytes()==custom
checks['replacement_keeps_mode']=designer.stat().st_mode&0o777==0o640
checks['replacement_uses_updated_source']=b'Synthetic upstream update' in designer.read_bytes()
checks['unrelated_preserved']=unrelated.read_text()=='Owner unrelated profile: preserve.\n' and unrelated.stat().st_mode&0o777==0o600
before=snap();repeat=run('repeat same update');checks['repeat_idempotent']=repeat['changed']==[] and snap()==before
argv=['python3','scripts/install.py','--agent','quality-engineer','--target',str(target)]
p=subprocess.run(argv,cwd=source,text=True,capture_output=True,timeout=30);records.append({'step':'add different partial selection','argv':argv,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});assert p.returncode==0
checks['smaller_different_selection_keeps_prior_profile']=designer.read_bytes()==(target.parent/'agents/designer.md').read_bytes() and designer.exists() and unrelated.exists()
(root/'records.json').write_text(json.dumps({'source_revision':revision,'installer_sha256':hashlib.sha256((source/'scripts/install.py').read_bytes()).hexdigest(),'checks':checks,'commands':records,'final_snapshot':snap(),'canonical_coverage_increment':0,'limits':'Disposable local exercise, no actual host configuration or installed user profiles changed; no model behavior inferred.'},indent=2)+'\n')
assert all(checks.values()),checks
print(json.dumps(checks,indent=2))
