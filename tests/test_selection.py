import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build import compile_profiles

class SelectionTests(unittest.TestCase):
    def test_individual_has_no_implicit_pack_or_coordinator(self):
        files=compile_profiles('opencode',agent_ids=['financial-analyst'])
        self.assertEqual({p for p in files if p.startswith('agents/')},{'agents/financial-analyst.md'})
        self.assertFalse(any(p.startswith('commands/') for p in files))
        self.assertEqual(json.loads(files['build-manifest.json'])['packs'],[])

    def test_team_brings_declared_roster_and_coordinator(self):
        root=Path(__file__).resolve().parents[1]
        metadata=json.loads((root/'teams/team-geo.json').read_text())
        expected={metadata['coordinator']}|{a['agent'] for s in metadata['stages'] for a in s['assignments']}
        files=compile_profiles('opencode',team_ids=['team-geo'])
        manifest=json.loads(files['build-manifest.json'])
        self.assertEqual(set(manifest['agents']),expected)
        self.assertEqual(manifest['teams'],['team-geo'])

    def test_combined_selection_deduplicates_and_rejects_unknown(self):
        files=compile_profiles('portable',packs=['core'],agent_ids=['financial-analyst','financial-analyst'])
        self.assertEqual(len(json.loads(files['build-manifest.json'])['agents']),17)
        for kwargs in [{'agent_ids':['missing']},{'team_ids':['missing']}]:
            with self.assertRaises(ValueError):compile_profiles('opencode',**kwargs)

    def test_unknown_selection_rejected_without_install_writes(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as raw:
            target=Path(raw)/'agents'
            p=subprocess.run([sys.executable,str(root/'scripts/install.py'),'--target',str(target),'--team','missing'],capture_output=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(target.exists())

    def test_individual_install_creates_no_commands_directory(self):
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as raw:
            target=Path(raw)/'agents'
            p=subprocess.run([sys.executable,str(root/'scripts/install.py'),'--target',str(target),'--agent','financial-analyst'],capture_output=True)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertTrue((target/'financial-analyst.md').exists())
            self.assertFalse((Path(raw)/'commands').exists())
