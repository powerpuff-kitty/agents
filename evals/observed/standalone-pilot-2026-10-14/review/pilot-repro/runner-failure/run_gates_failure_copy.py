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
ROOT = Path("/private/tmp/standalone-pilot-2026-10-14/pilot/project")
LOGS = BASE / "logs"
SCRATCH = BASE / "scratch"
LOGS.mkdir(exist_ok=True)
SCRATCH.mkdir(exist_ok=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(SCRATCH))

def capture(argv):
    return subprocess.check_output(argv, cwd=ROOT, env=env, text=True).strip()

paths = capture(["git", "ls-files", "-z"]).split("\0")
source = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
          for name in paths if name}
identity = {"revision": capture(["git", "rev-parse", "HEAD"]),
            "status_before": capture(["git", "status", "--porcelain"]),
            "python": sys.version, "platform": platform.platform(),
            "model": "unknown", "token_usage": "unknown",
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "tracked_sha256": source}
(LOGS / "source-before.json").write_text(json.dumps(identity, indent=2) + "\n")
commands = [
    [sys.executable, "scripts/validate.py"],
    [sys.executable, "scripts/check_docs.py"],
    [sys.executable, "scripts/build.py", "--adapter", "portable"],
    [sys.executable, "scripts/build.py", "--adapter", "opencode"],
    [sys.executable, "scripts/build.py", "--adapter", "portable", "--check"],
    [sys.executable, "scripts/build.py", "--adapter", "opencode", "--check"],
]
commands += [[sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", name, "-v"]
             for name in ["test_workflows.py", "test_selection.py", "test_audit_regressions.py",
                          "test_native_probe.py", "test_docs.py"]]
commands = [["/usr/bin/false"]]  # Reviewer fault input; retain original aggregation below.
records = []
for number, argv in enumerate(commands, 1):
    result = subprocess.run(argv, cwd=ROOT, env=env, capture_output=True, text=True, timeout=90)
    path = LOGS / f"gate-{number:02d}.log"
    path.write_text(result.stdout + result.stderr)
    record = {"argv": argv, "cwd": str(ROOT), "exit": result.returncode, "log": str(path.relative_to(BASE))}
    records.append(record)
    print(json.dumps(record), flush=True)
after = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source}
identity_after = {"status_after": capture(["git", "status", "--porcelain"]),
                  "tracked_source_unchanged": after == source,
                  "changes": [name for name in source if source[name] != after[name]]}
(LOGS / "source-after.json").write_text(json.dumps(identity_after, indent=2) + "\n")
(LOGS / "gate-results.json").write_text(json.dumps(records, indent=2) + "\n")
print(json.dumps(identity_after))
