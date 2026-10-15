#!/usr/bin/env python3
"""Prepare matched native trials offline; run only with explicit host/model/bounds.

OpenCode 2.0.27 API adapter. Records host usage, not invoice-complete accounting.
Exit 1: collection/invariant failure; 2: collected, task acceptance needs review.
"""
import argparse
import base64
import hashlib
import json
import math
import os
from pathlib import Path
import random
import secrets
import signal
import shutil
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.error
import urllib.request

import behavior_eval
from opencode_probe import stage_export

class NativeHTTPError(ValueError):
    def __init__(self, status, path, detail):
        self.status = status
        super().__init__('Native API ' + path + ' HTTP ' + str(status) + ': ' + detail)


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    'implementation-dirty-worktree': ('feature-developer', 'systematic-debugging',
        'Fix the pagination boundary bug and verify the change. Preserve my pending labels.txt edit.'),
    'focused-review-with-skills': ('quality-engineer', 'change-review',
        'Review all pending staged, unstaged and relevant new code for concrete defects. Do not edit files or the index.'),
    'implementation-unavailable-check': ('feature-developer', 'systematic-debugging',
        'Implement the input-validation contract in port.ts. Preserve owner-note.txt. Run feasible checks and report remaining verification gaps.'),
}
SCOPE = (' Work only within this project. Do not install tools, commit, publish or use web/network tools. '
         'Report actual checks, failures and limits. Existing executable availability and permission to use it are separate questions.')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def snapshot(root):
    result = {}
    for p in sorted(Path(root).rglob('*')):
        if {'.git', '__pycache__'} & set(p.relative_to(root).parts):
            continue
        if p.is_symlink():
            raise ValueError('Linked project input/output: ' + str(p.relative_to(root)))
        if p.is_file():
            result[str(p.relative_to(root))] = digest(p.read_bytes())
    return result


def git_state(project):
    if not (project / '.git').is_dir():
        return None
    env = {**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}
    entries = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=project, env=env, timeout=10)
    index = project / '.git/index'
    return {'staged_entries_sha256': digest(entries),
            'index_bytes_sha256': digest(index.read_bytes()) if index.exists() else None}


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items()
                if k not in {'reasoning', 'thinking', 'encrypted_content', 'signature'}}
    if isinstance(value, list):
        return [clean(v) for v in value if not isinstance(v, dict)
                or v.get('type') not in {'reasoning', 'thinking', 'redacted_thinking'}]
    return value


def permissions(case):
    rules = [{'action': '*', 'resource': '*', 'effect': 'deny'}]
    for action in ['read', 'glob', 'grep', 'skill', 'subagent', 'execute']:
        rules.append({'action': action, 'resource': '*', 'effect': 'allow'})
    for command in ['pwd', 'ls', 'ls *', 'git status*', 'git diff*', 'git ls-files*',
                    'python3 -B -m unittest*', 'command -v *', 'which *',
                    'standalone-pilot-tsc*', 'node --version', 'bun --version']:
        rules.append({'action': 'shell', 'resource': command, 'effect': 'allow'})
    if case != 'focused-review-with-skills':
        rules.append({'action': 'edit', 'resource': '*', 'effect': 'allow'})
    for action, resource in [('external_directory', '*'), ('read', '*.env*')]:
        rules.append({'action': action, 'resource': resource, 'effect': 'deny'})
    for resource in ['.git/*', '.agents/*', '.opencode/*', 'opencode.json',
                     'labels.txt', 'test_pagination.py', 'owner-note.txt', 'CONTRACT.md']:
        rules.append({'action': 'edit', 'resource': resource, 'effect': 'deny'})
    return rules


def revision(root):
    if not (root / '.git').exists():
        return None
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True, timeout=10).strip()


def prepare(output, skills, export, repeats=2, seed=17, cases=None, model="deepseek/deepseek-v4-pro"):
    output, skills, export = Path(output).resolve(), Path(skills).resolve(), Path(export).resolve()
    if output.exists() or repeats < 1:
        raise ValueError('Choose a new output directory and positive repetitions')
    owned = sorted(skills.glob('*/SKILL.md'))
    if not owned:
        raise ValueError('No skill folders')
    for f in owned:
        if f.parent.is_symlink() or any(p.is_symlink() for p in f.parent.rglob('*')):
            raise ValueError('Linked skill source')
    roster = [(case, mode, repeat) for case in (cases or CASES)
              for mode in ['ordinary', 'skill', 'named-agent'] for repeat in range(1, repeats + 1)]
    random.Random(seed).shuffle(roster)
    plan = {'format_version': 1, 'seed': seed, 'repetitions': repeats,
            'agents_revision': revision(ROOT), 'skills_revision': revision(skills),
            'runner_sha256': digest(Path(__file__).read_bytes()), 'model': model, 'runs': []}
    output.mkdir(parents=True)
    for number, (case, mode, repeat) in enumerate(roster, 1):
        run_id = f'{number:02d}-{case}-{mode}-{repeat}'
        run = output / run_id
        behavior_eval.prepare(case, run, skills)
        # Participant receives native folders, never grader/expected-answer metadata.
        project = run / 'workspace'
        stage_export(export, project)
        for f in owned:
            shutil.copytree(f.parent, project / '.agents/skills' / f.parent.name)
        ids = [p.stem for p in (project / '.opencode/agents').glob('*.md')]
        config = {'autoupdate': False, 'model': model, 'default_agent': 'build', 'permissions': permissions(case),
                  'agents': {name: {'steps': 12, 'model': model} for name in ids + ['build', 'general', 'explore']}}
        write(project / 'opencode.json', config)
        role, skill, task = CASES[case]
        prompt = task + SCOPE
        if mode == 'skill':
            prompt += f' Use the installed {skill} skill for this task.'
        (run / 'prompt.txt').write_text(prompt + '\n', encoding='utf-8')
        before = snapshot(project)
        write(run / 'before.json', before)
        write(run / 'git-before.json', git_state(project))
        plan['runs'].append({'id': run_id, 'case': case, 'mode': mode, 'repeat': repeat,
                             'agent': role if mode == 'named-agent' else None,
                             'skill': skill if mode == 'skill' else None,
                             'prompt_sha256': digest((run / 'prompt.txt').read_bytes()),
                             'fixture_sha256': digest(json.dumps(before, sort_keys=True).encode())})
    write(output / 'plan.json', plan)
    (output / 'plan.sha256').write_text(digest((output / 'plan.json').read_bytes()) + '\n')
    return plan


def verify_binding(expected, location, session, model):
    expected = str(Path(expected).resolve())
    if location.get('directory') != expected or location.get('project', {}).get('directory') != expected:
        raise ValueError('Host project mismatch')
    if session.get('location', {}).get('directory') != expected:
        raise ValueError('Session project mismatch')
    actual = session.get('model', {})
    if any(actual.get(k) != model[k] for k in ['id', 'providerID']):
        raise ValueError('Resolved model mismatch')


def verify_inventory(project, skills, agents):
    loaded_skills = {v['id']: v for v in skills}
    loaded_agents = {v['id']: v for v in agents}
    result = {'skills': {}, 'agents': {}}
    for kind, files in [('skills', (project / '.agents/skills').glob('*/SKILL.md')),
                        ('agents', (project / '.opencode/agents').glob('*.md'))]:
        for f in sorted(files):
            name = f.parent.name if kind == 'skills' else f.stem
            body = f.read_text().split('\n---\n', 1)[1].strip()
            entry = (loaded_skills if kind == 'skills' else loaded_agents).get(name, {})
            actual = entry.get('content' if kind == 'skills' else 'system', '').strip()
            if actual != body or (kind == 'skills' and entry.get('path') != str(f)):
                raise ValueError('Instruction identity mismatch: ' + name)
            if kind == 'agents' and entry.get('steps') != 12:
                raise ValueError('Agent step bound mismatch')
            result[kind][name] = {'body_sha256': digest(body.encode()), 'utf8_bytes': len(body.encode())}
    if not result['skills'] or not result['agents'] or loaded_agents.get('build', {}).get('steps') != 12:
        raise ValueError('Incomplete inventory or default step bound')
    result['built_in_build'] = {'registered_system_sha256': digest(str(loaded_agents['build'].get('system', '')).encode()), 'steps': loaded_agents['build']['steps'], 'limits': 'Registered fields only; the complete provider prompt is not exposed.'}
    return result


class Host:
    def __init__(self, executable, project, deadline=None):
        self.deadline = deadline
        self.project = project
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('OPENCODE_') and k != 'INIT_CWD'}
        self.env.update(PWD=str(project), OPENCODE_CONFIG_CONTENT='{"autoupdate":false}',
                        OPENCODE_USERNAME='opencode', OPENCODE_PASSWORD=secrets.token_hex(24),
                        PYTHONDONTWRITEBYTECODE='1')
        self.version = subprocess.check_output([executable, '--version'], text=True, env=self.env, timeout=10).strip()
        if self.version != 'opencode v2.0.27':
            raise ValueError('This API adapter requires OpenCode 2.0.27')
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
        self.url = f'http://127.0.0.1:{port}'
        self.auth = base64.b64encode(('opencode:' + self.env['OPENCODE_PASSWORD']).encode()).decode()
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.process = subprocess.Popen([executable, 'serve', '--hostname', '127.0.0.1', '--port', str(port)],
                                        cwd=project, env=self.env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

    def request(self, path, body=None):
        request = urllib.request.Request(self.url + path, data=json.dumps(body).encode() if body is not None else None,
                                         headers={'Authorization': 'Basic ' + self.auth, 'Content-Type': 'application/json'})
        remaining = self.deadline - time.monotonic() if self.deadline else 10
        if remaining <= 0:
            raise TimeoutError('Native request deadline expired')
        try:
            with self.opener.open(request, timeout=min(10, remaining)) as response:
                raw = response.read(20_000_001)
        except urllib.error.HTTPError as error:
            detail = error.read(4000).decode('utf-8', errors='replace')
            raise NativeHTTPError(error.code, path.split('?')[0], detail) from None
        if len(raw) > 20_000_000:
            raise ValueError('Host response bound exceeded')
        return json.loads(raw) if raw else None

    def ready(self):
        for _ in range(50):
            if self.deadline and time.monotonic() >= self.deadline:
                raise TimeoutError('Native readiness deadline expired')
            if self.process.poll() is not None:
                raise ValueError('Host exited before readiness')
            try:
                return self.request('/openapi.json')
            except NativeHTTPError as error:
                if error.status != 503:
                    raise
                time.sleep(.1)
            except OSError:
                time.sleep(.1)
        raise TimeoutError('Host readiness timeout')

    def close(self):
        # serve owns a new process group; clean descendants even if its parent exits.
        try:
            os.killpg(self.process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(self.process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        self.process.wait(timeout=3)


def pages(host, path):
    result, seen = [], set()
    base = path
    for _ in range(100):
        page = host.request(path)
        result.extend(page['data'])
        cursor = page.get('cursor', {}).get('next')
        if not cursor:
            return result
        if cursor in seen:
            raise ValueError('Repeated API cursor')
        seen.add(cursor)
        parsed = urllib.parse.urlsplit(base)
        filters = [(key, value) for key, value in urllib.parse.parse_qsl(parsed.query) if key not in {'order', 'cursor'}]
        path = parsed.path + '?' + urllib.parse.urlencode(filters + [('cursor', cursor)])
    raise ValueError('API pagination bound exceeded')


def capture(host, session_id, project):
    queue, sessions, messages = [session_id], {}, {}
    while queue:
        current = queue.pop(0)
        if current in sessions or len(sessions) >= 30:
            raise ValueError('Duplicate or excessive child sessions')
        session = host.request('/api/session/' + current)['data']
        if session['location']['directory'] != str(project):
            raise ValueError('Session moved outside fixture')
        sessions[current] = clean(session)
        messages[current] = clean(pages(host, '/api/session/' + current + '/message?limit=100&order=asc'))
        children = pages(host, '/api/session?' + urllib.parse.urlencode({'parentID': current, 'limit': 100, 'order': 'asc'}))
        queue.extend(child['id'] for child in children)
    return sessions, messages


def usage(sessions):
    result = {'input': 0, 'output': 0, 'cache_read': 0, 'cache_write': 0, 'reported_cost': 0.0,
              'complete_session_fields': True}
    for session in sessions.values():
        tokens = session.get('tokens', {})
        values = {'input': tokens.get('input'), 'output': tokens.get('output'),
                  'cache_read': tokens.get('cache', {}).get('read'), 'cache_write': tokens.get('cache', {}).get('write'),
                  'reported_cost': session.get('cost')}
        for key, value in values.items():
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                result['complete_session_fields'] = False
                result[key] = None
            elif result[key] is not None:
                result[key] += value
    return result


def invariant_checks(run, case):
    project = run / 'workspace'
    before = json.loads((run / 'before.json').read_text())
    after = snapshot(project)
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    allowed = {'implementation-dirty-worktree': {'pagination.py'},
               'implementation-unavailable-check': {'port.ts'}, 'focused-review-with-skills': set()}[case]
    before_git = json.loads((run / 'git-before.json').read_text())
    after_git = git_state(project)
    checks = {'source_scope_preserved': set(changed) <= allowed,
              'staging_entries_preserved': (before_git is None and after_git is None) or
              (before_git is not None and after_git is not None and
               before_git['staged_entries_sha256'] == after_git['staged_entries_sha256'])}
    commands = []
    if case == 'implementation-dirty-worktree':
        p = subprocess.run([sys.executable, '-B', '-m', 'unittest', '-v'], cwd=project, capture_output=True, text=True, timeout=20)
        commands.append({'argv': [sys.executable, '-B', '-m', 'unittest', '-v'], 'exit': p.returncode,
                         'stdout': p.stdout, 'stderr': p.stderr})
        checks['boundary_tests'] = p.returncode == 0
    write(run / 'after.json', after)
    write(run / 'git-after.json', git_state(project))
    write(run / 'checks.json', {'checks': checks, 'changed_files': changed, 'commands': commands,
                               'task_acceptance': 'needs_independent_review',
                               'limits': 'Artifact checks do not grade review reasoning, compiler success or authenticated side effects.'})
    return checks


def execute(run, entry, executable, model, timeout, max_cost):
    run = Path(run).resolve()
    if any((run / name).exists() for name in ['attempt.started.json', 'result.json', 'preflight.json', 'submitted-prompt.json', 'sessions.json', 'messages.json']):
        raise ValueError('Existing/partial attempt; never overwrite a trial')
    with (run / 'attempt.started.json').open('x') as marker:
        json.dump({'started_utc_epoch': time.time()}, marker)
    project = run / 'workspace'
    result = {'entry': entry, 'model_requested': model, 'timeout_seconds': timeout, 'max_reported_cost': max_cost,
              'task_acceptance': 'needs_independent_review', 'status': 'setup_failed',
              'runner_sha256': digest(Path(__file__).read_bytes()),
              'usage_limits': 'Host session totals, including discovered descendants. Hidden auxiliary calls/billing remain unknown; reported-cost interrupt can overshoot.'}
    host, session_id = None, None
    started = time.monotonic()
    sessions, messages = {}, {}
    try:
        before = json.loads((run / 'before.json').read_text())
        if snapshot(project) != before or digest(json.dumps(before, sort_keys=True).encode()) != entry['fixture_sha256']:
            raise ValueError('Prepared fixture drift')
        if digest((run / 'prompt.txt').read_bytes()) != entry['prompt_sha256']:
            raise ValueError('Prompt drift')
        if git_state(project) != json.loads((run / 'git-before.json').read_text()):
            raise ValueError('Prepared Git metadata drift')
        host = Host(executable, project, started + timeout)
        result['host_version'] = host.version
        host.ready()
        if time.monotonic() >= started + timeout:
            raise TimeoutError('Deadline expired before preflight')
        query = '?' + urllib.parse.urlencode({'location[directory]': str(project)})
        location = host.request('/api/location' + query)
        # Reject wrong location before fetching any project inventory or starting inference.
        verify_binding(project, location, {'location': {'directory': str(project)}, 'model': model}, model)
        inventory = None
        for _ in range(40):
            skills = host.request('/api/skill' + query)['data']
            agents = host.request('/api/agent' + query)['data']
            try:
                inventory = verify_inventory(project, skills, agents)
                break
            except ValueError:
                time.sleep(.2)
        if inventory is None:
            raise ValueError('Native inventory failed identity check')
        body = {'title': 'Native evaluation ' + entry['id'], 'model': model,
                'location': {'directory': str(project)},
                'permissions': json.loads((project / 'opencode.json').read_text())['permissions']}
        body['agent'] = entry['agent'] or 'build'
        if time.monotonic() >= started + timeout:
            raise TimeoutError('Deadline expired before session creation')
        created = host.request('/api/session', body)['data']
        session_id = created['id']
        resolved = host.request('/api/session/' + session_id)['data']
        verify_binding(project, location, created, model)
        verify_binding(project, location, resolved, model)
        if resolved.get('agent') != body['agent']:
            raise ValueError('Named agent not resolved')
        write(run / 'preflight.json', {'location': location, 'session': clean(resolved), 'inventory': inventory})
        prompt = {'text': (run / 'prompt.txt').read_text().strip()}
        if entry['skill']:
            prompt['skills'] = [{'id': entry['skill']}]
        write(run / 'submitted-prompt.json', prompt)
        if time.monotonic() >= started + timeout:
            raise TimeoutError('Deadline expired before prompting')
        host.request('/api/session/' + session_id + '/prompt', prompt)
        result['status'] = 'running'
        while True:
            sessions, messages = capture(host, session_id, project)
            write(run / 'sessions.json', sessions)
            write(run / 'messages.json', messages)
            observed = usage(sessions)
            elapsed = time.monotonic() - started
            if any(s.get('model', {}).get('providerID') != model['providerID'] or s.get('model', {}).get('id') != model['id'] for s in sessions.values()):
                result['status'] = 'model_mismatch'
                break
            if elapsed >= timeout:
                result['status'] = 'timed_out'
                break
            if not observed['complete_session_fields'] or observed['reported_cost'] >= max_cost:
                result['status'] = 'usage_bound_reached'
                break
            if all(s.get('outcome') in {'succeeded', 'failed', 'interrupted'} for s in sessions.values()):
                result['status'] = 'collected' if all(s['outcome'] == 'succeeded' for s in sessions.values()) else 'host_failed'
                break
            time.sleep(1)
    except Exception as error:
        if isinstance(error, TimeoutError):
            result['status'] = 'timed_out'
        elif result['status'] == 'running':
            result['status'] = 'collection_failed'
        result['error'] = {'type': type(error).__name__, 'message': str(error)}
    finally:
        if host:
            try:
                if session_id and result['status'] != 'collected':
                    host.deadline = time.monotonic() + 10
                    for sid in set(sessions) | {session_id}:
                        host.request('/api/session/' + sid + '/interrupt', {})
                    sessions, messages = capture(host, session_id, project)
                    write(run / 'sessions.json', sessions)
                    write(run / 'messages.json', messages)
            except Exception as error:
                result['final_capture_error'] = type(error).__name__
            finally:
                host.close()
        result['seconds'] = round(time.monotonic() - started, 3)
        result['usage'] = usage(sessions) if sessions else None
        try:
            result['invariants'] = invariant_checks(run, entry['case'])
        except Exception as error:
            result['invariant_error'] = type(error).__name__
        write(run / 'result.json', result)
    return result


def report(output):
    plan = json.loads((output / 'plan.json').read_text())
    if digest((output / 'plan.json').read_bytes()) != (output / 'plan.sha256').read_text().strip():
        raise ValueError('Plan drift')
    rows = []
    for entry in plan['runs']:
        path = output / entry['id'] / 'result.json'
        row = json.loads(path.read_text()) if path.exists() else {'entry': entry, 'status': 'not_run', 'task_acceptance': 'unverified', 'usage': None}
        rows.append(row)
    result = {'plan_sha256': digest((output / 'plan.json').read_bytes()), 'planned': len(rows), 'runs': rows,
              'limits': 'No aggregate success rate or savings claim without independent acceptance and matched comparable outcomes. Usage fields exclude unexposed auxiliary calls.'}
    write(output / 'report.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--skills-source', required=True, type=Path)
    p.add_argument('--agents-export', required=True, type=Path)
    p.add_argument('--repeats', type=int, default=2)
    p.add_argument('--model', required=True, help='Model pin for all built-in/custom agents; preparation makes no calls')
    p.add_argument('--case', action='append', choices=list(CASES))
    for command in ['run', 'report']:
        p = sub.add_parser(command)
        p.add_argument('--output', required=True, type=Path)
        if command == 'run':
            p.add_argument('--id', required=True)
            p.add_argument('--opencode', required=True)
            p.add_argument('--model', required=True, help='Explicit provider/model; no provider fallback')
            p.add_argument('--timeout', required=True, type=float)
            p.add_argument('--max-cost', required=True, type=float, help='Host-reported cost interrupt threshold, not a hard billing cap')
    args = parser.parse_args()
    if args.command == 'prepare':
        plan = prepare(args.output, args.skills_source, args.agents_export, args.repeats, cases=args.case, model=args.model)
        print(json.dumps({'planned': len(plan['runs']), 'model_calls': 0}))
    elif args.command == 'report':
        print(json.dumps({'planned': report(args.output)['planned']}))
    else:
        if not all(math.isfinite(x) and x > 0 for x in [args.timeout, args.max_cost]):
            parser.error('Positive finite time and cost bounds required')
        provider, separator, model = args.model.partition('/')
        if not separator or not provider or not model:
            parser.error('Use explicit provider/model')
        plan = report(args.output)
        original_plan = json.loads((args.output / 'plan.json').read_text())
        if original_plan['model'] != args.model:
            parser.error('Model must match the frozen plan')
        entries = [x['entry'] for x in plan['runs'] if x['entry']['id'] == args.id]
        if len(entries) != 1:
            parser.error('Unknown/ambiguous planned run')
        result = execute(args.output / args.id, entries[0], args.opencode,
                         {'providerID': provider, 'id': model}, args.timeout, args.max_cost)
        print(json.dumps(result))
        report(args.output)
        return 2 if result['status'] == 'collected' and all(result.get('invariants', {}).values()) and 'invariant_error' not in result else 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
