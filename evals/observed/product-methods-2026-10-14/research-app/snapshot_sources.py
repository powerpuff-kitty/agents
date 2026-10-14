"""Copy only explicitly selected public skill evidence; never alter source files."""
from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

BASE = Path('/Users/tcsntcsn/TCSN/skills')
OUT = Path(__file__).resolve().parent
files = []
for skill in ('competitor-monitoring', 'native-app-delivery', 'user-research', 'market-opportunity-research'):
    files += [f'{skill}/SKILL.md', f'{skill}/references/method.md', f'{skill}/assets/report-template.md']
files += ['native-app-delivery/references/ios.md', 'native-app-delivery/references/android.md',
          'test-engineering/SKILL.md', 'test-engineering/references/browser-recovery.md',
          'test-engineering/references/test-design.md', 'test-engineering/references/fresh-review.md',
          'competitor-monitoring/scripts/compare_snapshots.py',
          'competitor-monitoring/tests/fixtures/baseline.json',
          'competitor-monitoring/tests/fixtures/current.json',
          'native-app-delivery/tests/fixtures/input.json',
          'user-research/tests/fixtures/input.json',
          'market-opportunity-research/tests/fixtures/input.json',
          'test-engineering/tests/fixtures/browser-recovery.json']

manifest = []
for relative in files:
    source = BASE / relative
    raw = source.read_bytes()
    target = OUT / 'sources' / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    exported = raw
    transformation = 'exact byte copy'
    if relative == 'user-research/tests/fixtures/input.json':
        data = json.loads(raw)
        for row in data['records']:
            if row['quote_allowed'] is False:
                row['note'] = '[PARAPHRASE] P02 reported that automatic cloud sharing would lead them to stop using the product.'
        data['_copy_notice'] = 'Analysis copy; quote-disallowed note replaced by a labeled paraphrase. Original SHA-256 is retained in source-identities.json.'
        exported = (json.dumps(data, indent=2) + '\n').encode()
        transformation = 'P02 note paraphrased to honor quote_allowed=false; all other records preserved semantically; JSON reformatted'
    target.write_bytes(exported)
    manifest.append({'source_path': str(source), 'source_sha256': hashlib.sha256(raw).hexdigest(),
                     'source_bytes': len(raw), 'copy_path': str(target.relative_to(OUT)),
                     'copy_sha256': hashlib.sha256(exported).hexdigest(), 'transformation': transformation})

(OUT / 'source-identities.json').write_text(json.dumps({
    'captured_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Explicitly selected public skill instructions, helper and synthetic fixtures only; repositories are read-only.',
    'files': manifest}, indent=2) + '\n')
print(json.dumps({'copied_files': len(manifest), 'sanitized_copies': 1, 'source_writes': 0}))
