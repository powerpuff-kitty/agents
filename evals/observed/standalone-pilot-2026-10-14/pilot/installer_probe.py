"""Exercise real installer update logic with in-memory rendered-version changes."""
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "project/scripts"))
import install

target = BASE / "scratch/update-probe/agents"
commands = target.parent / "commands"
assert not target.parent.exists(), "Choose a fresh disposable probe directory"
target.mkdir(parents=True)
(target / "unrelated.md").write_bytes(b"owner profile\n")
commands.mkdir()
(commands / "unrelated.md").write_bytes(b"owner command\n")
events = []

def tree():
    return {str(p.relative_to(target.parent)): (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in target.parent.rglob("*") if p.is_file()}

before = tree()
preview = install.install("opencode", target, dry_run=True, agent_ids=["quality-engineer"])
assert tree() == before
events.append({"check": "dry run preserves all bytes and mtimes", "result": preview})
initial = install.install("opencode", target, agent_ids=["quality-engineer"])
assert not (commands / ".agents-managed.json").exists()
assert {p.name for p in target.glob("*.md")} == {"unrelated.md", "quality-engineer.md"}
events.append({"check": "individual selection creates only named agent and no command state", "result": initial})
before = tree()
repeat = install.install("opencode", target, agent_ids=["quality-engineer"])
assert repeat["changed"] == [] and tree() == before
events.append({"check": "repeat is byte and mtime no-op", "result": repeat})
team = install.install("opencode", target, team_ids=["team-geo"])
metadata = json.loads((BASE / "project/teams/team-geo.json").read_text())
roster = {metadata["coordinator"]} | {a["agent"] for s in metadata["stages"] for a in s["assignments"]}
assert all((target / (name + ".md")).exists() for name in roster)
assert (commands / "team-geo.md").exists()
before = tree()
smaller = install.install("opencode", target, agent_ids=["quality-engineer"])
assert tree() == before
events.append({"check": "explicit team roster installed; smaller selection does not prune", "roster": sorted(roster), "result": team})

original_compiler = install.compile_profiles
def next_version(*args, **kwargs):
    files = original_compiler(*args, **kwargs)
    files["agents/quality-engineer.md"] += "\nSynthetic v2 instruction for update probe.\n"
    return files

old_profile = (target / "quality-engineer.md").read_bytes()
old_state = (target / ".agents-managed.json").read_bytes()
(target / "quality-engineer.md").chmod(0o600)
with patch.object(install, "compile_profiles", side_effect=next_version):
    updated = install.install("opencode", target, agent_ids=["quality-engineer"])
    assert updated["changed"] == ["agents/quality-engineer.md"]
    backup = Path(updated["backup"])
    assert (backup / "quality-engineer.md").read_bytes() == old_profile
    assert (backup / ".agents-managed.json").read_bytes() == old_state
    assert (target / "quality-engineer.md").stat().st_mode & 0o777 == 0o600
    state = json.loads((target / ".agents-managed.json").read_text())
    assert state["files"]["quality-engineer.md"] == hashlib.sha256((target / "quality-engineer.md").read_bytes()).hexdigest()
    assert all((target / (name + ".md")).exists() for name in roster)
    events.append({"check": "untouched managed v1 updates to v2 with byte-exact profile/state backups and preserved mode", "result": updated})
    before = tree()
    repeat_v2 = install.install("opencode", target, agent_ids=["quality-engineer"])
    assert repeat_v2["changed"] == [] and tree() == before
    events.append({"check": "repeat updated version is no-op", "result": repeat_v2})
    (target / "quality-engineer.md").write_bytes(b"local owner customization\n")
    before = tree()
    try:
        install.install("opencode", target, agent_ids=["quality-engineer"])
    except ValueError as error:
        assert "locally edited" in str(error)
        assert tree() == before
        events.append({"check": "local edit refused before any writes", "error": str(error)})
    else:
        raise AssertionError("Local edit was not refused")
assert (target / "unrelated.md").read_bytes() == b"owner profile\n"
assert (commands / "unrelated.md").read_bytes() == b"owner command\n"
events.append({"check": "unrelated profile and command preserved", "passed": True})
(BASE / "logs/installer-probe.json").write_text(json.dumps(events, indent=2) + "\n")
print(json.dumps({"status": "passed", "checks": len(events), "evidence": "logs/installer-probe.json",
                  "limit": "Version change simulated in compiled content; project source was not edited."}))
