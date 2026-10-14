import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('check_docs',ROOT/'scripts/check_docs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Docs(unittest.TestCase):
 def test_code_is_not_a_link_but_missing_prose_link_is(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw)
   (root/'README.md').write_text("profiles-0; 0 profiles; 0 team workflows; 0 optional packs\n\n```python\nvalues['quote'](3,50,10)\n[example](not-a-real-link.md)\n```\n`[inline](not-a-link.md)`\n[real](target.md)\n")
   result=m.check(root);self.assertEqual(result['errors'],['README.md: missing target.md'])
   (root/'target.md').write_text('Real target.\n')
   self.assertTrue(m.check(root)['passed'])
