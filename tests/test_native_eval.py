"""Fail-closed native evaluation contracts; no real host or inference calls."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import shutil
import time
import threading
import os
import unittest
from unittest.mock import patch, Mock, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import native_eval as native


class NativeEvalTests(unittest.TestCase):
    def fixture(self, root):
        run = root / 'run'
        project = run / 'workspace'
        skill = project / '.agents/skills/example/SKILL.md'
        agent = project / '.opencode/agents/feature-developer.md'
        skill.parent.mkdir(parents=True)
        agent.parent.mkdir(parents=True)
        skill.write_text('---\nname: example\ndescription: Local fixture.\n---\nLocal skill body.\n')
        agent.write_text('---\ndescription: Local fixture.\n---\nLocal role body.\n')
        (project / 'pagination.py').write_text('def pages(items, size):\n    return [items[i:i+size] for i in range(0, len(items), size)]\n')
        native.write(project / 'opencode.json', {'permissions': []})
        (run / 'prompt.txt').write_text('Fix the scoped bug.\n')
        before = native.snapshot(project)
        native.write(run / 'before.json', before)
        native.write(run / 'git-before.json', None)
        entry = {'id': 'run', 'case': 'implementation-dirty-worktree', 'agent': None,
                 'skill': None, 'mode': 'ordinary', 'repeat': 1,
                 'fixture_sha256': native.digest(json.dumps(before, sort_keys=True).encode()),
                 'prompt_sha256': native.digest((run / 'prompt.txt').read_bytes())}
        return run, project, entry

    def test_wrong_project_and_model_cannot_be_accepted(self):
        project = Path('/tmp/expected').resolve()
        location = {'directory': str(project), 'project': {'directory': str(project)}}
        session = {'location': {'directory': str(project)}, 'model': {'id': 'v1', 'providerID': 'p', 'variant': 'default'}}
        model = {'id': 'v1', 'providerID': 'p'}
        native.verify_binding(project, location, session, model)
        for target, key, value in [('location', 'directory', '/tmp/wrong'), ('project', 'directory', '/tmp/wrong'), ('session', 'directory', '/tmp/wrong'), ('model', 'id', 'v2')]:
            loc, sess = copy.deepcopy(location), copy.deepcopy(session)
            {'location': loc, 'project': loc['project'], 'session': sess['location'], 'model': sess['model']}[target][key] = value
            with self.subTest(target=target), self.assertRaises(ValueError):
                native.verify_binding(project, loc, sess, model)

    def test_instruction_content_and_path_are_checked(self):
        with tempfile.TemporaryDirectory() as raw:
            _, project, _ = self.fixture(Path(raw))
            skills = [{'id': 'example', 'path': str(project / '.agents/skills/example/SKILL.md'), 'content': 'Local skill body.'}]
            agents = [{'id': 'feature-developer', 'system': 'Local role body.', 'steps': 12}, {'id': 'build', 'steps': 12}]
            native.verify_inventory(project, skills, agents)
            for field, value in [('path', '/tmp/global/SKILL.md'), ('content', 'Altered body')]:
                bad = copy.deepcopy(skills);bad[0][field] = value
                with self.assertRaises(ValueError):native.verify_inventory(project, bad, agents)
            bad = copy.deepcopy(agents);bad[0]['steps'] = 100
            with self.assertRaises(ValueError):native.verify_inventory(project, skills, bad)

    def test_fixture_drift_never_starts_a_host_and_retains_failure(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            (project / 'pagination.py').write_text('owner change\n')
            with patch.object(native, 'Host') as host:
                result = native.execute(run, entry, 'unused', {'providerID': 'p', 'id': 'v'}, 1, .1)
            host.assert_not_called()
            self.assertEqual(result['status'], 'setup_failed')
            self.assertTrue((run / 'result.json').exists())
            self.assertEqual((project / 'pagination.py').read_text(), 'owner change\n')
            with self.assertRaises(ValueError):native.execute(run, entry, 'unused', {}, 1, .1)

    def test_wrong_native_project_stops_before_inventory_or_prompt(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            with patch.object(native, 'Host') as host:
                client = host.return_value
                client.version = 'opencode v2.0.27'
                client.request.return_value = {'directory': '/wrong', 'project': {'directory': '/wrong'}}
                result = native.execute(run, entry, 'unused', {'providerID': 'p', 'id': 'v'}, 1, .1)
            self.assertEqual(result['status'], 'setup_failed')
            self.assertEqual(len(client.request.call_args_list), 1)
            self.assertTrue(client.request.call_args[0][0].startswith('/api/location?'))
            client.close.assert_called_once()

    def test_expired_setup_cannot_submit_prompt(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            with patch.object(native, 'Host') as host:
                client = host.return_value
                client.version = 'opencode v2.0.27'
                client.ready.side_effect = lambda: time.sleep(.01)
                result = native.execute(run, entry, 'unused', {'providerID': 'p', 'id': 'v'}, .001, .1)
            self.assertEqual(result['status'], 'timed_out')
            client.request.assert_not_called()
            client.close.assert_called_once()

    def test_partial_preflight_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            native.write(run / 'preflight.json', {'original': True})
            before = (run / 'preflight.json').read_bytes()
            with self.assertRaises(ValueError):native.execute(run, entry, 'unused', {}, 1, .1)
            self.assertEqual((run / 'preflight.json').read_bytes(), before)

    def test_deleted_git_metadata_is_not_preservation(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            subprocess.run(['git', 'init', '-q'], cwd=project, check=True)
            subprocess.run(['git', 'add', 'pagination.py'], cwd=project, check=True)
            native.write(run / 'git-before.json', native.git_state(project))
            shutil.rmtree(project / '.git')
            checks = native.invariant_checks(run, entry['case'])
            self.assertFalse(checks['staging_entries_preserved'])

    @unittest.skipUnless(hasattr(os, 'killpg'), 'POSIX host adapter')
    def test_cleanup_stops_owned_process_group(self):
        with tempfile.TemporaryDirectory() as raw:
            marker = Path(raw) / 'child'
            code = 'import subprocess,sys,time; p=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"]);open(sys.argv[1],"w").write(str(p.pid));time.sleep(60)'
            process = subprocess.Popen([sys.executable, '-c', code, str(marker)], start_new_session=True)
            host = native.Host.__new__(native.Host);host.process = process
            try:
                for _ in range(100):
                    if marker.exists():break
                    time.sleep(.01)
                self.assertTrue(marker.exists())
                child = int(marker.read_text())
                host.close()
                for _ in range(100):
                    state = subprocess.run(['ps', '-o', 'stat=', '-p', str(child)], capture_output=True, text=True).stdout.strip()
                    if not state or state.startswith('Z'):break
                    time.sleep(.01)
                self.assertTrue(not state or state.startswith('Z'), state)
            finally:
                if process.poll() is None:host.close()

    def test_readiness_retries_service_starting_but_not_bad_requests(self):
        host = native.Host.__new__(native.Host)
        host.deadline = time.monotonic() + 2
        host.process = Mock();host.process.poll.return_value = None
        host.request = Mock(side_effect=[native.NativeHTTPError(503, '/openapi.json', 'service_starting'), {'paths': {}}])
        self.assertEqual(host.ready(), {'paths': {}})
        self.assertEqual(host.request.call_count, 2)
        host.request = Mock(side_effect=native.NativeHTTPError(400, '/openapi.json', 'bad request'))
        with self.assertRaises(native.NativeHTTPError):host.ready()
        self.assertEqual(host.request.call_count, 1)

    def test_meaningful_new_verification_file_does_not_mask_owner_changes(self):
        before = {'port.ts': 'original', 'owner-note.txt': 'owner', '.agents/skills/example/SKILL.md': 'instructions'}
        after = {**before, 'port.ts': 'fixed', 'port.check.ts': 'new verification'}
        self.assertTrue(native.source_scope_preserved(before, after, 'implementation-unavailable-check'))
        self.assertFalse(native.source_scope_preserved(before, {**after, 'owner-note.txt': 'lost'}, 'implementation-unavailable-check'))
        self.assertFalse(native.source_scope_preserved(before, {**after, '.agents/skills/example/SKILL.md': 'changed'}, 'implementation-unavailable-check'))
        self.assertFalse(native.source_scope_preserved(before, after, 'focused-review-with-skills'))

    def test_response_crossing_deadline_is_not_accepted(self):
        host = native.Host.__new__(native.Host)
        host.deadline = 1;host.url = 'http://127.0.0.1';host.auth = 'test'
        host.opener = MagicMock()
        host.opener.open.return_value.__enter__.return_value.read.return_value = b'{}'
        with patch.object(native.time, 'monotonic', side_effect=[0, 2]):
            with self.assertRaises(TimeoutError):host.request('/owned')

    @unittest.skipUnless(hasattr(os, 'killpg'), 'POSIX host adapter')
    def test_deadline_watchdog_stops_owned_server_without_a_response(self):
        process = subprocess.Popen([sys.executable, '-c', 'import time;time.sleep(60)'], start_new_session=True)
        host = native.Host.__new__(native.Host);host.process = process;host.deadline_expired = False
        host._close_lock = threading.Lock();host._closed = False
        host._watchdog = threading.Timer(.05, host._expire)
        host._watchdog.start()
        try:
            process.wait(timeout=3)
            self.assertTrue(host.deadline_expired)
            host.close()
            self.assertIsNotNone(process.returncode)
        finally:
            host.close()

    def test_read_only_index_bytes_are_a_separate_invariant(self):
        with tempfile.TemporaryDirectory() as raw:
            run, project, entry = self.fixture(Path(raw))
            subprocess.run(['git', 'init', '-q'], cwd=project, check=True)
            subprocess.run(['git', 'add', 'pagination.py'], cwd=project, check=True)
            native.write(run / 'git-before.json', native.git_state(project))
            subprocess.run(['git', 'update-index', '--assume-unchanged', 'pagination.py'], cwd=project, check=True)
            value = native.invariant_checks(run, 'focused-review-with-skills')
            self.assertTrue(value['staging_entries_preserved'])
            self.assertFalse(value['index_bytes_preserved'])

    def test_host_disables_optional_git_index_refresh(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw);executable = root / 'host';executable.write_text('fixture')
            with patch.object(native.subprocess, 'check_output', return_value='opencode v2.0.27'), patch.object(native.subprocess, 'Popen'):
                host = native.Host(str(executable), root)
            self.assertEqual(host.env['GIT_OPTIONAL_LOCKS'], '0')

    def test_missing_usage_is_unknown_not_zero(self):
        value = native.usage({'a': {'cost': .1, 'tokens': {'input': 4, 'output': 2, 'cache': {'read': 0, 'write': 0}}}, 'b': {}})
        self.assertFalse(value['complete_session_fields'])
        self.assertIsNone(value['input'])
        self.assertIsNone(value['reported_cost'])

    def test_pagination_retains_order_and_detects_repeated_cursor(self):
        with patch.object(native, 'Host') as host:
            client = host.return_value
            client.request.side_effect = [{'data': [1], 'cursor': {'next': 'a'}}, {'data': [2], 'cursor': {}}]
            self.assertEqual(native.pages(client, '/x?order=asc'), [1, 2])
            self.assertIn('cursor=a', client.request.call_args[0][0])
            self.assertNotIn('order=', client.request.call_args[0][0])
            client.request.side_effect = [{'data': [1], 'cursor': {'next': 'a'}}, {'data': [2], 'cursor': {'next': 'a'}}]
            with self.assertRaises(ValueError):native.pages(client, '/x?order=asc')

    def test_planned_missing_run_stays_visible_and_plan_drift_refuses(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            native.write(root / 'plan.json', {'runs': [{'id': 'never-started'}]})
            (root / 'plan.sha256').write_text(native.digest((root / 'plan.json').read_bytes()))
            report = native.report(root)
            self.assertEqual(report['runs'][0]['status'], 'not_run')
            self.assertIsNone(report['runs'][0]['usage'])
            (root / 'plan.json').write_text('{"runs": []}')
            with self.assertRaises(ValueError):native.report(root)

    def test_reasoning_excluded_but_tool_failure_kept(self):
        trace = [{'type': 'reasoning', 'text': 'private'}, {'type': 'assistant', 'content': [{'type': 'tool', 'state': {'status': 'error', 'error': 'compiler unavailable'}}, {'type': 'thinking', 'text': 'private'}]}]
        cleaned = native.clean(trace)
        self.assertEqual(len(cleaned), 1)
        self.assertEqual(cleaned[0]['content'][0]['state']['status'], 'error')
        self.assertEqual(len(cleaned[0]['content']), 1)


if __name__ == '__main__':
    unittest.main()
