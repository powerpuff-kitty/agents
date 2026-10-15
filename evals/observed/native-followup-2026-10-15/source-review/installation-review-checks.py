import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOTS = [Path('/private/tmp/installation-followup-20261015'), Path('/private/tmp/installation-followup-recheck-20261015')]
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def snapshot(root, metadata=False):
    value={}
    if root.exists():
        for p in [root,*sorted(root.rglob('*'))]:
            s=p.lstat()
            item={'type':'dir' if p.is_dir() else 'file', 'mode':oct(stat.S_IMODE(s.st_mode))}
            if p.is_file(): item['sha256']=sha(p)
            if metadata: item.update(mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
            value[str(p.relative_to(root))]=item
    return value
identities={}; artifacts={}
original_snapshots={str(root):snapshot(root) for root in ROOTS}
for root in ROOTS:
    records=json.loads((root/'records.json').read_text())
    identities[str(root)]={'declared_source_revision':records['source_revision'], 'exercise_sha256':sha(root/'exercise.py'), 'records_sha256':sha(root/'records.json'), 'installer_sha256':sha(root/'source/scripts/install.py'), 'source_files_sha256':{str(p.relative_to(root/'source')):sha(p) for p in sorted((root/'source').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}}
    assert identities[str(root)]['installer_sha256']==records['installer_sha256']
    installed=root/'installed'
    actual={str(p.relative_to(installed)):{'sha256':sha(p),'mode':oct(stat.S_IMODE(p.stat().st_mode))} for p in sorted(installed.rglob('*')) if p.is_file()}
    assert actual==records['final_snapshot']
    target=installed/'agents'
    assert (target/'unrelated.md').read_bytes()==b'Owner unrelated profile: preserve.\n'
    assert stat.S_IMODE((target/'unrelated.md').stat().st_mode)==0o600
    assert stat.S_IMODE((target/'designer.md').stat().st_mode)==0o640
    state=json.loads((target/'.agents-managed.json').read_text())
    assert {'designer.md','quality-engineer.md','.agents-LICENSE'}==set(state['files'])
    assert all(sha(target/name)==digest for name,digest in state['files'].items())
    backups=list((installed/'backups').glob('*/designer.md'))
    assert len(backups)==1
    backup=backups[0]
    assert stat.S_IMODE(backup.stat().st_mode)==0o640
    custom=b'\nOwner local customization: preserve unless replacement is explicit.\n'
    assert backup.read_bytes().endswith(custom)
    prior=backup.read_bytes()[:-len(custom)]
    backup_state=json.loads((backup.parent/'.agents-managed.json').read_text())
    assert hashlib.sha256(prior).hexdigest()==backup_state['files']['designer.md']
    assert b'Synthetic upstream update for disposable installation exercise.' in (target/'designer.md').read_bytes()
    assert b'Synthetic upstream update for disposable installation exercise.' not in prior
    artifacts[str(root)]={'final_snapshot_verified':True,'managed_hashes_match_actual_files':True,'backup_mode':'0o640','backup_contains_original_plus_exact_customization':True,'unrelated_bytes_mode_preserved':True, 'original_bytecode_files': [str(p.relative_to(root)) for p in (root/'source').rglob('*.pyc')]}
assert identities[str(ROOTS[0])]['source_files_sha256']==identities[str(ROOTS[1])]['source_files_sha256']

work=OUT/'installation-independent-reproduction'
source=work/'source'
shutil.copytree(ROOTS[1]/'source',source)
for cache in list(source.rglob('__pycache__')): shutil.rmtree(cache)
suffix='\nSynthetic upstream update for disposable installation exercise.\n'
upstream=source/'agents/designer/instructions.md'
assert upstream.read_text().endswith(suffix)
upstream.write_text(upstream.read_text()[:-len(suffix)])
target=work/'installed/agents';target.mkdir(parents=True)
unrelated=target/'unrelated.md';unrelated.write_bytes(b'Owner unrelated profile: preserve.\n');unrelated.chmod(0o600)
commands=[]; checks={}
def run(name,role='designer',flags=(),expected=0):
    argv=[sys.executable,'scripts/install.py','--agent',role,'--target',str(target),*flags]
    env={k:v for k,v in os.environ.items() if k not in {'PYTHONDONTWRITEBYTECODE','PYTHONPYCACHEPREFIX'}}
    p=subprocess.run(argv,cwd=source,env=env,capture_output=True,text=True,timeout=30)
    commands.append({'name':name,'argv':argv,'cwd':str(source),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    assert p.returncode==expected,(name,p.stderr)
    return json.loads(p.stdout) if p.returncode==0 else None
before_target=snapshot(target.parent,True); before_source=snapshot(source)
run('initial dry run',flags=('--dry-run',))
checks['initial_dry_no_target_nodes_content_mode_mtime_changes']=snapshot(target.parent,True)==before_target
new_source=set(snapshot(source))-set(before_source)
checks['initial_dry_created_source_nodes']=sorted(new_source)
assert checks['initial_dry_no_target_nodes_content_mode_mtime_changes']
assert any(name.endswith('.pyc') for name in new_source)
run('initial install'); designer=target/'designer.md';original=designer.read_bytes();designer.chmod(0o640)
upstream.write_text(upstream.read_text()+suffix)
custom=original+b'\nOwner local customization: preserve unless replacement is explicit.\n';designer.write_bytes(custom)
before=snapshot(work,True)
run('ordinary edited-profile update',expected=1)
checks['conflict_no_tree_content_mode_mtime_changes']=snapshot(work,True)==before
assert checks['conflict_no_tree_content_mode_mtime_changes']
before=snapshot(work,True)
run('replacement dry run',flags=('--replace','--dry-run'))
checks['replacement_dry_no_tree_content_mode_mtime_changes']=snapshot(work,True)==before
assert checks['replacement_dry_no_tree_content_mode_mtime_changes']
result=run('explicit replacement',flags=('--replace',))
backup=Path(result['backup'])/'designer.md'
checks['replacement_backup_exact_bytes_mode']=backup.read_bytes()==custom and stat.S_IMODE(backup.stat().st_mode)==0o640
checks['replacement_target_mode_and_update']=stat.S_IMODE(designer.stat().st_mode)==0o640 and suffix.strip().encode() in designer.read_bytes()
assert checks['replacement_backup_exact_bytes_mode'] and checks['replacement_target_mode_and_update']
before=snapshot(work,True)
result=run('repeat same update')
checks['repeat_no_tree_content_mode_mtime_changes']=result['changed']==[] and snapshot(work,True)==before
assert checks['repeat_no_tree_content_mode_mtime_changes']
prior_designer=snapshot(target)['designer.md'];prior_unrelated=snapshot(target)['unrelated.md'];before_designer=designer.stat()
run('different partial selection',role='quality-engineer')
checks['partial_preserves_prior_designer_bytes_mode_mtime']=snapshot(target)['designer.md']==prior_designer and designer.stat().st_mtime_ns==before_designer.st_mtime_ns
checks['partial_preserves_unrelated_bytes_mode']=snapshot(target)['unrelated.md']==prior_unrelated
checks['partial_installs_new_selected_role']=(target/'quality-engineer.md').is_file()
assert all(checks[key] for key in ['partial_preserves_prior_designer_bytes_mode_mtime','partial_preserves_unrelated_bytes_mode','partial_installs_new_selected_role'])
for root in ROOTS: assert snapshot(root)==original_snapshots[str(root)]
result={'identities':identities,'original_artifact_checks':artifacts,'independent_checks':checks,'commands':commands,'originals_unchanged':True,'limits':'No native host or inference; filesystem snapshots omit access time and cannot prove no transient writes or writes outside the bounded trees.'}
(OUT/'installation-review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'original_artifact_checks':artifacts,'independent_checks':checks,'originals_unchanged':True},indent=2))
