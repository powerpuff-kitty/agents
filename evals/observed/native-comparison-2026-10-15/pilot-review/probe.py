import argparse,hashlib,importlib.util,json,pathlib,subprocess,sys,tempfile
p=argparse.ArgumentParser();p.add_argument('source',type=pathlib.Path);p.add_argument('output',type=pathlib.Path);a=p.parse_args()
spec=importlib.util.spec_from_file_location('independent_behavior_eval',a.source/'scripts/behavior_eval.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
log=[]
def git(work,*args,input=None):
 r=subprocess.run(['git','-C',str(work),*args],input=input,capture_output=True,check=True);log.append({'argv':['git','-C',str(work),*args],'exit':r.returncode,'stdout':r.stdout.decode(errors='replace'),'stderr':r.stderr.decode(errors='replace')});return r.stdout
with tempfile.TemporaryDirectory(prefix='independent-staging-') as raw:
 root=pathlib.Path(raw);(root/'skills/change-review').mkdir(parents=True);(root/'skills/change-review/SKILL.md').write_text('Synthetic offline review instructions\n')
 out=root/'case';initial=m.prepare('focused-review-with-skills',out,root/'skills');w=out/'workspace'
 status_before=git(w,'status','--porcelain');entries_before=git(w,'ls-files','--stage','-z');workspace_before=m.snapshot(w)
 baseline=m.grade(out)
 newblob=git(w,'hash-object','-w','--stdin',input=b'def quote(*args):\n    return 999\n').decode().strip()
 git(w,'update-index','--cacheinfo',f'100644,{newblob},pricing.py');git(w,'update-index','--assume-unchanged','pricing.py')
 status_after=git(w,'status','--porcelain');entries_after=git(w,'ls-files','--stage','-z');mutated=m.grade(out)
 legacy=json.loads((out/'initial.json').read_text());legacy={k:v for k,v in legacy.items() if k in ['format_version','case_id','role','skill','workspace_sha256','instruction_sha256','task_sha256','source_revision','instruction_mode','preparer_sha256','skills_revision','source_note','initial_git_status']};(out/'initial.json').write_text(json.dumps(legacy));legacy_result=m.grade(out)
 result={'source':str(a.source),'source_sha256':hashlib.sha256((a.source/'scripts/behavior_eval.py').read_bytes()).hexdigest(),'status_before':status_before.decode(),'status_after':status_after.decode(),'same_status':status_before==status_after,'semantic_staging_changed':entries_before!=entries_after,'workspace_unchanged':workspace_before==m.snapshot(w),'initial':initial,'baseline_grade':baseline,'changed_index_grade':mutated,'legacy_grade':legacy_result,'commands':log}
 a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['source_sha256','same_status','semantic_staging_changed','workspace_unchanged','baseline_grade','changed_index_grade','legacy_grade']},indent=2))
