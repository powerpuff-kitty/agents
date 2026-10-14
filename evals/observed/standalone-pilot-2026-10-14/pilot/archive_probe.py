"""Check the actual HEAD source archive as an independent consumer input."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

BASE = Path(__file__).resolve().parent
ROOT = BASE / "project"
SCRATCH = BASE / "scratch"
ARCHIVE = SCRATCH / "ai-agents-0.1.0-beta.1-candidate.tar"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TMPDIR=str(SCRATCH))
argv = ["git", "archive", "--format=tar", "--prefix=ai-agents-candidate/", "HEAD"]
with ARCHIVE.open("wb") as stream:
    subprocess.run(argv, cwd=ROOT, stdout=stream, check=True, env=env)
original_hash = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
again = subprocess.check_output(argv, cwd=ROOT, env=env)
assert hashlib.sha256(again).hexdigest() == original_hash
destination = SCRATCH / "archive-consumer"
assert not destination.exists()
with tarfile.open(ARCHIVE) as archive:
    members = archive.getmembers()
    assert all(m.isfile() or m.isdir() for m in members), "Unexpected nonregular source member"
    names = [m.name for m in members]
    assert all(not Path(name).is_absolute() and ".." not in Path(name).parts for name in names)
    assert not any("dist" in Path(name).parts or ".git" in Path(name).parts for name in names)
    assert "ai-agents-candidate/LICENSE" in names
    archive.extractall(destination, filter="data")
source = destination / "ai-agents-candidate"
target = SCRATCH / "archive-install/agents"
commands = [
    [sys.executable, "scripts/validate.py"],
    [sys.executable, "scripts/check_docs.py"],
    [sys.executable, "scripts/build.py", "--adapter", "portable"],
    [sys.executable, "scripts/build.py", "--adapter", "opencode"],
    [sys.executable, "scripts/build.py", "--adapter", "portable", "--check"],
    [sys.executable, "scripts/build.py", "--adapter", "opencode", "--check"],
    [sys.executable, "scripts/install.py", "--target", str(target), "--commands-target", str(target.parent / "commands"), "--pack", "core", "--dry-run"],
    [sys.executable, "scripts/install.py", "--target", str(target), "--commands-target", str(target.parent / "commands"), "--pack", "core"],
    [sys.executable, "scripts/install.py", "--target", str(target), "--commands-target", str(target.parent / "commands"), "--pack", "core"],
]
records = []
for index, command in enumerate(commands, 1):
    result = subprocess.run(command, cwd=source, env=env, capture_output=True, text=True, timeout=60)
    path = BASE / "logs" / f"archive-{index:02d}.log"
    path.write_text(result.stdout + result.stderr)
    records.append({"argv": command, "cwd": str(source), "exit": result.returncode,
                    "log": str(path.relative_to(BASE))})
    assert result.returncode == 0, path
    if index == 7:
        assert not target.exists() and not target.parent.exists()
    if index == 9:
        assert json.loads(result.stdout)["changed"] == []
for adapter in ("portable", "opencode"):
    def output_bytes(base):
        return {str(p.relative_to(base)): p.read_bytes() for p in base.rglob("*") if p.is_file()}
    assert output_bytes(source / "dist" / adapter) == output_bytes(ROOT / "dist" / adapter)
manifests = {adapter: {"sha256": hashlib.sha256((ROOT / "dist" / adapter / "build-manifest.json").read_bytes()).hexdigest(),
                       "files": len(json.loads((ROOT / "dist" / adapter / "build-manifest.json").read_text())["output_sha256"])}
             for adapter in ("portable", "opencode")}
evidence = {"archive_argv": argv, "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "archive": str(ARCHIVE.relative_to(BASE)), "archive_sha256": original_hash,
            "repeat_archive_identical": True, "regular_source_members": len(members),
            "no_git_or_dist_members": True, "commands": records,
            "consumer_exports_identical_to_checkout": True, "build_manifests": manifests,
            "release_status": "local candidate only; no tag, publication, download or host execution"}
(BASE / "logs/archive-probe.json").write_text(json.dumps(evidence, indent=2) + "\n")
print(json.dumps({"status": "passed", "archive_sha256": original_hash, "consumer_checks": len(records), "build_manifests": manifests}))
