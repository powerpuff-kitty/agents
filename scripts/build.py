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


def render_team_prompt(team):
    lines = [f"# Team preset: {team['title']}", "", team["intent"], "",
             f"Coordinator: {team['coordinator']}", f"Intent mode: {team['mode']}",
             f"Maximum active independent assignments: {team['max_parallel']}", "",
             "Follow the coordinator's operating contract. Supply focused briefs to",
             "isolated delegates, honor stage dependencies, explain conditional selections,",
             "serialize source writers, and gather actual results before the final verdict.",
             "This preset requests scoped delegation; it does not authorize unrelated",
             "external actions or claim that any model has already run the workflow."]
    for number, stage in enumerate(team["stages"], 1):
        lines.extend(["", f"## Stage {number}: {stage['id']}", "", f"Execution: {stage['execution']}"])
        for assignment in stage["assignments"]:
            lines.extend(["", f"- Agent: {assignment['agent']}",
                          f"  Apply when: {assignment['when']}", f"  Assignment: {assignment['task']}"])
    lines.extend(["", "## Completion evidence", ""])
    lines.extend("- " + criterion for criterion in team["completion"])
    return "\n".join(lines)


def load_teams(agents):
    names = {agent["metadata"]["id"] for agent in agents}
    teams, sources = [], []
    fields = {"schema_version", "id", "title", "description", "coordinator", "intent",
              "mode", "max_parallel", "stages", "completion"}
    directory = ROOT / "teams"
    if not directory.is_dir():
        raise ValueError("Missing team source directory")
    for path in sorted(directory.iterdir()):
        if path.suffix != ".json" or not path.is_file():
            raise ValueError(f"Unexpected team source entry: {path.name}")
        team = json.loads(path.read_text())
        if set(team) != fields or team["schema_version"] != 1:
            raise ValueError(f"Invalid team metadata: {path.name}")
        if not isinstance(team["id"], str) or not ID.fullmatch(team["id"]) or team["id"] != path.stem:
            raise ValueError(f"Team ID/file mismatch: {path.name}")
        if any(not isinstance(team[field], str) or not team[field].strip()
               for field in ("title", "description", "intent")):
            raise ValueError(f"Empty team text: {path.name}")
        if team["coordinator"] not in names or team["mode"] not in {"review", "delivery"}:
            raise ValueError(f"Invalid coordinator or mode: {path.name}")
        if type(team["max_parallel"]) is not int or not 1 <= team["max_parallel"] <= len(names):
            raise ValueError(f"Invalid parallel assignment limit: {path.name}")
        if not isinstance(team["stages"], list) or not team["stages"]:
            raise ValueError(f"Missing team stages: {path.name}")
        stages = set()
        for stage in team["stages"]:
            if set(stage) != {"id", "execution", "assignments"}:
                raise ValueError(f"Invalid stage fields: {path.name}")
            if not isinstance(stage["id"], str) or not ID.fullmatch(stage["id"]) or stage["id"] in stages:
                raise ValueError(f"Invalid or duplicate stage: {path.name}")
            stages.add(stage["id"])
            if stage["execution"] not in {"serial-review", "parallel-review", "exclusive-write"}:
                raise ValueError(f"Invalid stage execution: {path.name}")
            assignments = stage["assignments"]
            if not isinstance(assignments, list) or not assignments:
                raise ValueError(f"Missing stage assignments: {path.name}")
            if stage["execution"] == "exclusive-write" and (team["mode"] != "delivery" or len(assignments) != 1):
                raise ValueError(f"Writing requires delivery mode and one owner: {path.name}")
            for assignment in assignments:
                if set(assignment) != {"agent", "task", "when"}:
                    raise ValueError(f"Invalid assignment fields: {path.name}")
                if assignment["agent"] not in names or assignment["agent"] == team["coordinator"]:
                    raise ValueError(f"Unknown or recursive team member: {path.name}")
                if any(not isinstance(assignment[field], str) or not assignment[field].strip()
                       for field in ("task", "when")):
                    raise ValueError(f"Empty assignment: {path.name}")
        if not isinstance(team["completion"], list) or not team["completion"] or any(
            not isinstance(item, str) or not item.strip() for item in team["completion"]
        ):
            raise ValueError(f"Missing completion evidence: {path.name}")
        teams.append({"metadata": team, "instructions": render_team_prompt(team)})
        sources.append(path)
    if not teams:
        raise ValueError("No team presets found")
    return teams, sources


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
    teams, team_sources = load_teams(agents)
    sources.extend(team_sources)
    contract_path = ROOT / "shared/operating-contract.md"
    contract = contract_path.read_text()
    if not contract.strip():
        raise ValueError("Empty shared contract")
    spec = importlib.util.spec_from_file_location("agent_adapter_" + adapter, renderer_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    files = module.render(agents, teams, contract, host_path.read_text(), config)
    for name, content in files.items():
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or not isinstance(content, str):
            raise ValueError(f"Invalid adapter output: {name}")
    sources.extend([contract_path, config_path, renderer_path, host_path, Path(__file__)])
    manifest = {
        "schema_version": 1,
        "adapter": adapter,
        "agents": [agent["metadata"]["id"] for agent in agents],
        "teams": [team["metadata"]["id"] for team in teams],
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
