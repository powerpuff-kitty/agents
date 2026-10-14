from pathlib import Path
import ast,hashlib,json,os,subprocess,sys,tarfile
BASE=Path('/private/tmp/standalone-pilot-2026-10-14/review');OUT=BASE/'correction-recheck-artifacts';PROBES=OUT/'runner-probes';PROBES.mkdir()
ORIGINAL=Path('/private/tmp/standalone-pilot-2026-10-14/pilot-tooling-correction');source=(ORIGINAL/'run_gates.py').read_text()
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL='/dev/null')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Identity of every supplied tooling file except Git internals; no originals executed in place.
tooling={str(p.relative_to(ORIGINAL)):sha(p) for p in ORIGINAL.rglob('*') if p.is_file() and '.git' not in p.relative_to(ORIGINAL).parts}
(OUT/'tooling-before.json').write_text(json.dumps(tooling,indent=2)+'\n')
def command_node(n):return isinstance(n,(ast.Assign,ast.AugAssign)) and ((isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='commands' for t in n.targets)) or (isinstance(n,ast.AugAssign) and isinstance(n.target,ast.Name) and n.target.id=='commands'))
def without_configuration(text):
 tree=ast.parse(text);tree.body=[n for n in tree.body if not command_node(n)];return ast.dump(tree,include_attributes=False)
for label in ['positive','negative']:
 assert without_configuration(source)==without_configuration((ORIGINAL/label/'run_gates.py').read_text())
results=[]
scenarios=[('clean-success',['/usr/bin/true'],None),('failed-command',['/usr/bin/false'],None),('tracked-source-changed',[sys.executable,'-B','-c',"from pathlib import Path;Path('fixture.txt').write_text('changed\\n')"],None),('dirty-tracked-before',['/usr/bin/true'],'tracked'),('dirty-untracked-after',[sys.executable,'-B','-c',"from pathlib import Path;Path('owner-draft.txt').write_text('new\\n')"],None),('dirty-untracked-before-removed',[sys.executable,'-B','-c',"from pathlib import Path;Path('owner-draft.txt').unlink()"],'untracked')]
for label,command,dirty in scenarios:
 root=PROBES/label;project=root/'project';project.mkdir(parents=True)
 (project/'fixture.txt').write_text('original\n')
 def git(*args):return subprocess.check_output(['git',*args],cwd=project,env=env,text=True)
 git('init','-q');git('add','fixture.txt');git('-c','user.name=Review Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Synthetic runner fixture')
 if dirty=='tracked':(project/'fixture.txt').write_text('owner edit\n')
 elif dirty=='untracked':(project/'owner-draft.txt').write_text('owner draft\n')
 tree=ast.parse(source);first=next(i for i,n in enumerate(tree.body) if command_node(n));tree.body=[n for n in tree.body if not command_node(n)]
 tree.body.insert(first,ast.parse('commands = '+repr([command])).body[0]);ast.fix_missing_locations(tree)
 script=root/'run_gates.py';script.write_text(ast.unparse(tree)+'\n')
 assert without_configuration(source)==without_configuration(script.read_text())
 result=subprocess.run([sys.executable,'-B',str(script)],cwd=root,env=env,capture_output=True,text=True,timeout=30)
 (root/'stdout.txt').write_text(result.stdout);(root/'stderr.txt').write_text(result.stderr)
 before=json.loads((root/'logs/source-before.json').read_text());after=json.loads((root/'logs/source-after.json').read_text());gates=json.loads((root/'logs/gate-results.json').read_text())
 results.append({'scenario':label,'runner_exit':result.returncode,'subcommand_exit':gates[0]['exit'],'status_before':before['status_before'],'status_after':after['status_after'],'tracked_source_unchanged':after['tracked_source_unchanged'],'expected_nonzero':label!='clean-success','script_sha256':sha(script)})
 print(json.dumps(results[-1]),flush=True)
(OUT/'runner-probes.json').write_text(json.dumps({'corrected_runner_sha256':sha(ORIGINAL/'run_gates.py'),'original_controlled_probe_aggregation_ast_matches':True,'probes':results},indent=2)+'\n')
# Correct the initial reporting member-class description, preserving old report/tar bytes.
archive=BASE/'pilot-repro/candidate.tar'
with tarfile.open(archive) as tar:
 members=tar.getmembers();classes={'regular_files':sum(m.isfile() for m in members),'directories':sum(m.isdir() for m in members),'symlinks':sum(m.issym() for m in members),'hardlinks':sum(m.islnk() for m in members),'other':sum(not (m.isfile() or m.isdir() or m.issym() or m.islnk()) for m in members)}
summary={'archive':str(archive),'sha256':sha(archive),'total_members':len(members),'member_classes':classes,'tracked_files_in_initial_source_manifest':len(json.loads((Path('/private/tmp/standalone-pilot-2026-10-14/pilot/logs/source-before.json')).read_text())['tracked_sha256']),'correction':'The initial pilot review called all 1268 members regular. The class-specific counts here supersede that wording; original report retained unchanged.'}
(OUT/'archive-member-classes.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary))
