"""Reproductions for independently reported export/install defects."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def run(script,*args,env=None):
 return subprocess.run([sys.executable,str(ROOT/'scripts'/script),*map(str,args)],capture_output=True,text=True,encoding='utf-8',env=env,timeout=30)

class AuditRegressions(unittest.TestCase):
 def test_export_and_install_retain_license(self):
  with tempfile.TemporaryDirectory() as raw:
   root=Path(raw)
   for adapter in ['portable','opencode']:
    dest=root/adapter;p=run('build.py','--adapter',adapter,'--agent','quality-engineer','--output',dest);self.assertEqual(p.returncode,0,p.stderr)
    self.assertEqual((dest/'LICENSE').read_bytes(),(ROOT/'LICENSE').read_bytes())
    manifest=json.loads((dest/'build-manifest.json').read_text())
    self.assertIn('LICENSE',manifest['source_sha256'])
    self.assertEqual(manifest['output_sha256']['LICENSE'],hashlib.sha256((dest/'LICENSE').read_bytes()).hexdigest())
   target=root/'profiles';p=run('install.py','--target',target,'--team','team-geo');self.assertEqual(p.returncode,0,p.stderr)
   for dest in [target,root/'commands']:
    self.assertEqual((dest/'.agents-LICENSE').read_bytes(),(ROOT/'LICENSE').read_bytes())
    self.assertIn('.agents-LICENSE',json.loads((dest/'.agents-managed.json').read_text())['files'])

 @unittest.skipIf(os.name=='nt','POSIX file modes')
 def test_private_state_mode_survives_selection_update(self):
  with tempfile.TemporaryDirectory() as raw:
   target=Path(raw)/'agents';p=run('install.py','--target',target,'--agent','quality-engineer');self.assertEqual(p.returncode,0,p.stderr)
   state=target/'.agents-managed.json';state.chmod(0o600)
   p=run('install.py','--target',target,'--agent','feature-developer');self.assertEqual(p.returncode,0,p.stderr)
   self.assertEqual(stat.S_IMODE(state.stat().st_mode),0o600)

 def test_generated_byte_hash_drift_is_not_hidden_by_newline_normalization(self):
  with tempfile.TemporaryDirectory() as raw:
   output=Path(raw)/'export';p=run('build.py','--adapter','portable','--output',output);self.assertEqual(p.returncode,0,p.stderr)
   file=output/'agents/quality-engineer.md';file.write_bytes(file.read_bytes().replace(b'\n',b'\r\n'))
   p=run('build.py','--adapter','portable','--output',output,'--check');self.assertNotEqual(p.returncode,0)
   self.assertIn('drift',p.stderr.lower())

 def test_documented_tooling_uses_utf8_independent_of_locale(self):
  env={**os.environ,'LC_ALL':'C','PYTHONUTF8':'0','PYTHONCOERCECLOCALE':'0'}
  with tempfile.TemporaryDirectory() as raw:
   for script,args in [('build.py',['--adapter','portable','--output',Path(raw)/'export']),('validate.py',[]),('check_docs.py',[])]:
    p=run(script,*args,env=env);self.assertEqual(p.returncode,0,(script,p.stderr))
