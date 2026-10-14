from pathlib import Path
import hashlib
import json
root = Path(__file__).resolve().parent
before = json.loads((root / 'snapshot.json').read_text())
checks = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
          for name, digest in before.items()}
report = {'checked_files': len(checks), 'unchanged': all(checks.values()), 'checks': checks}
(root / 'integrity-results.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
assert all(checks.values()), 'read-only inputs changed'
