"""Offline evidence gates detect drift without rewriting or executing trials."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import check_evidence
import native_eval_report


class EvidenceTests(unittest.TestCase):
    def write(self, path, value):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value) + '\n')

    def seal(self, bundle):
        files = {p.relative_to(bundle).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in bundle.rglob('*') if p.is_file() and p.name != 'manifest.json'}
        self.write(bundle / 'manifest.json', {'files_sha256': files})

    def prepare(self, root):
        bundle = root / 'bundle';trials = bundle / 'trials'
        entries = [{'id': name, 'case': 'fixture', 'mode': 'ordinary', 'repeat': i,
                    'fixture_sha256': 'same'} for i, name in enumerate(['failed', 'missing'], 1)]
        self.write(trials / 'plan.json', {'runs': entries})
        (trials / 'plan.sha256').write_text(native_eval_report.sha(trials / 'plan.json'))
        self.write(trials / 'failed/result.json', {'entry': entries[0], 'status': 'timed_out', 'usage': None, 'seconds': 10})
        self.write(bundle / 'review.json', {'runs': [{'id': 'failed', 'acceptance': 'blocked',
                                                     'result_sha256': native_eval_report.sha(trials / 'failed/result.json')}]})
        report = native_eval_report.summarize(trials, bundle / 'review.json')
        self.write(trials / 'measurements.json', report)
        (trials / 'measurements.md').write_text(native_eval_report.markdown(report))
        self.seal(bundle)
        self.write(root / 'evals/evidence-checks.json', {'bundles': [{'path': 'bundle', 'reports': [
            {'path': 'trials', 'review': 'review.json'}]}]})
        return bundle

    def test_valid_gate_preserves_failed_missing_rows_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);self.prepare(root)
            before = {str(p): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = check_evidence.verify(root)
            self.assertEqual(result['model_calls'], 0)
            self.assertEqual(result['bundles'][0]['reports'][0], {'path': 'trials', 'planned': 2, 'classified': 1})
            self.assertEqual(before, {str(p): p.read_bytes() for p in root.rglob('*') if p.is_file()})

    def test_changed_added_and_deleted_artifacts_fail(self):
        for mutation in ['change', 'add', 'delete']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as raw:
                root = Path(raw);bundle = self.prepare(root)
                path = bundle / 'review.json'
                if mutation == 'change':path.write_text(path.read_text() + ' ')
                elif mutation == 'add':(bundle / 'unexpected.txt').write_text('extra')
                else:path.unlink()
                with self.assertRaisesRegex(ValueError, 'manifest differs'):check_evidence.verify(root)

    def test_resealed_changed_result_still_rejects_stale_review(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);bundle = self.prepare(root)
            path = bundle / 'trials/failed/result.json';path.write_text(path.read_text() + ' ')
            self.seal(bundle)
            with self.assertRaisesRegex(ValueError, 'another result'):check_evidence.verify(root)

    def test_resealed_report_cannot_drop_failed_or_missing_runs(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);bundle = self.prepare(root)
            path = bundle / 'trials/measurements.json';value = json.loads(path.read_text());value['runs'] = []
            self.write(path, value);self.seal(bundle)
            with self.assertRaisesRegex(ValueError, 'regenerated evidence'):check_evidence.verify(root)

    def test_paths_links_duplicates_and_nonfinite_json_fail(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);bundle = self.prepare(root)
            for path in ['../escape', '/absolute', 'trials/../review.json', 'trials\\bad', '.']:
                with self.subTest(path=path), self.assertRaises(ValueError):check_evidence.child(bundle, path)
            (bundle / 'link').symlink_to(bundle / 'review.json')
            with self.assertRaisesRegex(ValueError, 'Linked evidence'):check_evidence.verify(root)
            (bundle / 'link').unlink()
            for text in ['{"x": 1, "x": 2}', '{"x": NaN}']:
                (bundle / 'invalid.json').write_text(text);self.seal(bundle)
                with self.assertRaises(ValueError):check_evidence.verify(root)


if __name__ == '__main__':
    unittest.main()
