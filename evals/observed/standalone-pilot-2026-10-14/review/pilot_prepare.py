from pathlib import Path
import hashlib,json,os,subprocess,tarfile,io,shutil
ROOT=Path('/private/tmp/standalone-pilot-2026-10-14/pilot')
OUT=Path('/private/tmp/standalone-pilot-2026-10-14/review/pilot-repro')
OUT.mkdir(exist_ok=False);(OUT/'logs').mkdir();(OUT/'scratch').mkdir()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.relative_to(ROOT).parts}
(OUT/'original-before.json').write_text(json.dumps(original,indent=2)+'\n')
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT/'project',env=env)
revision=git('rev-parse','HEAD').decode().strip();status=git('status','--porcelain').decode()
source=json.loads((ROOT/'logs/source-before.json').read_text());final=json.loads((ROOT/'logs/source-final.json').read_text())
assert revision==source['revision']=='73b241f5eb9240034d78f531abd8ace804ed0890'
assert not status
assert all(sha(ROOT/'project'/name)==digest for name,digest in source['tracked_sha256'].items())
archive=git('archive','--format=tar','--prefix=ai-agents-candidate/','HEAD');repeat=git('archive','--format=tar','--prefix=ai-agents-candidate/','HEAD')
assert archive==repeat
archive_sha=hashlib.sha256(archive).hexdigest();retained=ROOT/'scratch/ai-agents-0.1.0-beta.1-candidate.tar'
assert archive_sha==sha(retained)==json.loads((ROOT/'logs/archive-probe.json').read_text())['archive_sha256']
(OUT/'candidate.tar').write_bytes(archive)
with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
 members=tar.getmembers()
 assert all(m.isfile() or m.isdir() for m in members)
 assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and '.git' not in Path(m.name).parts and 'dist' not in Path(m.name).parts for m in members)
 assert any(m.name=='ai-agents-candidate/LICENSE' for m in members)
 tar.extractall(OUT/'extract',filter='data')
shutil.move(OUT/'extract/ai-agents-candidate',OUT/'project')
shutil.copyfile(ROOT/'installer_probe.py',OUT/'installer_probe.py')
instructions=json.loads((ROOT/'logs/instruction-sha256.json').read_text())
# Read the actual shape and retain it; next assertion uses only catalog-listed/local authorized paths.
if isinstance(instructions,dict):
 for name,digest in instructions.items():
  if isinstance(digest,str) and len(digest)==64: assert sha(Path(name))==digest,(name,digest)
summary={'revision':revision,'git_status':status,'tracked_files_verified':len(source['tracked_sha256']),'retained_final_identity':final,'initial_and_final_result_equal':(ROOT/'result.initial.md').read_bytes()==(ROOT/'result.md').read_bytes(),'archive_sha256':archive_sha,'archive_repeat_equal':True,'archive_members':len(members),'archive_current_equals_retained':True,'tags':git('tag','--list').decode(),'pin_diff_names':git('diff','--name-only','18584173054bb7d16c2448e5892da923cd68370e','HEAD').decode(),'pin_diff':git('diff','18584173054bb7d16c2448e5892da923cd68370e','HEAD','--','INSTALL.md').decode()}
(OUT/'identity.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ['retained_final_identity','pin_diff']}))
