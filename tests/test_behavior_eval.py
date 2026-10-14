import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('behavior_eval',ROOT/'scripts/behavior_eval.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class BehaviorEval(unittest.TestCase):
 def make_skills(self,root):
  for name in ['systematic-debugging','change-review','geo-measurement']:
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
