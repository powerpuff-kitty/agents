from pathlib import Path
import subprocess,os,sys,json,hashlib
BASE=Path('/private/tmp/standalone-pilot-2026-10-14/review/pilot-repro');ROOT=BASE/'project'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(BASE/'scratch'),GIT_OPTIONAL_LOCKS='0')
commands=[['scripts/validate.py'],['scripts/check_docs.py'],['scripts/build.py','--adapter','portable'],['scripts/build.py','--adapter','opencode'],['scripts/build.py','--adapter','portable','--check'],['scripts/build.py','--adapter','opencode','--check']]
commands += [['-m','unittest','discover','-s','tests','-p',name,'-v'] for name in ['test_workflows.py','test_selection.py','test_audit_regressions.py','test_native_probe.py','test_docs.py']]
commands += [['-m','unittest','-v','test_behavior_eval.BehaviorEval.test_no_overwrite_of_an_existing_evaluation','test_behavior_eval.BehaviorEval.test_new_cases_route_both_modes_and_keep_reasoning_ungraded']]
records=[]
for i,args in enumerate(commands,1):
 cwd=ROOT/'tests' if i==12 else ROOT
 argv=[sys.executable,'-B',*args]
 r=subprocess.run(argv,cwd=cwd,env=env,capture_output=True,text=True,timeout=90)
 log=BASE/'logs'/f'recheck-{i:02d}.log';log.write_text(r.stdout+r.stderr)
 records.append({'argv':argv,'cwd':str(cwd),'exit':r.returncode,'log':str(log.relative_to(BASE))})
 print(json.dumps(records[-1]),flush=True)
 assert r.returncode==0,log
# This is the unchanged retained probe in a review-owned root with copied project source.
probe=subprocess.run([sys.executable,'-B','installer_probe.py'],cwd=BASE,env=env,capture_output=True,text=True,timeout=90)
(BASE/'logs/installer-probe.stdout.txt').write_text(probe.stdout);(BASE/'logs/installer-probe.stderr.txt').write_text(probe.stderr)
assert probe.returncode==0,probe.stderr
# Export repeat-byte and retained artifact comparison.
def outputs(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
exports={}
for adapter in ['portable','opencode']:
 first=outputs(ROOT/'dist'/adapter)
 r=subprocess.run([sys.executable,'-B','scripts/build.py','--adapter',adapter],cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
 assert r.returncode==0
 again=outputs(ROOT/'dist'/adapter)
 retained=outputs(Path('/private/tmp/standalone-pilot-2026-10-14/pilot/project/dist')/adapter)
 assert first==again==retained
 exports[adapter]={'file_count':len(first),'repeat_equal':True,'retained_export_equal':True,'manifest_sha256':first['build-manifest.json']}
(BASE/'recheck-results.json').write_text(json.dumps({'gates':records,'installer_probe_exit':probe.returncode,'exports':exports,'excluded_tests':['test_boundary_fixture_fails_then_detects_fix_and_owner_edit','test_readonly_fixture_detects_source_mutation','test_discovery_stages_candidates_without_assigned_instructions'],'exclusion_reason':'Each calls behavior_eval.prepare on fixture path reaching git commit; no commits authorized.'},indent=2)+'\n')
print(json.dumps({'gates':len(records),'installer_probe_exit':probe.returncode,'exports':exports}))
