"""New case inputs exercise their declared local boundary without inference."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import native_eval
import native_fixtures


class NativeFixtureTests(unittest.TestCase):
    def test_default_roster_stays_18_and_explicit_case_mode_selects_only_requested_run(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);skills = root / 'skills';export = root / 'export'
            for name in ['systematic-debugging', 'change-review', 'security-review']:
                path = skills / name / 'SKILL.md';path.parent.mkdir(parents=True)
                path.write_text('---\nname: ' + name + '\ndescription: Fixture.\n---\nFixture body.\n')
            profile = export / 'agents/feature-developer.md';profile.parent.mkdir(parents=True)
            profile.write_text('---\ndescription: Fixture.\n---\nFixture profile.\n')
            default = native_eval.prepare(root / 'default', skills, export)
            self.assertEqual(len(default['runs']), 18)
            self.assertEqual({x['case'] for x in default['runs']}, set(native_eval.DEFAULT_CASES))
            selected = native_eval.prepare(root / 'selected', skills, export, repeats=1,
                cases=['security-isolated-repro'], modes=['named-agent'])
            self.assertEqual(len(selected['runs']), 1)
            self.assertEqual(selected['runs'][0]['agent'], 'security-auditor')
            self.assertIsNone(selected['runs'][0]['skill'])
            with self.assertRaises(ValueError):
                native_eval.prepare(root / 'invalid', skills, export, modes=['skill', 'skill'])

    def test_cases_are_canonical_and_readonly_scope_rejects_added_tests(self):
        cases = json.loads((native_eval.ROOT / 'evals/behavior-cases.json').read_text())['cases']
        declared = {item['id']: item for item in cases}
        for case, (role, _, _) in native_fixtures.CASES.items():
            self.assertIn(case, declared)
            self.assertIn(declared[case]['expected_agent'], ['*', role])
            self.assertFalse(native_eval.source_scope_preserved({'input': 'same'}, {'input': 'same', 'test_extra.py': 'new'}, case))
            self.assertFalse(any(x['action'] == 'edit' and x['effect'] == 'allow' for x in native_eval.permissions(case)))

    def test_local_security_controls_and_coordinator_failure(self):
        for case, expected in [('security-isolated-repro', 0), ('coordination-missing-delegation', 1)]:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as raw:
                root = Path(raw);native_fixtures.populate(case, root)
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'], cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertIn('Ran 3 tests' if expected == 0 else 'Ran 2 tests', result.stderr)

    def test_sanitizer_preserves_useful_locations_without_printing_canary(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);native_fixtures.populate('security-secret-evidence', root)
            result = subprocess.run([sys.executable, '-B', 'sanitize_log.py'], cwd=root, capture_output=True, text=True, check=True)
            self.assertNotIn(native_fixtures.SYNTHETIC_CANARY, result.stdout + result.stderr)
            self.assertIn('1: INFO request authorization=[REDACTED]', result.stdout)
            self.assertIn('2: INFO healthcheck ok', result.stdout)

    def test_capability_denial_is_actual_rule_and_other_cases_keep_delegation(self):
        for case in ['coordination-missing-delegation', 'security-isolated-repro']:
            effects = [x['effect'] for x in native_eval.permissions(case) if x['action'] == 'subagent']
            self.assertEqual(effects[-1], 'deny' if case == 'coordination-missing-delegation' else 'allow')


if __name__ == '__main__':
    unittest.main()
