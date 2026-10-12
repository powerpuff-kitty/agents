#!/usr/bin/env python3
"""Install generated profiles with backups and protection for local edits."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

from build import compile_profiles


def digest(content):
    return hashlib.sha256(content).hexdigest()


def atomic_write(path, content, mode=0o644):
    descriptor, temporary = tempfile.mkstemp(prefix=".agents-install-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def install(tool, target, replace=False, dry_run=False):
    profiles = compile_profiles(tool)
    desired = {Path(name).name: content.encode() for name, content in profiles.items()
               if name.startswith("agents/") and name.endswith(".md")}
    if not desired:
        raise ValueError("Adapter produced no installable profiles")
    target = Path(target).expanduser()
    if target.is_symlink() or (target.exists() and not target.is_dir()):
        raise ValueError("Target must be a regular directory")
    state_path = target / ".agents-managed.json"
    if state_path.is_symlink():
        raise ValueError("Refusing managed-state symlink")
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    if state and (state.get("schema_version") != 1 or state.get("tool") != tool):
        raise ValueError("Incompatible installed management state")
    managed = state.get("files", {})
    if not isinstance(managed, dict) or any(
        not isinstance(name, str) or not isinstance(value, str)
        for name, value in managed.items()
    ):
        raise ValueError("Invalid installed file management state")
    old = {}
    changes = []
    conflicts = []
    for name, content in desired.items():
        path = target / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f"Refusing nonregular profile: {name}")
        previous = path.read_bytes() if path.exists() else None
        old[name] = previous
        if previous == content:
            continue
        changes.append(name)
        if previous is not None and digest(previous) != managed.get(name) and not replace:
            conflicts.append(name)
    if conflicts:
        raise ValueError("Unmanaged or locally edited profiles: " + ", ".join(conflicts) +
                         "; use --replace to back up and replace these files")
    result = {"tool": tool, "target": str(target), "changed": changes,
              "unchanged": sorted(set(desired) - set(changes)), "dry_run": dry_run, "backup": None}
    if dry_run:
        return result
    target.mkdir(parents=True, exist_ok=True)
    overwrites = [name for name in changes if old[name] is not None]
    backup = None
    if overwrites:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = target.parent / "backups" / ("reusable-agents-" + stamp)
        backup.mkdir(parents=True, exist_ok=False)
        for name in overwrites:
            shutil.copy2(target / name, backup / name)
        if state_path.exists():
            shutil.copy2(state_path, backup / state_path.name)
        result["backup"] = str(backup)
    for name in changes:
        path = target / name
        current = path.read_bytes() if path.exists() else None
        if path.is_symlink() or current != old[name]:
            raise ValueError(f"Profile changed during installation: {name}; original backup: {backup}")
        mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
        atomic_write(path, desired[name], mode)
    updated = {"schema_version": 1, "tool": tool, "repository": "powerpuff-kitty/agents",
               "files": {**managed, **{name: digest(content) for name, content in desired.items()}}}
    state_bytes = (json.dumps(updated, indent=2, sort_keys=True) + "\n").encode()
    if not state_path.exists() or state_path.read_bytes() != state_bytes:
        atomic_write(state_path, state_bytes)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tool", choices=["opencode"], default="opencode")
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    parser.add_argument("--target", type=Path, default=config_home / "opencode/agents")
    parser.add_argument("--replace", action="store_true", help="Back up and replace conflicting profiles")
    parser.add_argument("--dry-run", action="store_true", help="Plan without writing anything")
    args = parser.parse_args()
    try:
        result = install(args.tool, args.target, args.replace, args.dry_run)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
