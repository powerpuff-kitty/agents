import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('behavior_eval',ROOT/'scripts/behavior_eval.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class BehaviorEval(unittest.TestCase):
 def make_skills(self,root):
  for name in ['systematic-debugging','change-review','geo-measurement','test-engineering']:
   folder=root/name;folder.mkdir(parents=True);(folder/'SKILL.md').write_text('Synthetic local test instructions\n')
 def test_boundary_fixture_fails_then_detects_fix_and_owner_edit(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);self.make_skills(root/'skills');out=root/'evaluation';module.prepare('implementation-dirty-worktree',out,root/'skills')
   result=module.grade(out);self.assertFalse(result['deterministic_checks']['boundary_tests'])
   p=out/'workspace/pagination.py';p.write_text(p.read_text().replace('        if start + size == len(items):\n            break\n',''))
   self.assertTrue(all(module.grade(out)['deterministic_checks'].values()))
   (out/'workspace/labels.txt').write_text('lost owner edit')
   self.assertFalse(module.grade(out)['deterministic_checks']['owner_label_preserved'])
 def test_readonly_fixture_detects_source_mutation(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);self.make_skills(root/'skills');out=root/'evaluation';module.prepare('focused-review-with-skills',out,root/'skills')
   self.assertTrue(all(module.grade(out)['deterministic_checks'].values()))
   (out/'workspace/pricing.py').write_text('unauthorized edit')
   self.assertFalse(module.grade(out)['deterministic_checks']['workspace_unchanged'])
 def test_no_overwrite_of_an_existing_evaluation(self):
  with tempfile.TemporaryDirectory() as raw:
   with self.assertRaises(ValueError):module.prepare('implementation-dirty-worktree',Path(raw),Path(raw))

 def test_source_archive_can_prepare_without_inventing_git_revision(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);source=root/'source';self.make_skills(root/'skills')
   (source/'agents/feature-developer').mkdir(parents=True)
   (source/'agents/feature-developer/instructions.md').write_text('Implement only the scoped change.\n')
   (source/'shared').mkdir();(source/'shared/operating-contract.md').write_text('Preserve evidence.\n')
   with patch.object(module,'ROOT',source):
    initial=module.prepare('implementation-unavailable-check',root/'evaluation',root/'skills')
   self.assertIsNone(initial['source_revision'])
   self.assertTrue(initial['preparer_sha256'])
   self.assertTrue(initial['instruction_sha256'])
   self.assertTrue((root/'evaluation/workspace/port.ts').is_file())

 def test_discovery_stages_candidates_without_assigned_instructions(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);self.make_skills(root/'skills');out=root/'evaluation'
   initial=module.prepare('implementation-dirty-worktree',out,root/'skills',discovery=True)
   self.assertEqual(initial['instruction_mode'],'discovery')
   self.assertFalse((out/'instructions/role.md').exists())
   self.assertFalse((out/'instructions/skill').exists())
   self.assertEqual({x.name for x in (out/'instructions/skills').iterdir()}, {'systematic-debugging','change-review','geo-measurement','test-engineering'})
   self.assertIn('instructions/catalog.md',(out/'task.md').read_text())
   self.assertTrue(module.grade(out)['deterministic_checks']['instructions_unchanged'])
   (out/'instructions/catalog.md').write_text('changed discovery inputs')
   self.assertFalse(module.grade(out)['deterministic_checks']['instructions_unchanged'])

 def test_new_cases_route_both_modes_and_keep_reasoning_ungraded(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);skills=root/'skills'
   names=['structured-reflection','project-memory','agent-security-review']
   for name in names:
    folder=skills/name;(folder/'tests/fixtures').mkdir(parents=True)
    (folder/'SKILL.md').write_text('---\nname: '+name+'\ndescription: Synthetic discovery fixture.\n---\n')
    (folder/'tests/fixtures/input.json').write_text('{"synthetic": true}')
   (skills/'agent-security-review/tests/fixtures/gateway.py').write_text('def authorize(*args): return False\n')
   for case in ['reflection-evidence-boundary','memory-retrieval-boundary','agent-tool-authorization-boundary']:
    for discovery in [False,True]:
     out=root/(case+str(discovery));module.prepare(case,out,skills,discovery)
     self.assertTrue((out/'workspace/input.json').is_file())
     if case=='agent-tool-authorization-boundary':self.assertTrue((out/'workspace/gateway.py').is_file())
     if discovery:
      self.assertIn('instructions/catalog.md',(out/'task.md').read_text())
      self.assertIn('instructions/operating-contract.md',(out/'task.md').read_text())
      self.assertIn('Read operating-contract.md first',(out/'instructions/catalog.md').read_text())
      self.assertNotIn('using the supplied role and optional skill',(out/'task.md').read_text())
     result=module.grade(out);self.assertEqual(result['review_verdict'],'unverified')
     self.assertTrue(all(result['deterministic_checks'].values()))
     (out/'workspace/input.json').write_text('changed')
     self.assertFalse(module.grade(out)['deterministic_checks']['workspace_unchanged'])

 def test_unavailable_checks_and_recovery_keep_behavior_unverified(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw);self.make_skills(root/'skills')
   for case in ['implementation-unavailable-check','browser-recovery-false-pass']:
    for discovery in [False,True]:
     out=root/(case+str(discovery));module.prepare(case,out,root/'skills',discovery)
     result=module.grade(out)
     self.assertEqual(result['review_verdict'],'unverified')
     self.assertTrue(all(result['deterministic_checks'].values()))
     self.assertEqual(result['commands'],[])
     if case=='implementation-unavailable-check':
      (out/'workspace/port.ts').write_text('still not type checked')
      self.assertTrue(all(module.grade(out)['deterministic_checks'].values()))
      self.assertEqual(module.grade(out)['review_verdict'],'unverified')
      (out/'workspace/owner-note.txt').write_text('lost owner work')
      self.assertFalse(module.grade(out)['deterministic_checks']['owner_note_preserved'])
     else:
      (out/'workspace/evidence.json').write_text('{}')
      self.assertFalse(module.grade(out)['deterministic_checks']['workspace_unchanged'])
