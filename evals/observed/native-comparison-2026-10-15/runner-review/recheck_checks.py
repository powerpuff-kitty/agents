"""Independent followup probes; no native executable or network invocation."""
from pathlib import Path
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import time
import unittest
from unittest.mock import patch

BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'recheck/scripts'))
import native_eval as n

WORK = BASE / 'recheck/disposable'
WORK.mkdir()
skills, export = WORK / 'skills', WORK / 'export'
for name in ['systematic-debugging', 'change-review']:
    path = skills / name / 'SKILL.md'
    path.parent.mkdir(parents=True)
    path.write_text('---\nname: ' + name + '\n---\nSynthetic offline procedure.\n')
for name in ['feature-developer', 'quality-engineer']:
    path = export / 'agents' / (name + '.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('---\nmode: all\n---\nSynthetic offline agent.\n')
    role = WORK / 'repo/agents' / name / 'instructions.md'
    role.parent.mkdir(parents=True, exist_ok=True)
    role.write_text('Synthetic role.\n')
(WORK / 'repo/shared').mkdir(parents=True)
(WORK / 'repo/shared/operating-contract.md').write_text('Synthetic contract.\n')
n.behavior_eval.ROOT = WORK / 'repo'

prepared = WORK / 'prepared'
plan = n.prepare(prepared, skills, export, repeats=1, model='synthetic/offline')
results = {'runner_sha256': n.digest(Path(n.__file__).read_bytes()), 'prepared_runs': len(plan['runs'])}
model = {'providerID': 'synthetic', 'id': 'offline'}

def locate(case, mode='ordinary'):
    entry = next(e for e in plan['runs'] if e['case'] == case and e['mode'] == mode)
    return prepared / entry['id'], entry

clock = [0.0]
activity = []
resolved_agent = ['build']
ready_delay = [0.0]
class FakeHost:
    version = 'opencode v2.0.27'
    def __init__(self, executable, project, deadline=None):
        self.project, self.deadline = project, deadline
    def ready(self):
        clock[0] += ready_delay[0]
    def request(self, path, body=None):
        activity.append({'at': clock[0], 'path': path, 'body': body})
        if path.startswith('/api/location'):
            return {'directory': str(self.project), 'project': {'directory': str(self.project)}}
        if path.startswith('/api/skill'):
            return {'data': [{'id': f.parent.name, 'path': str(f), 'content': f.read_text().split('\n---\n', 1)[1].strip()} for f in (self.project / '.agents/skills').glob('*/SKILL.md')]}
        if path.startswith('/api/agent'):
            data = [{'id': f.stem, 'steps': 12, 'system': f.read_text().split('\n---\n', 1)[1].strip()} for f in (self.project / '.opencode/agents').glob('*.md')]
            # Intentionally omit build.system: the inventory must reveal whether
            # missing and empty fields are distinguished in the evidence.
            return {'data': data + [{'id': 'build', 'steps': 12}]}
        if path == '/api/session' or path == '/api/session/root':
            return {'data': {'id': 'root', 'agent': resolved_agent[0], 'location': {'directory': str(self.project)}, 'model': model,
                'outcome': 'succeeded', 'tokens': {'input': 1, 'output': 1, 'cache': {'read': 0, 'write': 0}}, 'cost': 0}}
        if '/message?' in path or path.startswith('/api/session?'):
            return {'data': []}
        return {}
    def close(self): pass

def execute(case, mode='ordinary'):
    activity.clear()
    run, entry = locate(case, mode)
    with patch.object(n, 'Host', FakeHost), patch.object(n.time, 'monotonic', lambda: clock[0]):
        outcome = n.execute(run, entry, 'never-invoked', model, timeout=1.0, max_cost=1.0)
    return run, outcome

ready_delay[0] = 10.0
run, outcome = execute('implementation-unavailable-check')
results['expired_preflight'] = {'status': outcome['status'], 'prompt_submitted': any(a['path'].endswith('/prompt') for a in activity)}
ready_delay[0] = 0.0

run, outcome = execute('implementation-unavailable-check', 'skill')
preflight = json.loads((run / 'preflight.json').read_text())
results['controlled_primary'] = {'status': outcome['status'],
    'requested_agent': next(a['body']['agent'] for a in activity if a['path'] == '/api/session'),
    'resolved_agent': preflight['session']['agent'],
    'built_in_evidence': preflight['inventory'].get('built_in_build')}

resolved_agent[0] = 'ambient-agent'
run, outcome = execute('focused-review-with-skills')
results['ambient_primary_rejected'] = {'status': outcome['status'], 'error': outcome.get('error'),
    'prompt_submitted': any(a['path'].endswith('/prompt') for a in activity)}
resolved_agent[0] = 'build'

run, entry = locate('focused-review-with-skills', 'skill')
sentinel = '{"prior_attempt":true}'
(run / 'preflight.json').write_text(sentinel)
with patch.object(n, 'Host') as host:
    try:
        n.execute(run, entry, 'unused', model, 1, 1)
        refused = False
    except ValueError:
        refused = True
    results['partial_attempt'] = {'refused': refused, 'prior_file_preserved': (run / 'preflight.json').read_text() == sentinel,
        'host_started': host.called}

run, entry = locate('focused-review-with-skills', 'named-agent')
project = run / 'workspace'
subprocess.run(['git', 'reset', '-q', 'HEAD', '--', 'pricing.py'], cwd=project, check=True)
with patch.object(n, 'Host') as host:
    result = n.execute(run, entry, 'unused', model, 1, 1)
    results['index_drift_preflight'] = {'status': result['status'], 'host_started': host.called, 'error': result.get('error')}
shutil.rmtree(project / '.git')
results['deleted_git_checks'] = n.invariant_checks(run, entry['case'])

pidfile = WORK / 'child.pid'
parent = subprocess.Popen([sys.executable, '-c',
    'import subprocess,sys,time; from pathlib import Path; '
    'p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"]); '
    'Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(60)', str(pidfile)], start_new_session=True)
for _ in range(100):
    if pidfile.exists(): break
    time.sleep(.01)
child = int(pidfile.read_text())
host = object.__new__(n.Host)
host.process = parent
try:
    host.close()
    # A killed orphan may briefly remain a zombie; inspect only this probe PID.
    state = subprocess.run(['ps', '-o', 'stat=', '-p', str(child)], capture_output=True, text=True).stdout.strip()
    results['owned_group_cleanup'] = {'parent_exited': parent.poll() is not None, 'child_state': state,
        'child_running': bool(state) and not state.startswith('Z')}
finally:
    try: os.kill(child, 15)
    except ProcessLookupError: pass
    if parent.poll() is None:
        parent.terminate()
        parent.wait(timeout=5)

# Test request-deadline mechanics without a socket. A slow read consumes the
# budget; whether control returns and whether another request is allowed is data.
class FakeResponse:
    def __enter__(self): return self
    def __exit__(self, *args): pass
    def read(self, limit):
        clock[0] += 10
        return b'{}'
class FakeOpener:
    def open(self, request, timeout): return FakeResponse()
host = object.__new__(n.Host)
host.url, host.auth, host.opener, host.deadline = 'http://synthetic.invalid', '', FakeOpener(), clock[0] + 1
with patch.object(n.time, 'monotonic', lambda: clock[0]):
    value = host.request('/offline-no-network')
    results['response_read_deadline'] = {'request_returned_after_deadline': clock[0] > host.deadline, 'value': value}
    try:
        host.request('/offline-no-network')
        refused = False
    except TimeoutError:
        refused = True
    results['response_read_deadline']['next_request_refused'] = refused

stream = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(BASE / 'recheck/tests'))
regression_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(BASE / 'recheck/regression-tests.log').write_text(stream.getvalue())
results['repository_regression_tests'] = {'run': regression_result.testsRun, 'failures': len(regression_result.failures), 'errors': len(regression_result.errors)}
(BASE / 'recheck/results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
