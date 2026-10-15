from pathlib import Path
import hashlib,json,shutil
OUT=Path('/Users/tcsntcsn/TCSN/agents/evals/observed/native-followup-2026-10-15')
OUT.mkdir(parents=True,exist_ok=True);provenance=[]
def copy(src,dest):
 if not src.is_file():return
 target=OUT/dest;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,target)
 provenance.append({'source':str(src),'published':str(dest),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
for name in ['failures','coverage','corrections']:
 root=Path('/private/tmp/native-'+name+'-followup-20261015')
 for f in root.iterdir():
  if f.is_file():copy(f,Path(name)/f.name)
 for f in (root/'collectors').iterdir():copy(f,Path(name)/'collectors'/f.name)
 plan=json.loads((root/'plan.json').read_text())
 for e in plan['runs']:
  run=root/e['id'];assert (run/'result.json').is_file(),e['id']
  for f in run.iterdir():
   if f.is_file():copy(f,Path(name)/e['id']/f.name)
  before=json.loads((run/'before.json').read_text())
  project=run/'workspace'
  for f in project.rglob('*'):
   rel=f.relative_to(project)
   if set(rel.parts)&{'.git','.agents','.opencode','__pycache__'}:continue
   if f.is_file():copy(f,Path(name)/e['id']/'final-workspace'/rel)
  for path,digest in before.items():
   rel=Path(path)
   if set(rel.parts)&{'.git','.agents','.opencode','__pycache__'}:continue
   f=project/rel
   data=f.read_bytes() if f.exists() else None
   kind='unchanged verified input'
   if data is None or hashlib.sha256(data).hexdigest()!=digest:
    if path=='port.ts':data=b'export function port(value: unknown): number {\n  return Number(value);\n}\n';kind='baseline reconstructed from frozen preparer; checked against original before hash'
    else:raise ValueError('Cannot recover initial input: '+path)
   assert hashlib.sha256(data).hexdigest()==digest
   target=OUT/name/e['id']/'initial-workspace'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
   provenance.append({'published':str(target.relative_to(OUT)),'sha256':digest,'regeneration':kind})
for dirname,target in [('native-followup-source-review-20261015','source-review'),('native-followup-trial-review-20261015','trial-review'),('coverage-review-20261015','coverage-selection'),('native-followup-pilot-review-20261015','pilot-review')]:
 root=Path('/private/tmp')/dirname
 if root.exists():
  for f in root.iterdir():
   if f.is_file():copy(f,Path(target)/(f.name+'.txt' if f.suffix=='.md' else f.name))
for label in ['installation-followup-20261015','installation-followup-recheck-20261015']:
 root=Path('/private/tmp')/label
 for name in ['exercise.py','records.json']:copy(root/name,Path('installation')/label/name)
root=Path('/private/tmp/native-project-pilot-followup-20261015')
assert (root/'run.json').is_file(),'Pilot pending'
for f in root.iterdir():
 if f.is_file():copy(f,Path('project-pilot')/f.name)
for rel in ['scripts/native_eval_report.py','tests/test_native_eval_report.py','owner-pilot-note.txt']:
 copy((Path('/private/tmp/native-followup-pilot-review-20261015/source') if rel!='owner-pilot-note.txt' else root/'project')/rel,Path('project-pilot/native-final')/rel)
for label in ['native-project-pilot-completion-20261015','native-project-pilot-completion-v2-20261015']:
 part=Path('/private/tmp')/label;assert (part/'run.json').is_file(),'Continuation pending'
 for f in part.iterdir():
  if f.is_file():copy(f,Path('project-pilot')/label/f.name)
 if 'v2' in label:
  for rel in ['scripts/native_eval_report.py','tests/test_native_eval_report.py','owner-pilot-note.txt']:copy(root/'project'/rel,Path('project-pilot/completed-final')/rel)
for p in ['/private/tmp/run-native-followups-20261015.py','/private/tmp/prepare-native-project-pilot-followup-20261015.py','/private/tmp/run-native-project-pilot-followup-20261015.py','/private/tmp/run-native-corrections-followup-20261015.py','/private/tmp/continue-native-project-pilot-20261015.py','/private/tmp/continue-native-project-pilot-v2-20261015.py',__file__]:
 f=Path(p);copy(f,Path('collectors')/f.name)
(OUT/'export-provenance.json').write_text(json.dumps({'format_version':1,'artifacts':provenance,'omissions':'Full native catalogs, duplicate instruction trees, complete project checkout, generated dist and .git metadata are omitted. Original input/config/source hashes and API traces are retained. Markdown reviewer reports use .md.txt to preserve their verbatim bytes and private-path context without claiming published local links.'},indent=2)+'\n')
print(json.dumps({'exported_files':len(provenance),'destination':str(OUT)}))
