"""Retain actual offline source-gate evidence without source writes or commits."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone
BASE = Path(__file__).resolve().parent
ROOT = BASE / 'project'
LOGS = BASE / 'logs'
SCRATCH = BASE / 'scratch'
LOGS.mkdir(exist_ok=True)
SCRATCH.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(SCRATCH))

def capture(argv):
    return subprocess.check_output(argv, cwd=ROOT, env=env, text=True).strip()
initial_status = capture(['git', 'status', '--porcelain'])
if initial_status:
    initial_identity = {'revision': capture(['git', 'rev-parse', 'HEAD']), 'status_before': initial_status, 'python': sys.version, 'platform': platform.platform(), 'model': 'unknown', 'token_usage': 'unknown', 'tracked_sha256': None, 'hash_status': 'not_collected_dirty_source', 'recorded_at_utc': datetime.now(timezone.utc).isoformat()}
    (LOGS / 'source-before.json').write_text(json.dumps(initial_identity, indent=2) + '\n')
    raise SystemExit('Source must be clean before checks; preserve existing work')
paths = capture(['git', 'ls-files', '-z']).split('\x00')
source = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in paths if name}
identity = {'revision': capture(['git', 'rev-parse', 'HEAD']), 'status_before': capture(['git', 'status', '--porcelain']), 'python': sys.version, 'platform': platform.platform(), 'model': 'unknown', 'token_usage': 'unknown', 'recorded_at_utc': datetime.now(timezone.utc).isoformat(), 'tracked_sha256': source}
(LOGS / 'source-before.json').write_text(json.dumps(identity, indent=2) + '\n')
if identity['status_before']:
    raise SystemExit('Source must be clean before checks; preserve existing work')
commands = [['/usr/bin/false']]
records = []
for number, argv in enumerate(commands, 1):
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, timeout=90)
    path = LOGS / f'gate-{number:02d}.log'
    path.write_text(result.stdout + result.stderr)
    record = {'argv': argv, 'cwd': str(ROOT), 'exit': result.returncode, 'log': str(path.relative_to(BASE))}
    records.append(record)
    print(json.dumps(record), flush=True)
after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source}
identity_after = {'status_after': capture(['git', 'status', '--porcelain']), 'tracked_source_unchanged': after == source, 'changes': [name for name in source if source[name] != after[name]]}
(LOGS / 'source-after.json').write_text(json.dumps(identity_after, indent=2) + '\n')
(LOGS / 'gate-results.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(identity_after))
failed = any((record['exit'] != 0 for record in records))
raise SystemExit(1 if failed or not identity_after['tracked_source_unchanged'] or identity_after['status_after'] else 0)
