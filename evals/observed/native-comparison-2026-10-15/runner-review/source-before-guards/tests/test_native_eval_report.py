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


if __name__ == '__main__':unittest.main()
