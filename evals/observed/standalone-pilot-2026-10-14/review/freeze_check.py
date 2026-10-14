from pathlib import Path
import json, hashlib, shutil
root=Path('/private/tmp/standalone-pilot-2026-10-14')
review=root/'review'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
casefiles=sorted(p for p in (root/'cases').rglob('*') if p.is_file())
(review/'frozen-before.json').write_text(json.dumps({str(p.relative_to(root)):sha(p) for p in casefiles},indent=2)+'\n')
results={}
for case in sorted((root/'cases').iterdir()):
 if not case.is_dir(): continue
 original=json.loads((case/'input-sha256.json').read_text())
 changed=[name for name,h in original.items() if sha(case/name)!=h]
 expected=['workspace/port.ts'] if case.name=='implementation-unavailable-check' else []
 assert changed==expected,(case,changed)
 instructions=json.loads((case/'instruction-sha256.json').read_text())
 mismatches={name:sha(Path(name)) for name,h in instructions.items() if sha(Path(name))!=h}
 assert not mismatches,(case,mismatches)
 result={'input_changes_vs_retained_manifest':changed,'instruction_hashes_verified':len(instructions),'instruction_hash_mismatches':mismatches}
 if case.name.startswith('reflection-'):
  data=json.loads((case/'workspace/input.json').read_text())
  result.update(evidence_ids=[x['id'] for x in data['evidence']],finding_id=data['finding_id'])
  if case.name=='reflection-insufficient-evidence': assert data['evidence']==[] and 'attempt_note' not in data
  elif case.name=='reflection-no-reflection-needed': assert data['finding_id'] is None and len(data['evidence'])==1
  elif case.name=='reflection-failed-test': assert [x['id'] for x in data['evidence']]==['evidence:contract','evidence:test']
  elif case.name=='reflection-architecture-finding': assert [x['id'] for x in data['evidence']]==['evidence:rule','evidence:edge']
 results[case.name]=result
impl=root/'cases/implementation-unavailable-check'
assert sha(impl/'port.original.ts')==json.loads((impl/'input-sha256.json').read_text())['workspace/port.ts']
assert (impl/'workspace/owner-note.txt').read_bytes()==b'Owner draft: keep this exact note.\n'
assert sha(impl/'workspace/port.ts')==json.loads((impl/'logic-check.json').read_text())['final_source_sha256']
copy=review/'implementation-copy'
copy.mkdir(exist_ok=True)
(copy/'workspace').mkdir(exist_ok=True)
for name in ['check-port.cjs','port.original.ts','workspace/port.ts']:
 shutil.copyfile(impl/name,copy/name)
browser=json.loads((root/'cases/browser-recovery-false-pass/workspace/evidence.json').read_text())
results['browser_record_check']={'mismatch_dimensions':[k for k in ['route','viewport','theme'] if browser['requested_journey'][k]!=browser['screenshot'][k]],'attempts':browser['attempts'],'baseline_approved':browser['screenshot']['baseline_approved'],'after_restart':browser['storage']['after_restart'],'browser_executed_by_reviewer':False}
(review/'case-input-checks.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'case_count':len([x for x in results if x!='browser_record_check']),'frozen_files':len(casefiles),'original_source_hash_verified':True,'owner_note_exact':True,'all_instruction_manifests_match':True}))
