#!/usr/bin/env python3
"""Build tool profiles deterministically from portable agent sources."""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^[a-z][a-z0-9-]*$")


def load_agents():
    agents = []
    sources = []
    for directory in sorted((ROOT / "agents").iterdir()):
        if not directory.is_dir():
            raise ValueError(f"Unexpected source entry: {directory.name}")
        metadata_path = directory / "agent.json"
        instructions_path = directory / "instructions.md"
        metadata = json.loads(metadata_path.read_text())
        if set(metadata) != {"schema_version", "id", "title", "description"}:
            raise ValueError(f"Invalid metadata fields: {directory.name}")
        if metadata["schema_version"] != 1:
            raise ValueError(f"Unsupported agent schema: {directory.name}")
        if not isinstance(metadata["id"], str) or not ID.fullmatch(metadata["id"]):
            raise ValueError(f"Invalid agent ID: {directory.name}")
        if metadata["id"] != directory.name:
            raise ValueError(f"ID/directory mismatch: {directory.name}")
        if any(not isinstance(metadata[field], str) or not metadata[field].strip()
               for field in ("title", "description")):
            raise ValueError(f"Empty metadata: {directory.name}")
        instructions = instructions_path.read_text()
        if not instructions.strip():
            raise ValueError(f"Empty instructions: {directory.name}")
        agents.append({"metadata": metadata, "instructions": instructions})
        sources.extend([metadata_path, instructions_path])
    if not agents:
        raise ValueError("No portable agents found")
    return agents, sources


def compile_profiles(adapter="opencode"):
    if not ID.fullmatch(adapter):
        raise ValueError("Invalid adapter ID")
    directory = ROOT / "adapters" / adapter
    config_path = directory / "adapter.json"
    renderer_path = directory / "render.py"
    host_path = directory / "instructions.md"
    config = json.loads(config_path.read_text())
    if config.get("schema_version") != 1 or config.get("tool") != adapter:
        raise ValueError("Adapter metadata mismatch")
    agents, sources = load_agents()
    contract_path = ROOT / "shared/operating-contract.md"
    contract = contract_path.read_text()
    if not contract.strip():
        raise ValueError("Empty shared contract")
    spec = importlib.util.spec_from_file_location("agent_adapter_" + adapter, renderer_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files = module.render(agents, contract, host_path.read_text(), config)
    for name, content in files.items():
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or not isinstance(content, str):
            raise ValueError(f"Invalid adapter output: {name}")
    sources.extend([contract_path, config_path, renderer_path, host_path, Path(__file__)])
    manifest = {
        "schema_version": 1,
        "adapter": adapter,
        "agents": [agent["metadata"]["id"] for agent in agents],
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sorted(sources)},
        "output_sha256": {name: hashlib.sha256(content.encode()).hexdigest()
                          for name, content in sorted(files.items())},
    }
    files["build-manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return files


def build(adapter, output=None, check=False):
    files = compile_profiles(adapter)
    destination = Path(output) if output else ROOT / "dist" / adapter
    expected = set(files)
    if destination.is_symlink() or any(path.is_symlink() for path in destination.rglob("*")):
        raise ValueError("Refusing symlinks in build output")
    existing = {str(path.relative_to(destination)) for path in destination.rglob("*") if path.is_file()}
    if check:
        if existing != expected:
            raise ValueError("Generated file inventory is missing or stale; rebuild")
        for name, content in files.items():
            if (destination / name).read_text() != content:
                raise ValueError(f"Generated output drift: {name}; rebuild")
    else:
        if destination.is_symlink():
            raise ValueError("Refusing to build into a symlink")
        # Do not silently delete files that might belong to the user.
        if existing - expected:
            raise ValueError("Unexpected files in build output; choose a clean output directory")
        for name, content in files.items():
            target = destination / name
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_symlink():
                raise ValueError(f"Refusing to overwrite symlink: {name}")
            target.write_text(content)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", default="opencode")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        path = build(args.adapter, args.output, args.check)
        print(f"{'Verified' if args.check else 'Built'} {args.adapter}: {path}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
