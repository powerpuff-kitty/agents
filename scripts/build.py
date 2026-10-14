#!/usr/bin/env python3
"""Build tool profiles deterministically from portable agent sources."""
import argparse
import copy
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
    if team["mode"] == "adaptive":
        lines.extend(["", "This is a candidate roster, not a requirement to invoke every role.",
                      "Derive research, review, implementation, and external-action scope from",
                      "the user's actual request and existing authorization. Select the smallest",
                      "useful set of available specialists; skip irrelevant assignments and empty",
                      "stages. Additional available project specialists may replace or supplement",
                      "candidates within the same scope, dependencies, and ownership rules.",
                      "Mutation conditions require task authorization; serial-action assignments",
                      "run one at a time and only after their prerequisites are verified."])
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
        if team["coordinator"] not in names or team["mode"] not in {"review", "delivery", "adaptive"}:
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
            if stage["execution"] not in {"serial-review", "parallel-review", "exclusive-write", "serial-action"}:
                raise ValueError(f"Invalid stage execution: {path.name}")
            assignments = stage["assignments"]
            if not isinstance(assignments, list) or not assignments:
                raise ValueError(f"Missing stage assignments: {path.name}")
            if stage["execution"] == "exclusive-write" and (team["mode"] not in {"delivery", "adaptive"} or len(assignments) != 1):
                raise ValueError(f"Writing requires delivery or adaptive mode and one owner: {path.name}")
            if stage["execution"] == "serial-action" and team["mode"] == "review":
                raise ValueError(f"Actions require delivery or adaptive mode: {path.name}")
            for assignment in assignments:
                if set(assignment) != {"agent", "task", "when"}:
                    raise ValueError(f"Invalid assignment fields: {path.name}")
                if assignment["agent"] not in names or assignment["agent"] == team["coordinator"]:
                    raise ValueError(f"Unknown or recursive team member: {path.name}")
                if any(not isinstance(assignment[field], str) or not assignment[field].strip()
                       for field in ("task", "when")):
                    raise ValueError(f"Empty assignment: {path.name}")
                if (team["mode"] == "adaptive" and stage["execution"] in {"exclusive-write", "serial-action"}
                        and assignment["when"].strip().lower() == "always"):
                    raise ValueError(f"Adaptive mutations require a task authorization condition: {path.name}")
        if not isinstance(team["completion"], list) or not team["completion"] or any(
            not isinstance(item, str) or not item.strip() for item in team["completion"]
        ):
            raise ValueError(f"Missing completion evidence: {path.name}")
        teams.append({"metadata": team, "instructions": render_team_prompt(team)})
        sources.append(path)
    if not teams:
        raise ValueError("No team presets found")
    return teams, sources


def load_packs(agents, teams):
    """Validate catalog ownership, dependency cycles, and workflow availability."""
    agent_names = {a["metadata"]["id"] for a in agents}
    team_map = {t["metadata"]["id"]: t for t in teams}
    packs, sources = {}, []
    owners = {"agents": {}, "teams": {}}
    for path in sorted((ROOT / "packs").iterdir()):
        if path.suffix != ".json" or not path.is_file():
            raise ValueError(f"Unexpected pack entry: {path.name}")
        pack = json.loads(path.read_text())
        if set(pack) != {"schema_version", "id", "title", "description", "requires", "agents", "teams"} or pack["schema_version"] != 1:
            raise ValueError(f"Invalid pack metadata: {path.name}")
        if not isinstance(pack["id"], str) or not ID.fullmatch(pack["id"]) or pack["id"] != path.stem:
            raise ValueError(f"Pack ID/file mismatch: {path.name}")
        if any(not isinstance(pack[k], str) or not pack[k].strip() for k in ("title", "description")):
            raise ValueError(f"Empty pack text: {path.name}")
        for kind in ("requires", "agents", "teams"):
            values = pack[kind]
            if not isinstance(values, list) or any(not isinstance(v, str) or not ID.fullmatch(v) for v in values) or len(set(values)) != len(values):
                raise ValueError(f"Invalid pack {kind}: {path.name}")
        for kind, known in (("agents", agent_names), ("teams", set(team_map))):
            for name in pack[kind]:
                if name not in known or name in owners[kind]:
                    raise ValueError(f"Unknown or multiply owned pack {kind}: {name}")
                owners[kind][name] = pack["id"]
        packs[pack["id"]] = pack
        sources.append(path)
    if set(owners["agents"]) != agent_names or set(owners["teams"]) != set(team_map):
        raise ValueError("Packs must cover every agent and team")
    closures = {}

    def closure(name, visiting):
        if name not in packs:
            raise ValueError(f"Unknown pack dependency: {name}")
        if name in visiting:
            raise ValueError(f"Pack dependency cycle: {name}")
        if name not in closures:
            included = {name}
            for dependency in packs[name]["requires"]:
                included.update(closure(dependency, visiting | {name}))
            closures[name] = included
        return closures[name]

    for name, pack in packs.items():
        available = {agent for dependency in closure(name, set()) for agent in packs[dependency]["agents"]}
        for team_id in pack["teams"]:
            team = team_map[team_id]["metadata"]
            required = {team["coordinator"]}
            if team["mode"] != "adaptive":
                required.update(a["agent"] for stage in team["stages"] for a in stage["assignments"])
            if not required <= available:
                raise ValueError(f"Pack dependencies cannot resolve team: {team_id}")
    return packs, closures, sources


def select_catalog(agents, teams, requested=None, agent_ids=None, team_ids=None):
    packs, closures, sources = load_packs(agents, teams)
    granular = agent_ids is not None or team_ids is not None
    selected = set(packs) if requested is None and not granular else set()
    for name in requested or []:
        if name not in packs:
            raise ValueError(f"Unknown pack: {name}; available: {', '.join(sorted(packs))}")
        selected.update(closures[name])
    if not selected and not granular:
        raise ValueError("At least one pack is required")
    names = {name for pack in selected for name in packs[pack]["agents"]}
    selected_team_ids = {name for pack in selected for name in packs[pack]["teams"]}
    known_agents = {a["metadata"]["id"] for a in agents}
    team_map = {t["metadata"]["id"]: t["metadata"] for t in teams}
    for name in agent_ids or []:
        if name not in known_agents:
            raise ValueError(f"Unknown agent: {name}")
        names.add(name)
    for name in team_ids or []:
        if name not in team_map:
            raise ValueError(f"Unknown team: {name}")
        selected_team_ids.add(name)
        # Explicit teams bring their full declared roster, including adaptive candidates.
        team = team_map[name]
        names.add(team["coordinator"])
        names.update(a["agent"] for stage in team["stages"] for a in stage["assignments"])
    if not names:
        raise ValueError("Select at least one agent, team, or pack")
    selected_teams = []
    for original in teams:
        if original["metadata"]["id"] not in selected_team_ids:
            continue
        team = copy.deepcopy(original["metadata"])
        if team["mode"] == "adaptive":
            for stage in team["stages"]:
                stage["assignments"] = [a for a in stage["assignments"] if a["agent"] in names]
            team["stages"] = [stage for stage in team["stages"] if stage["assignments"]]
        selected_teams.append({"metadata": team, "instructions": render_team_prompt(team)})
    return ([a for a in agents if a["metadata"]["id"] in names], selected_teams, sources, sorted(selected))


def compile_profiles(adapter="opencode", packs=None, agent_ids=None, team_ids=None):
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
    if set(config.get("mode_overrides", {})) - {a["metadata"]["id"] for a in agents}:
        raise ValueError("Unknown profile in mode overrides")
    teams, team_sources = load_teams(agents)
    sources.extend(team_sources)
    agents, teams, pack_sources, selected_packs = select_catalog(agents, teams, packs, agent_ids, team_ids)
    sources.extend(pack_sources)
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
        "packs": selected_packs,
        "agents": [agent["metadata"]["id"] for agent in agents],
        "teams": [team["metadata"]["id"] for team in teams],
        "source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sorted(sources)},
        "output_sha256": {name: hashlib.sha256(content.encode()).hexdigest()
                          for name, content in sorted(files.items())},
    }
    files["build-manifest.json"] = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    return files


def build(adapter, output=None, check=False, packs=None, agent_ids=None, team_ids=None):
    files = compile_profiles(adapter, packs, agent_ids, team_ids)
    suffix = "-" + "-".join(sorted(set(packs))) if packs else ""
    if agent_ids is not None or team_ids is not None:
        selection = json.dumps([sorted(set(packs or [])), sorted(set(agent_ids or [])), sorted(set(team_ids or []))])
        suffix = "-selection-" + hashlib.sha256(selection.encode()).hexdigest()[:12]
    destination = Path(output) if output else ROOT / "dist" / (adapter + suffix)
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
    parser.add_argument("--pack", action="append", help="Select a pack plus dependencies; repeat to combine. Default: all packs")
    parser.add_argument("--agent", action="append", help="Select an individual profile; repeat or combine with packs/teams")
    parser.add_argument("--team", action="append", help="Select a team and its declared profiles; repeat or combine")
    args = parser.parse_args()
    try:
        path = build(args.adapter, args.output, args.check, args.pack, args.agent, args.team)
        print(f"{'Verified' if args.check else 'Built'} {args.adapter}: {path}")
        return 0
    except (OSError, ValueError, KeyError, TypeError, ImportError) as error:
        print(f"Build failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
