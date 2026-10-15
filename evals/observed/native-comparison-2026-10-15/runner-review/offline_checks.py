"""Disposable source-only probes. No OpenCode executable or provider is invoked."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
from unittest.mock import patch

BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(BASE / 'source'))
import native_eval as n

WORK = BASE / 'disposable-2'
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
plan = n.prepare(prepared, skills, export, repeats=1)
report = n.report(prepared)
results = {'prepared_runs': len(plan['runs']),
           'not_run_rows': sum(r['status'] == 'not_run' for r in report['runs']),
           'matched_workspaces': {case: len({e['fixture_sha256'] for e in plan['runs'] if e['case'] == case}) for case in n.CASES}}

def locate(case, mode='ordinary'):
    entry = next(e for e in plan['runs'] if e['case'] == case and e['mode'] == mode)
    return prepared / entry['id'], entry

run, entry = locate('focused-review-with-skills')
project = run / 'workspace'
original = n.snapshot(project)
subprocess.run(['git', 'reset', '-q', 'HEAD', '--', 'pricing.py'], cwd=project, check=True)
results['index_drift'] = {
    'snapshot_still_matches': n.snapshot(project) == original,
    'staged_hash_changed': n.git_state(project)['staged_entries_sha256'] != json.loads((run / 'git-before.json').read_text())['staged_entries_sha256']}
shutil.rmtree(project / '.git')
results['deleted_git_checks'] = n.invariant_checks(run, entry['case'])

clock = [0.0]
model = {'providerID': 'synthetic', 'id': 'offline'}
activity = []
class FakeHost:
    version = 'opencode v2.0.27'
    def __init__(self, executable, project):
        self.project = project
    def ready(self):
        clock[0] += 10.0
    def request(self, path, body=None):
        activity.append({'at': clock[0], 'path': path})
        if path.startswith('/api/location'):
            return {'directory': str(self.project), 'project': {'directory': str(self.project)}}
        if path.startswith('/api/skill'):
            return {'data': [{'id': f.parent.name, 'path': str(f), 'content': f.read_text().split('\n---\n', 1)[1].strip()} for f in (self.project / '.agents/skills').glob('*/SKILL.md')]}
        if path.startswith('/api/agent'):
            data = [{'id': f.stem, 'steps': 12, 'system': f.read_text().split('\n---\n', 1)[1].strip()} for f in (self.project / '.opencode/agents').glob('*.md')]
            return {'data': data + [{'id': 'build', 'steps': 12}, {'id': 'ambient-agent', 'steps': 99, 'system': 'Unverified ambient instructions.'}]}
        if path == '/api/session' or path == '/api/session/root':
            return {'data': {'id': 'root', 'agent': 'ambient-agent', 'location': {'directory': str(self.project)}, 'model': model,
                'outcome': 'succeeded', 'tokens': {'input': 1, 'output': 1, 'cache': {'read': 0, 'write': 0}}, 'cost': 0}}
        if '/message?' in path or path.startswith('/api/session?'):
            return {'data': []}
        return {}
    def close(self):
        activity.append({'at': clock[0], 'path': 'close'})

run, entry = locate('implementation-unavailable-check')
(run / 'preflight.json').write_text('{"prior_attempt": true}')
(run / 'submitted-prompt.json').write_text('{"prior_attempt": true}')
with patch.object(n, 'Host', FakeHost), patch.object(n.time, 'monotonic', lambda: clock[0]):
    result = n.execute(run, entry, 'never-invoked', model, timeout=1.0, max_cost=1.0)
results['expired_timeout'] = {'status': result['status'], 'prompt_requests': [a for a in activity if a['path'].endswith('/prompt')]}
results['prior_attempt_overwritten'] = {
    name: 'prior_attempt' not in json.loads((run / name).read_text()) for name in ['preflight.json', 'submitted-prompt.json']}
preflight = json.loads((run / 'preflight.json').read_text())
results['unverified_default_agent'] = {'resolved_agent': preflight['session']['agent'],
    'inventoried_agent_ids': sorted(preflight['inventory']['agents']),
    'prompt_still_submitted': bool(results['expired_timeout']['prompt_requests'])}

# Run actual local parent/child processes only; do not construct Host, whose
# constructor inherits ambient configuration. Track and clean only our child PID.
pidfile = WORK / 'child.pid'
parent = subprocess.Popen([sys.executable, '-c',
    'import subprocess,sys,time; from pathlib import Path; '
    'p=subprocess.Popen([sys.executable,"-c","import time; time.sleep(60)"]); '
    'Path(sys.argv[1]).write_text(str(p.pid)); time.sleep(60)', str(pidfile)])
import time
for _ in range(100):
    if pidfile.exists(): break
    time.sleep(.01)
child = int(pidfile.read_text())
host = object.__new__(n.Host)
host.process = parent
try:
    host.close()
    try:
        os.kill(child, 0)
        alive = True
    except ProcessLookupError:
        alive = False
    results['host_close'] = {'parent_exited': parent.poll() is not None, 'owned_descendant_still_alive': alive}
finally:
    try: os.kill(child, 15)
    except ProcessLookupError: pass
    if parent.poll() is None:
        parent.terminate()
        parent.wait(timeout=5)

(BASE / 'offline-results.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
