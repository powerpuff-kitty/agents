"""Read-only snapshot audit reproductions; all generated files use TemporaryDirectory."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile

ROOT = Path('/private/tmp/independent-audit-agents')
sys.path.insert(0, str(ROOT / 'scripts'))
import build
import install

results = {}
with tempfile.TemporaryDirectory(prefix='fresh-agents-audit-') as temporary:
    base = Path(temporary)
    env = {**os.environ, 'LC_ALL': 'C', 'PYTHONUTF8': '0', 'PYTHONCOERCECLOCALE': '0'}
    run = subprocess.run([sys.executable, str(ROOT / 'scripts/build.py'), '--adapter', 'portable', '--output', str(base / 'ascii-export')], env=env, capture_output=True, text=True)
    results['non_utf8_locale'] = {'exit': run.returncode, 'stderr': run.stderr.strip()}
    output = build.build('portable', base / 'portable', agent_ids=['financial-analyst'])
    profile = output / 'agents/financial-analyst.md'
    profile.write_bytes(profile.read_bytes().replace(b'\n', b'\r\n'))
    manifest = json.loads((output / 'build-manifest.json').read_text())
    results['newline_integrity'] = {
        'manifest_hash_matches_actual_file': manifest['output_sha256']['agents/financial-analyst.md'] == hashlib.sha256(profile.read_bytes()).hexdigest(),
        'check_passes': build.build('portable', output, check=True, agent_ids=['financial-analyst']) == output,
    }
    target = base / 'installed/agents'
    install.install('opencode', target, agent_ids=['financial-analyst'])
    results['notice_distribution'] = {
        'compiled_exports_contain_license': {adapter: any('Permission is hereby granted' in body for body in build.compile_profiles(adapter, agent_ids=['financial-analyst']).values()) for adapter in ['portable', 'opencode']},
        'installed_files': sorted(str(path.relative_to(base / 'installed')) for path in (base / 'installed').rglob('*') if path.is_file()),
        'installed_profile_contains_notice': 'Permission is hereby granted' in (target / 'financial-analyst.md').read_text(),
    }
    state = target / '.agents-managed.json'
    state.chmod(0o600)
    before = stat.S_IMODE(state.stat().st_mode)
    install.install('opencode', target, agent_ids=['quant-researcher'])
    results['management_state_permissions'] = {'before': oct(before), 'after': oct(stat.S_IMODE(state.stat().st_mode))}
print(json.dumps(results, indent=2))
