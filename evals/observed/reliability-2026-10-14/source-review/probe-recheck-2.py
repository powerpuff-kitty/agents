from pathlib import Path
import hashlib,json,shutil,types
OUT=Path(__file__).resolve().parent/'probe-recheck-2'
OUT.mkdir()
SOURCE=Path('/Users/tcsntcsn/TCSN/agents/scripts/behavior_eval.py')
SKILLS=Path('/Users/tcsntcsn/TCSN/skills')
source=SOURCE.read_text()
(OUT/'captured-recheck-behavior_eval.py').write_text(source)
root=OUT/'synthetic-root';root.mkdir()
(root/'shared').mkdir();shutil.copyfile('/Users/tcsntcsn/TCSN/agents/shared/operating-contract.md',root/'shared/operating-contract.md')
(root/'LICENSE').write_text('Synthetic probe license marker\n')
for role in ['feature-developer','team-lead','security-auditor']:
 folder=root/'agents'/role;folder.mkdir(parents=True)
 (folder/'agent.json').write_text(json.dumps({'id':role,'description':'Synthetic role for staging-only probe'}))
 (folder/'instructions.md').write_text('Synthetic role instructions; no task authority.\n')
skills=OUT/'synthetic-skills'
for name in ['structured-reflection','project-memory','agent-security-review']:
 shutil.copytree(SKILLS/name,skills/name)
results=[]
for label,text in [('captured-recheck-2',source)]:
 module=types.ModuleType('behavior_'+label.replace('-','_'));module.__file__=str(SOURCE)
 exec(compile(text,str(SOURCE),'exec'),module.__dict__)
 module.ROOT=root
 module.git=lambda *args:'synthetic-revision\n'
 for case in ['reflection-evidence-boundary','memory-retrieval-boundary','agent-tool-authorization-boundary']:
  for discovery in [False,True]:
   dest=OUT/'probe-outputs'/label/(case+('-discovery' if discovery else '-explicit'))
   initial=module.prepare(case,dest,skills,discovery=discovery)
   task=(dest/'task.md').read_text()
   catalog=(dest/'instructions/catalog.md').read_text() if discovery else ''
   grade=module.grade(dest)
   row={'source':label,'source_sha256':hashlib.sha256(text.encode()).hexdigest(),'case':case,'mode':initial['instruction_mode'],'task_points_to_catalog':'instructions/catalog.md' in task,'shared_contract_staged':(dest/'instructions/operating-contract.md').exists(),'task_mentions_operating_contract':'instructions/operating-contract.md' in task,'catalog_instructs_shared_contract':'Read operating-contract.md first' in catalog,'artifact_checks_before_mutation':grade['deterministic_checks']}
   (dest/'workspace/input.json').write_text('unauthorized synthetic mutation\n')
   row['detects_workspace_mutation']=not module.grade(dest)['deterministic_checks']['workspace_unchanged']
   results.append(row)
(OUT/'probe-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
