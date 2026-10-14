from pathlib import Path
import subprocess,os,sys,json,hashlib,re
BASE=Path('/private/tmp/standalone-pilot-2026-10-14/review/pilot-repro');ROOT=BASE/'project';ORIG=Path('/private/tmp/standalone-pilot-2026-10-14/pilot/project')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(BASE/'scratch'),GIT_OPTIONAL_LOCKS='0')
args=[sys.executable,'-B','-m','unittest','-v','test_behavior_eval.BehaviorEval.test_no_overwrite_of_an_existing_evaluation','test_behavior_eval.BehaviorEval.test_new_cases_route_both_modes_and_keep_reasoning_ungraded']
r=subprocess.run(args,cwd=ORIG/'tests',env=env,capture_output=True,text=True,timeout=90)
(BASE/'logs/behavior-checkout-safe.log').write_text(r.stdout+r.stderr)
assert r.returncode==0,r.stderr
safe={'argv':args,'cwd':str(ORIG/'tests'),'exit':r.returncode,'log':'logs/behavior-checkout-safe.log','outputs_in_review_TMPDIR':True,'reason':'Fixture preparation records Git HEAD, absent in archive copy. No source/commit mutation occurs in these selected tests.'}
probe=subprocess.run([sys.executable,'-B','installer_probe.py'],cwd=BASE,env=env,capture_output=True,text=True,timeout=90)
(BASE/'logs/installer-probe.stdout.txt').write_text(probe.stdout);(BASE/'logs/installer-probe.stderr.txt').write_text(probe.stderr)
assert probe.returncode==0,probe.stderr
def outputs(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
exports={}
for adapter in ['portable','opencode']:
 first=outputs(ROOT/'dist'/adapter)
 r=subprocess.run([sys.executable,'-B','scripts/build.py','--adapter',adapter],cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
 assert r.returncode==0
 again=outputs(ROOT/'dist'/adapter);retained=outputs(ORIG/'dist'/adapter)
 assert first==again==retained
 exports[adapter]={'file_count':len(first),'repeat_equal':True,'retained_export_equal':True,'manifest_sha256':first['build-manifest.json']}
# Actual archive-consumer CLI install in a separate review-owned core target.
target=BASE/'scratch/archive-core-install/agents';commands=target.parent/'commands'
assert not target.parent.exists()
installs=[]
for mode in ['dry-run','initial','repeat']:
 argv=[sys.executable,'-B','scripts/install.py','--target',str(target),'--commands-target',str(commands),'--pack','core']
 if mode=='dry-run':argv.append('--dry-run')
 r=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
 (BASE/'logs'/f'archive-core-{mode}.log').write_text(r.stdout+r.stderr)
 assert r.returncode==0
 data=json.loads(r.stdout)
 if mode=='dry-run':assert not target.parent.exists()
 if mode=='repeat':assert not data['changed']
 installs.append({'mode':mode,'argv':argv,'cwd':str(ROOT),'exit':r.returncode,'changed':len(data['changed']),'unchanged':len(data['unchanged'])})
summary={'source_validation_log':'logs/recheck-01.log','docs_log':'logs/recheck-02.log','archive_gate_exits':[0]*11,'archive_tests_passed':37,'archive_safe_behavior_attempt':{'exit':1,'passed':1,'errors':1,'log':'logs/recheck-12.log','cause':'behavior_eval.prepare requires Git HEAD absent from git archive'},'checkout_safe_behavior':safe,'installer_probe_exit':probe.returncode,'installer_probe_checks':len(json.loads((BASE/'logs/installer-probe.json').read_text())),'exports':exports,'archive_core_installs':installs,'excluded_tests':['test_boundary_fixture_fails_then_detects_fix_and_owner_edit','test_readonly_fixture_detects_source_mutation','test_discovery_stages_candidates_without_assigned_instructions'],'exclusion_reason':'Each calls prepare on fixture path reaching git commit; no commits authorized.'}
(BASE/'recheck-results.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
