import collections
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'source'
sys.path.insert(0, str(SOURCE / 'scripts'))
import native_eval
import native_fixtures

identity = json.loads((HERE / 'source-identity.json').read_text())
for name, expected in identity['uncommitted_overlay_sha256'].items():
    assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == expected, name
print('All 9 overlay hashes match source-identity.json')
skills = HERE / 'synthetic-skills'
for _, skill, _ in native_eval.CASES.values():
    folder = skills / skill
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'SKILL.md').write_text('---\nname: ' + skill + '\ndescription: Disposable offline review input.\n---\nReview only authorized evidence.\n')
plan = native_eval.prepare(HERE / 'default-prepared', skills, HERE / 'export-opencode', model='synthetic/no-inference')
assert len(plan['runs']) == 18
assert set(x['case'] for x in plan['runs']) == set(native_eval.DEFAULT_CASES)
assert all(v == 2 for v in collections.Counter((x['case'], x['mode']) for x in plan['runs']).values())
print('Default roster is exactly 3 original cases x 3 modes x 2 repetitions')
plan = native_eval.prepare(HERE / 'optional-prepared', skills, HERE / 'export-opencode', cases=list(native_fixtures.CASES), repeats=1, model='synthetic/no-inference')
assert len(plan['runs']) == 15
for entry in plan['runs']:
    run = HERE / 'optional-prepared' / entry['id']
    checks = native_eval.invariant_checks(run, entry['case'])
    assert all(checks.values()), (entry['id'], checks)
    work = run / 'workspace'
    (work / 'test_review_added.py').write_text('unauthorized read-only mutation\n')
    checks = native_eval.invariant_checks(run, entry['case'])
    assert checks['source_scope_preserved'] is False
    (work / 'test_review_added.py').unlink()
    rules = json.loads((work / 'opencode.json').read_text())['permissions']
    assert not any(x['action'] == 'edit' and x['effect'] == 'allow' for x in rules)
    subagent = [x for x in rules if x['action'] == 'subagent'][-1]
    assert subagent['effect'] == ('deny' if entry['case'] == 'coordination-missing-delegation' else 'allow')
print('All 5 optional cases prepare in all 3 modes, preserve unchanged scope, reject added tests, and configure expected delegation rules')
print('Permission-rule inspection is static; no live host enforcement claim')
node = shutil.which('node')
print('Required compiler available:', bool(shutil.which('standalone-pilot-tsc')))
if node:
    print('Local Node version:', subprocess.check_output([node, '--version'], text=True).strip())
    work = HERE / 'local-port-contract'
    work.mkdir()
    (work / 'port.contract.check.mjs').write_text(native_fixtures.PORT_CHECK)
    (work / 'port.ts').write_text('export function port(value: unknown): number {\n if (typeof value !== "number" && (typeof value !== "string" || !/^[0-9]+$/.test(value) || value.endsWith("\\n"))) throw new TypeError();\n const n = Number(value);\n if (!Number.isInteger(n) || n < 1 || n > 65535) throw new TypeError();\n return n;\n}\n')
    p = subprocess.run([node, '--experimental-strip-types', 'port.contract.check.mjs'], cwd=work, capture_output=True, text=True)
    print('Local independent implementation contract check exit:', p.returncode)
    print(p.stdout, end='')
    print(p.stderr, end='')
print('No native executable, provider credential, external network or AI Skills checkout used')
