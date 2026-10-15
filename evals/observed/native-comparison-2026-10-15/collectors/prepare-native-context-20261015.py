import json,hashlib,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,'/Users/tcsntcsn/TCSN/agents/scripts');import native_eval as n
base=Path('/private/tmp/native-matched-2026-10-15-v3');original=base/'06-implementation-dirty-worktree-skill-2';oldplan=json.loads((base/'plan.json').read_text());oldentry=next(e for e in oldplan['runs'] if e['id']==original.name)
root=Path('/private/tmp/native-context-20261015');root.mkdir();candidate=Path('/private/tmp/systematic-debugging-candidate-20261015.md')
plan={k:v for k,v in oldplan.items() if k!='runs'};plan.update(runs=[],repetitions=2,context_treatment='Only systematic-debugging/SKILL.md body shortened; same description, resources, task and permissions. Fresh project paths differ.',baseline_plan_sha256=n.digest((base/'plan.json').read_bytes()),runner_sha256=n.digest(Path('/Users/tcsntcsn/TCSN/agents/scripts/native_eval.py').read_bytes()))
for repeat in [1,2]:
 run=root/f'context-candidate-{repeat}';run.mkdir();project=run/'workspace';shutil.copytree(original/'workspace',project)
 source=subprocess.check_output(['git','show','HEAD:pagination.py'],cwd=project);(project/'pagination.py').write_bytes(source)
 baseline=n.snapshot(project);assert baseline==json.loads((original/'before.json').read_text())
 old=(project/'.agents/skills/systematic-debugging/SKILL.md').read_bytes();(project/'.agents/skills/systematic-debugging/SKILL.md').write_bytes(candidate.read_bytes())
 after=n.snapshot(project);changed=[p for p in baseline if baseline[p]!=after[p]];assert changed==['.agents/skills/systematic-debugging/SKILL.md']
 shutil.copyfile(original/'prompt.txt',run/'prompt.txt');n.write(run/'before.json',after);n.write(run/'git-before.json',n.git_state(project));shutil.copyfile(original/'initial.json',run/'initial.json')
 entry={**oldentry,'id':run.name,'repeat':repeat,'fixture_sha256':n.digest(json.dumps(after,sort_keys=True).encode())};plan['runs'].append(entry)
 n.write(run/'treatment.json',{'baseline_fixture_sha256':oldentry['fixture_sha256'],'changed_files':changed,'baseline_skill_bytes':len(old),'candidate_skill_bytes':len(candidate.read_bytes()),'candidate_sha256':n.digest(candidate.read_bytes())})
n.write(root/'plan.json',plan);(root/'plan.sha256').write_text(n.digest((root/'plan.json').read_bytes())+'\n');shutil.copyfile('/Users/tcsntcsn/TCSN/agents/scripts/native_eval.py',root/'frozen-runner.py');print(root)
