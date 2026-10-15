import io,json,sys,subprocess,tarfile,shutil
from pathlib import Path
sys.path.insert(0,'/Users/tcsntcsn/TCSN/agents/scripts')
import native_eval as n
from opencode_probe import stage_export
root=Path('/private/tmp/native-project-pilot-followup-20261015');root.mkdir();project=root/'project';project.mkdir()
repo=Path('/Users/tcsntcsn/TCSN/agents');commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
archive=subprocess.check_output(['git','archive',commit],cwd=repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
 for member in tar.getmembers():
  assert '..' not in Path(member.name).parts and not Path(member.name).is_absolute()
  dest=project/member.name
  if member.isdir():dest.mkdir(parents=True,exist_ok=True)
  else:
   assert member.isfile();dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(member).read());dest.chmod(member.mode & 0o777)
subprocess.run(['git','init','-q'],cwd=project,check=True);subprocess.run(['git','add','.'],cwd=project,check=True);subprocess.run(['git','-c','user.name=Pilot Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Reviewed public source snapshot'],cwd=project,check=True)
(project/'owner-pilot-note.txt').write_text('Owner note: preserve this exact pending draft.\n')
stage_export(repo/'dist/opencode',project)
for f in Path('/Users/tcsntcsn/TCSN/skills').glob('*/SKILL.md'):shutil.copytree(f.parent,project/'.agents/skills'/f.parent.name)
permissions=n.permissions('focused-review-with-skills')
for resource in ['scripts/native_eval_report.py','tests/test_native_eval_report.py']:
 permissions.append({'action':'edit','resource':resource,'effect':'allow'})
for command in ['python3 scripts/validate.py','python3 scripts/check_docs.py','python3 scripts/build.py --adapter portable*','python3 scripts/build.py --adapter opencode*','python3 -B -m unittest*','python3 -m unittest*']:
 permissions.append({'action':'shell','resource':command,'effect':'allow'})
ids=[p.stem for p in (project/'.opencode/agents').glob('*.md')]
n.write(project/'opencode.json',{'autoupdate':False,'model':'deepseek/deepseek-v4-pro','default_agent':'build','permissions':permissions,'agents':{name:{'steps':12,'model':'deepseek/deepseek-v4-pro'} for name in ids+['build','general','explore']}})
prompt='''Improve native evaluation measurement reporting in this isolated public AI Agents source checkout.
Accepted behavior: token/cache/cost and elapsed-time summaries must treat boolean, negative, NaN and Infinity values as unknown/missing, preserving their planned rows and failure statuses. Only finite nonnegative numeric observations belong in metric samples. Do not infer task acceptance from these values. JSON reports must not emit NaN/Infinity due to these malformed observations. Add meaningful regression coverage with malformed and valid observations, failure/missing rows and exact result-bound reviews. Preserve existing reporting behavior for valid measurements.
Use team-feature: implement with 1 writer, then request an independent read-only quality review in a new native subagent session, address confirmed findings, run required project gates and report final readiness and actual commands. Only scripts/native_eval_report.py and tests/test_native_eval_report.py may be edited; generated dist outputs are allowed. Read AGENTS.md. Preserve owner-pilot-note.txt and Git staging exactly. All delegates use DeepSeek. No installs, network tools, model/provider switching, commits, publication or deployment. Use tool workdir parameters and separate permitted shell commands; a compound-command permission rejection does not imply every command or executable is unavailable. Distinguish check failure, denial and checks never run.
'''
(root/'prompt.txt').write_text(prompt)
n.write(root/'before.json',n.snapshot(project));n.write(root/'git-before.json',n.git_state(project));n.write(root/'source.json',{'repository':'powerpuff-kitty/ai-agents','source_commit':commit,'working_source_note':'Only native exports, native skill copies, configuration and owner note added to this exact source archive; source files unchanged.','skills_commit':n.revision(Path('/Users/tcsntcsn/TCSN/skills')),'allowed_source_changes':['scripts/native_eval_report.py','tests/test_native_eval_report.py'],'prompt_sha256':n.digest(prompt.encode())})
print(root)
