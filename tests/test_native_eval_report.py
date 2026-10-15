"""Reports never erase failed/missing trials or apply a review to changed evidence."""
import json
from pathlib import Path
import tempfile
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import native_eval_report as report


class NativeReportTests(unittest.TestCase):
    def prepared(self, root):
        entries = [{'id': name, 'case': 'case', 'mode': 'ordinary', 'repeat': i,
                    'fixture_sha256': 'same'} for i, name in enumerate(['failed', 'missing'], 1)]
        (root / 'plan.json').write_text(json.dumps({'runs': entries}))
        (root / 'plan.sha256').write_text(report.sha(root / 'plan.json'))
        run = root / 'failed';run.mkdir()
        (run / 'result.json').write_text(json.dumps({'entry': entries[0], 'status': 'timed_out', 'usage': None, 'seconds': 10}))
        return run

    def test_missing_failure_and_unknown_usage_survive(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);self.prepared(root)
            value = report.summarize(root)
            self.assertEqual([x['status'] for x in value['runs']], ['timed_out', 'not_run'])
            self.assertEqual(value['groups'][0]['metrics']['input']['missing'], 2)
            self.assertIsNone(value['groups'][0]['metrics']['input']['mean'])
            self.assertEqual(value['groups'][0]['independent_acceptance'], {'unverified': 2})

    def test_review_is_bound_to_exact_result(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);run = self.prepared(root)
            review = root / 'review.json'
            review.write_text(json.dumps({'runs': [{'id': 'failed', 'acceptance': 'blocked', 'result_sha256': report.sha(run / 'result.json')}]}))
            self.assertEqual(report.summarize(root, review)['runs'][0]['acceptance'], 'blocked')
            (run / 'result.json').write_text((run / 'result.json').read_text() + ' ')
            with self.assertRaises(ValueError):report.summarize(root, review)

    def test_absent_result_can_only_be_explicitly_unverified(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);self.prepared(root)
            review = root / 'review.json'
            review.write_text(json.dumps({'runs': [{'id': 'missing', 'acceptance': 'unverified', 'result_sha256': None}]}))
            self.assertEqual(report.summarize(root, review)['runs'][1]['acceptance'], 'unverified')
            review.write_text(json.dumps({'runs': [{'id': 'missing', 'acceptance': 'pass', 'result_sha256': None}]}))
            with self.assertRaises(ValueError):report.summarize(root, review)

    def test_completed_tool_can_have_failed_result(self):
        value = report.instruction_events({'session': [{'type': 'assistant', 'agent': 'build', 'content': [
            {'type': 'tool', 'name': 'shell', 'state': {'status': 'completed', 'metadata': {'exit': 127}}},
            {'type': 'tool', 'name': 'execute', 'state': {'status': 'completed', 'metadata': {'error': True}}}]}]})
        self.assertEqual(value['tool_statuses'], {'completed': 2})
        self.assertEqual(value['tool_result_failures'], 2)

    def test_actual_skill_events_are_distinct_from_requested_attachments(self):
        messages = {'session': [{'type': 'user', 'skills': [{'id': 'requested'}, {'id': 'attached', 'text': 'body'}]},
                               {'type': 'skill', 'skill': 'loaded', 'text': 'abc'},
                               {'type': 'assistant', 'agent': 'build', 'content': [{'type': 'tool', 'name': 'skill', 'state': {'status': 'error', 'input': {'id': 'failed'}}}]}]}
        result = report.instruction_events(messages)
        self.assertEqual(result['skill_events'], {'attached': 1, 'loaded': 1})
        self.assertEqual(result['skill_message_utf8_bytes'], 7)
        self.assertEqual(result['tool_statuses'], {'error': 1})

    def _make_plan(self, root, entries):
        (root / 'plan.json').write_text(json.dumps({'runs': entries}))
        (root / 'plan.sha256').write_text(report.sha(root / 'plan.json'))

    def _write_run(self, root, entry, extra):
        run = root / entry['id'];run.mkdir()
        result = {'entry': entry};result.update(extra)
        # Default allow_nan writes literal NaN/Infinity, mirroring malformed data on disk.
        (run / 'result.json').write_text(json.dumps(result))

    def test_malformed_observations_treated_as_missing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            inputs = [100, 0, True, False, -5, -2.5, float('nan'), float('inf'), float('-inf'), '100']
            entries = [{'id': f'r{i}', 'case': 'case', 'mode': 'ordinary', 'repeat': i, 'fixture_sha256': 'same'}
                       for i in range(len(inputs))]
            self._make_plan(root, entries)
            for entry, value in zip(entries, inputs):
                self._write_run(root, entry, {'status': 'completed', 'usage': {'input': value}, 'seconds': 1})
            result = report.summarize(root)
            metrics = result['groups'][0]['metrics']
            # Only 100 and 0 are valid; booleans, negatives, NaN, infinities and strings are missing.
            self.assertEqual(metrics['input']['observed'], 2)
            self.assertEqual(metrics['input']['missing'], 8)
            self.assertEqual(metrics['input']['mean'], 50.0)
            self.assertEqual(metrics['input']['min'], 0)
            self.assertEqual(metrics['input']['max'], 100)

    def test_malformed_seconds_treated_as_missing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            entries = [{'id': f'r{i}', 'case': 'case', 'mode': 'ordinary', 'repeat': i, 'fixture_sha256': 'same'}
                       for i in range(4)]
            self._make_plan(root, entries)
            for entry, seconds in zip(entries, [float('nan'), float('inf'), float('-inf'), 2.5]):
                self._write_run(root, entry, {'status': 'completed', 'usage': None, 'seconds': seconds})
            result = report.summarize(root)
            metrics = result['groups'][0]['metrics']['seconds']
            self.assertEqual(metrics['observed'], 1)
            self.assertEqual(metrics['missing'], 3)
            self.assertEqual(metrics['mean'], 2.5)
            self.assertEqual(metrics['min'], 2.5)
            self.assertEqual(metrics['max'], 2.5)

    def test_malformed_observations_preserve_rows_and_status(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            entries = [
                {'id': 'bad', 'case': 'case', 'mode': 'ordinary', 'repeat': 1, 'fixture_sha256': 'same'},
                {'id': 'missing', 'case': 'case', 'mode': 'ordinary', 'repeat': 2, 'fixture_sha256': 'same'},
            ]
            self._make_plan(root, entries)
            self._write_run(root, entries[0], {'status': 'timed_out',
                                               'usage': {'input': float('nan'), 'output': float('inf')},
                                               'seconds': float('-inf')})
            result = report.summarize(root)
            self.assertEqual(len(result['runs']), 2)
            self.assertEqual([x['status'] for x in result['runs']], ['timed_out', 'not_run'])
            self.assertEqual([x['acceptance'] for x in result['runs']], ['unverified', 'unverified'])
            self.assertEqual(result['groups'][0]['planned'], 2)
            self.assertEqual(result['groups'][0]['statuses'], {'timed_out': 1, 'not_run': 1})

    def test_review_binding_survives_malformed_observations(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            entry = {'id': 'bad', 'case': 'case', 'mode': 'ordinary', 'repeat': 1, 'fixture_sha256': 'same'}
            self._make_plan(root, [entry])
            self._write_run(root, entry, {'status': 'completed',
                                          'usage': {'input': float('nan')}, 'seconds': float('inf')})
            review = root / 'review.json'
            review.write_text(json.dumps({'runs': [{'id': 'bad', 'acceptance': 'fail',
                                                    'result_sha256': report.sha(root / 'bad' / 'result.json')}]}))
            self.assertEqual(report.summarize(root, review)['runs'][0]['acceptance'], 'fail')
            (root / 'bad' / 'result.json').write_text((root / 'bad' / 'result.json').read_text() + ' ')
            with self.assertRaises(ValueError):report.summarize(root, review)

    def test_truthy_non_dict_usage_treated_as_missing(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            entries = [
                {'id': 'bad', 'case': 'case', 'mode': 'ordinary', 'repeat': 1, 'fixture_sha256': 'same'},
                {'id': 'good', 'case': 'case', 'mode': 'ordinary', 'repeat': 2, 'fixture_sha256': 'same'},
            ]
            self._make_plan(root, entries)
            # Truthy non-dict usage must not crash and must count as missing.
            self._write_run(root, entries[0], {'status': 'completed', 'usage': '100', 'seconds': 5})
            self._write_run(root, entries[1], {'status': 'completed',
                                               'usage': {'input': 30, 'output': 7}, 'seconds': 9})
            result = report.summarize(root)  # must not raise
            metrics = result['groups'][0]['metrics']
            # The bad run's input/output/cache/cost are all missing; only the good run contributes.
            self.assertEqual(metrics['input']['observed'], 1)
            self.assertEqual(metrics['input']['missing'], 1)
            self.assertEqual(metrics['input']['mean'], 30)
            self.assertEqual(metrics['output']['observed'], 1)
            self.assertEqual(metrics['output']['missing'], 1)
            self.assertEqual(metrics['cache_read']['observed'], 0)
            self.assertEqual(metrics['cache_read']['missing'], 2)
            # Both seconds values are valid and unaffected by the bad usage dict.
            self.assertEqual(metrics['seconds']['observed'], 2)
            self.assertEqual(metrics['seconds']['missing'], 0)
            self.assertEqual(metrics['seconds']['min'], 5)
            self.assertEqual(metrics['seconds']['max'], 9)
            # Rows and statuses survive.
            self.assertEqual([x['status'] for x in result['runs']], ['completed', 'completed'])

    def test_json_output_has_no_nonfinite_floats(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            entry = {'id': 'bad', 'case': 'case', 'mode': 'ordinary', 'repeat': 1, 'fixture_sha256': 'same'}
            self._make_plan(root, [entry])
            self._write_run(root, entry, {'status': 'completed',
                                          'usage': {'input': float('nan'), 'output': float('inf'),
                                                    'cache_read': float('-inf'), 'cache_write': 0},
                                          'seconds': float('nan')})
            result = report.summarize(root)
            # allow_nan=False raises if any NaN/Infinity survives serialization.
            encoded = json.dumps(result, allow_nan=False)
            self.assertNotIn('NaN', encoded)
            self.assertNotIn('Infinity', encoded)
            row = result['runs'][0]
            self.assertIsNone(row['usage']['input'])
            self.assertIsNone(row['usage']['output'])
            self.assertIsNone(row['usage']['cache_read'])
            self.assertEqual(row['usage']['cache_write'], 0)
            self.assertIsNone(row['seconds'])


if __name__ == '__main__':unittest.main()
